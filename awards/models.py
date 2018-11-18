from django.db import models

class Dummy(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    text = models.CharField(max_length=10)
