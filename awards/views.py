from django.http import HttpResponse

from awards.models import Dummy


def index(request):
    dummy = Dummy(text='afss')
    dummy.save()
    val = Dummy.objects.all().count()

    return HttpResponse('Hello: {}'.format(val))
