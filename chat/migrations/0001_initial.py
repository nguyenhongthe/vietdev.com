# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-09 05:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField()),
                ('users', models.ManyToManyField(related_name='_conversation_users_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-last_updated',),
            },
        ),
    ]
