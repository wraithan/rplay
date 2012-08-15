from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from storages.backends.s3boto import S3BotoStorage

import sc2reader
from django.utils import timezone
from model_utils import Choices
from friendship.models import Friend, Follow

import hashlib

if settings.PROD:
    storage_engine = S3BotoStorage(bucket='rplay-sc2')
else:
    storage_engine = default_storage

SHARE = Choices(
    (0, 'PUBLIC', _("Public")),
    (1, 'FRIENDS', _("Friends")),
    (2, 'FOLLOWERS', _("Followers")),
    (3, 'PRIVATE', _("Private")),
)

REGIONS = Choices(
    #    STATUS = Choices((0, 'draft', _('draft')), (1, 'published', _('published')))
    (0, 'NA', _('North America')),
    (1, 'LA', _('Latin America')),
    (2, 'EU', _('Europe')),
    (3, 'RU', _('Russia')),
    (4, 'KO', _('Korea')),
    (5, 'Taiwan', _('Taiwan')),
    (6, 'SEA', _('Southeast Asia & ANZ')),

)


class Player(models.Model):
    user = models.ForeignKey(User, null=True)
    username = models.CharField(max_length=64)
    battle_net_url = models.URLField(help_text="Go to http://us.battle.net/sc2/en/ and click on your avatar to go to your profile URL", blank=True)
    region = models.PositiveSmallIntegerField(choices=REGIONS, default=REGIONS.NA)

    def __unicode__(self):
        return self.username

    class Meta:
        unique_together = ['username', 'battle_net_url']


class PlayerResult(models.Model):
    RACES = Choices(
        ("terran", _("Terran")),
        ("protoss", _("Protoss")),
        ("zerg", _("Zerg")),
        ("observer", _("Observer")),
    )

    RESULTS = Choices(
        (True, _("Win")),
        (None, _("Tie")),
        (False, _("Loss")),
    )

    player = models.ForeignKey(Player, related_name="matches", null=True)
    nick = models.CharField(max_length=64, default='', blank=True)
    pid = models.PositiveSmallIntegerField(default=0)
    is_human = models.BooleanField(default=True)
    difficulty = models.CharField(max_length=64, blank=True, default='')
    handicap = models.PositiveSmallIntegerField(default=100)
    match = models.ForeignKey('Match', related_name="players")
    result = models.NullBooleanField(default=None, choices=RESULTS)
    color = models.CharField(max_length=32)
    random = models.BooleanField(default=False)
    race = models.CharField(choices=RACES, max_length=8, blank=True)
    is_observer = models.BooleanField(default=False)

    @property
    def race_letter(self):
        if self.race:
            return self.race[0].upper()
        return '-'


class Map(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to="maps", blank=True, null=True, storage=storage_engine)
    map_file = models.FileField(upload_to="map_files", blank=True, null=True)
    url = models.URLField(editable=False, blank=True, default='')
    region = models.PositiveSmallIntegerField(choices=REGIONS, default=REGIONS.NA)


    def __unicode__(self):
        return self.name


class MatchMessage(models.Model):
    match = models.ForeignKey("Match", related_name="messages")
    player = models.ForeignKey("PlayerResult")
    frame = models.PositiveIntegerField(default=0)
    flags = models.IntegerField(default=0)
    to_all = models.BooleanField(default=True)
    to_allies = models.BooleanField(default=True)
    message = models.TextField()

    class Meta:
        ordering = ['match', 'frame']

    @property
    def time_display(self):
        if self.frame:
            minutes = self.frame / (60*16)
            seconds = self.duration % (60 * 16)
            if seconds < 10:
                seconds = "0%s" % seconds
            return '%s:%s' % (minutes, seconds)
        else:
            return '-'


class ProcessedManager(models.Manager):

    def processed(self):
        return self.get_query_set().filter(processed=True)

    def unprocessed(self):
        return self.get_query_set().filter(processed=None)

    def errors(self):
        return self.get_query_set().filter(processed=None)


class ShareManager(models.Manager):

    def available(self, to_user):
        following = Follow.objects.following(to_user)
        friends = Friend.objects.friends(to_user)

        return self.get_query_set().filter(processed=True).filter(
            models.Q(match_share=SHARE.PUBLIC)
            | models.Q(match_share=SHARE.FRIENDS, owner__in=friends)
            | models.Q(match_share=SHARE.FOLLOWERS, owner__in=following)
            | models.Q(owner=to_user)
        ).distinct()

    def public(self):
        return self.get_query_set().filter(match_share=SHARE.PUBLIC)

    def friends(self, to_user):
        friends = Friend.objects.friends(to_user)
        return self.get_query_set().filter(match_share=SHARE.FRIENDS, owner__in=friends)

    def following(self, to_user):
        following = Follow.objects.following(to_user)
        return self.get_query_set().filter(match_share=SHARE.FOLLOWERS, owner__in=following)


def generate_filename(instance, filename):
    return "replay_files/%s/%s" % (
        instance.owner.id,
        filename
    )


class Match(models.Model):
    owner = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(editable=False)
    replay_file = models.FileField(upload_to=generate_filename, storage=storage_engine)
    mapfield = models.ForeignKey(Map, null=True, editable=False)
    duration = models.PositiveIntegerField(null=True, editable=False)
    gateway = models.CharField(max_length=32, default="us")
    processed = models.NullBooleanField(default=None)
    process_error = models.TextField(blank=True, default='', editable=False)
    match_share = models.PositiveSmallIntegerField(choices=SHARE, default=SHARE.FRIENDS)
    matchhash = models.CharField(max_length=512, editable=False, blank=True, default='')
    is_ladder = models.BooleanField(default=True)
    game_played_on = models.DateTimeField(null=True, blank=True)
    game_type = models.CharField(max_length=64, blank=True, default=True)
    game_speed = models.CharField(max_length=64, blank=True, default=True)
    events_json = models.TextField(editable=False, blank=True)

    objects = models.Manager()
    share = ShareManager()
    processing = ProcessedManager()

    def __init__(self, *args, **kwargs):
        self._replay = None
        super(Match, self).__init__(*args, **kwargs)

    def __unicode__(self):
        if self.processed:
            return "%s" % ", ".join(self.players.all().values_list('nick', flat=True).order_by("nick"))
        else:
            return "unprocessed match %s" % self.created

    def process_now(self):
        from .tasks import parse_replay
        parse_replay(self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('match_detail', [self.id])

    @property
    def replay(self):
        if not self._replay:
            self._replay = sc2reader.load_replay(self.replay_file.file, load_map=False)
        return self._replay

    @property
    def time_display(self):
        if self.duration:
            minutes = self.duration / 60
            seconds = self.duration % 60
            if seconds < 10:
                seconds = "0%s" % seconds
            return '%s:%s' % (minutes, seconds)
        else:
            return '-'

    def make_hash(self, block_size=2**8):
        md5 = hashlib.md5()
        while True:
            data = self.replay_file.read(block_size)
            if not data:
                break
            md5.update(data)
        data = self.replay_file.seek(0)
        self.matchhash = md5.hexdigest()

    @property
    def winners(self):
        return self.players.filter(result=True)

    @property
    def losers(self):
        return self.players.filter(result=False)

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        if not self.matchhash:
            self.make_hash()
        super(Match, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-game_played_on', '-modified']
        unique_together = ['owner', 'matchhash']
