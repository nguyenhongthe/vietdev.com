# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20170402_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='total_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
