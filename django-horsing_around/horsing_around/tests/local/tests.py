from django.test import TestCase
from bs4 import BeautifulSoup
from ..models import FixtureTestData, ResultTestData, RaceDayTestData
from ...enum import PageType, City
from ...scrappers import ResultScrapper, FixtureScrapper, HorseScrapper, PageDoesNotExist
from ...scrappers.row import ResultRowScrapper, FixtureRowScrapper


class RowScrapperTestCase(TestCase):
    def assert_row_scrapper(self, test_model, row_scrapper):
        # We pick one lucky record
        recorded_result = test_model.objects.get_random()

        # Initializing a soup object from html in order to parse more
        soup_object = BeautifulSoup(recorded_result.html_row, "lxml")

        scrapper = row_scrapper(soup_object)
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

    def test_can_scrap_single_result_row(self):
        self.assert_row_scrapper(ResultTestData, ResultRowScrapper)

    def test_can_scrap_single_fixture_row(self):
        self.assert_row_scrapper(FixtureTestData, FixtureRowScrapper)


class RaceDayScrapperTestCase(TestCase):
    def assert_race_day(self, page_type, scrapper):
        test_race_days = RaceDayTestData.objects.filter(page_type=page_type.value)

        for race_day in test_race_days:
            scrapper = scrapper.from_test_data_model(race_day)

            # It could either be fixtures or results for the race_day
            runs = getattr(race_day, page_type.name.lower() + 's')
            recorded_results = runs.all()

            scraped_races = scrapper.get()
            for race in scraped_races:
                for scrapped_result in race:
                    recorded_result = recorded_results.get(horse_id=scrapped_result.horse_id,
                                                           race_id=scrapped_result.race_id)
                    # The scrapped race is not going have an id we simple assign the recorded_result's id
                    scrapped_result.id = recorded_result.id
                    self.assertEqual(recorded_result, scrapped_result)

    def test_can_scrap_race_day_result(self):
        self.assert_race_day(PageType.Result, ResultScrapper)

    def test_can_scrap_race_day_fixture(self):
        self.assert_race_day(PageType.Fixture, FixtureScrapper)

    def test_will_fail_on_invalid_result_page(self):
        # There was no race run in Izmir at 2017-10-24 therefore PageDoesNotExist exception should be raised
        self.assertRaises(PageDoesNotExist, ResultScrapper.scrap, City.Izmir, 2017, 10, 24)

    def test_will_fail_on_invalid_fixture_page(self):
        # There was no race run in Kocaeli at 2017-10-21 therefore PageDoesNotExist exception should be raised
        self.assertRaises(PageDoesNotExist, FixtureScrapper.scrap, City.Kocaeli, 2017, 10, 21)

    def test_will_fail_on_invalid_horse_page(self):
        # There is no horse with the id: 545454 therefore PageDoesNotExist exception should be raised
        self.assertRaises(PageDoesNotExist, HorseScrapper.scrap, 545454)


class ResultTestDataTestCase(TestCase):
    def test_str(self):
        expected = 'race_id: 110862|race_date: 2017-07-03|jockey_id: 576|owner_id: 12282|trainer_id: 1473|' \
                   'horse_name: KARAHİNDİBAYA |horse_id: 70111|horse_age: 2y d  d|horse_father_id: 20224|' \
                   'horse_mother_id: 17924|horse_weight: 55+1.90|track_type: Çim|distance: 1100|city: Bursa|' \
                   'result: 1|handicap: -1|time: 1.05.76|race_day_id: 1'

        outcome = str(ResultTestData.objects.get(horse_id=70111, race_id=110862))
        self.assertEqual(expected, outcome, "The outcome: {0} is not equal to the expected: {1}".format(outcome,
                                                                                                        expected))
