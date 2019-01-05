import operator
from collections import namedtuple

from awards.models import Flight, Changes
from sas_api.email import email_diffs
from sas_api.requester import CabinClass

ChangedResultExisting = namedtuple('ChangedResultExisting', 'result existing')


def diff_from_results_and_existing(results, existing):
    """
    :type results: list[sas_api.requester.Result]
    :type existing: list[awards.models.Flight]
    :rtype: dict
    """
    result_key = lambda x: (x.origin, x.destination, x.departure_date)
    result_by_key = {result_key(each): each for each in results}

    flight_key = lambda x: (x.origin, x.destination, x.date)
    existing_by_key = {flight_key(each): each for each in existing}

    added_keys = result_by_key.keys() - existing_by_key.keys()
    added = [result_by_key[key] for key in added_keys]

    deleted_keys = existing_by_key.keys() - result_by_key.keys()
    deleted = [existing_by_key[key] for key in deleted_keys]

    changed_keys = set(existing_by_key.keys()).intersection(result_by_key.keys())
    changed = [ChangedResultExisting(result=result_by_key[key],
                                     existing=existing_by_key[key]) for key in changed_keys]

    return {
        'added': added,
        'changed': changed,
        'deleted': deleted,
    }


def get_diffs(results):
    """
    :type results: list[sas_api.requester.Result]
    """
    # TODO: Only fetch existing for the dates we have results, attach meta data to results?
    # E.g. {'meta': {'from_date': ..., 'to_date': ...}, 'results': list[Results]}
    # Will not remove old flights in db if start_date moves forward
    existing = Flight.objects.all()
    return diff_from_results_and_existing(results, existing)


def save_result(result):
    """
    :type results: sas_api.requester.Result
    """
    def positive_change(existing_flight, result):
        """
        :type result: sas_api.requester.Result
        """
        if not existing_flight:
            return True
        return result.business_seats > existing_flight.business_seats

    if result.business_seats:
        flight, created = Flight.objects.get_or_create(origin=result.origin,
                                                       destination=result.destination,
                                                       date=result.departure_date)

        if created or positive_change(existing_flight=flight, result=result):
            Changes.objects.create(prev_seats=flight.business_seats, to=flight)

        flight.business_seats = result.business_seats
        flight.plus_seats = result.plus_seats
        flight.save()
    else:
        # TODO: This is dangerous if we want to an extra round for a specific week e.g. in May
        # will wipe the rest of the data from the database. Flag to the config? Multiple configs at the same time?
        Flight.objects.filter(origin=result.origin,
                              destination=result.destination,
                              date=result.out_date).delete()


def save_results(results):
    """
    :type results: list[sas_api.requester.Result]
    """
    for result in results:
        save_result(result)


def handle_results(results):
    """
    :type results: list[sas_api.requester.Result]
    """
    diffs = get_diffs(results)
    save_results(results)
    email_diffs(diffs)
