# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-21 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0018_predictiontestdata_predictor'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixturetestdata',
            name='testable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='horsetestdata',
            name='testable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='resulttestdata',
            name='testable',
            field=models.BooleanField(default=True),
        ),
    ]
