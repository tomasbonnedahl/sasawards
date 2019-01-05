import datetime

import pytest

from awards.models import Flight
from sas_api.email import get_positive_changes
from sas_api.requester import Result
from sas_api.response_handler import ChangedResultExisting


@pytest.mark.django_db
def test_get_positive_changes():
    result_increase = Result('OR1', 'DS1', datetime.date(2019, 1, 1), business_seats=3, plus_seats=3)
    result_same = Result('OR2', 'DS2', datetime.date(2019, 1, 1), business_seats=2, plus_seats=2)
    result_decrease = Result('OR3', 'DS3', datetime.date(2019, 1, 1), business_seats=1, plus_seats=1)

    existing1 = Flight(origin='OR1', destination='DS1', date=datetime.date(2019, 1, 1), business_seats=2, plus_seats=2)
    existing2 = Flight(origin='OR2', destination='DS2', date=datetime.date(2019, 1, 1), business_seats=2, plus_seats=2)
    existing3 = Flight(origin='OR3', destination='DS3', date=datetime.date(2019, 1, 1), business_seats=2, plus_seats=2)

    changes = [
        ChangedResultExisting(result=result_increase, existing=existing1),
        ChangedResultExisting(result=result_same, existing=existing2),
        ChangedResultExisting(result=result_decrease, existing=existing3),
    ]
    positive_changes = get_positive_changes(changes)
    assert len(positive_changes) == 1
    assert positive_changes[0] == result_increase
