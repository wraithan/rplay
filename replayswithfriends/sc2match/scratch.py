django-admin.py shell --settings=replayswithfriends.settings.prod


from replayswithfriends.sc2match.models import Match
m = Match.objects.get(id=791)
m.process_now()


from replayswithfriends.sc2match.models import Match
for m in Match.objects.order_by('id'):
 m.process_now()

