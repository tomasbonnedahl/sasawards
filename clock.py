import os

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)  # TODO: Temp
def timed_job():
    print('This job is run every fifteen minutes.')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")
    import django_rq
    from sas_api import a_test
    django_rq.enqueue(a_test.a_test)
    # from sas_api.services import fetch_flights
    # fetch_flights()


sched.start()
