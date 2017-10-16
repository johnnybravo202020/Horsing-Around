from django.db import models
from HorsingAround.collections import OrderedClassMembers
import copy


class BaseModel(models.Model):
    class Meta:
        abstract = True
    __metaclass__ = OrderedClassMembers
    race_id = models.IntegerField(default=0)
    race_date = models.DateField(blank=True, null=True)
    horse_id = models.IntegerField()
    jockey_id = models.IntegerField()
    owner_id = models.IntegerField()
    trainer_id = models.IntegerField()

    past_results = list()

    def set_past_results(self):
        from scrapper.scrappers.page import HorseScrapper
        past_scrapper = HorseScrapper(self.horse_id)
        past_results = past_scrapper.get()
        self.past_results.append(past_results)

    def get_pure_dict(self, *remove_keys):
        # We need to have a separate dictionary because we are going to pop keys and we need to avoid changing the
        # original object
        _dict = copy.deepcopy(self.__dict__)
        for key in remove_keys:
            _dict.pop(key)

        try:
            _dict.pop('_state')
        except KeyError:
            # No need to handle since we generally do not care about _state
            pass

        return _dict

    def __str__(self):
        return "|".join(k + ': ' + str(v) for k, v in self.get_pure_dict('id').items())

    def __eq__(self, other):
        return self.get_pure_dict() == other.get_pure_dict()


class BaseRaceResult(BaseModel):
    class Meta:
        abstract = True

    horse_name = models.CharField(max_length=200)
    horse_id = models.IntegerField()
    horse_age = models.CharField(max_length=200)
    horse_father_id = models.IntegerField()
    horse_mother_id = models.IntegerField()
    horse_weight = models.CharField(max_length=200)
    track_type = models.CharField(max_length=200)
    distance = models.IntegerField()
    city = models.CharField(max_length=200)


class BaseTestData(BaseRaceResult):
    class Meta:
        abstract = True

    html_row = models.TextField()

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


