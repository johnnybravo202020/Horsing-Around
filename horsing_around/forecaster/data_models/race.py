from ..regression import LinearRegression
from ... import City


class RaceDay:
    def __init__(self, scrapped_races):
        # Get the first horse of the first to extract race info
        first_horse = scrapped_races[0][0]
        self.race_date = first_horse.race_date
        self.city = first_horse.city

        self.races = list()

        for race in scrapped_races:
            self.races.append(Race(race))


class Race:
    def __init__(self, horses):
        self.horses = sorted(horses, key=lambda x: x.order)

        # Get the first horse to extract race info
        first_horse = horses[0]

        self.track_type = first_horse.track_type
        self.distance = first_horse.distance
        self.id = first_horse.race_id
        self.forecasts = list()

        self.append_forecast(LinearRegression)

    def append_forecast(self, machine):
        machine = LinearRegression(horses=self.horses, distance=self.distance)
        self.forecasts.append(machine.forecast())

    def __str__(self):
        return "{0} meters, {1}".format(self.distance, self.track_type)