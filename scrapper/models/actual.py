from .abstract import BaseRaceResult
from scrapper.managers import RaceResultManager


class RaceResult(BaseRaceResult):
    objects = RaceResultManager()

