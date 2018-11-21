from collections import namedtuple
from datetime import timedelta
from random import random
from time import sleep

import requests

# TODO: have a dict instead? Check for keys, e.g. business_seats
LegData = namedtuple('LegData', 'origin destination date business_seats')


class Requester(object):
    def __init__(self, base_url):
        self.base_url = base_url

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
        # Responsible to map params to what the actual API is called
        params = self._params(origin, destination, out_date)
        r = requests.get(self.base_url + params)
        if not r.ok:
            print('Not ok for {}-{}@{}, status code: {}'.format(origin, destination, out_date, r.status_code))
            return
        return r.json()


class FlightGetter(object):
    def __init__(self, config, requester, parser):
        self.config = config
        self.parser = parser
        self.requester = requester

    def execute(self):
        parsed_data = []
        for dst in self.config.destinations:
            for day in range(self.__days):
                out_date = self.config.min_date + timedelta(day)
                json_data = self.requester.request(origin='CPH', destination=dst, out_date=out_date)
                result = self.parser.parse(json_data)
                if result:
                    parsed_data.append(result)

                sleep(1 + round(random(), 2))
        return parsed_data

    @property
    def __days(self):
        delta = self.config.max_date - self.config.min_date
        return delta.days + 1  # Inclusive of last date
