from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from friendship.models import Friend, Follow
from .models import Profile


class UserResource(ModelResource):
    """
    An iPhone (right now, tests the user-agent) should be able to create a 'User'

    send the password, email, and username to us.
    """
    def obj_get_list(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return User.objects.filter(
                id__in=[set(
                    Follow.objects.followers(request.user).values_list('id', flat=True),
                    Friend.objects.friends(request.user).values_list('id', flat=True),
                    profile__profile_share=Profile.SHARE.PUBLIC
                )])

        return User.objects.none()

    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        api_name = "user"
        allowed_methods = ['get']
        fields = ['first_name', 'last_name', 'username', 'email', 'id', 'last_login']
        always_return_data = True
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()

