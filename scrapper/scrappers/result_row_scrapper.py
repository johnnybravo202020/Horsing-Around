class ResultRowScrapper:
    def get(self):
        from scrapper.models import RaceResult
        result = RaceResult(
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

        return result
