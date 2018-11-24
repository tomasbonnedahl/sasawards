import datetime
from django.db import models
from enumfields import EnumField

from sas_api.requester import CabinClass


class Flight(models.Model):
    ts = models.DateTimeField(auto_now_add=True)

    origin = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    date = models.DateField(default=datetime.date.today)
    seats = models.IntegerField(default=0)
    cabin = EnumField(CabinClass)


class Changes(models.Model):
    """
    Defined as positive changes, i.e. adding a new flight or increasing seats
    """
    ts = models.DateTimeField(auto_now_add=True)

    prev_seats = models.IntegerField(default=0)
    to = models.ForeignKey('Flight', on_delete=models.CASCADE)

# Multiple rows for origin, destination, and date, depends on enum type
