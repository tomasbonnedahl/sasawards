import datetime
import os
from time import sleep

import requests
from apscheduler.schedulers.background import BackgroundScheduler

# sched = BlockingScheduler()  # Use when in separate clock dyno
from sas_api.requester import Result
from sasawards.settings import MINUTE_INTERVAL_FLIGHT_FETCH

sched = BackgroundScheduler()  # Use when used from wsgi.py


# @sched.scheduled_job('interval', minutes=MINUTE_INTERVAL_FLIGHT_FETCH, next_run_time=datetime.datetime.now())
def test_email():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")
    os.environ.setdefault("SEND_EMAILS", "True")

    # Too eager, wait for other services to boot
    sleep(3)

    # from awards.email import results_to_email
    from sas_api.email import results_to_email
    result = Result(origin='CPH',
                    destination='NRT',
                    departure_date=datetime.date(2019, 1, 1),
                    business_seats=6)
    print('*** Trying to e-mail....')
    results_to_email("Testing", [result])
    print('*** Done sending')


@sched.scheduled_job('interval', minutes=MINUTE_INTERVAL_FLIGHT_FETCH, next_run_time=datetime.datetime.now())
def timed_job():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")
    # django.setup()  # Only used when in separate dyno?

    # Too eager, wait for other services to boot
    sleep(5)

    import django_rq
    # from rq.worker import logger as rq_logger

    queue = django_rq.get_queue()
    if queue.is_empty():
        from sas_api.services import fetch_flights_and_store_results
        django_rq.enqueue(fetch_flights_and_store_results)

    # worker = django_rq.get_worker()
    # print('worker state: {} for worker {}'.format(worker.get_state(), worker.name))
    # if worker.get_state() == 'idle':


@sched.scheduled_job('interval', minutes=20)
def keep_alive():
    requests.get('http://thawing-ravine-34523.herokuapp.com')


sched.start()
