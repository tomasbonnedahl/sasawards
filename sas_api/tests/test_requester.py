import datetime

from unittest import TestCase

from sas_api.config import Config
from sas_api.requester import FlightGetter, LegData


class DummyRequester(object):
    def __init__(self, base_url):
        pass

    def request(self, origin, destination, out_date):
        pass


class DummyParser(object):
    def parse(self, response):
        return LegData(business_seats=123,
                       origin='origin',
                       destination='destination',
                       date='date')


class TestRequester(TestCase):
    def setUp(self):
        pass

    def test_dummy(self):
        config = Config('http://dummy',
                        min_date=datetime.date(2018, 7, 20),
                        max_date=datetime.date(2018, 7, 21),
                        destinations=['EWR', 'SFO'])

        requester = DummyRequester("")
        response = FlightGetter(config, requester, DummyParser()).execute()

        assert len(response) == 4
        assert response[0].business_seats == 123
