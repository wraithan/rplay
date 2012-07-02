from .models import PlayerResult, Map, Match, MatchMessage
from .models import Player
from celery.task import task
import datetime
from sc2reader.events import PlayerActionEvent
from sc2reader.exceptions import ReadError


def as_signal(sender, instance, created, raw, **kwargs):
    if created:
        parse_replay.delay(instance.id)

@task
def parse_replay(match_id):
    match = Match.objects.get(id=match_id)
    match.players.all().delete()
    match.process_error = ''
    errors = []
    #try:
    try:
        match.mapfield, created = Map.objects.get_or_create(
            url=match.replay.map.url,
        )
    except AttributeError:
        errors.append('Map Not Found in replay, but trying %s' % match.replay.map_name)
        try:
            match.mapfield, created = Map.objects.get_or_create(
               name=match.replay.map_name,
            )
        except AttributeError:
            errors.append("Didnt work.")
    except ReadError, x:
        match.proces_error = x
        match.save()
        return False


    match.duration = match.replay.game_length.seconds
    match.gateway = match.replay.gateway
    match.is_ladder = match.replay.is_ladder

    el = []
    for e in match.replay.events:
        if isinstance(e, PlayerActionEvent):
            try:
                print str(e)
            except Exception, x:
                print x

    match.game_played_on = datetime.datetime.fromtimestamp(int(match.replay.unix_timestamp))
    try:
        match.game_type = match.replay.type
        match.game_speed = match.replay.game_speed
    except AttributeError:
        errors.append('ignoring attribute error about type or game speed.')

    playas = {}

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

        playa = PlayerResult(
            match=match,
            player=player,
            pid=p.pid,
            nick=p.name,
            difficulty=p.difficulty,
            is_human=p.is_human,
            handicap=p.handicap,
            result=result,
            random=random,
            color='rgb(%(r)s, %(g)s, %(b)s)' % p.color,
            race=p.play_race,
        )
        playas[p.pid] = playa
        playa.save()

    for p in match.replay.observers:
        errors.append('Observer %s here that we can\'t identify without a url' % p.name)
        result = None
        playa = PlayerResult.objects.create(
            match=match,
            player=None,
            nick=p.name,
            result=result,
            is_observer=True,
            color='rgb(%(r)s, %(g)s, %(b)s)' % {'r': '33', 'g': '33', 'b': '33'},
            race='observer',
            pid=p.pid
        )
        playa.save()
        playas[p.pid] = playa


    for msg in match.replay.messages:
        mm = MatchMessage(
            player=playas[msg.pid],
            match=match,
            flags=msg.flags,
            message=msg.text,
            to_all=msg.to_all,
            to_allies=msg.to_allies
        )
        mm.save()

    match.processed = True
    #except Exception, e:
    #    errors.append(e.__repr__())
    #    match.processed = False

    match.process_error = '\n'.join(errors)
    match.save()
