from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from boards.forms import BoardCreateForm
from boards.forms import BoardUpdateForm
from boards.models import Board


class BoardDeleteView(LoginRequiredMixin, DeleteView):
    model = Board
    success_url = reverse_lazy('board_list')
    context_object_name = 'board'
    pk_url_kwarg = 'board_pk'
    template_name = 'boards/delete.html'
    success_url = reverse_lazy('board_list')

    def get_object(self, queryset=None) -> Board:
        user = self.request.user
        board_pk = self.kwargs[self.pk_url_kwarg]
        queryset = (self.get_queryset() if queryset is None else queryset).distinct()

        if user.is_superuser:
            return get_object_or_404(queryset, pk=board_pk)
        else:
            return get_object_or_404(queryset, pk=board_pk, owner=user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        board = context[self.context_object_name]
        context['page_title'] = f'Delete board: {board.title}'
        context['form_action_url'] = reverse_lazy('board_delete', kwargs={'board_pk': board.pk})
        return context


class BoardUpdateView(LoginRequiredMixin, UpdateView):
    model = Board
    form_class = BoardUpdateForm
    context_object_name = 'board'
    pk_url_kwarg = 'board_pk'
    template_name = 'boards/update.html'

    def get_object(self, queryset=None) -> Board:
        user = self.request.user
        board_pk = self.kwargs[self.pk_url_kwarg]
        queryset = (self.get_queryset() if queryset is None else queryset).distinct()

        if user.is_superuser:
            return get_object_or_404(queryset, pk=board_pk)
        else:
            return get_object_or_404(queryset, pk=board_pk, owner=user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        board = context[self.context_object_name]
        context['page_title'] = f'Update board: {board.title}'
        context['form_action_url'] = reverse_lazy('board_update', kwargs={'board_pk': board.pk})
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('board_detail', kwargs={'board_pk': self.object.pk})  # type: ignore


class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    context_object_name = 'board'
    pk_url_kwarg = 'board_pk'
    template_name = 'boards/detail.html'

    def get_object(self, queryset=None) -> Board:
        user = self.request.user
        board_pk = self.kwargs[self.pk_url_kwarg]
        queryset = (self.get_queryset() if queryset is None else queryset).distinct()

        if user.is_superuser:
            return get_object_or_404(queryset, pk=board_pk)
        else:
            return get_object_or_404(queryset, Q(owner=user) | Q(members=user), pk=board_pk)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        board = context[self.context_object_name]
        context['page_title'] = f'Detail of board: {board.title}'
        return context


class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/list.html'
    extra_context = {'page_title': 'Boards'}

    def get_queryset(self) -> QuerySet[Board]:
        user = self.request.user

        if user.is_superuser:
            boards = Board.objects.all().prefetch_related('owner', 'members')
        else:
            boards = Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

        return boards.prefetch_related('owner', 'members')


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardCreateForm
    template_name = 'boards/create.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create board'
        context['form_action_url'] = reverse_lazy('board_create')
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('board_detail', kwargs={'board_pk': self.object.pk})  # type: ignore
