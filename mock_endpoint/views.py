from django.http import HttpResponse

from mock_endpoint.mock_data import get_mock_response


def mock(request):
    """
    http://localhost:5000/mock/?to=PVG&from=CPH&outDate=20191002

    """
    print(request.GET.get('from', ''))
    print(request.GET.get('to', ''))
    print(request.GET.get('outDate', ''))

    get_data = request.GET
    response = get_mock_response(origin=get_data.get('from'),
                                 destination=get_data.get('to'),
                                 out_date=get_data.get('outDate', ''))

    # return JsonResponse(s)
    return HttpResponse(response, content_type="application/json")
