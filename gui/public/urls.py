from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^forecaster$', views.Forecaster.as_view(), name='forecaster'),
    url(r'^scrapper/(?P<s>[A-Z])$', views.RaceDayScrapperFormView.as_view(), name='scrapper'),
]
