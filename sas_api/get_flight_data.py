from collections import namedtuple

from datetime import datetime, timedelta
from random import random
from time import sleep

import requests

from conf import MIN_DATE, MAX_DATE, DAYS_AHEAD, DESTINATIONS, BASE_URL

LegData = namedtuple('LegData', 'origin destination date business_seats')


def get_bus_seats_from_dict(d):
    """
    :rtype: LegData|None
    """
    try:
        if 'outboundFlights' in d:
            outbound = d['outboundFlights']
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
        print(json.dumps(d))

    return None


def get_stuff():
    # TODO: Separate code that reads config and sends a namedtuple to something?
    min_date = datetime.strptime(MIN_DATE, "%Y%m%d").date()
    if MAX_DATE is not None:
        max_date = datetime.strptime(MAX_DATE, "%Y%m%d").date()
    else:
        max_date = datetime.now().date() + timedelta(days=DAYS_AHEAD)

    delta = max_date - min_date

    data_dicts = []
    for dst in DESTINATIONS:
        for day in range(delta.days + 1):
            out_date = min_date + timedelta(day)
            r = requests.get(BASE_URL + 'from=CPH&to={dst}&outDate={out_date}'.format(  # TODO: dict and unpack
                dst=dst,
                out_date=out_date.strftime("%Y%m%d")
            ))

            sleep(1 + round(random(), 2))

            if not r.ok:
                print('Not ok for {} {}, status code: {}'.format(dst, out_date, r.status_code))
                continue

            data_dicts.append(get_bus_seats_from_dict(r.json()))

    return data_dicts

d = get_stuff()
for each in d:
    print(each)

# This class is the scheduled, which will be a worker at some point
# It's given a configuration from the scheduling task with dates and destinations
# It will call on something with a list of defined objects containing the data
# That is the interface to the rest of the application + the database
# That callee will be responsible for
# a) checking what is in the database,
# b) updating the database,
# c) e-mailing the positive changes
