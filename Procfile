#web: gunicorn sasawards.wsgi --log-file -
web: waitress-serve --port=${PORT} sasawards.wsgi:application
worker: python manage.py rqworker default
