from conf import ORIGINS, DESTINATIONS, MAX_DATE, DAYS_AHEAD, SECONDS_BETWEEN_REQUESTS, MIN_DATE
from sas_api.config import create_config
from sas_api.email import EmailService
from sas_api.parser import ResponseParser
from sas_api.requester import FlightGetter, Requester
from sas_api.response_handler import ResponseHandler
import datetime

from sas_api.utils import calculate_max_date


def expected_duration_in_min():
    # ORIGIN * DESTINATION * 2 * (MAX_DATE - START_DATE) * (SECONDS_BETWEEN_REQUESTS + 0.5)
    max_date = calculate_max_date(MAX_DATE, DAYS_AHEAD)
    min_date = datetime.datetime.strptime(MIN_DATE, "%Y%m%d").date()
    days = (max_date - min_date).days
    return round(len(ORIGINS) * len(DESTINATIONS) * 2 * days * (SECONDS_BETWEEN_REQUESTS + 0.5) / 60.0)


def get_new_flight_data(log):
    # TODO: Decorator
    start_time = datetime.datetime.now()
    log.info("Expected duration: {} min".format(expected_duration_in_min()))
    config = create_config()
    requester = Requester(config.base_url, log)
    response = FlightGetter(config, requester, ResponseParser(), log).execute()
    email_service = EmailService(log)
    ResponseHandler(response, email_service, log).execute()
    actual = round((datetime.datetime.now() - start_time).seconds / 60.0)
    log.info("Actual duration: {} min".format(actual))
