def test_scrap():
    from scrapper.scrappers import FixtureScrapper, City
    import datetime
    fixs = FixtureScrapper.scrap_by_date(City.Istanbul, datetime.datetime(2017, 10, 8), save_data_for_test=True)

    return fixs
