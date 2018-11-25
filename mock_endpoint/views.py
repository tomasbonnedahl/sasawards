from django.http import HttpResponse

from mock_endpoint.mock_data import get_mock_response


def mock(request):
    get_data = request.GET
    response = get_mock_response(origin=get_data.get('from'),
                                 destination=get_data.get('to'),
                                 out_date=get_data.get('outDate', ''))
    return HttpResponse(response, content_type="application/json")
