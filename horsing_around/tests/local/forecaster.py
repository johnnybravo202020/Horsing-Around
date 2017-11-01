from django.test import TestCase
from ..models import RaceDayTestData


class RegressionTestCase(TestCase):
    def test_can_do_linear_regression(self):
        race_day = RaceDayTestData.objects.get(id=46)
        fixtures = race_day.fixtures.all()
        data_model = race_day.data_model

        ls = list()

        for race in data_model.races:
            for forecast in race.forecasts:
                for prediction in forecast:
                    ls.append(prediction.prediction)
                    # Getting the pre-saved prediction to compare
                    prediction_test_data = fixtures.get(race_id=race.id, horse_id=prediction.horse_id).prediction.get()
                    self.assertEqual(str(prediction.prediction), prediction_test_data.prediction)