from apscheduler.schedulers.blocking import BlockingScheduler

from sas_api.services import fetch_flights

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=5)  # TODO: Temp
def timed_job():
    print('This job is run every fifteen minutes.')
    fetch_flights()


@sched.scheduled_job('interval', minutes=10)
def keep_alive():
    pass
    # requests.get('http://peaceful-crag-39211.herokuapp.com')
    # print('keep alive')


sched.start()
