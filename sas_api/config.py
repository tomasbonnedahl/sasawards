from collections import namedtuple
from datetime import datetime, timedelta

from conf import MIN_DATE, MAX_DATE, DAYS_AHEAD, BASE_URL, DESTINATIONS

Config = namedtuple('Config', 'base_url min_date max_date destinations')


def create_config():
    min_date = datetime.strptime(MIN_DATE, "%Y%m%d").date()
    if MAX_DATE is not None:
        max_date = datetime.strptime(MAX_DATE, "%Y%m%d").date()
    else:
        max_date = datetime.now().date() + timedelta(days=DAYS_AHEAD)

    return Config(base_url=BASE_URL, min_date=min_date, max_date=max_date, destinations=DESTINATIONS)
