# -*- coding: utf-8 -*-
# The above line is for turkish characters in comments, unless it is there a encoding error is raised in the server


from bs4 import BeautifulSoup
import urllib.request
from .row import FixtureRowScrapper, ResultRowScrapper
import datetime
from enum import Enum
from scrapper import models


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


class BaseRaceDayScrapper:
    """
    Race Day Scrapper(RDS) makes a request to an url in order to get the page source that contains information about
    the past, present or upcoming races usually from Turkey.
    """

    """
    Each race day contains many races and each of them wrapped by a single div tag, and it's class is 'races-panes'.
    We store that div inside this property
    """
    race_divs = ''

    """
    Fixture and Result has one particular difference in the url, thus this property determines that
    Fixture: 'GunlukYarisProgrami'
    Result: 'GunlukYarisSonuclari'
    """
    race_type = ''

    """
    Fixture and Result pages have minor differences, therefore they need different scrappers to scrap html table rows
    """
    row_scrapper = ''

    def __init__(self, city, date, html=''):
        self.city = city
        self.date = date

        # Means we have to download the html source our selves
        if not html:
            # -- start url parsing --
            # {0} is race type, {1} is city id, {2} is city name
            self.url = 'http://www.tjk.org/TR/YarisSever/Info/Sehir/{0}?SehirId={' \
                       '1}&QueryParameter_Tarih={2}&SehirAdi={3}'

            # Feeding the city information to url
            self.url = self.url.format(self.race_type, city.value, '{0}', city.name)

            # Feeding the date information to url by formatting the date to appropriate string
            # Ex: '03%2F07%2F2017'
            # But first we use dashes as separator so we won't confuse 'date.strftime' function
            date_format = '{0}-{1}-{2}'.format('%d', '%m', '%Y')

            # Now we are replacing dashes with appropriate chars to match the original url
            formatted_dated = date.strftime(date_format).replace('-', '%2F')

            self.url = self.url.format(formatted_dated)
            # -- end url parsing --

            print(self.url)

            # Get the html of the page that contains the results
            self.html = urllib.request.urlopen(self.url).read()
        else:
            self.html = html

        # Get the Soap object for easy scraping
        soup = BeautifulSoup(self.html, "lxml")

        # Get the div containing all the races
        race_div = soup.find_all("div", class_='races-panes')[0]

        # Getting the one level inner divs which contains each race. Recursive is set to false because we don't want
        # to go the the inner child of those divs. Just trying to stay on the first level
        self.race_divs = race_div.find_all("div", recursive=False)

    @classmethod
    def from_date_values(cls, city, year, month, day):
        return cls(city, datetime.date(year, month, day))

    @classmethod
    def from_test_data_model(cls, model):
        return cls(City(model.city_id), model.date, model.html_source)

    def get(self, is_test=False):
        # Create an empty list to hold each race
        races = []
        # Process each race
        for rDiv in self.race_divs:
            # Get the raw race details
            race_id = int(rDiv.get('id'))

            race_detail_div = rDiv.find("div", class_="race-details")

            # The race_detail_div contains some needed information on one of it's children <h3>
            race_info_html = race_detail_div.find("h3", class_="race-config")
            # The second element contains the two info we need Distance and track type We use stripped_strings here
            # to eliminate unnecessary blank spaces Ex: 2 Yaşlı İngilizler, 57 kg,   1100 Çim
            race_info = "".join(race_info_html.stripped_strings)

            # We split from the comma and the we we get
            # Race_info: '   1100\r\n\r\nÇim'
            race_info = race_info.split(",")[-1]

            # Split to separate distance and track type
            race_info = race_info.split("\r\n\r\n")

            # distance is the first element and it has unnecessary space on it, we remove those
            distance = race_info[0].replace(" ", "")

            # track type is the second element and it has unnecessary characters  we split from the first '\r' and
            # take before
            track_type = race_info[1].split(r"\r")[0]

            # Common data for the race is ready, time to get the results get the result of each horse in the table
            horse_rows = rDiv.find("tbody").find_all("tr")

            # Create an empty list to hold each result for this race
            results = []

            # Go through the each result and process
            for row in horse_rows:
                # Initialize the scrapper for a single row
                scrapper = self.row_scrapper(row)

                # Get the result model with scrapped data in it
                model = scrapper.get(is_test)

                # Assign the values that are specific to this race
                model.track_type = track_type
                model.distance = int(distance)
                model.race_id = race_id
                model.city = self.city.name
                model.race_date = self.date

                # Append the model to the result list
                results.append(model)

            # This point we have all the results of one race we can append it to the race list
            races.append(results)

        # We got all the information about the race day in the given city and date. We can return the races list now
        return races

    def get_test_data_model(self):
        return models.RaceDayTestData(
            html_source=self.html,
            url=self.url,
            city=self.city.name,
            date=self.date)


class FixtureScrapper(BaseRaceDayScrapper):
    """
    Ex: 'http://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId=9&QueryParameter_Tarih=26%2F09%2F2017&SehirAdi=Kocaeli'
    """
    race_type = 'GunlukYarisProgrami'
    row_scrapper = FixtureRowScrapper


class ResultScrapper(BaseRaceDayScrapper):
    """
    Ex: 'http://www.tjk.org/EN/YarisSever/Info/Sehir/GunlukYarisSonuclari?SehirId=9&QueryParameter_Tarih=26%2F09%2F2017&SehirAdi=Kocaeli'
    """
    race_type = 'GunlukYarisSonuclari'
    row_scrapper = ResultRowScrapper
