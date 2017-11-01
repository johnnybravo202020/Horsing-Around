from django.test import TestCase
from horsing_around.scrappers import ResultScrapper, FixtureScrapper
from ... import City, PageType
from bs4 import BeautifulSoup
from ..models import RaceDayTestData
from ..string_util import turkish_chars_to_ascii_chars
import datetime


class LongWebTest(TestCase):
    def assert_city(self, city, date):
        '''
        Helper method to determine if correct city has been gotten from the scrapper
        :param city: one case from enum City which will determine which city to get html for
        :param date: date of the desired race
        '''
        # Download the source of the html page
        html = ResultScrapper(city, date).html

        # Get the Soap object for easy tag search
        soup = BeautifulSoup(html, "lxml")

        # Get the name of the city in the html
        city_in_html = soup.find("div", class_='program').get('id').lower()

        # It might contain some non-ascii characters since it is Turkish
        city_in_html = turkish_chars_to_ascii_chars(city_in_html)

        self.assertEqual(city_in_html, city.name.lower())

    def test_can_get_source_from_city_bursa(self):
        self.assert_city(City.Bursa, datetime.date(2017, 7, 3))

    def test_if_tjk_is_the_same(self):
        """
        We pick a random race day test data and try to match it with the current html. It will scrap both html's
        separately and will try to match them
        """
        random_race_day = RaceDayTestData.objects.get_random()
        scrapped_races_from_test_data = random_race_day.get_scrapper().get()
        scrapper_races_from_web_site = PageType(random_race_day.page_type).scrapper(City(random_race_day.city_id),
                                                                                    random_race_day.date).get()

        for race_index, test_race in enumerate(scrapped_races_from_test_data):
            for result_index, test_result in enumerate(test_race):
                self.assertEqual(scrapper_races_from_web_site[race_index][result_index],
                                 test_result,
                                 "Results are inconsistent, probably TJK's web site has been updated.")
