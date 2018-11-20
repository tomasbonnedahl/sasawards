def a_test():
    from awards.models import Flight
    print('flights: {}'.format(Flight.objects.all()))
    # print('hello')
