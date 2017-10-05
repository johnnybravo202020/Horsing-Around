from django.contrib import admin
from .models import Result, RaceDayTestData, ResultTestData

# Register your models here
admin.site.register(Result)
admin.site.register(ResultTestData)
admin.site.register(RaceDayTestData)