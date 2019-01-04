from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string

from awards.models import Flight, Changes, ApiError
from awards.unsubscribe import user_from_token, unsubscribe_user, unsubscribe_url


# @login_required
def index(request):
    return HttpResponse('Hello')


def unsubscribe(request, token):
    user = user_from_token(token)
    if user is None:
        return HttpResponse('Unknown user'.format())
    unsubscribe_user(user)
    return HttpResponse('{} un-subscribed'.format(user.email))


def show_seats_and_changes(request):
    flights = Flight.objects.all().order_by('-ts')
    changes = Changes.objects.all().order_by('-ts')
    return render(request, "flights.html", {"flights": flights,
                                            "changes": changes,
                                            })


@login_required
def errors(requests):
    errors = ApiError.objects.all().order_by('-ts')
    return render(requests, "errors.html", {"errors": errors})
