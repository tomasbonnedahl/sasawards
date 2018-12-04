from awards.models import Flight, Changes, ApiError
from sas_api.requester import CabinClass


class ResponseHandler(object):
    def __init__(self, response, email_service, log):
        """
        :type response: sas_api.requester.ResultHandler
        """
        self.response = response
        self.log = log
        self.email_service = email_service

    def execute(self):
        for flight in self.response.valid_results:
            self._handle_flight(flight)
        self.email_service.send('Update from SAS Awards')

        for error in self.response.errors:
            self._handle_error(error)
        self.email_service.send('Errors from SAS Awards')

    def _handle_flight(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        if new_flight.seats_in_cabin(CabinClass.BUSINESS):
            flight, created = Flight.objects.get_or_create(origin=new_flight.origin,
                                                           destination=new_flight.destination,
                                                           date=new_flight.out_date)

            if created or self._positive_change(existing_flight=flight, new_flight=new_flight):
                Changes.objects.create(prev_seats=flight.business_seats, to=flight)
                self.email_service.add_flight(new_flight)

            flight.business_seats = new_flight.seats_in_cabin(CabinClass.BUSINESS)
            flight.plus_seats = new_flight.seats_in_cabin(CabinClass.PLUS)
            flight.save()

    def _positive_change(self, existing_flight, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        if not existing_flight:
            return True
        return new_flight.seats_in_cabin(CabinClass.BUSINESS) > existing_flight.business_seats

    @property
    def __ignored_errors(self):
        return ['225034', '225044', '225036']

    def _handle_error(self, new_flight):
        # Only save unexpected errors - not where there are no flights
        if any(error_code in new_flight.error for error_code in self.__ignored_errors):
            return

        ApiError.objects.get_or_create(
            origin=new_flight.origin,
            destination=new_flight.destination,
            date=new_flight.out_date,
            error_str=new_flight.error
        )
        self.email_service.add_error(new_flight)
