# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-30 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0015_predictiontestdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictiontestdata',
            name='prediction',
            field=models.CharField(max_length=50),
        ),
    ]
