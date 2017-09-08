from django.db import models
from HorsingAround.collections import OrderedClassMembers


class BaseRaceResult(models.Model):
    class Meta:
        abstract = True
    __metaclass__ = OrderedClassMembers

    race_id = models.IntegerField(default=0)
    race_date = models.DateField(blank=True, null=True)
    horse_name = models.CharField(max_length=200)
    horse_id = models.IntegerField()
    result = models.IntegerField()
    horse_age = models.CharField(max_length=200)
    horse_father_id = models.IntegerField()
    horse_mother_id = models.IntegerField()
    horse_weight = models.CharField(max_length=200)
    jockey_id = models.IntegerField()
    owner_id = models.IntegerField()
    trainer_id = models.IntegerField()
    time = models.CharField(max_length=200)
    handicap = models.IntegerField()
    track_type = models.CharField(max_length=200)
    distance = models.IntegerField()
    city = models.CharField(max_length=200)

    def get_pure_dict(self, *remove_keys):
        _dict = self.__dict__
        for key in remove_keys:
            _dict.pop(key)

        try:
            _dict.pop('_state')

            # This is only record id, it is in irrelevant
        except KeyError:
            # No need to handle since we generally do not care about _state
            pass

        return _dict

    def __str__(self):
        return "|".join(list(self.get_pure_dict("id").values()))

    def __eq__(self, other):
        return self.get_pure_dict() == other.get_pure_dict()