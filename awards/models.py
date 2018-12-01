import datetime
from django.db import models
from enumfields import EnumField


class Flight(models.Model):
    ts = models.DateTimeField(auto_now_add=True)

    origin = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    date = models.DateField(default=datetime.date.today)
    business_seats = models.IntegerField(default=0)
    plus_seats = models.IntegerField(default=0)

    def __str__(self):
        return ("Flight {}-{} at {}, {}/{} (bus/plus)".format(
            self.origin,
            self.destination,
            self.date,
            self.business_seats,
            self.plus_seats
        ))


class Changes(models.Model):
    """
    Defined as positive changes, i.e. adding a new flight or increasing seats
    """
    ts = models.DateTimeField(auto_now_add=True)

    prev_seats = models.IntegerField(default=0)
    to = models.ForeignKey('Flight', on_delete=models.CASCADE)


class ApiError(models.Model):
    """
    Catches errors received from the API
    """
    ts = models.DateTimeField(auto_now_add=True)

    origin = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    date = models.DateField(default=datetime.date.today)

    error_str = models.CharField(max_length=1000)
