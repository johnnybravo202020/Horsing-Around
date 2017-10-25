from django import forms
import datetime
from horsing_around.enum import PageType
from horsing_around import City
from horsing_around.scrappers import PageDoesNotExist
from .view_models import StatisticTableViewModel
from main.shortcuts import render_to_html_string
from django.template.loader import render_to_string


class BaseScrapperForm(forms.Form):
    page_type = forms.CharField(widget=forms.HiddenInput())
    exclude_fields = {'id', 'race_id', 'race_date', 'distance', 'city', 'horse_id', 'track_type'}
    template = NotImplemented

    def render_to_html_string(self):
        return render_to_html_string('base/partial/scrapper_form.html', {'form': self})

    def __init__(self, *args, **kwargs):
        super(BaseScrapperForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'

    def scrap(self):
        pass

    def get_context(self, scrapped_data, title):
        pass

    def scrap_and_render_to_string(self):
        scrapped_data, title = self.scrap()
        return render_to_string(self.template, self.get_context(scrapped_data, title))


class RaceDayScrapperForm(BaseScrapperForm):
    date = forms.DateField(initial=datetime.date.today)
    city = forms.ChoiceField(choices=[(c.value, c.name) for c in City])
    template = 'base/partial/race_pane.html'

    def scrap(self):

        page_type = PageType(self.cleaned_data['page_type'])
        date = self.cleaned_data['date']
        city = City(int(self.cleaned_data['city']))

        return page_type.scrapper.scrap_by_date(city, date), \
               "{0} for the race at {1} in {2}".format(page_type.name, date, city.name)


    def get_context(self, scrapped_data, title):
        models = list()
        for result in scrapped_data:
            models.append(StatisticTableViewModel(result, *self.exclude_fields))

        return {'title': title, 'races': models}


class HorseScrapperForm(BaseScrapperForm):
    horse_id = forms.IntegerField()

    def scrap(self):
        page_type = PageType(self.cleaned_data['page_type'])
        horse_id = self.cleaned_data['horse_id']

        return page_type.scrapper.scrap(horse_id), "Past results of the horse with the id: {0}".format(horse_id)

    def get_context(self, scrapped_data, title):
        return {'title': title, 'model': StatisticTableViewModel(scrapped_data, *self.exclude_fields)}
