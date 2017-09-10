# -*- coding: utf-8 -*-
# The above line is for turkish characters in comments, unless it is there a encoding error is raised in the server


from bs4 import BeautifulSoup
import urllib.request
from .result_row_scrapper import ResultRowScrapper
import datetime
from enum import Enum


class City(Enum):
    """
    Cities and they are respected ids determined by TJK.org for their query parameters
    """
    Izmir = 2
    Istanbul = 3
    Bursa = 4
    Adana = 1
    Ankara = 5
    Kocaeli = 9
    Urfa = 6
    Elazig = 7

class RaceDayScrapper:
    """
    Race Day Scrapper(RDS) makes a request to an url in order to get the page source that contains information about
    the past, present or upcoming races usually from Turkey.
    """
    race_divs = ''

    def __init__(self, city, date):
        # Assigning them to properties so we can get them when we need them in order to save them to the model
        self.city = city
        self.date = date

        # Creating the url
        # {0} is city id, {1} is city name
        url_base = 'http://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisSonuclari?SehirId={' \
                   '0}&QueryParameter_Tarih=03%2F7%2F2017&SehirAdi={1}'

        actual_url = url_base.format(city.value, city.name)

        # Get the html of race results of a particular date and city
        self.html = urllib.request.urlopen(actual_url).read()

        # Get the Soap object for easy scraping
        soup = BeautifulSoup(self.html)

        # Get the div containing all the races
        race_div = soup.find_all("div", class_='races-panes')[0]

        # Getting the one level inner divs which contains each race. Recursive is set to false because we don't want
        # to go the the inner child of those divs. Just trying to stay on the first level
        self.race_divs = race_div.find_all("div", recursive=False)

    @classmethod
    def from_date_values(cls, city, year, month, day):
        return cls(city, datetime.date(year, month, day))

    def get(self):

        # Create an empty list to hold each race
        races = []

        # Date and city is the same for all races in the html page
        race_date = datetime.date(2017, 7, 3)
        city = 'Bursa'

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
                scrapper = ResultRowScrapper(row)

                # Get the result model with scrapped data in it
                model = scrapper.get()

                # Assign the values that are specific to this race
                model.track_type = track_type
                model.distance = int(distance)
                model.race_id = race_id
                model.city = city
                model.race_date = race_date

                # Append the model to the result list
                results.append(model)

            # This point we have all the results of one race we can append it to the race list
            races.append(results)

        # We got all the information about the race day in the given city and date We can return the races list now
        return races
