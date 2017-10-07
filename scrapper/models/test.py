from django.db import models
from .abstract import BaseTestData
from scrapper.managers import TestDataManager
from scrapper.scrappers import City, PageType
from .mixin import ResultMixin


class RaceDayTestData(models.Model):
    """
    Will store the entire html source code of a particular race day for the purpose of making unit tests faster
    rather than waiting for the page to be downloaded.
    """
    objects = TestDataManager()

    html_source = models.TextField()
    url = models.CharField(max_length=200)
    city_id = models.IntegerField(default=0)
    date = models.DateField(blank=True, null=True)
    page_type = models.CharField(max_length=1)

    def __str__(self):
        return "{0}: In {1}, at {2}".format(PageType(self.page_type).name, City(self.city_id).name, self.date)


class ResultTestData(BaseTestData, ResultMixin):
    objects = TestDataManager()
    race_day = models.ForeignKey(RaceDayTestData, related_name='results')


class FixtureTestData(BaseTestData):
    objects = TestDataManager()
    race_day = models.ForeignKey(RaceDayTestData, related_name='fixtures')
