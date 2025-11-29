from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.views import AppBaseView
from boards.forms import BoardCreateForm
from boards.models import Board


class BoardsView(LoginRequiredMixin, AppBaseView):
    def get(self, request: HttpRequest, *args, **kwargs):
        filters = {}
        if not request.user.is_superuser:
            filters.update({'members': request.user})

        boards = Board.objects.filter(**filters)
        return render(
            request=request,
            template_name=self.template_name,
            context=self.get_context({'boards': boards}),
        )


class BoardCreateView(LoginRequiredMixin, AppBaseView):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request=request,
            template_name=self.template_name,
            context=self.get_context({'form': BoardCreateForm}),
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        form = BoardCreateForm(data=request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(redirect_to=reverse(viewname='board_new'))

        user = request.user
        title = form.cleaned_data['title']
        board = Board(title=title, owner=user)
        board.save()
        board.members.add(user)

        return HttpResponseRedirect(redirect_to=reverse(viewname='boards'))
