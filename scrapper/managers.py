from django.db import models
from django.db.models.aggregates import Count
from random import randint
from .scrappers import (RaceDayScrapper, ResultRowScrapper)


class RaceResultTestDataManager(models.Manager):
    def get_random(self):
        """
        :return: A a single record picked randomly
        """
        # Pick the lucky index and return the value
        random_index = randint(0, self.count() - 1)
        return self.all()[random_index]


class RaceResultManager(models.Manager):
    def scrap(self):
        """
        Scraps data from TJK.org
        :return: Will return the results of a hard-coded url from a past race
        """
        scrapper = RaceDayScrapper()
        return scrapper.get()

