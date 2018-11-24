import datetime
from unittest import TestCase

from sas_api.config import Config
from sas_api.requester import FlightGetter, Result, CabinClass


class DummyRequester(object):
    def __init__(self, _):
        pass

    def request(self, origin, destination, out_date):
        pass


class DummyParser(object):
    def parse(self, response):
        r = Result(origin='origin',
                   destination='destination',
                   out_date='date')
        r.add(CabinClass.BUSINESS, 123)
        return r


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
        assert response[0].seats_in_cabin(CabinClass.BUSINESS) == 123
