import os
import sendgrid
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from sendgrid import Email
from sendgrid.helpers.mail import Content, Mail

from sas_api.matcher import org_dst_by_user, match
from awards.unsubscribe import unsubscribe_url
from sasawards import settings


def get_positive_changes(changes):
    """
    :type changes: list[response_handler.ChangedResultExisting]
    :rtype: list[sas_api.requester.Result]
    """
    def more_seats(result, existing):
        """
        :type result: sas_api.requester.Result
        :type existing: awards.models.Flight
        """
        return result.business_seats > existing.business_seats

    return [each.result for each in changes if more_seats(each.result, each.existing)]


def compile_diffs(diffs):
    """
    :type diffs: dict
    """
    return diffs['added'] + get_positive_changes(diffs['changed'])


def send_email(to, subject, message):
    if not settings.SEND_EMAILS:
        return

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("no-reply@sasawards.com")
    to_email = Email(to)
    content = Content("text/html", message)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())


def results_to_email(subject, results):
    """
    :type subject: str
    :type results: list[sas_api.requester.Result]
    """
    if not results:
        return

    def all_active_users():
        return User.objects.filter(is_active=True)

    # TODO: Turn this around to {('ORG', 'DST): [user1, user2, ..], ('ORG2', 'DST2): [user3, user4, ...]}?
    _org_dst_by_user = org_dst_by_user(all_active_users())
    results_by_user = match(results, _org_dst_by_user)

    for user, filtered_results in results_by_user.items():
        print('Sending to {}'.format(user.email))
        message = render_to_string('email_template.html', {'results': filtered_results,
                                                           'unsubscribe_url': unsubscribe_url(user)})
        send_email(user.email, subject, message)


def email_diffs(diffs):
    """
    :type diffs: dict
    """
    to_be_mailed = compile_diffs(diffs)
    results_to_email(subject='New seats found', results=to_be_mailed)
