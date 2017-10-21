from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404
from horsing_around.enum import PageType
from horsing_around.scrappers import HorseScrapper


class Index( View):
    def get(self, request, *args, **kwargs):
        return render(request, 'public/index.html')


class Forecaster(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'public/forecaster.html')


class Scrapper(View):
    def get(self, request, *args, **kwargs):
        pass