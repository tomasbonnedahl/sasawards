import os

from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=1)  # TODO: Temp
def timed_job():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")

    import django_rq
    from sas_api.services import get_new_flight_data
    django_rq.enqueue(get_new_flight_data)

sched.start()
