from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.http import Http404
from horsing_around.enum import PageType
from horsing_around import City
from horsing_around.scrappers import HorseScrapper
from .view_models import StatisticTableViewModel
from django.views.generic.edit import FormView
from .forms import FixtureForm


class Index( View):
    def get(self, request, *args, **kwargs):
        return render(request, 'public/index.html')


class Forecaster(View):
    def get(self, request, *args, **kwargs):
        results = HorseScrapper.scrap(75043)
        model = StatisticTableViewModel('asdads', results)
        return render(request, 'public/forecaster.html', {"model": model})


class BaseScrapperFormView(FormView):
    form_class = FixtureForm

    def form_invalid(self, form):
        raise Exception(form.errors)
        response = super(BaseScrapperFormView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def redirect(self, results):
        model = StatisticTableViewModel('asdads', results)
        return JsonResponse(dict())


class RaceDayScrapperFormView(BaseScrapperFormView):
    def form_valid(self, form):
        page_type = form.cleaned_data['page_type']
        date = form.cleaned_data['date']
        city = City(int(form.cleaned_data['city']))
        results = PageType(page_type).scrapper.scrap_by_date(city, date)
        return self.redirect(results)