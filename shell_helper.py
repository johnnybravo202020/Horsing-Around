def test_scrap():
    from scrapper.scrappers import FixtureScrapper, City
    import datetime
    scrapper = FixtureScrapper(City.Kocaeli, datetime.datetime(2017, 9, 26))
    return scrapper.get()
