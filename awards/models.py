import datetime

from django.contrib.auth.models import User
from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=3)
    currently_fetching = models.BooleanField(default=True)

    # Separate origin from destination
    destination = models.BooleanField(default=True)

    def __str__(self):
        return "{}, {}".format(self.code, "fetching" if self.currently_fetching else "not fetching")


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return "For {}".format(self.user.email)


class SubscriptionToAirport(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return "{} for {}".format(self.subscription.user.email, self.airport.code)


class Conf(models.Model):
    start_date = models.DateField(default=datetime.date.today)
    stop_date = models.DateField(default=datetime.date.today, null=True, blank=True)

    # Used if stop_date is None
    days_ahead = models.IntegerField(default=330)

    def __str__(self):
        return "{} {}".format(self.start_date,
                              self.stop_date if self.stop_date is not None else "and {} days ahead".format(
                                  self.days_ahead
                              ))


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
