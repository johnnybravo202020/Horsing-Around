# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0005_resulttestdata_html_row'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixtureTestData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.IntegerField(default=0)),
                ('race_date', models.DateField(blank=True, null=True)),
                ('horse_name', models.CharField(max_length=200)),
                ('horse_id', models.IntegerField()),
                ('horse_age', models.CharField(max_length=200)),
                ('horse_father_id', models.IntegerField()),
                ('horse_mother_id', models.IntegerField()),
                ('horse_weight', models.CharField(max_length=200)),
                ('jockey_id', models.IntegerField()),
                ('owner_id', models.IntegerField()),
                ('trainer_id', models.IntegerField()),
                ('track_type', models.CharField(max_length=200)),
                ('distance', models.IntegerField()),
                ('city', models.CharField(max_length=200)),
                ('html_row', models.TextField()),
                ('race_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixtures', to='scrapper.RaceDayTestData')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]