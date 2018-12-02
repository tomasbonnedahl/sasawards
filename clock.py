import os

import requests
from apscheduler.schedulers.background import BackgroundScheduler

# sched = BlockingScheduler()  # Use when in separate clock dyno
sched = BackgroundScheduler()  # Use when used from wsgi.py


@sched.scheduled_job('interval', minutes=120)
def timed_job():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")
    # django.setup()  # Only used when in separate dyno?

    import django_rq
    from rq.worker import logger as rq_logger
    from sas_api.services import get_new_flight_data

    queue = django_rq.get_queue()
    if queue.is_empty():
        django_rq.enqueue(get_new_flight_data, rq_logger)

    # worker = django_rq.get_worker()
    # print('worker state: {} for worker {}'.format(worker.get_state(), worker.name))
    # if worker.get_state() == 'idle':


@sched.scheduled_job('interval', minutes=1)
def keep_alive():
    requests.get('http://thawing-ravine-34523.herokuapp.com')


sched.start()
