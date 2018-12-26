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
        for result in self.response.valid_results:
            self._handle_result(result)
        self.email_service.send('New seats found')

        for error in self.response.errors:
            self._handle_error(error)
        # self.email_service.send('Errors from SAS Awards')

    def _handle_result(self, result):
        """
        :type result: sas_api.requester.Result
        """
        if result.seats_in_cabin(CabinClass.BUSINESS):
            flight, created = Flight.objects.get_or_create(origin=result.origin,
                                                           destination=result.destination,
                                                           date=result.out_date)

            if created or self._positive_change(existing_flight=flight, result=result):
                Changes.objects.create(prev_seats=flight.business_seats, to=flight)
                self.email_service.add_result(result)

            flight.business_seats = result.seats_in_cabin(CabinClass.BUSINESS)
            flight.plus_seats = result.seats_in_cabin(CabinClass.PLUS)
            flight.save()
        else:
            Flight.objects.filter(origin=result.origin,
                                  destination=result.destination,
                                  date=result.out_date).delete()

    def _positive_change(self, existing_flight, result):
        """
        :type result: sas_api.requester.Result
        """
        if not existing_flight:
            return True
        return result.seats_in_cabin(CabinClass.BUSINESS) > existing_flight.business_seats

    @property
    def __ignored_errors(self):
        return ['225034', '225044', '225036', '225046', '225014']

    def _handle_error(self, result):
        # Only save unexpected errors - not where there are no flights
        if any(error_code in result.error for error_code in self.__ignored_errors):
            return

        ApiError.objects.get_or_create(
            origin=result.origin,
            destination=result.destination,
            date=result.out_date,
            error_str=result.error
        )
        # self.email_service.add_error(new_flight)
