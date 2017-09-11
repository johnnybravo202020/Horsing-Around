from django.contrib import admin
from .models import (RaceResult, RaceResultTestData, RaceDayTestData)

# Register your models here
admin.site.register(RaceResult)
admin.site.register(RaceResultTestData)
admin.site.register(RaceDayTestData)