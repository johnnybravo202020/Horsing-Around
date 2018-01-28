from django.db import models
from .managers import TestDataManager
from .. import City, PageType
from horsing_around.models import Horse, Result, Fixture
from horsing_around.models.mixin import ResultMixin
from horsing_around.models.abstract import BasePage
import importlib
from itertools import groupby
from ..forecaster import RaceDay


class BaseTestData(BasePage):
    class Meta:
        abstract = True

    objects = TestDataManager()
    html_row = models.TextField(null=True)
    scrapper = NotImplemented
    actual_model = NotImplemented
    testable = models.BooleanField(default=True)

    def to_actual(self, *exclude_fields):
        return self.actual_model(**self.get_pure_dict(*exclude_fields))

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
                raise Exception('Value of key: {0} is not equal to other value. ({1}<value {2}, {3}<value {4}>)'.
                                format(key,
                                       type(value),
                                       value,
                                       type(other_value),
                                       other_value))

                return False
        return True


def __str__(self):
    return "|".join(k + ': ' + str(v) for k, v in self.get_pure_dict('html_row', 'id').items())


@staticmethod
def get_from_page_type(page_type):
    scrapper_module = importlib.import_module("horsing_around.tests.models")
    return getattr(scrapper_module, '{0}TestData'.format(page_type.name))


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
        return scrapper(City(self.city_id), self.date, self.html_source, self.url)

    @classmethod
    def from_scrapper(cls, scrapper):
        return cls(city_id=scrapper.city.value,
                   date=scrapper.date,
                   html_source=scrapper.html,
                   url=scrapper.url,
                   page_type=scrapper.page_type.value)

    @property
    def data_model(self):
        races = []
        for k, race in groupby(self.fixtures.all(), lambda r: r.race_id):
            # Make all past results to list
            _race = []
            for index, result in enumerate(race):
                actual_result = result.to_actual('race_day_id', '_race_day_cache', 'testable')
                actual_result.past_results = list(result.past_results.all())
                _race.append(actual_result)
            races.append(_race)
        return RaceDay(races)

    def __str__(self):
        return "{0}: In {1}, at {2}".format(PageType(self.page_type).name, City(self.city_id).name, self.date)


class ResultTestData(BaseTestData, ResultMixin):
    race_day = models.ForeignKey(RaceDayTestData, related_name='results')
    actual_model = Result


class FixtureTestData(BaseTestData):
    race_day = models.ForeignKey(RaceDayTestData, related_name='fixtures')
    actual_model = Fixture

    @classmethod
    def from_actual(cls, actual, html_row):
        delattr(actual, 'past_results')
        return super(FixtureTestData, cls).from_actual(actual, html_row)


class HorseTestData(BaseTestData, ResultMixin):
    fixture = models.ForeignKey(FixtureTestData, related_name='past_results')
    actual_model = Horse


class PredictionTestData(models.Model):
    fixture = models.ForeignKey(FixtureTestData, related_name='prediction')
    prediction = models.CharField(max_length=50)
    predictor = models.CharField(max_length=50)
