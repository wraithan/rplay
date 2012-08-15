from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.response import TemplateResponse
from django.db.models import Q
from .models import Profile
from friendship.models import Friend, Follow
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from replayswithfriends.sc2match.models import Player, Match, PlayerResult
from django.http import HttpResponse
from django.db.models import Count


@login_required
def me(request):
    matches = Profile.objects.filter(user=request.user)
    if not matches:
        profile = Profile.objects.create(
            user=request.user
        )
    else:
        profile = matches[0]


    players = request.user.player_set.all()

    results = PlayerResult.objects.filter(player__in=players)
    wins = draws = losses = most_played_race = best_maps = worst_maps = None


    if results.exists():
        no_results = False

        wins = results.filter(result=True)
        draws = results.filter(result=None)
        losses = results.filter(result=False)

        most_played_race = results.values('race').annotate(race_count=Count('race')).order_by('-race_count')
        best_maps = wins.values('match__mapfield__name', 'match__mapfield__id').annotate(wins=Count('match__mapfield__id')).order_by('-wins')
        worst_maps = losses.values('match__mapfield__name', 'match__mapfield__id').annotate(losses=Count('match__mapfield__id')).order_by('-losses')

        beat_opponents = PlayerResult.objects.filter(
            match__in=Match.objects.filter(players__in=wins),
        ).exclude(player__in=players)

        lost_to = PlayerResult.objects.filter(
            match__in=Match.objects.filter(players__in=losses),
        ).exclude(player__in=players)

        beat_you = beat_opponents.values('race').annotate(race_count=Count('race')).order_by('-race_count')
        you_win = lost_to.values('race').annotate(race_count=Count('race')).order_by('-race_count')

    else:
        no_results = True

    if not request.user.player_set.all().exists():
        possible_players = Player.objects.filter(
            matches__match__owner=request.user
        ).annotate(Count('matches')).order_by('matches__count').distinct()[:4]
    else:
        possible_players = Player.objects.none()

    return TemplateResponse(request, "profiles/me.html", {
        "profile": profile,
        "possible_players": possible_players,
        "most_played_race": most_played_race,
        "best_maps": best_maps,
        "worst_maps": worst_maps,
        "no_results": no_results,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "results": results,
        "beat_you": beat_you,
        "you_win": you_win,
    })


class ProfileDetail(DetailView):
    queryset = Profile.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Profile.objects.filter(
                Q(user=self.request.user)
                | Q(user__in=Friend.objects.friends(self.request.user))
                | Q(user__in=Follow.objects.following(self.request.user))
                | Q(profile_share=Profile.SHARE.PUBLIC)
            )
        return Profile.objects.filter(profile_share=Profile.SHARE.PUBLIC)


class ProfileList(ListView):
    queryset = Profile.objects.all().order_by('user__username')

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Profile.objects.filter(
                Q(user=self.request.user)
                | Q(user__in=Friend.objects.friends(self.request.user))
                | Q(user__in=Follow.objects.following(self.request.user))
                | Q(profile_share=Profile.SHARE.PUBLIC)
            )
        return Profile.objects.filter(profile_share=Profile.SHARE.PUBLIC)


@login_required
def claim_player(request):
    player = get_object_or_404(Player, id=request.GET.get('player', None))

    if player.user:
        return HttpResponse("FAILYOU, Totally not OK")

    if not Match.objects.filter(owner=request.user, players__player=player).exists():
        return HttpResponse("You've never uploaded a match with this player, it's probably not you")

    player.user = request.user
    player.save()

    return redirect("me")
