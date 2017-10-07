from django.db import models
from random import randint


class TestDataManager(models.Manager):
    def get_random(self):
        """
        :return: A a single record picked randomly
        """
        # Pick the lucky index and return the value
        random_index = randint(0, self.count() - 1)
        return self.all()[random_index]
