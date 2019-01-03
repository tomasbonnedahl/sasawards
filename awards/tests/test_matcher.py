import datetime

import pytest
from django.contrib.auth.models import User

from awards.email import results_to_email
from awards.matcher import match
from awards.models import Airport
from sas_api.requester import Result, CabinClass


def create_airport(code, destination=False):
    return Airport.objects.create(code=code, currently_fetching=True, destination=destination)


@pytest.fixture
def user():
    return User.objects.create(email='dummy@gmail.com', username='dummy', first_name='Dummy', last_name='Dummysson')


def create_airports(prefix, destination, num_airports):
    return [create_airport(code=prefix + str(each), destination=destination) for each in range(0, num_airports)]


@pytest.fixture
def origins():
    return create_airports(prefix="OR", destination=False, num_airports=3)


@pytest.fixture
def destinations():
    return create_airports(prefix="DS", destination=True, num_airports=3)


@pytest.mark.django_db
def test_matcher_single_hit(user, origins, destinations):
    airports_by_user = {user: {'origins': origins, 'destinations': destinations}}

    result = Result(origins[0].code, destinations[0].code, datetime.date(2019, 10, 10))
    result.add(CabinClass.BUSINESS, 6)

    matched_result = match([result], airports_by_user)
    assert matched_result == {user: [result]}


@pytest.mark.django_db
def test_matcher_mutiple_users_same_hit(user, origins, destinations):
    another_user = User.objects.create(email='dummy2@gmail.com', username='dummy2')

    airports_by_user = {
        user: {'origins': origins, 'destinations': destinations},
        another_user: {'origins': origins, 'destinations': destinations},
    }

    result = Result(origins[0].code, destinations[0].code, datetime.date(2019, 10, 10))
    result.add(CabinClass.BUSINESS, 6)

    matched_result = match([result], airports_by_user)
    assert matched_result == {
        user: [result],
        another_user: [result]
    }


@pytest.mark.django_db
def test_matcher_mutiple_users_different_hit(user, origins, destinations):
    another_user = User.objects.create(email='dummy2@gmail.com', username='dummy2')

    xxx = Airport.objects.create(code='XXX', currently_fetching=True, destination=False)
    yyy = Airport.objects.create(code='YYY', currently_fetching=True, destination=True)

    airports_by_user = {
        user: {'origins': origins, 'destinations': destinations},
        another_user: {'origins': [xxx], 'destinations': [yyy]},
    }

    result = Result(origins[0].code, destinations[0].code, datetime.date(2019, 10, 10))
    result.add(CabinClass.BUSINESS, 6)

    result2 = Result(xxx.code, yyy.code, datetime.date(2019, 10, 10))
    result2.add(CabinClass.BUSINESS, 2)

    matched_result = match([result, result2], airports_by_user)
    assert matched_result == {
        user: [result],
        another_user: [result2]
    }


@pytest.mark.django_db
def test_matcher_only_origin_matching(user, origins, destinations):
    airports_by_user = {user: {'origins': origins, 'destinations': destinations}}

    result = Result(origins[0].code, 'NIL', datetime.date(2019, 10, 10))
    result.add(CabinClass.BUSINESS, 6)

    matched_result = match([result], airports_by_user)
    assert matched_result == {}


@pytest.mark.django_db
def test_matcher_only_destination_matching(user, origins, destinations):
    airports_by_user = {user: {'origins': origins, 'destinations': destinations}}

    result = Result('NIL', destinations[0].code, datetime.date(2019, 10, 10))
    result.add(CabinClass.BUSINESS, 6)

    matched_result = match([result], airports_by_user)
    assert matched_result == {}


@pytest.mark.django_db
def test_matcher_multiple(user, origins, destinations):
    airports_by_user = {user: {'origins': origins, 'destinations': destinations}}

    result1 = Result(origins[0].code, destinations[0].code, datetime.date(2019, 10, 10))
    result1.add(CabinClass.BUSINESS, 6)
    result2 = Result(origins[1].code, destinations[1].code, datetime.date(2019, 10, 10))
    result2.add(CabinClass.BUSINESS, 3)

    matched_result = match([result1, result2], airports_by_user)
    assert matched_result == {user: [result1, result2]}


@pytest.mark.django_db
def test_matcher_zero_result(user, origins, destinations):
    airports_by_user = {user: {'origins': origins, 'destinations': destinations}}

    result = Result('XXX', 'YYY', datetime.date(2019, 10, 10))
    result.add(CabinClass.BUSINESS, 6)

    matched_result = match([result], airports_by_user)
    assert matched_result == {}


@pytest.mark.django_db
def test_matcher_no_result(user, origins, destinations):
    airports_by_user = {user: {'origins': origins, 'destinations': destinations}}
    matched_result = match([], airports_by_user)
    assert matched_result == {}


@pytest.mark.django_db
def test_prop(user, origins, destinations):
    result = Result(origins[0].code, destinations[0].code, datetime.date(2019, 10, 10))
    results_to_email('Subject', [result])