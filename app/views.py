from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class HomeView(View):

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {'page_title': 'Home page'}
        return render(request=request, template_name='app/home.html', context=context)
