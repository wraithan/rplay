from registration.backends.default import DefaultBackend
from replayswithfriends.profiles.models import Profile
from replayswithfriends.profiles.backends.forms import Sc2RegForm

class Sc2Backend(DefaultBackend):

    def register(self, request, **kwargs):
        user = super(Sc2Backend, self).register(request, **kwargs)
        profile, created = Profile.objects.create(
            user=user,
        )
        profile.save()

    def get_form_class(self):
        return Sc2RegForm

