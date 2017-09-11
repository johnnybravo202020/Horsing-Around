from django.test import TestCase
from .models import (RaceResult, RaceResultTestData, RaceDayTestData)
from .scrappers import ResultRowScrapper, City, RaceDayScrapper
from bs4 import BeautifulSoup
import datetime
from HorsingAround.string_util import turkish_chars_to_ascii_chars


class ResultRowScrapperTestCase(TestCase):
    def test_can_scrap_single_row(self):
        # We pick one lucky record
        recorded_result = RaceResultTestData.objects.get_random()

        # Initializing a soup object from html in order to parse more
        soup_object = BeautifulSoup(recorded_result.html_row)

        scrapper = ResultRowScrapper(soup_object)
        scrapped_result = scrapper.get()

        # Since it is not row scrappers job to scrap the information of the race itself we assign manually
        scrapped_result.id = recorded_result.id
        scrapped_result.race_id = recorded_result.race_id
        scrapped_result.race_date = recorded_result.race_date
        scrapped_result.track_type = recorded_result.track_type
        scrapped_result.city = recorded_result.city
        scrapped_result.distance = recorded_result.distance

        # Delete the html_row property which is not a part of the actual model
        delattr(recorded_result, "html_row")

        self.assertEqual(recorded_result, scrapped_result)


class RaceDayScrapperTestCase(TestCase):
    def test_can_scrap_race_day(self):

        test_race_days = RaceDayTestData.objects.all()

        for race_day in test_race_days:
            scrapper = RaceDayScrapper.from_test_data_model(race_day)
            recorded_results = race_day.results.all()

            scraped_races = scrapper.get()
            for race in scraped_races:
                for scrapped_result in race:
                    recorded_result = recorded_results.get(horse_id=scrapped_result.horse_id,
                                                           race_id=scrapped_result.race_id)
                    # The scrapped race is not going have an id we simple assign the recorded_result's id
                    scrapped_result.id = recorded_result.id
                    self.assertEqual(recorded_result, scrapped_result)

    def assert_city(self, city, date):
        '''
        Helper method to determine if correct city has been gotten from the scrapper
        :param city: one case from enum City which will determine which city to get html for
        :param date: date of the desired race
        '''
        # Download the source of the html page
        html = RaceDayScrapper(city, date).html

        # Get the Soap object for easy tag search
        soup = BeautifulSoup(html)

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
        sepeartly and will try to match them
        """
        random_race_day = RaceDayTestData.objects.get_random()
        scrapped_races_from_test_data = RaceDayScrapper.from_test_data_model(random_race_day).get()
        scrapper_races_from_web_site = RaceDayScrapper(City(random_race_day.city_id), random_race_day.date).get()

        for race_index, test_race in enumerate(scrapped_races_from_test_data):
            for result_index, test_result in enumerate(test_race):
                self.assertEqual(scrapper_races_from_web_site[race_index][result_index],
                                 test_result,
                                 "Results are inconsistent, probably TJK's web site has been updated.")


class RaceResultTestDataTestCase(TestCase):
    def test_str(self):
        expected = 'race_id: 110862|race_date: 2017-07-03|horse_name: KARAHİNDİBAYA |horse_id: 70111|result: 1|' \
                   'horse_age: 2y d  d|horse_father_id: 20224|horse_mother_id: 17924|horse_weight: 55+1.90|' \
                   'jockey_id: 576|owner_id: 12282|trainer_id: 1473|time: 1.05.76|handicap: -1|track_type: Çim|' \
                   'distance: 1100|city: Bursa|race_day_id: 1'

        outcome = str(RaceResultTestData.objects.get(horse_id=70111, race_id=110862))
        self.assertEqual(expected, outcome, "The outcome: " + outcome)
