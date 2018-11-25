from awards.models import Flight, Changes
from sas_api.requester import CabinClass


class ResponseHandler(object):
    def __init__(self, response, log):
        """
        :type response: list[sas_api.requester.Result]
        """
        self.response = response
        self.log = log

    def execute(self):
        for flight in self.response:
            self._handle_flight(flight)

    def _handle_flight(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        if new_flight is None:
            # TODO: We should still update the flight that it's removed/no seats/etc
            return

        flight, created = Flight.objects.get_or_create(origin=new_flight.origin,
                                                       destination=new_flight.destination,
                                                       date=new_flight.out_date,
                                                       cabin=CabinClass.BUSINESS)

        if created or self._positive_change(existing_flight=flight, new_flight=new_flight):
            Changes.objects.create(prev_seats=flight.seats, to=flight)

        flight.seats = new_flight.seats_in_cabin(CabinClass.BUSINESS)
        flight.save()

    def _positive_change(self, existing_flight, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        if not existing_flight:
            return True
        return new_flight.seats_in_cabin(CabinClass.BUSINESS) > existing_flight.seats
