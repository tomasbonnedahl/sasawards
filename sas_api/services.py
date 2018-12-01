from sas_api.config import create_config
from sas_api.email import EmailService
from sas_api.parser import ResponseParser
from sas_api.requester import FlightGetter, Requester
from sas_api.response_handler import ResponseHandler


def get_new_flight_data(log):
    config = create_config()
    requester = Requester(config.base_url, log)
    response = FlightGetter(config, requester, ResponseParser(), log).execute()
    email_service = EmailService()
    ResponseHandler(response, email_service, log).execute()
