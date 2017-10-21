from enum import Enum
import importlib


class PageType(Enum):
    """
    Cities and their are respected ids determined by TJK.org for their query parameters
    """
    Fixture = 'F'
    Result = 'R'
    Horse = 'H'

    @property
    def scrapper(self):
        scrapper_module = importlib.import_module("horsing_around.scrappers")
        return getattr(scrapper_module, '{0}Scrapper'.format(self.name))


class City(Enum):
    """
    Cities and their are respected ids determined by TJK.org for their query parameters
    """
    Izmir = 2
    Istanbul = 3
    Bursa = 4
    Adana = 1
    Ankara = 5
    Kocaeli = 9
    Urfa = 6
    Elazig = 7


class ManagerType(Enum):
    """
    The class of the columns in the each race table
    """
    Jockey = 'JokeAdi'
    Owner = 'SahipAdi'
    Trainer = 'AntronorAdi'