

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render

from app.views import AppBaseView


class BoardsView(LoginRequiredMixin, AppBaseView):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request=request,
            template_name=self.template_name,
            context=self.get_context(),
        )
