from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from boards.forms import BoardCreateForm
from boards.models import Board


class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    context_object_name = 'board'
    pk_url_kwarg = 'board_pk'
    template_name = 'boards/detail.html'
    extra_context = {'page_title': 'Board detail'}

    def get_object(self, queryset=None) -> Board:
        user = self.request.user
        board_pk = self.kwargs['board_pk']
        queryset = self.get_queryset() if queryset is None else queryset

        if user.is_superuser:
            return get_object_or_404(queryset, pk=board_pk)
        else:
            return get_object_or_404(queryset, Q(owner=user) | Q(members=user), pk=board_pk)


class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/list.html'
    extra_context = {'page_title': 'Boards'}

    def get_queryset(self) -> QuerySet[Board]:
        user = self.request.user

        if user.is_superuser:
            return Board.objects.all().prefetch_related('owner', 'members')
        else:
            return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct().prefetch_related('owner', 'members')


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardCreateForm
    template_name = 'boards/create.html'
    extra_context = {'page_title': 'Create board'}

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('board_detail', kwargs={'board_pk': self.object.pk})
