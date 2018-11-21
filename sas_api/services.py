from sas_api.config import create_config
from sas_api.requester import FlightGetter, Requester
from sas_api.parser import ResponseParser
from sas_api.response_handler import ResponseHandler


def get_new_flight_data():
    config = create_config()
    requester = Requester(config.base_url)
    response = FlightGetter(config, requester, ResponseParser()).execute()
    ResponseHandler(response).execute()
