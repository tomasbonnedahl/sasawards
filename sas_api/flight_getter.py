import json
from collections import namedtuple
from datetime import timedelta, datetime
from random import random
from time import sleep

import requests


LegData = namedtuple('LegData', 'origin destination date business_seats')


def do_single_request(base_url, origin, destination, out_date):
    # Responsible to map params to what the actual API is called
    r = requests.get(base_url + 'from={origin}&to={dst}&outDate={out_date}'.format(  # TODO: dict and unpack
        origin=origin,
        dst=destination,
        out_date=out_date.strftime("%Y%m%d")
    ))
    if not r.ok:
        print('Not ok for {}-{}@{}, status code: {}'.format(origin, destination, out_date, r.status_code))
        return
    return r.json()


class ResponseParser(object):
    def __init__(self, response):
        """
        :type response: dict
        """
        self.response = response

    def parse(self):
        try:
            return self.__parse()
        except Exception as e:
            print('Exception caught: {}'.format(e))
            print(json.dumps(self.response))
        return None

    def __parse(self):
        if 'pricingType' in self.response and self.response['pricingType'] == 'O':
            # Paid flights only?
            return None

        if 'outboundFlights' in self.response:
            outbound = self.response['outboundFlights']
            for flight_id in outbound:
                if outbound[flight_id]['stops'] == 0:
                    if 'isSoldOut' in flight_id:  # TODO: Check value is True also
                        continue

                    a_date = outbound[flight_id]['startTimeInLocal']
                    stripped_date = a_date.split('+')[0]
                    date_t = datetime.strptime(stripped_date, "%Y-%m-%dT%H:%M:%S.%f")
                    business_seats = 0

                    cabins = outbound[flight_id]['cabins']
                    if 'BUSINESS' in cabins:
                        if 'SAS BUSINESS' in cabins['BUSINESS']:
                            sas_bus = cabins['BUSINESS']['SAS BUSINESS']
                            if 'products' in sas_bus:
                                for product_key in sas_bus['products']:
                                    product = sas_bus['products'][product_key]
                                    if 'fares' in product:
                                        for fare in product['fares']:
                                            if 'avlSeats' in fare:
                                                business_seats = fare['avlSeats']

                    return LegData(business_seats=business_seats,
                                   origin=outbound[flight_id]['origin']['code'],
                                   destination=outbound[flight_id]['destination']['code'],
                                   date=date_t.date())


def get_flight_info(config):
    delta = config.max_date - config.min_date
    results = []
    for dst in config.destinations:
        for day in range(delta.days + 1):
            out_date = config.min_date + timedelta(day)
            response = do_single_request(config.base_url, origin='CPH', destination=dst, out_date=out_date)
            if response:
                result = ResponseParser(response).parse()
                results.append(result)

            sleep(1 + round(random(), 2))
    return results


def handle_flight_response(flight_info):
    """
    :type flight_info: list[LegData]
    """
    # That is the interface to the rest of the application + the database
    # a) checking what is in the database,
    # b) updating the database,
    # c) e-mailing the positive changes

    # TODO: Why does they have to be imported here instead of in the top?
    from awards.models import Flight, Changes

    print('Got flight info')
    for updated_flight in flight_info:
        print(updated_flight)
        existing = Flight.objects.filter(origin=updated_flight.origin,
                                         destination=updated_flight.destination,
                                         date=updated_flight.date)
        if existing:
            existing_flight = existing.first()  # Should only be one
            if updated_flight.business_seats > existing_flight.business_seats:
                Changes.objects.create(prev_business_seats=existing_flight.business_seats,
                                       to=existing_flight)

            existing_flight.update(business_seats=updated_flight.business_seats)
        else:
            # get_or_create?
            new_flight = Flight.objects.create(origin=updated_flight.origin,
                                               destination=updated_flight.destination,
                                               date=updated_flight.date,
                                               business_seats=updated_flight.business_seats)

            Changes.objects.create(prev_business_seats=0, to=new_flight)


def xxx(config):
    flight_info = get_flight_info(config)
    handle_flight_response(flight_info)
