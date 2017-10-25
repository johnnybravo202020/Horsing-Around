from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404
from horsing_around.enum import PageType
from horsing_around import City
from horsing_around.scrappers import PageDoesNotExist
from .view_models import StatisticTableViewModel
from django.views.generic.edit import FormView
from .forms import FixtureForm
from main.shortcuts import render_to_html_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string


class Results(View):
    form_class = FixtureForm

    def post(self, request, pt):
        scrapper_form = self.form_class(request.POST)
        return render(request, 'scrapper/results.html', {'form': scrapper_form.render_to_html_string()})

@method_decorator(csrf_exempt, name='dispatch')
class BaseScrapperFormView(FormView):
    form_class = FixtureForm

    def form_invalid(self, form):
        response = super(BaseScrapperFormView, self).form_invalid(form)
        if self.request.is_ajax():
            return HttpResponse(form.errors, status=400)
        else:
            return response

    def redirect(self, results, form):
        models = list()
        for result in results:
            models.append(StatisticTableViewModel(result))

        title = "Fixture for the race at {0} in {1}".format(form.cleaned_data['date'],
                                                            City(int(form.cleaned_data['city'])).name)
        return HttpResponse(render_to_string('base/partial/race_pane.html', {'title': title,
                                                                             'races': models}))


class RaceDayScrapperFormView(BaseScrapperFormView):
    def form_valid(self, form):
        page_type = form.cleaned_data['page_type']
        date = form.cleaned_data['date']
        city = City(int(form.cleaned_data['city']))
        try:
            results = PageType(page_type).scrapper.scrap_by_date(city, date)
        except PageDoesNotExist as not_exist:
            return HttpResponse(not_exist, status=404)
        return self.redirect(results, form)
