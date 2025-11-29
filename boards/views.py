from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.views import AppBaseView
from boards.forms import BoardCreateForm
from boards.models import Board


class BoardDetailView(LoginRequiredMixin, AppBaseView):
    def get(self, request: HttpRequest, *args, **kwargs):
        filters = {'pk': kwargs.get('board_pk')}
        if not request.user.is_superuser:
            filters.update({'members': request.user})

        board = Board.objects.filter(**filters).prefetch_related('members').first()
        if board is None:
            return HttpResponseNotFound(f'<h1>The board with id: {filters["pk"]} not found.</h1>')

        return render(
            request=request,
            template_name=self.template_name,
            context=self.get_context({'board': board}),
        )


class BoardListView(LoginRequiredMixin, AppBaseView):
    def get(self, request: HttpRequest, *args, **kwargs):
        filters = {}
        if not request.user.is_superuser:
            filters.update({'members': request.user})

        boards = Board.objects.filter(**filters).prefetch_related('owner')
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

        return HttpResponseRedirect(redirect_to=reverse(viewname='board_detail', kwargs={'board_pk': board.pk}))
