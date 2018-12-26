# TODO: Add these to the database and have an interface for it?
from sasawards import settings

MIN_DATE = '20191001'
# MAX_DATE = '20191115'  # Inclusive, could be None
MAX_DATE = None

DAYS_AHEAD = 335

ORIGINS = [
    'ARN',
    'CPH',
]

DESTINATIONS = [
    'HKG',
    # 'EWR',
    'SFO',
    'NRT',
    'LAX',
]

SECONDS_BETWEEN_REQUESTS = settings.SECONDS_BETWEEN
