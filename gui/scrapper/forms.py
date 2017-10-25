from django import forms
import datetime
from horsing_around import City
from main.shortcuts import render_to_html_string


class FixtureForm(forms.Form):
    date = forms.DateField(initial=datetime.date.today)
    city = forms.ChoiceField(choices=[(c.value, c.name) for c in City])
    page_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(FixtureForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['date'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'

    def render_to_html_string(self):
        return render_to_html_string('base/partial/scrapper_form.html', {'form': self})
