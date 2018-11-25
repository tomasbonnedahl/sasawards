from collections import defaultdict
from datetime import timedelta
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
    def __init__(self, origin, destination, out_date):
        self.origin = origin
        self.destination = destination
        self.out_date = out_date
        self.seats_by_cabin_class = defaultdict(int)

    def add(self, cabin_class, seats):
        """
        :type cabin_class: CabinClass
        :type seats: int
        """
        self.seats_by_cabin_class[cabin_class] = seats

    def seats_in_cabin(self, cabin_class):
        """
        :type cabin_class: CabinClass
        """
        return self.seats_by_cabin_class[cabin_class]


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

    def execute(self):
        parsed_data = []

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
            if result:
                # self.log.info('Got data for {}-{} at {}'.format(origin, dst, out_date))
                parsed_data.append(result)

            sleep(self.config.seconds + round(random(), 2))
        return parsed_data

    @property
    def __days(self):
        delta = self.config.max_date - self.config.min_date
        return delta.days + 1  # Inclusive of last date
