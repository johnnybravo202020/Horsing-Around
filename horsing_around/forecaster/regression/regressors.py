from sklearn.linear_model import LinearRegression as SKLearnLinearRegression
from ..data_models.forecast import Prediction, RaceForecast
from ..data_models.util import TrainingSet
from sklearn.preprocessing import PolynomialFeatures


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
        for result in self.horses:
            horse_results = result.past_results
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

                        predictions.append(Prediction(horse_id=result.horse_id,
                                                      horse_name=result.horse_name,
                                                      prediction=prediction,
                                                      result_count="{0}/{1}".format(len(training_set.x),
                                                                                    len(horse_results))))
                    except ValueError as error:
                        logger.info("{0}:{1} failed to get a prediction from {2}, error: {3}".format(result.horse_id,
                                                                                                     result.horse_name,
                                                                                                     type(self),
                                                                                                     error))
        return RaceForecast('Polynomial Regression', predictions)


