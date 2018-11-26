from awards.email import send_email
from sas_api.requester import CabinClass


class EmailService(object):
    def __init__(self):
        self.__email_messages = []

    def add_flight(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        self.__email_messages.append(self.__email_message(new_flight))

    def send(self):
        send_email("\n".join(self.__email_messages))

    def __email_message(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        return "{origin}-{destination} at {date} offers {seats} seats in {cabin}".format(
            origin=new_flight.origin,
            destination=new_flight.destination,
            date=new_flight.out_date.strftime("%Y-%m-%d"),
            seats=new_flight.seats_in_cabin(CabinClass.BUSINESS),
            cabin=CabinClass.BUSINESS,
        )
