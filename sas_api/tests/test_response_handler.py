import datetime

import pytest

from awards.models import Flight
from sas_api.requester import Result
from sas_api.response_handler import diff_from_results_and_existing, remove_empty_seats


@pytest.mark.django_db
def test_diff_from_results_and_existing():
    added1 = Result('OR1', 'DS1', datetime.date(2019, 1, 1), business_seats=2, plus_seats=3)
    added2 = Result('ORa', 'DSa', datetime.date(2019, 1, 1), business_seats=2, plus_seats=3)
    empty_seats = Result('ORb', 'DSb', datetime.date(2019, 1, 1), business_seats=0, plus_seats=0)
    none = None

    result_changed1 = Result('ORx', 'DSx', datetime.date(2019, 1, 1), business_seats=2, plus_seats=3)  # Increase in seats
    result_changed2 = Result('ORy', 'DSy', datetime.date(2019, 1, 1), business_seats=1, plus_seats=1)  # Decrease in seats

    results = [
        added1,
        added2,
        empty_seats,
        none,
        result_changed1,
        result_changed2,
    ]

    deleted = Flight(origin='OR2', destination='DS2', date=datetime.date(2019, 1, 2), business_seats=2, plus_seats=3)
    flight_changed1 = Flight(origin='ORx', destination='DSx', date=datetime.date(2019, 1, 1), business_seats=2, plus_seats=3)
    flight_changed2 = Flight(origin='ORy', destination='DSy', date=datetime.date(2019, 1, 1), business_seats=2, plus_seats=3)
    existing = [
        deleted,
        flight_changed1,
        flight_changed2,
    ]

    diff = diff_from_results_and_existing(results, existing)
    assert len(diff['added']) == 2
    for actual, expected in zip(sorted(diff['added']), sorted([added1, added2])):
        assert actual == expected

    assert len(diff['deleted']) == 1
    assert diff['deleted'][0] == deleted

    assert len(diff['changed']) == 2
    expected_changed = [(result_changed1, flight_changed1), (result_changed2, flight_changed2)]
    for actual, expected in zip(sorted(diff['changed']), expected_changed):
        expected_result, expected_existing = expected
        assert actual.result == expected_result
        assert actual.existing == expected_existing


def test_remove_empty_seats():
    a = Result('OR1', 'DS1', datetime.date(2019, 1, 1), business_seats=2, plus_seats=3)
    b = Result('ORa', 'DSa', datetime.date(2019, 1, 1), business_seats=2, plus_seats=3)
    c = Result('ORb', 'DSb', datetime.date(2019, 1, 1), business_seats=0, plus_seats=0)
    d = None

    assert sorted([a, b]) == sorted(remove_empty_seats([a, b, c, d]))
