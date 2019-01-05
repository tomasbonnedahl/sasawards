import datetime
import json
import urllib.parse
from collections import defaultdict

import pytest
from django.contrib.auth.models import User

from awards.models import Airport, Subscription, SubscriptionToAirport
from sas_api.config import Config
from sas_api.requester import fetch_flights
from sas_api.response_handler import handle_results


def create_airport(code, destination=False):
    return Airport.objects.create(code=code, currently_fetching=True, destination=destination)


@pytest.fixture
def user():
    return User.objects.create(email='dummy@gmail.com', username='dummy', first_name='Dummy', last_name='Dummysson')


def create_airports(prefix, destination, num_airports):
    return [create_airport(code=prefix + str(each), destination=destination) for each in range(0, num_airports)]


@pytest.fixture
def origins():
    return create_airports(prefix="OR", destination=False, num_airports=2)


@pytest.fixture
def destinations():
    return create_airports(prefix="DS", destination=True, num_airports=2)


@pytest.fixture
def subscribed_airports(origins, destinations, user):
    airports = []
    subscription = Subscription.objects.create(user=user)
    for airport in [origins[0], origins[1], destinations[0]]:
        SubscriptionToAirport.objects.create(subscription=subscription, airport=airport)
        airports.append(airport)
    return airports


def api_result_raw(origin, destination, departure_date):
    """
    :type departure_date: datetime.datetime
    """
    s = '''{{"pricingType":"C","outboundFlights":{{"F0":{{"id":0,"origin":{{"code":"{origin}","name":"Kastrup"}},"destination":{{"code":"{destination}","name":"Pudong  "}},"originCountry":{{"code":"DK","name":"Denmark"}},"destinationCountry":{{"code":"CN","name":"China"}},"originCity":{{"code":"{origin}","name":"Copenhagen"}},"destinationCity":{{"code":"SHA","name":"Shanghai"}},"connectionDuration":"10:15:00","startTimeInLocal":"{departure_date}T18:40:00.000+02:00","startTimeInGmt":"{departure_date}T16:40:00.000Z","endTimeInLocal":"2019-10-03T10:55:00.000+08:00","endTimeInGmt":"2019-10-03T02:55:00.000Z","stops":0,"segments":[{{"id":11,"arrivalTerminal":"2","arrivalDateTimeInLocal":"2019-10-03T10:55:00.000+08:00","arrivalDateTimeInGmt":"2019-10-03T02:55:00.000Z","departureTerminal":"3","departureDateTimeInLocal":"2019-10-02T18:40:00.000+02:00","departureDateTimeInGmt":"2019-10-02T16:40:00.000Z","departureAirport":{{"code":"{origin}","name":"Kastrup"}},"arrivalAirport":{{"code":"PVG","name":"Pudong  "}},"departureCity":{{"code":"{origin}","name":"Copenhagen"}},"arrivalCity":{{"code":"SHA","name":"Shanghai"}},"departureCountry":{{"code":"DK","name":"Denmark"}},"arrivalCountry":{{"code":"CN","name":"China"}},"airCraft":{{"code":"343","name":"Airbus Industrie A340-300"}},"flightNumber":"997","duration":"10:15:00","marketingCarrier":{{"code":"SK","name":"Scandinavian Airlines"}},"onTimePerformance":0.0,"miles":0,"numberOfStops":0}}],"cabins":{{"BUSINESS":{{"SAS BUSINESS":{{"products":{{"O_2":{{"productName":"SAS BUSINESS","productCode":"EBSARB","lowestFare":true,"recommendations":[1],"price":{{"currency":"NOK","basePrice":0.0,"totalTax":428.0,"totalPrice":428.0,"formattedTotalTax":"428,-","formattedTotalPrice":"428,-","points":120000,"credits":0,"pricePerPassengerType":[{{"id":1,"type":"ADT","numberCount":2,"price":{{"currency":"NOK","basePrice":0.0,"totalTax":214.0,"totalPrice":214.0,"formattedTotalTax":"214,-","formattedTotalPrice":"214,-","points":60000,"credits":0}}}}]}},"fares":[{{"segmentId":"11","fareClass":"IBP00","bookingClass":"I","avlSeats":10}}],"fareKey":"I","flyingToOrOverRussia":true}}}}}}}},"PLUS":{{"SAS PLUS":{{"products":{{"O_1":{{"productName":"SAS PLUS","productCode":"EBSARP","lowestFare":true,"recommendations":[0],"price":{{"currency":"NOK","basePrice":0.0,"totalTax":428.0,"totalPrice":428.0,"formattedTotalTax":"428,-","formattedTotalPrice":"428,-","points":96000,"credits":0,"pricePerPassengerType":[{{"id":1,"type":"ADT","numberCount":2,"price":{{"currency":"NOK","basePrice":0.0,"totalTax":214.0,"totalPrice":214.0,"formattedTotalTax":"214,-","formattedTotalPrice":"214,-","points":48000,"credits":0}}}}]}},"fares":[{{"segmentId":"11","fareClass":"XFBP00","bookingClass":"F","avlSeats":10}}],"fareKey":"F","flyingToOrOverRussia":true}}}}}}}}}},"lowestFares":{{"BUSINESS":{{"product":"SAS BUSINESS","productId":"O_2","avlSeats":10,"points":60000.0}},"PLUS":{{"product":"SAS PLUS","productId":"O_1","avlSeats":10,"points":48000.0}}}}}}}},"productInfo":{{"BUSINESS":{{"1":"SAS BUSINESS"}},"PLUS":{{"1":"SAS PLUS"}}}},"tabsInfo":{{"outboundInfo":[{{"date":"2019-10-01","price":"214,-","points":48000.0}},{{"date":"2019-10-02","price":"214,-","points":48000.0}},{{"date":"2019-10-03","price":"214,-","points":48000.0}}]}},"currency":{{"code":"NOK","name":"Norwegian Krone","symbol":",-","decimalSeperator":".","position":"Suffix","currencyDelimiter":"space"}},"links":[{{"rel":"GetEBMSPoints","href":"/offers/flightproducts/getAccrualPoints"}},{{"rel":"FareReview","href":"/offers/flightproducts/getFare"}},{{"rel":"InitiateCheckout","href":"/checkout/initiate"}}],"regionName":"EB Intercont","offerId":"420e12aa-c1cd-485a-a67c-9af7074d445f_2018-11-16","outboundLowestFare":{{"product":"SAS PLUS","productId":"O_1","avlSeats":10,"points":48000.0,"cabinName":"PLUS","flightId":"F0"}},"isOutboundIntercontinental":true}}'''
    return json.loads(s.format(origin=origin,
                               destination=destination,
                               departure_date=departure_date.strftime("%Y-%m-%d")))


