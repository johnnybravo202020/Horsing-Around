from django.db import models
from .abstract import BaseRaceResult
from scrapper.managers import RaceResultTestDataManager
from .actual import RaceResult


class RaceResultTestData(BaseRaceResult):
    html_row = models.TextField()
    objects = RaceResultTestDataManager()

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