from collections import namedtuple
from datetime import datetime, timedelta

import os

from conf import MIN_DATE, MAX_DATE, DAYS_AHEAD, DESTINATIONS, ORIGINS, SECONDS_BETWEEN_REQUESTS

Config = namedtuple('Config', 'base_url min_date max_date origins destinations seconds')

def create_config():
    min_date = datetime.strptime(MIN_DATE, "%Y%m%d").date()
    if MAX_DATE is not None:
        max_date = datetime.strptime(MAX_DATE, "%Y%m%d").date()
    else:
        max_date = datetime.now().date() + timedelta(days=DAYS_AHEAD)

    return Config(base_url=os.environ['BASE_URL'],
                  min_date=min_date,
                  max_date=max_date,
                  origins=ORIGINS,
                  destinations=DESTINATIONS,
                  seconds=SECONDS_BETWEEN_REQUESTS)
