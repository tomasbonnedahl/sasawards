from collections import defaultdict
from datetime import timedelta, datetime
from enum import Enum
from random import random
from time import sleep

import itertools
import requests


class CabinClass(Enum):
    BUSINESS = 'b'
    PLUS = 'p'
    GO = 'g'


class Result(object):
    def __init__(self, origin=None, destination=None, out_date=None, error=None):
        self.origin = origin
        self.destination = destination
        self.out_date = out_date
        self.seats_by_cabin_class = defaultdict(int)
        self.error = error

    def add(self, cabin_class, seats):
        """
        :type cabin_class: CabinClass
        :type seats: int
        """
        self.seats_by_cabin_class[cabin_class] = seats

    def add_error(self, error):
        """
        :type error: str
        """
        self.error = error

    def has_errors(self):
        return self.error is not None

    def seats_in_cabin(self, cabin_class):
        """
        :type cabin_class: CabinClass
        """
        return self.seats_by_cabin_class[cabin_class]


class ResultHandler(object):
    def __init__(self):
        self.valid_results = []
        self.errors = []

    def add(self, origin, destination, out_date, result):
        """
        :type result: Result|None
        """
        if result is None:
            result = Result(error="Unknown error, result was None")

        if not all([result.origin, result.destination, result.out_date]):
            result.origin = origin
            result.destination = destination
            result.out_date = out_date

        if result.error is not None:
            self.errors.append(result)
        else:
            self.valid_results.append(result)


class Requester(object):
    def __init__(self, base_url, log):
        self.base_url = base_url
        self.log = log

    def _params(self, origin, destination, out_date):
        """
        :type origin: str
        :type destination: str
        :type out_date: datetime.date
        """
        value_by_api_keyword = {
            'from=': origin,
            'to=': destination,
            'outDate=': out_date.strftime("%Y%m%d")
        }
        return "&".join([str(k) + str(v) for k, v in value_by_api_keyword.items()])

    def request(self, origin, destination, out_date):
        params = self._params(origin, destination, out_date)
        r = requests.get(self.base_url + params)
        if not r.ok:
            self.log.error('Not ok for {}-{}@{}, status code: {}'.format(origin, destination, out_date, r.status_code))
            return
        return r.json()


class FlightGetter(object):
    def __init__(self, config, requester, parser, log):
        """
        :type config: sas_api.config.Config
        """
        self.config = config
        self.parser = parser
        self.requester = requester
        self.log = log
        self.result_handler = ResultHandler()

    def execute(self):
        outbound_data = [self.config.origins, self.config.destinations, range(self.__days)]
        inbound_data = [self.config.destinations, self.config.origins, range(self.__days)]

        outbound = itertools.product(*outbound_data)
        inbound = itertools.product(*inbound_data)

        for origin, dst, day in itertools.chain(outbound, inbound):
            out_date = self.config.min_date + timedelta(day)
            json_data = self.requester.request(origin=origin,
                                               destination=dst,
                                               out_date=out_date)
            result = self.parser.parse(json_data)
            self.result_handler.add(origin, dst, out_date, result)

            sleep(self.config.seconds + round(random(), 2))

        return self.result_handler

    @property
    def errors(self):
        return self.errors

    @property
    def __days(self):
        delta = self.config.max_date - self.config.min_date
        return delta.days + 1  # Inclusive of last date