@pytest.mark.django_db
def test_config_to_email(monkeypatch, user, origins, destinations, subscribed_airports):
    def from_url_to_json_mock(url):
        parsed_query_str = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        departure_date = datetime.datetime.strptime(parsed_query_str['outDate'][0], "%Y%m%d")
        return api_result_raw(origin=parsed_query_str['from'][0],
                              destination=parsed_query_str['to'][0],
                              departure_date=departure_date)

    monkeypatch.setattr('sas_api.requester.from_url_to_json', from_url_to_json_mock)

    email_values_by_type = defaultdict()
    def send_email_mock(to, subject, message):
        email_values_by_type['to'] = to
        email_values_by_type['subject'] = subject
        email_values_by_type['message'] = message

    monkeypatch.setattr('sas_api.email.send_email', send_email_mock)

    def zero_random():
        return 0.0

    monkeypatch.setattr('sas_api.requester.random', zero_random)

    config = Config(base_url='http://fakeurl.com/?',
                    min_date=datetime.date(2019, 1, 1),
                    max_date=datetime.date(2019, 1, 2),
                    origins=[each.code for each in origins],
                    destinations=[each.code for each in destinations],
                    seconds=0)

    results = fetch_flights(config)
    handle_results(results)

    assert email_values_by_type['to'] == user.email
    assert email_values_by_type['subject'] == "New seats found"
    for expected in [airport.code for airport in subscribed_airports]:
        assert expected in email_values_by_type['message']
