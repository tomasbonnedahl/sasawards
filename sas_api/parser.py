import json
from datetime import datetime

from sas_api.requester import LegData


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

        if 'outboundFlights' in response:
            outbound = response['outboundFlights']
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
        return None