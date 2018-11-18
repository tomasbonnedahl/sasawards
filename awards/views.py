from django.http import HttpResponse

from awards.models import Dummy2


def index(request):
    dummy = Dummy2(text='afss')
    dummy.save()
    val = Dummy2.objects.all().count()

    return HttpResponse('Hello: {}'.format(val))
