#web: gunicorn sasawards.wsgi --log-file -
web: waitress-serve --port=80 sasawards.wsgi:application
worker: python manage.py rqworker default
