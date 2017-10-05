from django.db import models


class ResultMixin(models.Model):
    class Meta:
        abstract = True

    result = models.IntegerField(default=-1)
    handicap = models.IntegerField(default=-1)
    time = models.CharField(max_length=200, default=-1)
