from django.db import models
from random import randint
from .scrappers import RaceDayScrapper
import datetime

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
    def scrap_by_date(self, city, date):
        """
        Scraps the results of the supplied city and date
        :param city: City which the race happened
        :param date: datetime object for the desired race
        :return: Returns the results of the desired race
        """
        scrapper = RaceDayScrapper(city, date)
        return scrapper.get()

    def scrap(self, city, year, month, day):
        """
        Scraps the results of the supplied city and date values
        :param city: City which the race happened
        :param year: The year of the wanted race
        :param month: The month of the wanted race
        :param day: The day of the wanted race
        :return: Returns the results of the desired race
        """
        return self.scrap_by_date(city, datetime.datetime(year, month, day))


class HTMLSourceTestDataManager(BaseTestModelManager):
    def get_html_and_save(self, city, date):
        """
        Gets the information from the scrapper and saves it to the db, for the sake of making unittests faster
        :param city: City of the desired race day
        :param date: Date of the desired race day
        """
        scrapper = RaceDayScrapper(city, date)
        scrapper.get_test_data_model().save()
