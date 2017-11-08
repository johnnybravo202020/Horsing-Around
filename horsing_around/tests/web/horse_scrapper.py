from django.test import TestCase
from horsing_around.scrappers import ResultScrapper, FixtureScrapper
from ... import City, PageType
from bs4 import BeautifulSoup
from ..models import RaceDayTestData
from ..string_util import turkish_chars_to_ascii_chars
import datetime


class RaceDayScrapperTestCase(TestCase):
    def test_can_get_past_results_1(self):
        res = FixtureScrapper.scrap(City.Istanbul, 2017, 8, 11, get_past_statistics=True)
        raise Exception(res)