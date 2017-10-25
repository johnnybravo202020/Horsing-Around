from django.views import View
from django.shortcuts import render


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base/index.html')

