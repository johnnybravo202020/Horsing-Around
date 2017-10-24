from django.db import models
from .managers import TestDataManager
from horsing_around.enum import City, PageType
from horsing_around.models.mixin import ResultMixin
from horsing_around.models.abstract import BaseRaceResult


class BaseTestData(BaseRaceResult):
    class Meta:
        abstract = True

    html_row = models.TextField()

    scrapper = NotImplemented

    @classmethod
    def from_actual(cls, actual, html_row):
        actual_as_dict = actual.get_pure_dict()

        model_as_dict = {'html_row': str(html_row)}

        for key, value in actual_as_dict.items():
            model_as_dict[key] = value

        return cls(**model_as_dict)

    def __eq__(self, other):
        self_as_dict = self.get_pure_dict()

        for key, value in other.get_pure_dict().items():
            other_value = self_as_dict[key]
            if other_value != value:
                print('Value of key: {0} is not equal to other value. ({1}<value {2}, {3}<value {4}>)'.
                      format(key,
                             type(value),
                             value,
                             type(other_value),
                             other_value))

                return False
        return True

    def __str__(self):
        return "|".join(k + ': ' + str(v) for k, v in self.get_pure_dict('html_row', 'id').items())


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

    def get_scrapper(self):
        scrapper = PageType(self.page_type).scrapper
        #raise Exception(type(scrapper))
        return scrapper(City(self.city_id), self.date, self.html_source, self.url)

    def __str__(self):
        return "{0}: In {1}, at {2}".format(PageType(self.page_type).name, City(self.city_id).name, self.date)


class ResultTestData(BaseTestData, ResultMixin):
    objects = TestDataManager()
    race_day = models.ForeignKey(RaceDayTestData, related_name='results')


class FixtureTestData(BaseTestData):
    objects = TestDataManager()
    race_day = models.ForeignKey(RaceDayTestData, related_name='fixtures')


class HorseTestData(BaseTestData):
    objects = TestDataManager()

