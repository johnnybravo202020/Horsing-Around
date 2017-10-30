import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression as SKLearnLinearRegression
from ...scrappers import FixtureScrapper
from ..data_models.forecast import Prediction, RaceForecast
from ..data_models.util import TrainingSet


class LinearRegression:
    def __init__(self, horses, distance):
        """
        :param fixture: List contains races which contains Fixture model
        """
        self.horses = horses
        self.distance = distance

    def forecast(self):
        predictions = list()
        for result in self.horses:
            prediction = -1
            horse_results = result.past_results.all()
            if horse_results:
                training_set = TrainingSet(horse_results)

                machine = SKLearnLinearRegression()
                machine.fit(training_set.x, training_set.y)

                prediction = machine.predict(self.distance)[0]

            predictions.append(Prediction(horse_id=result.horse_id,
                                          horse_name=result.horse_name,
                                          prediction=prediction))

        return RaceForecast('Linear Regression', predictions)



