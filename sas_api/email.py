import os

from django.conf import settings
from django.core.mail import send_mail

from sas_api.requester import CabinClass


def send_email(subject, message):
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [os.environ['EMAIL_HOST_USER'], ]
    send_mail(subject, message, email_from, recipient_list)


class EmailService(object):
    def __init__(self, log):
        self.log = log
        self.__email_messages = []

    def add_flight(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        self.__email_messages.append(self.__email_message(new_flight))

    def add_error(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        self.__email_messages.append("Error for flight {}-{} at {}".format(
            new_flight.origin,
            new_flight.destination,
            new_flight.out_date
        ))

    def send(self, subject):
        try:
            send_email(subject, "\n\n".join(self.__email_messages))
            self.__email_messages = []  # Do not want to keep old messages once sent
        except Exception as e:
            self.log('Received exception in e-mail: {}'.format(e))

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
