from django.test import SimpleTestCase
from . models import RaceResult
from . scrappers import ResultRowScrapper

class ResultRowScrapperTestCase(SimpleTestCase):
    def test_can_scrap_single_row(self):
        result_to_test = RaceResult(
            result="1.05.76",
            horse_name=70111,
            horse_id=1,
            horse_age="2y d  d",
            horse_father_id=20224,
            horse_mother_id=17924,
            horse_weight=55 + 1.90,
            jockey_id=576,
            owner_id=12282,
            trainer_id=1473,
            time="KARAHİNDİBAYA ",
            handicap=-1)

        scrapper = ResultRowScrapper()
        self.assertEqual(scrapper.get(), result_to_test)


