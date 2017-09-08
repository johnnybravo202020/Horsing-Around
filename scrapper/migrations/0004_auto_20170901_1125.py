# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0003_raceresult_resultrowscrappertestdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='raceresult',
            name='race_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='raceresult',
            name='race_id',
            field=models.IntegerField(default=0),
        ),
    ]
