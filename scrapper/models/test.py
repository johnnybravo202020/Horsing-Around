from django.db import models
from .actual import Result, Fixture
from .abstract import BaseTestData
from scrapper.managers import RaceResultTestDataManager, HTMLSourceTestDataManager
from scrapper.scrappers import City
from .mixin import ResultMixin


class RaceDayTestData(models.Model):
    """
    Will store the entire html source code of a particular race day for the purpose of making unit tests faster
    rather than waiting for the page to be downloaded.
    """
    objects = HTMLSourceTestDataManager()
    html_source = models.TextField()
    url = models.CharField(max_length=200)
    city_id = models.IntegerField(default=0)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "In {0}, at {1}".format(City(self.city_id).name, self.date)


class ResultTestData(BaseTestData, ResultMixin):
    objects = RaceResultTestDataManager()

    from .test import RaceDayTestData
    race_day = models.ForeignKey(RaceDayTestData, related_name='results')
