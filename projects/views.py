from typing import Any
from typing import cast

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

from authentication.models import User
from projects.forms import ProjectCreateForm
from projects.forms import ProjectUpdateForm
from projects.models import Project


class ProjectViewMixin(LoginRequiredMixin):
    model = Project

    def get_queryset(self) -> QuerySet[Project]:
        queryset = self.model.objects.all()
        queryset = queryset.select_related('owner')
        queryset = queryset.prefetch_related('members', 'sections')
        return queryset.distinct()


class ProjectListView(ProjectViewMixin, ListView):
    context_object_name = 'projects'
    template_name = 'projects/list.html'
    extra_context = {'page_title': 'Projects'}

    def get_queryset(self) -> QuerySet[Project]:
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superuser:
            return queryset
        else:
            return queryset.filter(Q(owner=user) | Q(members=user))

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        projects = cast(list[Project], self.object_list)  # pyright: ignore[reportAttributeAccessIssue]
        context['projects'] = dict()

        # user is owner;
        context['projects']['my'] = filter(lambda p: user == p.owner, projects)
        # user is member and not owner;
        context['projects']['member'] = filter(lambda p: user in p.members.all() and not p.owner == user, projects)

        if not user.is_superuser:
            return context

        # user is not member and is not owner;
        context['projects']['admin_list'] = filter(lambda p: user != p.owner and user not in p.members.all(), projects)

        return context


class ProjectCreateView(ProjectViewMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'projects/create.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        project = cast(Project, form.instance)
        user = cast(User, self.request.user)
        project.owner = user
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create project'
        return context

    def get_success_url(self) -> str:
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        return reverse_lazy('project_detail', kwargs={'project_pk': project.pk})


class ProjectDetailView(ProjectViewMixin, DetailView):
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'
    template_name = 'projects/detail.html'

    def get_object(self, queryset=None) -> Project:
        user = self.request.user
        project_pk = self.kwargs[self.pk_url_kwarg]
        queryset = self.get_queryset() if queryset is None else queryset

        if user.is_superuser:
            return get_object_or_404(queryset, pk=project_pk)
        else:
            return get_object_or_404(queryset, Q(owner=user) | Q(members=user), pk=project_pk)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        user = self.request.user
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Detail of project: {project.title}'
        context['user_is_project_owner_or_superuser'] = user.is_superuser or (project.owner == user)
        return context


class ProjectUpdateView(ProjectViewMixin, UpdateView):
    form_class = ProjectUpdateForm
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'
    template_name = 'projects/update.html'

    def get_object(self, queryset=None) -> Project:
        user = self.request.user
        project_pk = self.kwargs[self.pk_url_kwarg]
        queryset = self.get_queryset() if queryset is None else queryset

        if user.is_superuser:
            return get_object_or_404(queryset, pk=project_pk)
        else:
            return get_object_or_404(queryset, pk=project_pk, owner=user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Update project: {project.title}'
        return context

    def get_success_url(self) -> str:
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        return reverse_lazy('project_detail', kwargs={'project_pk': project.pk})


class ProjectDeleteView(ProjectViewMixin, DeleteView):
    success_url = reverse_lazy('project_list')
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'
    template_name = 'projects/delete.html'
    success_url = reverse_lazy('project_list')

    def get_object(self, queryset=None) -> Project:
        user = self.request.user
        project_pk = self.kwargs[self.pk_url_kwarg]
        queryset = self.get_queryset() if queryset is None else queryset

        if user.is_superuser:
            return get_object_or_404(queryset, pk=project_pk)
        else:
            return get_object_or_404(queryset, pk=project_pk, owner=user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete project: {project.title}'
        return context
