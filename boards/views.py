from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class BoardsView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {'page_title': 'Boards'}
        return render(request=request, template_name='boards/index.html', context=context)
