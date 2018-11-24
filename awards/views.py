from django.http import HttpResponse
from django.shortcuts import render

from awards.models import Dummy2, Flight, Changes


def index(request):
    dummy = Dummy2(text='afss')
    dummy.save()
    val = Dummy2.objects.all().count()

    return HttpResponse('Hello: {}'.format(val))


def show_seats_and_changes(request):
    flights = Flight.objects.all()
    changes = Changes.objects.all()
    return render(request, "flights.html", {"flights": flights, "changes": changes})
