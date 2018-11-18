from django.http import HttpResponse
from django.shortcuts import render

from awards.models import Dummy2, Flight
from sas_api.mock_data import get_response


def index(request):
    dummy = Dummy2(text='afss')
    dummy.save()
    val = Dummy2.objects.all().count()

    return HttpResponse('Hello: {}'.format(val))


def show_seats_and_changes(request):
    data = Flight.objects.all()
    render(request, "flights.html", {"data": data})


def mock(request):
    """
    http://localhost:5000/mock/?to=PVG&from=CPH&outDate=20191002

    """
    print(request.GET.get('from', ''))
    print(request.GET.get('to', ''))
    print(request.GET.get('outDate', ''))

    get_data = request.GET
    response = get_response(origin=get_data.get('from'),
                            destination=get_data.get('to'),
                            out_date=get_data.get('outDate', ''))

    # return JsonResponse(s)
    return HttpResponse(response, content_type="application/json")
