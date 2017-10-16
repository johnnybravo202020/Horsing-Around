from enum import Enum


class PageType(Enum):
    """
    Cities and their are respected ids determined by TJK.org for their query parameters
    """
    Fixture = 'F'
    Result = 'R'
    Horse = 'H'


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