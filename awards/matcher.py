from collections import defaultdict
from itertools import product

from awards.models import SubscriptionToAirport, Subscription


def org_dst_by_user(users):
    # A dict per user -> {'origins': [...], 'destinations': [...]}
    res = {}
    for user in users:  # TODO: Not efficient, use __in=() instead (or use a Manager?)
        sub_to_airports = SubscriptionToAirport.objects.filter(subscription__in=user.subscriptions.all())
        airports = [sub_to_airport.airport for sub_to_airport in sub_to_airports]

        origins = [airport.code for airport in airports if airport.destination == False]
        destinations = [airport.code for airport in airports if airport.destination == True]
        res[user] = {'origins': origins, 'destinations': destinations}
    return res


def match(results, org_dst_by_user):
    """
    All updated flights as list of Result
    A dict per user -> {'origins': [...], 'destinations': [...]}
    Returns dict user -> [Result, Result, ...]

    :type results: list[sas_api.requester.Result]
    :type org_dst_by_user: dict[User|dict[str|list]]
    """

    """
    results:
    [result1, result2, result3]
    
    org_dst_by_user:
    user1: {'origins': [OR1, OR2], 'destinations': [DS1, DS2]},
    user2: {'origins': [OR3, OR4], 'destinations': [DS4, DS4]},
    
    users_by_org_dst (inverted from input) + includes the return trip:
    {
    (OR1, DS1): [user1, ...],
    (OR1, DS2): [user1, ...],
    ...
    (OR4, DS4): [user2, ...],
    }
    
    """

    users_by_org_dst = defaultdict(list)
    for user, org_dst in org_dst_by_user.items():
        for org, dst in product(org_dst['origins'], org_dst['destinations']):
            key = (org, dst)
            for key in [(org, dst), ((dst, org))]:  # Adding return-trip
                users_by_org_dst[key].append(user)

    result_by_user = {}
    for result in results:
        key = (result.origin, result.destination)
        users = users_by_org_dst.get(key, [])
        for user in users:
            if user not in result_by_user:
                result_by_user[user] = []
            result_by_user[user].append(result)

    return result_by_user
