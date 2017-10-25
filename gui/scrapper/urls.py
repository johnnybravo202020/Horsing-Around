from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^results/(?P<pt>[A-Z])$', views.Results.as_view(), name='results'),
    url(r'^scrap/(?P<pt>[A-Z])$', views.RaceDayScrapperFormView.as_view(), name='scrap'),
]
