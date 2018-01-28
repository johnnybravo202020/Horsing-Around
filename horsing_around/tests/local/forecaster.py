from django.test import TestCase
from ..models import RaceDayTestData

class RegressionTestCase(TestCase):
    def tesat_can_do_regression_2017_10_28_ankara(self):
        race_day = RaceDayTestData.objects.get(id=46)
        fixtures = race_day.fixtures.all()
        data_model = race_day.data_model

        for race in data_model.races:
            for forecast in race.forecasts:
                for prediction in forecast:
                    # Getting the pre-saved prediction to compare
                    prediction_test_data = fixtures.get(race_id=race.id,
                                                        horse_id=prediction.horse_id).prediction.get(
                                                        predictor=forecast.title.replace(' ', ''))
                    self.assertEqual(str(prediction.prediction), prediction_test_data.prediction, forecast.title)


    def test(self):
        race_day = RaceDayTestData.objects.get(id=48)
        fixtures = race_day.fixtures.all()
        race_day = race_day.data_model
        from horsing_around.forecaster.regression.regressors import PolynomialRegression

        for race in race_day.races:
            reg = PolynomialRegression(race.horses, race.distance, race.track_type)

        forecast = reg.forecast()

