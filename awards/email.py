import os

import sendgrid
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from sendgrid.helpers.mail import *

from awards.unsubscribe import unsubscribe_url
from sas_api.requester import CabinClass
from sasawards import settings


# for to in ["bonnedahl@gmail.com",
# "cassonlucy@gmail.com",
# "josefin@backman.se",
# "t.bonnedahl@gmail.com"
# ]:


def send_email(to, subject, message):
    if not settings.SEND_EMAILS:
        return

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("seats@sasawards.com")
    to_email = Email(to)
    content = Content("text/html", message)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())


def results_to_email(subject, results):
    """
    :type subject: str
    :type results: list[sas_api.requester.Result]
    """
    if results:
        for user in User.objects.filter(is_active=True):
            print('Sending to {}'.format(user.email))
            message = render_to_string('email_template.html', {'results': results,
                                                               'unsubscribe_url': unsubscribe_url(user)})
            send_email(user.email, subject, message)


class EmailService(object):
    def __init__(self, log):
        self.log = log
        self.errors = []
        self.results = []

    def add_result(self, result):
        """
        :type result: sas_api.requester.Result
        """
        self.results.append(result)

    def add_error(self, new_flight):
        """
        :type new_flight: sas_api.requester.Result
        """
        self.errors.append("Error for flight {}-{} at {}".format(
            new_flight.origin,
            new_flight.destination,
            new_flight.out_date
        ))

    def send(self, subject):
        try:
            results_to_email(subject, self.results)

            # Do not want to keep old messages once sent
            self.results = []
        except Exception as e:
            self.log('Received exception in e-mail: {}'.format(e))
