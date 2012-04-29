from base64_fields import Base64FileField
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie import fields
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from friendship.models import Friend, Follow


class UserResource(ModelResource):
    """
    An iPhone (right now, tests the user-agent) should be able to create a 'User'

    send the password, email, and username to us.
    """
    def obj_get_list(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return Following.objects.followers(request.user)

        return User.objects.none()

    def obj_create(self, bundle, *args, **kwargs):
        bundle = super(UserResource, self).obj_create(bundle, password="!", *args, **kwargs)
        bundle.obj.set_password(bundle.data['password'])
        bundle.obj.save()
        return bundle

    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        api_name = "user"
        allowed_methods = ['post', 'get']
        fields = ['first_name', 'last_name', 'username', 'email', 'id', 'last_login']
        always_return_data = True
        authorization = Authorization()
        authentication = Authentication()
