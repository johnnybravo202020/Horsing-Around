# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-30 03:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0016_auto_20171030_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictiontestdata',
            name='fixture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction', to='tests.FixtureTestData'),
        ),
    ]
