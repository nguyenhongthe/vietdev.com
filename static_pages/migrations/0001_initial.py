# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-12 10:17
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import simplemde.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=True, populate_from='title', unique=True)),
                ('content', simplemde.fields.SimpleMDEField(blank=True)),
                ('content_safe', models.TextField(blank=True)),
                ('desc', models.CharField(blank=True, max_length=300)),
                ('public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-updated_at',),
            },
        ),
    ]