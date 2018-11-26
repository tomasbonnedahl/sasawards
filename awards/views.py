from django.http import HttpResponse
from django.shortcuts import render

from awards.email import send_email
from awards.models import Flight, Changes


def index(request):
    return HttpResponse('Hello')


def show_seats_and_changes(request):
    flights = Flight.objects.all()
    changes = Changes.objects.all()
    return render(request, "flights.html", {"flights": flights, "changes": changes})
