from apscheduler.schedulers.background import BackgroundScheduler

from awards.models import Flight
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


# def apa():
#     from awards.models import Flight
#     print('flights: {}'.format(Flight.objects.all()))
#
#
# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(apa, 'interval', minutes=1)
#     scheduler.start()


@sched.scheduled_job('interval', minutes=1)  # TODO: Temp
def timed_job():
    print('This job is run every fifteen minutes.')
    # from sas_api.services import fetch_flights
    # fetch_flights()
    print('flights: {}'.format(Flight.objects.all()))


# @sched.scheduled_job('interval', minutes=10)
# def keep_alive():
#     pass
    # requests.get('http://peaceful-crag-39211.herokuapp.com')
    # print('keep alive')


sched.start()
