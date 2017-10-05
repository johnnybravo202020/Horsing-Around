from .abstract import BaseRaceResult
from scrapper.managers import RaceResultManager
from .mixin import ResultMixin
from django.db import models


class Result(BaseRaceResult, ResultMixin):
    objects = RaceResultManager()

    def __str__(self):
        return "Result:" + super(Result, self).__str__()


class Fixture(BaseRaceResult, models.Model):
    def __str__(self):
        return "Fixture:" + super(Fixture, self).__str__()
