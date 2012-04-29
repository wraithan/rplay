from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _

from friendship.models import Friend

class Profile(models.Model):

    SHARE = Choices(
        (0, 'PUBLIC', _("Public")),
        (1, 'FRIENDS', _("Public")),
        (2, 'FOLLOWERS', _("Followers")),
        (3, 'PRIVATE', _("Public")),
    )

    user = models.OneToOneField(User, null=True)
    default_match_share = models.PositiveSmallIntegerField(choices=SHARE, default=SHARE.FRIENDS)
    profile_share = models.PositiveSmallIntegerField(choices=SHARE, default=SHARE.FRIENDS)
    can_friend_req = models.BooleanField(default=True)
    can_follow_req = models.BooleanField(default=True)
    follow_code = models.CharField(blank=True, default='', max_length=16)
    friend_code = models.CharField(blank=True, default='', max_length=16)


class EmailInvite(models.Model):
    from_user = models.ForeignKey(User, related_name="invited")
    to_email = models.EmailField()
    accepted_by = models.ForeignKey(User, related_name="invited_by", null=True, editable=False)
    accepted = models.BooleanField(default=False, editable=False)
    email_sent = models.DateTimeField(null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if self.accepted_by and not self.accepted:
            Friend.objects.get_or_create(
                to_user=self.from_user,
                from_user=self.accepted_by
            )
            Friend.objects.get_or_create(
                from_user=self.from_user,
                to_user=self.accepted_by
            )
            self.accepted = True
        super(EmailInvite, self).save(*args, **kwargs)
