import os
from collections import namedtuple
from datetime import datetime

from awards.models import Airport
from sas_api.utils import calculate_future_date
from sasawards import settings

Config = namedtuple('Config', 'base_url min_date max_date origins destinations seconds')

MIN_DATE = '20191001'
# MAX_DATE = '20191115'  # Inclusive, could be None
MAX_DATE = None

DAYS_AHEAD = 335

SECONDS_BETWEEN_REQUESTS = settings.SECONDS_BETWEEN


def origins():
    return [airport.code for airport in Airport.objects.filter(destination=False)]


def destinations():
    # DESTINATIONS = [
    #     'HKG',
    #     'SFO',
    #     'NRT',
    #     'LAX',
    # ]
    return [airport.code for airport in Airport.objects.filter(destination=True)]


def create_config():
    min_date = datetime.strptime(MIN_DATE, "%Y%m%d").date()
    max_date = calculate_future_date(MAX_DATE, DAYS_AHEAD)
    return Config(base_url=os.getenv('BASE_URL'),
                  min_date=min_date,
                  max_date=max_date,
                  origins=origins(),
                  destinations=destinations(),
                  seconds=SECONDS_BETWEEN_REQUESTS)
