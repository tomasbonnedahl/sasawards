# Generated by Django 2.1.3 on 2018-12-27 19:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0008_airport_subscription_subscriptiontoairport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('stop_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('days_ahead', models.IntegerField(default=330)),
            ],
        ),
    ]