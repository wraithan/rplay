from .models import PlayerResult, Map, Match, MatchMessage
from .models import Player
from celery.task import task
import datetime
from sc2reader.events import *
from sc2reader.exceptions import ReadError, FileError
import json

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
    except FileError, x:
        match.proces_error = x
        match.save()
        return False

    match.duration = match.replay.game_length.seconds
    match.gateway = match.replay.gateway
    match.is_ladder = match.replay.is_ladder

    events = []
    for e in match.replay.events:
        event = {
            "pid": e.pid,
            "frame": e.frame,
            "second": e.second,
            "name": e.name,
            "text": str(e),
        }
        if isinstance(e, GameEvent):
            event.update({
                'type': e.type,
                'code': e.code,
                'is_local': e.is_local,
                'is_init': e.is_init,
                'is_player_action': e.is_player_action,
                'is_camera_movement': e.is_camera_movement,
                'is_unknown': e.is_unknown,
            })
        if isinstance(e, MessageEvent):
            event.update({
                'type': 'MessageEvent',
                'flags': e.flags,
            })
        if isinstance(e, ChatEvent):
            event.update({
                'target': e.target,
                'text': e.text,
                'to_all': e.to_all,
                'to_allies': e.to_allies,
            })
        if isinstance(e, PacketEvent):
            event['data'] = e.data
        if isinstance(e, PingEvent):
            event.update({'x': e.x, 'y': e.y})
        if isinstance(e, ResourceTransferEvent):
            event.update({
                'sender': e.sender,
                'receiver': e.receiver,
                'minerals': e.minerals,
                'vespene': e.vespene,
            })
        if isinstance(e, AbilityEvent):
            event['ability_code'] = e.ability_code
            event['ability_text'] = e.ability
        if isinstance(e, TargetAbilityEvent):
            event['target_string'] = str(e.target)
        if isinstance(e, LocationAbilityEvent):
            event['location'] = str(e.location)
        if isinstance(e, HotkeyEvent):
            event.update({
                'hotkey': e.hotkey,
                'deselect': e.deselect,
            })
        if isinstance(e, SelectionEvent):
            event.update({
                'bank': e.bank,
                'objects': [str(x) for x in e.objects],
                'deselect': e.deselect
            })
        events.append(event)

    match.events_json = json.dumps(events)

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
