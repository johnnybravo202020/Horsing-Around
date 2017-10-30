class RaceForecast(list):
    def __init__(self, title, prediction_views):
        self.title = title
        self.extend(sorted(prediction_views, key=lambda x: x.prediction, reverse=True))

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
