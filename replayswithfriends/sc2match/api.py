from base64_fields import Base64FileField
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import Http404
from tastypie import fields
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from .models import Match, Map, PlayerResult, Player
from friendship.models import Friend, Follow


class PlayerResource(ModelResource):

    def get_object_list(self, request):
        return super(PlayerResource, self).get_object_list(request).filter(
            Q(user__in=Follow.objects.following(request.user))
            | Q(user__in=Friend.objects.friends(request.user))
        )

    class Meta:
        queryset = Player.objects.all()
        resource_name = "player"
        api_name = "player"
        always_return_data = True
        authorization = Authorization()
        authentication = Authentication()


class MapResource(ModelResource):
    image = Base64FileField("image", null=True)
    map_file = Base64FileField("map_file", null=True)

    class Meta:
        queryset = Map.objects.all()
        resource_name = "map"
        api_name = "map"
        always_return_data = True
        authorization = Authorization()
        authentication = Authentication()


class PlayerResultResource(ModelResource):

    def get_object_list(self, request):
        return super(PlayerResultResource, self).get_object_list(request).filter(
            Q(player__user__in=Friend.objects.friends(request.user))
            | Q(player__user__in=Follow.objects.following(request.user))

        )

    class Meta:
        queryset = PlayerResult.objects.all()
        resource_name = "player_result"
        api_name = "player_result"
        always_return_data = True
        authorization = Authorization()
        authentication = Authentication()


class MatchResource(ModelResource):
    replay_file = Base64FileField("replay_file", null=True)

    def get_object_list(self, request):
        return Match.share.available()

    class Meta:
        queryset = Match.objects.all()
        resource_name = "match"
        api_name = "match"
        allowed_methods = ['post', 'get', 'patch', 'put', 'delete']
        always_return_data = False
        authorization = Authorization()
        authentication = Authentication()
