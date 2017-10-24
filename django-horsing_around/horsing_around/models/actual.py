from .abstract import BaseRaceResult, BaseModel
from .mixin import ResultMixin


class Result(BaseRaceResult, ResultMixin):
    class Meta:
        app_label = 'horsing_around'

    def __str__(self):
        return "Result:" + super(Result, self).__str__()


class Fixture(BaseRaceResult):
    class Meta:
        app_label = 'horsing_around'

    def __str__(self):
        return "Fixture:" + super(Fixture, self).__str__()


class Horse(BaseModel, ResultMixin):
    class Meta:
        app_label = 'horsing_around'

    def __str__(self):
        return "Horse Result:" + super(Horse, self).__str__()
