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


def get_result_from_response(response):
    """
    :type response: dict
    :rtype: LegData|None
    """
    try:
        if 'outboundFlights' in response:
            outbound = response['outboundFlights']
            for fx in outbound:
                if 'isSoldOut' in fx:  # TODO: Check value is True also
                    continue

                cabins = outbound[fx]['cabins']
                if outbound[fx]['stops'] == 0:
                    if 'BUSINESS' in cabins:
                        if 'SAS BUSINESS' in cabins['BUSINESS']:
                            sas_bus = cabins['BUSINESS']['SAS BUSINESS']
                            if 'products' in sas_bus:
                                if 'O_2' in sas_bus['products']:
                                    O2 = sas_bus['products']['O_2']
                                    if 'fares' in O2:
                                        for fare in O2['fares']:
                                            if 'avlSeats' in fare:
                                                seats = fare['avlSeats']
                                                a_date = outbound[fx]['startTimeInLocal']
                                                stripped_date = a_date.split('+')[0]
                                                date_t = datetime.strptime(stripped_date, "%Y-%m-%dT%H:%M:%S.%f")

                                                return LegData(business_seats=seats,
                                                               origin=outbound[fx]['origin']['code'],
                                                               destination=outbound[fx]['destination']['code'],
                                                               date=date_t.date())
    except Exception as e:
        print('Exception caught: {}'.format(e))
        print(json.dumps(response))
    return None


def get_flight_info(config):
    delta = config.max_date - config.min_date
    results = []
    for dst in config.destinations:
        for day in range(delta.days + 1):
            out_date = config.min_date + timedelta(day)
            response = do_single_request(config.base_url, origin='CPH', destination=dst, out_date=out_date)
            if response:
                result = get_result_from_response(response)
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
    print('Got flight info')
    for each in flight_info:
        print(each)


def xxx(config):
    flight_info = get_flight_info(config)
    handle_flight_response(flight_info)
