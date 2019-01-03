from sas_api.config import create_config
from awards.email import EmailService
from sas_api.parser import ResponseParser
from sas_api.requester import FlightGetter, Requester
from sas_api.requester_dod import fetch_flights
from sas_api.response_handler import ResponseHandler
import datetime

from sas_api.response_handler_dod import handle_results
from sas_api.utils import calculate_future_date


def expected_duration_in_min(config):
    # ORIGIN * DESTINATION * 2 * (MAX_DATE - START_DATE) * (SECONDS_BETWEEN_REQUESTS + 0.5 + 1.5 SEC REQUEST)
    # max_date = calculate_future_date(config.max_date, config.)
    # min_date = datetime.datetime.strptime(MIN_DATE, "%Y%m%d").date()
    days = (config.max_date - config.min_date).days
    return round(len(config.origins) * len(config.destinations) * 2 * days * (config.seconds + 0.5 + 1.5) / 60.0)


def get_new_flight_data(log):
    # TODO: Decorator
    start_time = datetime.datetime.now()
    config = create_config()
    log.info("Expected duration: {} min".format(expected_duration_in_min(config)))
    requester = Requester(config.base_url, log)
    response = FlightGetter(config, requester, ResponseParser(), log).execute()
    email_service = EmailService(log)
    ResponseHandler(response, email_service, log).execute()
    actual = round((datetime.datetime.now() - start_time).seconds / 60.0)
    log.info("Actual duration: {} min".format(actual))


def fetch_flights_and_store_results():
    config = create_config()
    results = fetch_flights(config)
    handle_results(results)