import datetime
from unittest import TestCase

from awards.models import Flight
from sas_api.config import Config
from sas_api.requester import FlightGetter, Result, CabinClass
from sas_api.response_handler import ResponseHandler


class DummyRequester(object):
    def __init__(self, base_url):
        pass

    def request(self, origin, destination, out_date):
        pass


class DummyParser(object):
    def parse(self, response):
        r = Result(origin='origin',
                   destination='destination',
                   out_date=datetime.date(2019, 10, 10))
        r.add(CabinClass.BUSINESS, 1)
        return r


class TestNotWorking(TestCase):
    def setUp(self):
        pass

    def test_dummy(self):
        config = Config('http://dummy',
                        min_date=datetime.date(2018, 7, 21),
                        max_date=datetime.date(2018, 7, 21),
                        destinations=['EWR'])

        requester = DummyRequester("")
        response = FlightGetter(config, requester, DummyParser()).execute()

        assert Flight.objects.count() == 0

        ResponseHandler(response).execute()

        assert Flight.objects.count() == 1
