# -*- coding: utf-8 -*-
# The above line is for turkish characters in comments, unless it is there a encoding error is raised in the server


from bs4 import BeautifulSoup
from .row import FixtureRowScrapper, ResultRowScrapper, HorseRowScrapper
from ..enum import PageType
from .abstract import BaseRaceDayScrapper, BasePageScrapper
from .exception import PageDoesNotExist


class FixtureScrapper(BaseRaceDayScrapper):
    """
    Ex: 'http://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId=9&QueryParameter_Tarih=26%2F09%2F2017&SehirAdi=Kocaeli'
    """
    race_type = 'GunlukYarisProgrami'
    row_scrapper = FixtureRowScrapper
    page_type = PageType.Fixture


class ResultScrapper(BaseRaceDayScrapper):
    """
    Ex: 'http://www.tjk.org/EN/YarisSever/Info/Sehir/GunlukYarisSonuclari?SehirId=9&QueryParameter_Tarih=26%2F09%2F2017&SehirAdi=Kocaeli'
    """
    race_type = 'GunlukYarisSonuclari'
    row_scrapper = ResultRowScrapper
    page_type = PageType.Result


class HorseScrapper(BasePageScrapper):
    row_scrapper = HorseRowScrapper
    page_type = PageType.Horse

    def __init__(self, horse_id, html='', url=''):
        self.horse_id = horse_id
        super(HorseScrapper, self).__init__(html, url)

    def set_url(self):
        self.url = 'http://www.tjk.org/TR/YarisSever/Query/ConnectedPage/AtKosuBilgileri?1=1&QueryParameter_AtId={' \
                   '0}'.format(self.horse_id)

    @classmethod
    def scrap(cls, horse_id):
        """
        Scraps the results of a particular horse
        :param horse_id: TJK ID of the horse
        :return: Returns the results of the desired horse
        """
        scrapper = cls(horse_id)
        return scrapper.get()

    def get(self):
        # Get the Soap object for easy scraping
        soup = BeautifulSoup(self.html, "lxml")
        # Get the table contains horse's results
        result_table = soup.find("table").find_all('tr')

        results = []

        # If horse has no results recorded there will be only one row in the table and that row is meaningless to us
        if len(result_table) is 1:
            raise PageDoesNotExist('Horse exists but apparently there is no recorded result for the horse.')

        for result in result_table[:-1]:
            scrapper = HorseRowScrapper(result)
            model = scrapper.get()
            results.append(model)

        return results
