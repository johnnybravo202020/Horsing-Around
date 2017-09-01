from django.db import models


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

    def __eq__(self, other):
        return self.horse_name == other.horse_name and self.horse_id == other.horse_id and self.result == other.result and self.horse_age == other.horse_age and self.horse_father_id == other.horse_father_id and self.horse_mother_id == other.horse_mother_id and self.horse_weight == other.horse_weight and self.jockey_id == other.jockey_id and self.owner_id == other.owner_id and self.trainer_id == other.trainer_id and self.time == other.time and self.handicap == other.handicap and self.track_type == other.track_type and self.distance == other.distance and self.city == other.city
