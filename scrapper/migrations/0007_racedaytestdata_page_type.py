# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-06 01:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0006_fixturetestdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='racedaytestdata',
            name='page_type',
            field=models.CharField(default='F', max_length=1),
            preserve_default=False,
        ),
    ]
