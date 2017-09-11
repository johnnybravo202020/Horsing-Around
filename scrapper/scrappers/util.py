from scrapper import models
from . import RaceDayScrapper


def get_race_day_from_db_scrap_save(id):
    race_day = models.RaceDayTestData.objects.get(id=id)

    # for race_day in test_race_days:
    scrapper = RaceDayScrapper.from_test_data_model(race_day)
    races = scrapper.get(is_test=True)

    counter = 0
    for race in races:
        for result in race:
            result.race_day = race_day
            result.save()
            counter += 1

    print('{0} results saves'.format(counter))
