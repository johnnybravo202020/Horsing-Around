from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def test(request):
    from scrapper.scrappers import FixtureScrapper
    from scrapper.scrappers import City
    import datetime
    races = FixtureScrapper.scrap_by_date(City.Bursa, datetime.date(2017, 7, 3), get_past_statistics=True)
    return HttpResponse(races)
