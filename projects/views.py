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

from projects.forms import ProjectCreateForm
from projects.forms import ProjectUpdateForm
from projects.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'
    extra_context = {'page_title': 'Projects'}

    def get_queryset(self) -> QuerySet[Project]:
        user = self.request.user

        if user.is_superuser:
            boards = Project.objects.all().prefetch_related('owner', 'members')
        else:
            boards = Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()

        return boards.prefetch_related('owner', 'members')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        projects = context['projects']

        context['projects'] = {
            'my': projects.filter(owner=user),
            'member': projects.filter(Q(members=user) & ~Q(owner=user)),
        }

        if user.is_superuser:
            context['projects'].update({
                'admin_list': projects.exclude(Q(owner=user) | Q(members=user))
            })

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/create.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create project'
        context['form_action_url'] = reverse_lazy('project_create')
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('project_detail', kwargs={'project_pk': self.object.pk})  # type: ignore


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'
    template_name = 'projects/detail.html'

    def get_object(self, queryset=None) -> Project:
        user = self.request.user
        project_pk = self.kwargs[self.pk_url_kwarg]
        queryset = (self.get_queryset() if queryset is None else queryset).distinct()

        if user.is_superuser:
            return get_object_or_404(queryset, pk=project_pk)
        else:
            return get_object_or_404(queryset, Q(owner=user) | Q(members=user), pk=project_pk)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        project = context[self.context_object_name]
        context['page_title'] = f'Detail of project: {project.title}'
        context['can_edit'] = (project.owner == user) or user.is_superuser
        context['can_delete'] = (project.owner == user) or user.is_superuser
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'
    template_name = 'projects/update.html'

    def get_object(self, queryset=None) -> Project:
        user = self.request.user
        project_pk = self.kwargs[self.pk_url_kwarg]
        queryset = (self.get_queryset() if queryset is None else queryset).distinct()

        if user.is_superuser:
            return get_object_or_404(queryset, pk=project_pk)
        else:
            return get_object_or_404(queryset, pk=project_pk, owner=user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project = context[self.context_object_name]
        context['page_title'] = f'Update project: {project.title}'
        context['form_action_url'] = reverse_lazy('project_update', kwargs={'project_pk': project.pk})
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('project_detail', kwargs={'project_pk': self.object.pk})  # type: ignore


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'
    template_name = 'projects/delete.html'
    success_url = reverse_lazy('project_list')

    def get_object(self, queryset=None) -> Project:
        user = self.request.user
        project_pk = self.kwargs[self.pk_url_kwarg]
        queryset = (self.get_queryset() if queryset is None else queryset).distinct()

        if user.is_superuser:
            return get_object_or_404(queryset, pk=project_pk)
        else:
            return get_object_or_404(queryset, pk=project_pk, owner=user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project = context[self.context_object_name]
        context['page_title'] = f'Delete project: {project.title}'
        context['form_action_url'] = reverse_lazy('project_delete', kwargs={'project_pk': project.pk})
        return context
