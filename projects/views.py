from typing import Any
from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from authentication.models import User
from projects.forms import ProjectCreateForm
from projects.forms import ProjectUpdateForm
from projects.models import Project


class ProjectViewMixin(LoginRequiredMixin, View):
    model = Project
    pk_url_kwarg = 'project_pk'

    def get_queryset(self) -> QuerySet[Project]:
        queryset = self.model.objects.all()
        queryset = queryset.select_related('owner')
        queryset = queryset.prefetch_related('members', 'sections')
        queryset = queryset.distinct()
        user = self.request.user

        if isinstance(self, (ProjectListView, ProjectDetailView)):
            filters = Q(owner=user) | Q(members=user)
        elif isinstance(self, (ProjectUpdateView, ProjectDeleteView)):
            filters = Q(owner=user)
        else:
            raise Exception()

        if user.is_superuser:
            return queryset
        else:
            return queryset.filter(filters)


class ProjectListView(ProjectViewMixin, ListView):
    """User can get the list of projects where he is a member or owner, if user is superuser he can get all projects."""
    context_object_name = 'projects'
    template_name = 'projects/list.html'
    extra_context = {'page_title': 'Projects'}

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
    """User can create new project if he is logged in."""
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
        return reverse_lazy('project_detail', kwargs={self.pk_url_kwarg: project.pk})


class ProjectDetailView(ProjectViewMixin, DetailView):
    """User can get the detail of the project only if he is a owner or member of project or superuser."""
    context_object_name = 'project'
    template_name = 'projects/detail.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        user = self.request.user
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Detail of project: {project.title}'
        context['user_is_admin'] = user.is_superuser
        context['user_is_project_owner'] = project.owner == user
        return context


class ProjectUpdateView(ProjectViewMixin, UpdateView):
    """User can update the project only if he is a owner of project or superuser."""
    form_class = ProjectUpdateForm
    context_object_name = 'project'
    template_name = 'projects/update.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Update project: {project.title}'
        return context

    def get_success_url(self) -> str:
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        return reverse_lazy('project_detail', kwargs={self.pk_url_kwarg: project.pk})


class ProjectDeleteView(ProjectViewMixin, DeleteView):
    """User can delete the project only if he is a owner of project or superuser."""
    context_object_name = 'project'
    template_name = 'projects/delete.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        project = cast(Project, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete project: {project.title}'
        return context
