from django.test import TestCase
from . models import (RaceResult, RaceResultTestData)
from . scrappers.result_row_scrapper import ResultRowScrapper
from bs4 import BeautifulSoup


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

        # And html_row property is not a part of actual model
        delattr(recorded_result, "html_row")

        self.assertEqual(recorded_result, scrapped_result)


class RaceDayScrapperTestCase(TestCase):
    def test_can_scrap_race_day(self):
        scraped_races = RaceResult.objects.scrap()
        recorded_results = RaceResultTestData.objects.all()
        for race in scraped_races:
            for scrapped_result in race:
                recorded_result = recorded_results.get(horse_id=scrapped_result.horse_id, race_id=scrapped_result.race_id)
                # The scrapped race is not going have an id we simple assign the recorded_result's id
                scrapped_result.id = recorded_result.id
                self.assertEqual(recorded_result, scrapped_result)


class RaceResultTestCase(TestCase):
    def test_str(self):
        expected = 'race_id: 110862|race_date: 2017-07-03|horse_name: KARAHİNDİBAYA |horse_id: 70111|result: 1|horse_age: 2y d  d|horse_father_id: 20224|horse_mother_id: 17924|horse_weight: 55+1.90|jockey_id: 576|owner_id: 12282|trainer_id: 1473|time: 1.05.76|handicap: -1|track_type: Çim|distance: 1100|city: Bursa'
        outcome = str(RaceResultTestData.objects.get(horse_id=70111, race_id=110862))
        self.assertEqual(expected, outcome, "The outcome: " + outcome)

