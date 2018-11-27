import os

# from apscheduler.schedulers.background import BackgroundScheduler

# sched = BackgroundScheduler()
import django
from apscheduler.schedulers.blocking import BlockingScheduler

# TODO: Comment
sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)  # TODO: Temp
def timed_job():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")
    django.setup()

    import django_rq
    from rq.worker import logger as rq_logger
    from sas_api.services import get_new_flight_data

    rq_logger.info('Job is executing!')
    queue = django_rq.get_queue()
    if queue.is_empty():
        rq_logger.info('Enqueuing')
        django_rq.enqueue(get_new_flight_data, rq_logger)

    # worker = django_rq.get_worker()
    # print('worker state: {} for worker {}'.format(worker.get_state(), worker.name))
    # if worker.get_state() == 'idle':

sched.start()
