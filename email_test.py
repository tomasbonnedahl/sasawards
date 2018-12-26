import os

os.environ.setdefault("DJANGO_SECRET_KEY", "abc123456")
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("REDIS_PASSWD", "tomas")
os.environ.setdefault("EMAIL_HOST_USER", "-")
os.environ.setdefault("EMAIL_HOST_PASSWORD", "-")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasawards.settings")

import django
django.setup()

from django.contrib.auth.models import User
user = User.objects.get(pk=1)

from awards.email import results_to_email
from awards.models import Flight
import datetime

flight = Flight(origin='ORG',
                destination='DST',
                date=datetime.date(2019, 1, 1),
                business_seats=2,
                plus_seats=3)

results_to_email("Testing", [flight])
