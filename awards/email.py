import os
from django.core.mail import send_mail
from django.conf import settings

def send_email(message):
    subject = 'Updates from SAS Awards'
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [os.environ['EMAIL_HOST_USER'], ]
    send_mail(subject, message, email_from, recipient_list)
