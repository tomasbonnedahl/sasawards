# TODO: Use .env or .txt instead?
# TODO: Add these to the database and have an interface for it?

# BASE_URL = 'https://thawing-ravine-34523.herokuapp.com/mock/?'
BASE_URL = 'http://127.0.0.1:7878/mock/?'
# BASE_URL = 'https://api.flysas.com/offers/flights?'

MIN_DATE = '20191002'
MAX_DATE = '20191003'  # Inclusive, could be None
# MAX_DATE=None

DAYS_AHEAD = 340

ORIGINS = [
    'CPH'
]

DESTINATIONS = [
    'PVG',
    'EWR',
    'NON'
]

SECONDS_BETWEEN_REQUESTS = 1
