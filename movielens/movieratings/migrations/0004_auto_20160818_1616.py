# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 20:16
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth import get_user_model


def connect_rater_to_user(apps, schema_editor):
    User = get_user_model()
    Rater = apps.get_model('movieratings', 'Rater')

    raters = Rater.objects.all()

    for rater in raters:
        temp_user = User.objects.create_user(
            username="user{}".format(rater.id),
            email="user{}@andchill.com".format(rater.id),
            password="password")
        rater.user_id = temp_user.id
        rater.save()


class Migration(migrations.Migration):

    dependencies = [
        ('movieratings', '0003_rater_user'),
    ]

    operations = [
        migrations.RunPython(connect_rater_to_user)
    ]
