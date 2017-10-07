from django.contrib import admin
from .models import RaceDayTestData, ResultTestData, FixtureTestData

# Register your models here
admin.site.register(ResultTestData)
admin.site.register(FixtureTestData)
admin.site.register(RaceDayTestData)
