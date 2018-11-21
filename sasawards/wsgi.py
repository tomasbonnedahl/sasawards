"""
WSGI config for sasawards project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sasawards.settings')

# TODO: Import clock instead
sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=45)  # TODO: Temp
def timed_job():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")

    import django_rq
    from sas_api.services import get_new_flight_data
    django_rq.enqueue(get_new_flight_data)

sched.start()
application = get_wsgi_application()
