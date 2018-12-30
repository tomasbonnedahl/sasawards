from collections import defaultdict
from itertools import product


def match(results, subscriptions_by_user):
    """
    All updated flights as list of Result
    A dict per user -> {'origins': [...], 'destinations': [...]}
    Returns dict user -> [Result, Result, ...]

    :type results: list[sas_api.requester.Result]
    :type subscriptions_by_user: dict[User|dict[str|list]]
    """

    org_dst_by_user = {}

    dd = defaultdict(list)
    for user, sub in subscriptions_by_user.items():
        for each in product(sub['origins'], sub['destinations']):

            key = tuple([e.code for e in each])
            dd[key].append(user)

    for result in results:
        if (result.origin, result.destination) in dd:
            for user in dd[(result.origin, result.destination)]:
                if user not in org_dst_by_user:
                    org_dst_by_user[user] = []
                org_dst_by_user[user].append(result)

    print('result: {}'.format(org_dst_by_user))
    return org_dst_by_user
