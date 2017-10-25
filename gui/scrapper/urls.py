from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^results/$', views.Results.as_view(), name='results'),
    url(r'^scrap/$', views.ScrapperFormView.as_view(), name='scrap'),
]
