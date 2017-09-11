from django.db import models
from random import randint
from .scrappers import RaceDayScrapper


class BaseTestModelManager(models.Manager):
    def get_random(self):
        """
        :return: A a single record picked randomly
        """
        # Pick the lucky index and return the value
        random_index = randint(0, self.count() - 1)
        return self.all()[random_index]


class RaceResultTestDataManager(BaseTestModelManager):
    pass


class RaceResultManager(models.Manager):
    def scrap(self, city, date):
        """
        Scraps data from TJK.org
        :return: Will return the results of a hard-coded url from a past race
        """
        scrapper = RaceDayScrapper(city, date)
        return scrapper.get()


class HTMLSourceTestDataManager(BaseTestModelManager):
    def get_html_and_save(self, city, date):
        """
        Gets the information from the scrapper and saves it to the db, for the sake of making unittests faster
        :param city: City of the desired race day
        :param date: Date of the desired race day
        """
        scrapper = RaceDayScrapper(city, date)
        scrapper.get_test_data_model().save()
