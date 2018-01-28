from sklearn.linear_model import LinearRegression as SKLearnLinearRegression
from ..data_models.forecast import Prediction, RaceForecast
from ..data_models.util import TrainingSet
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


class LinearRegression:
    def __init__(self, horses, distance, track_type):
        """
        :param fixture: List contains races which contains Fixture model
        """
        self.horses = horses
        self.distance = distance
        self.track_type = track_type

    def forecast(self):
        predictions = list()
        for result in self.horses:
            horse_results = result.past_results
            if horse_results:
                training_set = TrainingSet(horse_results, self.track_type)
                if training_set.validate():
                    machine = SKLearnLinearRegression()
                    machine.fit(training_set.x, training_set.y)

                    prediction = machine.predict(self.distance)[0]

                    predictions.append(Prediction(horse_id=result.horse_id,
                                                  horse_name=result.horse_name,
                                                  prediction=prediction,
                                                  result_count="{0}/{1}".format(len(training_set.x), len(horse_results))))

        return RaceForecast('Linear Regression', predictions)


class PolynomialRegression:
    def __init__(self, horses, distance, track_type):
        """
        :param fixture: List contains races which contains Fixture model
        """
        self.horses = horses
        self.distance = distance
        self.track_type = track_type

    def forecast(self):
        predictions = list()
        for horse in self.horses:
            horse_results = horse.past_results
            if horse_results:
                training_set = TrainingSet(horse_results, self.track_type)

                if training_set.validate():
                    poly_reg = PolynomialFeatures(degree=2)
                    X_poly = poly_reg.fit_transform(training_set.x)

                    machine = SKLearnLinearRegression()
                    machine.fit(X_poly, training_set.y)

                    try:
                        per = poly_reg.fit_transform(self.distance)
                        prediction = machine.predict(per)[0]

                        predictions.append(Prediction(horse_id=horse.horse_id,
                                                      horse_name=horse.horse_name,
                                                      prediction=prediction,
                                                      result_count="{0}/{1}".format(len(training_set.x),
                                                                                    len(horse_results))))
                    except ValueError as error:
                        logger.info("{0}:{1} failed to get a prediction from {2}, error: {3}".format(horse.horse_id,
                                                                                                     horse.horse_name,
                                                                                                     type(self),
                                                                                                     error))
        return RaceForecast('Polynomial Regression', predictions)

    @property
    def best_worst(self):
        """
        Add the best + worst records from all the horses' past results (results in the same distance and track type
        of the race) that are going to participate in the race, then divide that value by two.
        :return: Best and worst time from all horses divided by two
        """
        filtered_results = [result for result in self.get_past_results_of_participant_horses()]

        filtered_results.sort(key=lambda x: x.time_as_seconds)

        best = filtered_results[0].time_as_seconds
        worst = filtered_results[-1].time_as_seconds

        return (best + worst) / 2

    @property
    def mean(self):
        return np.mean([result.time_as_seconds for result in self.get_past_results_of_participant_horses()])

    def get_past_results_of_participant_horses(self):
        rtn_results = []
        for horse in self.horses:
            rtn_results += horse.past_results
        return rtn_results

    def boost(self, training_set, strategy_property):
        """
        If the horse never ran on the distance +/-100 than we add a phantom record calculated with either mean or 
        best_worst depending on the strategy_property.

        :param strategy_property: PolynomialRegression.mean or PolynomialRegression.best_worst
        :param training_set: horsing_around.forecaster.data_models.util.TrainingSet object
        :return: boosted horsing_around.forecaster.data_models.util.TrainingSet object
        """
        different_distanced_results = [r.distance for r in training_set.x if r.distance != self.distance]

        if not different_distanced_results:
            raise Exception('')
            # This horse is running this distance officially first time in his life therefore we boost
            training_set.append(strategy_property, self.distance)

    def result_matches_this_race(self, result):
        return self.track_type in result.track_type and self.distance == result.distance
