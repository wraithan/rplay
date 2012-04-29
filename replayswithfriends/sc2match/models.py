from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import sc2reader
from django.utils import timezone
from model_utils import Choices
from friendship.models import Friend, Follow

from queued_storage.backends import QueuedStorage
queued_s3storage = QueuedStorage(
    'django.core.files.storage.FileSystemStorage',
    'storages.backends.s3boto.S3BotoStorage'
)

if settings.DEBUG:
    storage_engine = default_storage
else:
    storage_engine = queued_s3storage


SHARE = Choices(
    (0, 'PUBLIC', _("Public")),
    (1, 'FRIENDS', _("Public")),
    (2, 'FOLLOWERS', _("Followers")),
    (3, 'PRIVATE', _("Public")),
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
    )

    RESULTS = Choices(
        (True, _("Win")),
        (None, _("Tie")),
        (False, _("Loss")),
    )

    player = models.ForeignKey(Player, related_name="matches")
    match = models.ForeignKey('Match', related_name="players")
    result = models.NullBooleanField(default=None, choices=RESULTS)
    color = models.CharField(max_length=32)
    random = models.BooleanField(default=False)
    race = models.CharField(choices=RACES, max_length=8)
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
    region = models.PositiveSmallIntegerField(choices=REGIONS, default=REGIONS.NA)


    def __unicode__(self):
        return self.name


class ShareManager(models.Manager):

    def available(self, to_user):
        following = Follow.objects.following(to_user)
        friends = Friend.objects.friends(to_user)

        return self.get_query_set().filter(
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


class Match(models.Model):
    owner = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(editable=False)
    replay_file = models.FileField(upload_to="replay_files/%Y/%m/%d", storage=storage_engine)
    mapfield = models.ForeignKey(Map, null=True, editable=False)
    duration = models.PositiveIntegerField(null=True, editable=False)
    gateway = models.CharField(max_length=32, default="us")
    processed = models.BooleanField(default=False)
    match_share = models.PositiveSmallIntegerField(choices=SHARE, default=SHARE.FRIENDS)

    objects = models.Manager()
    share = ShareManager()

    def __init__(self, *args, **kwargs):
        self._replay = None
        super(Match, self).__init__(*args, **kwargs)

    def __unicode__(self):
        if self.processed:
            return "%s" % ", ".join(self.players.all().values_list('player__username', flat=True).order_by("?"))
        else:
            return "unprocessed match %s" % self.created

    @models.permalink
    def get_absolute_url(self):
        return ('match_detail', [self.id])

    @property
    def replay(self):
        if not self._replay:
            self._replay = sc2reader.load_replay(self.replay_file.file)
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


    @property
    def winners(self):
        return self.players.filter(result=True)

    @property
    def losers(self):
        return self.players.filter(result=False)


    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(Match, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-modified']
