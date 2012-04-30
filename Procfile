web: python manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3 --settings=replayswithfriends.settings.prod
scheduler: python manage.py celeryd -B -E --maxtasksperchild=1000 --settings=replayswithfriends.settings.prod
worker: python manage.py celeryd -E --maxtasksperchild=1 -c 1 --settings=replayswithfriends.settings.prod
