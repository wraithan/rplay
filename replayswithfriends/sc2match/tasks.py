from .models import PlayerResult, Map, Match
from .models import Player
from celery.task import task


def as_signal(sender, instance, created, raw, **kwargs):
    if created:
        parse_replay.delay(instance.id)

@task
def parse_replay(match_id):
    match = Match.objects.get(id=match_id)
    match.players.all().delete()
    errors = []
    try:
        try:
            match.mapfield, created = Map.objects.get_or_create(
                name=match.replay.map_name,
            )
        except AttributeError:
            errors.append('Map Not Found in replay, but %s' % match.replay.map)

        match.duration = match.replay.game_length.seconds
        match.gateway = match.replay.gateway

        for p in match.replay.players:
            player, created = Player.objects.get_or_create(
                username=p.name,
                battle_net_url=p.url
            )
            result = None
            if p.result == 'Win':
                result = True
            elif p.result == 'Loss':
                result = False

            if p.pick_race == 'Random':
                random=True
            else:
                random=False

            PlayerResult.objects.create(
                match=match,
                player=player,
                result=result,
                random=random,
                color='rgb(%(r)s, %(g)s, %(b)s)' % p.color,
                race=p.play_race,
            )

        for p in match.replay.observers:
            errors.append('Observer %s here that we can\'t identify without a url' % p.name)
            #player, created = Player.objects.get_or_create(
            #    username=p.name,
            #    battle_net_url=p.url
            #)
            #result = None
            #PlayerResult.objects.create(
            #    match=match,
            #    player=player,
            #    result=result,
            #    is_observer=True,
            #    color='rgb(%(r)s, %(g)s, %(b)s)' % p.color,
            #    race=p.play_race,
            #)

        match.processed = True
    except Exception, e:
        if hasattr(e, 'code'):
            errors.append("Replay Parse Error: %s %s at location %s -- %s" % (
                e.message,
                e.code or 'X',
                e.location,
                e.type
            ))
        else:
            errors.append(e.message)
        match.processed = False

    match.process_error = '\n'.join(errors)
    match.save()
