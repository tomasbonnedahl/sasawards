from collections import namedtuple
from datetime import datetime, timedelta

import os

from conf import MIN_DATE, MAX_DATE, DAYS_AHEAD, DESTINATIONS, ORIGINS, SECONDS_BETWEEN_REQUESTS
from sas_api.utils import calculate_max_date

Config = namedtuple('Config', 'base_url min_date max_date origins destinations seconds')

def create_config():
    min_date = datetime.strptime(MIN_DATE, "%Y%m%d").date()
    max_date = calculate_max_date(MAX_DATE, DAYS_AHEAD)
    return Config(base_url=os.getenv('BASE_URL'),
                  min_date=min_date,
                  max_date=max_date,
                  origins=ORIGINS,
                  destinations=DESTINATIONS,
                  seconds=SECONDS_BETWEEN_REQUESTS)
