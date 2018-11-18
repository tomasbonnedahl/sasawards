from django.db import models

class Dummy(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    text = models.CharField(max_length=10)


class Dummy2(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    text = models.CharField(max_length=10)


class Flight(models.Model):
    ts = models.DateTimeField(auto_now_add=True)

    business_seats = models.IntegerField(default=0)
    origin = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)


class Changes(models.Model):
    ts = models.DateTimeField(auto_now_add=True)

    prev_business_seats = models.IntegerField(default=0)
    to = models.ForeignKey('Flight', on_delete=models.CASCADE)
