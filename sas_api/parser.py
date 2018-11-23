import json
from datetime import datetime

from collections import defaultdict

from sas_api.requester import LegData, Result, CabinClass


class ResponseParser(object):
    def parse(self, response):
        try:
            return self.__parse(response)
        except Exception as e:
            print('Exception caught: {}'.format(e))
            print(json.dumps(response))
        return None

    def __parse(self, response):
        if response is None:
            return None

        if 'pricingType' in response and response['pricingType'] == 'O':
            # Paid flights only?
            return None

        # TODO: Clean this up
        if 'outboundFlights' in response:
            outbound = response['outboundFlights']
            for flight_id in outbound:
                if outbound[flight_id]['stops'] == 0:
                    if 'isSoldOut' in flight_id:  # TODO: Check value is True also
                        continue

                    a_date = outbound[flight_id]['startTimeInLocal']
                    stripped_date = a_date.split('+')[0]
                    date_t = datetime.strptime(stripped_date, "%Y-%m-%dT%H:%M:%S.%f")

                    cabins = outbound[flight_id]['cabins']
                    seats_by_cabin = self.__seats_by_cabin(cabins)
                    business_seats = seats_by_cabin['BUSINESS']

                    result = Result(origin=outbound[flight_id]['origin']['code'],
                                    destination=outbound[flight_id]['destination']['code'],
                                    out_date=date_t.date())

                    for cabin, avl_seats in seats_by_cabin.items():
                        result.add(cabin_class=self.__cabin_mapper(cabin), seats=avl_seats)

                    # TODO: Remove and use result instead
                    return LegData(business_seats=business_seats,
                                   origin=outbound[flight_id]['origin']['code'],
                                   destination=outbound[flight_id]['destination']['code'],
                                   date=date_t.date())
        return None

    def __seats_by_cabin(self, cabins):
        d = defaultdict(int)
        for cabin_class_name, cabin_class_values in cabins.items():
            for sas_cabin_class_values in cabin_class_values.values():
                products = sas_cabin_class_values['products']
                for product_value in products.values():
                    for fare in product_value['fares']:
                        if fare['avlSeats'] > d[cabin_class_name]:
                            d[cabin_class_name] = fare['avlSeats']
        return d

    def __cabin_mapper(self, sas_cabin_name):
        # TODO: Shouldn't be in this class?
        # From SAS cabin name to enum
        return {
            'BUSINESS': CabinClass.BUSINESS,
            'PLUS': CabinClass.PLUS,
            'GO': CabinClass.GO,
        }[sas_cabin_name]
