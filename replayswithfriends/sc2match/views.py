from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from .models import Match, Player
from .forms import MatchUploadForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from sc2reader.events import *
import json


class PlayerDetail(DetailView):
    queryset = Player.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Player.objects.filter(match__in=Match.share.available(self.request.user))
        else:
            return Player.objects.filter(match__in=Match.share.public())

class PlayerList(ListView):
    queryset = Player.objects.all()
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Player.objects.filter(match__in=Match.share.available(self.request.user))
        else:
            return Player.objects.filter(match__in=Match.share.public())

class MatchView(DetailView):
    queryset = Match.share.all().select_related('playerresult', 'playerresult__player', 'message')

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Match.share.available(self.request.user).select_related('playerresult', 'playerresult__player', 'message')
        else:
            return Match.share.public().select_related('playerresult', 'playerresult__player', 'message')

class MatchList(ListView):
    queryset = Match.share.all()
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Match.share.available(self.request.user)
        else:
            return Match.share.public()


class MatchUpload(CreateView):
    success_url = '/sc2/match/upload/'
    form_class = MatchUploadForm
    template_name = 'sc2match/upload.html'
    queryset = Match.objects.all()

    def get_form_kwargs(self):
        kw = super(MatchUpload, self).get_form_kwargs()
        kw.update({'user': self.request.user})
        return kw

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MatchUpload, self).dispatch(*args, **kwargs)

def match_upload_done(request):
    return HttpResponse('{"upload":"complete"}', content_type="application/json")

