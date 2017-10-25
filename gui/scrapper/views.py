from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404
from horsing_around.enum import PageType
from horsing_around import City
from horsing_around.scrappers import PageDoesNotExist
from .view_models import StatisticTableViewModel
from django.views.generic.edit import FormView
from .forms import RaceDayScrapperForm, HorseScrapperForm
from main.shortcuts import render_to_html_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class BaseScrapperView(View):
    def get_form(self, request):
        page_type = PageType(request.POST['page_type'])
        form_class = None
        if page_type is PageType.Fixture or page_type is PageType.Result:
            form_class = RaceDayScrapperForm
        else:
            form_class = HorseScrapperForm
        return form_class(request.POST)


class Results(BaseScrapperView):
    def post(self, request):
        scrapper_form = self.get_form(request)
        return render(request, 'scrapper/results.html', {'form': scrapper_form.render_to_html_string()})


@method_decorator(csrf_exempt, name='dispatch')
class ScrapperFormView(BaseScrapperView):
    def post(self, request):
        form = self.get_form(request)
        if form.is_valid():
            return HttpResponse(form.scrap_and_render_to_string())
        else:
            return HttpResponse(form.errors.as_data())
