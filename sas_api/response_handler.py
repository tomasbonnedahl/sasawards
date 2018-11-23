from awards.models import Flight, Changes


class ResponseHandler(object):
    def __init__(self, response):
        """
        :type response: list[LegData]
        """
        self.response = response

    def execute(self):
        # That is the interface to the rest of the application + the database
        # a) checking what is in the database,
        # b) updating the database,
        # c) e-mailing the positive changes

        print('Got flight info')
        for flight in self.response:
            self._handle_flight(flight)

    def _handle_flight(self, new_flight):
        """
        :type new_flight: LegData
        """
        if new_flight is None:
            # TODO: We should still update the flight that it's removed/no seats/etc
            return

        flight, created = Flight.objects.get_or_create(origin=new_flight.origin,
                                                       destination=new_flight.destination,
                                                       date=new_flight.date)

        if created or self._positive_change(existing_flight=flight, new_flight=new_flight):
            Changes.objects.create(prev_business_seats=flight.business_seats if flight else 0,
                                   to=flight)

        flight.business_seats = flight.business_seats
        flight.save()

    def _positive_change(self, existing_flight, new_flight):
        if not existing_flight:
            return True
        return new_flight.business_seats > existing_flight.business_seats
