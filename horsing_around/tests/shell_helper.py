from .models import FixtureTestData, RaceDayTestData, HorseTestData, PredictionTestData, ResultTestData
from ..scrappers import FixtureScrapper, HorseScrapper
import datetime
from .. import City, PageType


def save_test_data():
    scrapper = FixtureScrapper(City.Adana, datetime.datetime(2017, 11, 21), get_past_statistics=True)
    races = scrapper.get()
    race_day = RaceDayTestData.from_scrapper(scrapper)
    race_day.save()
    for i, race in enumerate(races):
        for j, result in enumerate(race):
            past_results = result.past_results
            fixture = FixtureTestData.from_actual(result, scrapper.rows[i][j])
            fixture.race_day = race_day
            fixture.save()
            for p_result in past_results:
                past_result = HorseTestData.from_actual(p_result, '-1')
                past_result.testable = False
                past_result.fixture = fixture
                past_result.save()


def set_order_column():
    scrapper = FixtureScrapper(City.Ankara, datetime.datetime(2017, 10, 28), get_past_statistics=False)
    races = scrapper.get()
    fixtures = RaceDayTestData.objects.get(id=46).fixtures

    for i, race in enumerate(races):
        for j, result in enumerate(race):
            f = fixtures.get(horse_id=result.horse_id)
            f.order = result.order
            f.save()


def update_race_day():
    race_days = RaceDayTestData.objects.all()
    for race_day in race_days:
        results = PageType(race_day.page_type).scrapper(city=City(race_day.city_id), date=race_day.date,
                                                        html=race_day.html_source, url=race_day.url)
        for race in results.get():
            for res in race:
                import importlib
                model_module = importlib.import_module("horsing_around.tests.models")

                result = getattr(model_module, '{0}TestData'.format(PageType(race_day.page_type).name)).objects.get(horse_id=res.horse_id, race_id=res.race_id)
                #result.horse_weight = res.horse_weight
                #result.save()


def save_predictions(race_day_test_data_id):
    race_day = RaceDayTestData.objects.get(id=race_day_test_data_id)
    fixtures = race_day.fixtures.all()
    data_model = race_day.data_model

    for race in data_model.races:
            for forecast in race.forecasts:
                for prediction in forecast:
                    p_test_data = PredictionTestData(fixture=fixtures.get(horse_id=prediction.horse_id,
                                                                          race_id=race.id),
                                                     prediction=str(prediction.prediction))
                    p_test_data.save()
