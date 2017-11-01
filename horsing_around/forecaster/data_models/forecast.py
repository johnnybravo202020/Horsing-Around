class RaceForecast(list):
    def __init__(self, title, prediction_views):
        self.title = title

        # Some horses might not have enough past statistics to forecast, or some predictions might be ridiculously
        # low, therefore we push predictions less then 50 seconds to end of the list
        threshold = 50

        valid_predictions = [p for p in prediction_views if p.prediction > threshold]
        invalid_predictions = [p for p in prediction_views if p.prediction <= threshold]

        self.extend(sorted(valid_predictions, key=lambda x: x.prediction))
        self.extend(invalid_predictions)

    def __str__(self):
        rtn = ""
        for prediction in self.forecast:
            rtn += "{0}|{1}\n".format(prediction.horse_name, prediction.prediction)
        return rtn


class Prediction:
    def __init__(self, horse_id, horse_name, prediction):
        self.horse_id = horse_id
        self.horse_name = horse_name
        self.prediction = prediction
