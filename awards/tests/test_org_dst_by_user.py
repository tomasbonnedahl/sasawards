import pytest
from django.contrib.auth.models import User

from awards.matcher import org_dst_by_user
from awards.models import Subscription, SubscriptionToAirport, Airport


def user(i):
    return User.objects.create(email='dummy{}@gmail.com.format(i)', username='dummy{}'.format(i))


@pytest.fixture
def users():
    return [user(i) for i in range(0, 2)]


@pytest.fixture
def airports_by_user(users):
    d = {}
    for i, user in enumerate(users):
        origin_airport = Airport.objects.create(code='OR{}'.format(i), destination=False)
        destination_airport = Airport.objects.create(code='OR{}'.format(i), destination=True)
        subscription = Subscription.objects.create(user=user)
        for airport in [origin_airport, destination_airport]:
            SubscriptionToAirport.objects.create(subscription=subscription, airport=airport)
        d[user] = (origin_airport.code, destination_airport.code)
    return d


@pytest.mark.django_db
def test_org_dst_by_user(users, airports_by_user):
    result = org_dst_by_user(users)

    assert len(result) == len(users)
    for user in users:
        expected_origin, expected_destination = airports_by_user[user]
        assert result[user]['origins'] == [expected_origin]
        assert result[user]['destinations'] == [expected_destination]
