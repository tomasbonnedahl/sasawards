# TODO: Add these to the database and have a (staff) interface for it?
from awards.models import Airport
from sasawards import settings

MIN_DATE = '20191001'
# MAX_DATE = '20191115'  # Inclusive, could be None
MAX_DATE = None

DAYS_AHEAD = 335

ORIGINS = [airport.code for airport in Airport.objects.filter(destination=False)]

DESTINATIONS = [airport.code for airport in Airport.objects.filter(destination=True)]

# DESTINATIONS = [
#     'HKG',
#     'SFO',
#     'NRT',
#     'LAX',
# ]

SECONDS_BETWEEN_REQUESTS = settings.SECONDS_BETWEEN
