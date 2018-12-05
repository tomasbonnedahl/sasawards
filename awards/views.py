from django.http import HttpResponse
from django.shortcuts import render

from awards.models import Flight, Changes, ApiError


def index(request):
    return HttpResponse('Hello')


def show_seats_and_changes(request):
    flights = Flight.objects.all()
    changes = Changes.objects.all()
    return render(request, "flights.html", {"flights": flights,
                                            "changes": changes,
                                            })

def errors(requests):
    errors = ApiError.objects.all().order_by('-ts')
    return render(requests, "errors.html", {"errors": errors})
