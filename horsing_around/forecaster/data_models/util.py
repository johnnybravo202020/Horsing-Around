import numpy as np
from sklearn.preprocessing import Imputer
from ...scrappers import MissingData


class TrainingSet:
    def __init__(self, results, track_type):
        x = []
        y = []

        for p_result in results:
            if track_type in p_result.track_type:
                try:
                    time = p_result.time_as_seconds
                    distance = p_result.distance
                    x.append(distance)
                    y.append(time)
                except MissingData:
                    pass

        self.x = np.array(x)[:, np.newaxis]
        self.y = np.array(y)
