from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

from django.contrib import admin
admin.autodiscover()

from replayswithfriends.profiles.views import ProfileList, ProfileDetail


urlpatterns = patterns('',
    url(r'^dj/', include(admin.site.urls)),
    url(r'^favicon.ico$', lambda request: HttpResponse('')),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}, name="home"),
    url(r'^invites/', include('privatebeta.urls')),
    url(r'^players/$', ProfileList.as_view(), name="player_list"),
    url(r'^players/', include('replayswithfriends.profiles.backends.urls')),
    url(r'^players/(?P<id>[\w0-9\.\-]+)/$', ProfileDetail.as_view(), name="profile_detail"),
    url(r'^sc2/', include('replayswithfriends.sc2match.urls')),
)

urlpatterns += staticfiles_urlpatterns()


from .sc2match.tasks import as_signal
from .sc2match.models import Match
from django.db.models.signals import post_save
post_save.connect(as_signal, Match)
