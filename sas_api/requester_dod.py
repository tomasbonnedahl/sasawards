import datetime
import itertools
from collections import namedtuple, defaultdict
from random import random
from time import sleep

import requests

from sas_api.requester import CabinClass

Result = namedtuple("Result", "origin destination departure_date business_seats plus_seats")


def from_config_to_url(base_url, origin, destination, departure_date):
    value_by_api_keyword = {
        'from': origin,
        'to': destination,
        'outDate': departure_date.strftime("%Y%m%d"),
        'adt': '2',
        'chd': '0',
        'inf': '0',
        'yth': '0',
        'bookingFlow': 'points',
        'pos': 'no',
        'channel': 'web',
        'displayType': 'upsell',
    }
    return base_url + "&".join([str(k) + '=' + str(v) for k, v in value_by_api_keyword.items()])


class Urls(object):
    def __init__(self, config):
        self.config = config

    @property
    def __days(self):
        delta = self.config.max_date - self.config.min_date
        return delta.days + 1  # Inclusive of last date

    def __iter__(self):
        outbound_data = [self.config.origins, self.config.destinations, range(self.__days)]
        inbound_data = [self.config.destinations, self.config.origins, range(self.__days)]

        outbound = itertools.product(*outbound_data)
        inbound = itertools.product(*inbound_data)

        for origin, dst, day in itertools.chain(outbound, inbound):
            yield from_config_to_url(base_url=self.config.base_url,
                                     origin=origin,
                                     destination=dst,
                                     departure_date=self.config.min_date + datetime.timedelta(day),
                                     )


def from_url_to_json(url):
    r = requests.get(url)
    if not r.ok:
        # TODO: Logging - file/area specific?
        # self.log.error('Not ok for {}-{}@{}, status code: {}'.format(origin, destination, out_date, r.status_code))
        return None
    return r.json()


def cabin_mapper(sas_cabin_name):
    # From SAS cabin name to enum
    return {
        'BUSINESS': CabinClass.BUSINESS,
        'PLUS': CabinClass.PLUS,
        'GO': CabinClass.GO,
    }[sas_cabin_name]


def from_json_to_result(json_response):
    """
    :type json_response: dict
    :rtype Result | None
    """

    def _seats_by_cabin(cabins):
        """
        :type cabins: dict
        """
        seats_by_cabin = defaultdict(int)
        for cabin_class_name, cabin_class_values in cabins.items():
            for sas_cabin_class_values in cabin_class_values.values():
                products = sas_cabin_class_values['products']
                for product_value in products.values():
                    for fare in product_value['fares']:
                        if fare['avlSeats'] > seats_by_cabin[cabin_class_name]:
                            seats_by_cabin[cabin_mapper(cabin_class_name)] = fare['avlSeats']
        return seats_by_cabin

    if json_response is None:
        return None

    if 'errors' in json_response:
        return None
        # TODO: Handle errors, add to Result? Should remove a previous db entry if we now get errors for it
        # return Result(error=json_response)

    if json_response.get('pricingType', '') == 'O':
        # Paid flights only?
        return None

    outbound = json_response.get('outboundFlights', [])
    for flight_id in outbound.values():
        if flight_id.get('isSoldOut', False):
            continue

        if flight_id.get('stops', 1):
            # Only interested in direct flights
            continue

        start_date = flight_id['startTimeInLocal'].split('T')[0]
        out_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        cabins = flight_id['cabins']
        seats_by_cabin = _seats_by_cabin(cabins)

        result = Result(origin=flight_id['origin']['code'],
                        destination=flight_id['destination']['code'],
                        departure_date=out_date,
                        business_seats=seats_by_cabin[CabinClass.BUSINESS],
                        plus_seats=seats_by_cabin[CabinClass.PLUS])
        return result

    return None


def from_url_to_result(url):
    flight_data = from_url_to_json(url)
    return from_json_to_result(flight_data)


def fetch_flights(config):
    urls = Urls(config)
    results = []
    for url in urls:
        results.append(from_url_to_result(url))
        sleep(config.seconds + round(random(), 2))
    return results