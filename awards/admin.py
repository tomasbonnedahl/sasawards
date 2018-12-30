from django.contrib import admin

# Register your models here.
from awards.models import Airport, Subscription, SubscriptionToAirport, Conf

admin.site.register(Airport)
admin.site.register(Subscription)
admin.site.register(SubscriptionToAirport)
admin.site.register(Conf)
