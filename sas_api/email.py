import os

import sendgrid
from sendgrid.helpers.mail import *

from email_template import mid, before, after
from sas_api.requester import CabinClass
from sasawards import settings


def send_email(subject, message):
    if not settings.SEND_EMAILS:
        return

    for to in ["bonnedahl@gmail.com",
               "cassonlucy@gmail.com",
               "josefin@backman.se",
               "t.bonnedahl@gmail.com"
               ]:
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("seats@sasawards.com")
        to_email = Email(to)
        content = Content("text/html", message)
        mail = Mail(from_email, subject, to_email, content)
        sg.client.mail.send.post(request_body=mail.get())


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
            if self.__email_messages:
                message = before
                for each in self.__email_messages:
                    message += each
                message += after
                send_email(subject, message)
                self.__email_messages = []  # Do not want to keep old messages once sent
        except Exception as e:
            self.log('Received exception in e-mail: {}'.format(e))

    def __email_message(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        return mid.format(origin=new_flight.origin,
                          to=new_flight.destination,
                          date=new_flight.out_date.strftime("%Y-%m-%d"),
                          business_seats=new_flight.seats_in_cabin(CabinClass.BUSINESS),
                          )
