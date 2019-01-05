import datetime

from sas_api.config import create_config
from sas_api.requester_dod import fetch_flights
from sas_api.response_handler import handle_results


def expected_duration_in_min(config):
    # ORIGIN * DESTINATION * 2 * (MAX_DATE - START_DATE) * (SECONDS_BETWEEN_REQUESTS + 0.5 + 1.5 SEC REQUEST)
    # max_date = calculate_future_date(config.max_date, config.)
    # min_date = datetime.datetime.strptime(MIN_DATE, "%Y%m%d").date()
    days = (config.max_date - config.min_date).days
    return round(len(config.origins) * len(config.destinations) * 2 * days * (config.seconds + 0.5 + 1.5) / 60.0)


def fetch_flights_and_store_results():
    start_time = datetime.datetime.now()

    config = create_config()
    print("Expected duration: {} min".format(expected_duration_in_min(config)))

    results = fetch_flights(config)
    handle_results(results)

    actual = round((datetime.datetime.now() - start_time).seconds / 60.0)
    print("Actual duration: {} min".format(actual))
