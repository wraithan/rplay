from django.conf.urls.defaults import patterns, url
from replayswithfriends.sc2match.views import (MatchView, MatchList, PlayerList,
    PlayerDetail, MatchUpload)

urlpatterns = patterns('replayswithfriends.sc2match.views',
    url(r'^player/$', PlayerList.as_view(), name='player_list'),
    url(r'^player/(?P<pk>[\d]+)$', PlayerDetail.as_view(), name='player_detail'),
    url(r'^match/$', MatchList.as_view(), name='match_list'),
    url(r'^match/(?P<pk>[\d]+)/$', MatchView.as_view(), name='match_detail'),
    url(r'^match/upload/$', MatchUpload.as_view(), name='match_upload'),
    url(r'^match/upload/done/$', 'match_upload_done', name='match_upload'),
)
