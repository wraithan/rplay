from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from .models import Profile
from friendship.models import Friend, Follow


class ProfileDetail(DetailView):
    queryset = Profile.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Profile.objects.filter(
                Q(user__in=Friend.objects.friends(self.request.user))
                | Q(user__in=Follow.objects.following(self.request.user))
                | Q(profile_share=Profile.SHARE.PUBLIC)
            )
        return Profile.objects.filter(default_profile_share=Profile.SHARE.PUBLIC)


class ProfileList(ListView):
    queryset = Profile.objects.all().order_by('user__username')

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Profile.objects.filter(
                Q(user__in=Friend.objects.friends(self.request.user))
                | Q(user__in=Follow.objects.following(self.request.user))
                | Q(profile_share=Profile.SHARE.PUBLIC)
            )
        return Profile.objects.filter(default_profile_share=Profile.SHARE.PUBLIC)
