from django.db import models
from .managers import RaceResultManager

class RaceResult(models.Model):
    horse_name = models.TextField()
    horse_id = models.IntegerField()
    result = models.IntegerField()
    horse_age = models.TextField()
    horse_father_id = models.IntegerField()
    horse_mother_id = models.IntegerField()
    horse_weight = models.FloatField()
    jockey_id = models.IntegerField()
    owner_id = models.IntegerField()
    trainer_id = models.IntegerField()
    time = models.TextField()
    handicap = models.IntegerField()
    track_type = models.TextField()
    distance = models.IntegerField()
    city = models.TextField()

    def __str__(self):
        return "{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|{13}".format(self.horse_name,
                                                                                    self.horse_id,
                                                                                    self.result,
                                                                                    self.horse_age,
                                                                                    self.horse_father_id,
                                                                                    self.horse_mother_id,
                                                                                    self.horse_weight,
                                                                                    self.jockey_id,
                                                                                    self.owner_id,
                                                                                    self.trainer_id,
                                                                                    self.time,
                                                                                    self.handicap,
                                                                                    self.track_type,
                                                                                    self.distance)
