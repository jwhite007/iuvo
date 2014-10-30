# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('name', models.CharField(max_length=30)),
                ('phone_str', models.CharField(max_length=15)),
                ('phone_int', models.CharField(max_length=10, null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=80)),
                ('message', models.TextField(blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('title', models.CharField(max_length=80)),
                ('start_day', models.CharField(max_length=15)),
                ('start_time', models.CharField(max_length=15)),
                ('start_date', models.DateTimeField()),
                ('end_day', models.CharField(max_length=15)),
                ('end_time', models.CharField(max_length=15)),
                ('end_date', models.DateTimeField()),
                ('notify_day', models.CharField(max_length=15)),
                ('notify_time', models.CharField(max_length=15)),
                ('notify_date', models.DateTimeField()),
                ('contacts', models.ManyToManyField(to='iuvo_app.Contact')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
