import datetime
import logging
from unittest import TestCase

from awards.models import Flight, Changes
from sas_api.email import EmailService
from sas_api.requester import Result, CabinClass, ResultHandler
from sas_api.response_handler import ResponseHandler


class DummyEmailService(object):
    # TODO: Mock
    def add_flight(self, new_flight):
        pass

    def add_error(self, new_flight):
        pass

    def send(self):
        pass


class TestResponseHandler(TestCase):
    def setUp(self):
        self.log = logging
        self.email_service = EmailService()

    def tearDown(self):
        Flight.objects.all().delete()
        Changes.objects.all().delete()

    def test_adding_business_seats(self):
        assert Flight.objects.count() == 0

        r = Result(origin='origin',
                   destination='destination',
                   out_date=datetime.date(2019, 10, 10))
        r.add(CabinClass.BUSINESS, 1)
        result_handler = ResultHandler()
        result_handler.add(origin='origin',
                           destination='destination',
                           out_date=datetime.date(2019, 10, 10),
                           result=r)

        ResponseHandler(result_handler, self.email_service, self.log).execute()

        assert Flight.objects.count() == 1
        flight = Flight.objects.first()

        assert flight.origin == r.origin
        assert flight.destination == r.destination
        assert flight.date == r.out_date
        assert flight.business_seats == r.seats_in_cabin(CabinClass.BUSINESS)

        assert Changes.objects.count() == 1
        changes = Changes.objects.first()
        assert changes.prev_seats == 0

    def test_seats_increasing(self):
        assert Flight.objects.count() == 0
        Flight.objects.create(
            origin='origin',
            destination='destination',
            date=datetime.date(2019, 10, 10),
            business_seats=2,
        )

        r = Result(origin='origin',
                   destination='destination',
                   out_date=datetime.date(2019, 10, 10))
        r.add(CabinClass.BUSINESS, 3)  # New value is 3 seats, increase with 1

        result_handler = ResultHandler()
        result_handler.add(origin='origin',
                           destination='destination',
                           out_date=datetime.date(2019, 10, 10),
                           result=r)

        ResponseHandler(result_handler, self.email_service, self.log).execute()

        assert Flight.objects.count() == 1
        flight = Flight.objects.first()

        assert flight.origin == r.origin
        assert flight.destination == r.destination
        assert flight.date == r.out_date
        assert flight.business_seats == r.seats_in_cabin(CabinClass.BUSINESS)

        assert Changes.objects.count() == 1
        changes = Changes.objects.first()
        assert changes.prev_seats == 2
        assert changes.to == flight

    def test_seats_decreasing(self):
        # Shouldn't update changed? Only positive change?
        assert Flight.objects.count() == 0
        Flight.objects.create(
            origin='origin',
            destination='destination',
            date=datetime.date(2019, 10, 10),
            business_seats=2,
        )

        r = Result(origin='origin',
                   destination='destination',
                   out_date=datetime.date(2019, 10, 10))
        r.add(CabinClass.BUSINESS, 1)  # New value is 1 seat, decrease with 1

        result_handler = ResultHandler()
        result_handler.add(origin='origin',
                           destination='destination',
                           out_date=datetime.date(2019, 10, 10),
                           result=r)

        ResponseHandler(result_handler, self.email_service, self.log).execute()

        assert Flight.objects.count() == 1
        flight = Flight.objects.first()

        assert flight.origin == r.origin
        assert flight.destination == r.destination
        assert flight.date == r.out_date
        assert flight.business_seats == r.seats_in_cabin(CabinClass.BUSINESS)

        assert Changes.objects.count() == 0

    def test_double_update_should_have_two_changes(self):
        assert Flight.objects.count() == 0
        Flight.objects.create(
            origin='origin',
            destination='destination',
            date=datetime.date(2019, 10, 10),
            business_seats=2,
        )

        r = Result(origin='origin',
                   destination='destination',
                   out_date=datetime.date(2019, 10, 10))
        r.add(CabinClass.BUSINESS, 3)  # New value is 3 seats, increase with 1

        result_handler = ResultHandler()
        result_handler.add(origin='origin',
                           destination='destination',
                           out_date=datetime.date(2019, 10, 10),
                           result=r)

        ResponseHandler(result_handler, self.email_service, self.log).execute()

        flight = Flight.objects.first()
        assert flight.business_seats == r.seats_in_cabin(CabinClass.BUSINESS)

        r2 = Result(origin='origin',
                    destination='destination',
                    out_date=datetime.date(2019, 10, 10))
        r2.add(CabinClass.BUSINESS, 4)  # New value is 4 seats, increase with 1

        result_handler = ResultHandler()
        result_handler.add(origin='origin',
                           destination='destination',
                           out_date=datetime.date(2019, 10, 10),
                           result=r2)

        ResponseHandler(result_handler, self.email_service, self.log).execute()

        assert Flight.objects.count() == 1
        flight = Flight.objects.first()

        assert flight.origin == r2.origin
        assert flight.destination == r2.destination
        assert flight.date == r2.out_date
        assert flight.business_seats == r2.seats_in_cabin(CabinClass.BUSINESS)

        assert Changes.objects.count() == 2
        changes = Changes.objects.all().order_by('ts').last()
        assert changes.prev_seats == 3
        assert changes.to == flight
