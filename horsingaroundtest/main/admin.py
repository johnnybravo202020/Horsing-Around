from django.contrib import admin
from .models import FixtureTestData, ResultTestData, HorseTestData, RaceDayTestData

admin.site.register(FixtureTestData)
admin.site.register(ResultTestData)
admin.site.register(HorseTestData)
admin.site.register(RaceDayTestData)