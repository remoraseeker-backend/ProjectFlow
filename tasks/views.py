from typing import Any
from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from authentication.models import User
from projects.views import ProjectViewMixin
from sections.models import Section
from sections.views import SectionDetailView
from sections.views import SectionViewMixin
from tasks.forms import TaskCreateForm
from tasks.models import Task


class TaskViewMixin(LoginRequiredMixin, View):
    model = Task
    pk_url_kwarg = 'task_pk'

    def get_queryset(self) -> QuerySet[Task]:
        queryset = self.model.objects.all()
        queryset = queryset.select_related('executor', 'creator', 'section', 'section__project', 'section__project__owner')
        queryset = queryset.distinct()
        user = self.request.user
        project_pk = self.kwargs[ProjectViewMixin.pk_url_kwarg]
        section_pk = self.kwargs[SectionViewMixin.pk_url_kwarg]

        if isinstance(self, (TaskListView, TaskDetailView)):
            filters = Q(section__project__owner=user) | Q(section__project__members=user)
        else:
            raise Exception()

        if user.is_superuser:
            return queryset.filter(section__project__pk=project_pk, section__pk=section_pk)
        else:
            return queryset.filter(filters, section__project__pk=project_pk, section__pk=section_pk)


class TaskListView(TaskViewMixin, ListView):
    """User can get all tasks of section only if he is a member or owner of the section.project or superuser."""
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        section = SectionDetailView(request=request, kwargs=kwargs).get_object()
        self.section = cast(Section, section)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Tasks of section: {self.section.name}'
        context['section'] = self.section
        return context


class TaskCreateView(TaskViewMixin, CreateView):
    """User can create new task for section only if he is a member or owner of the section.project or superuser."""
    form_class = TaskCreateForm
    template_name = 'tasks/create.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        section = SectionDetailView(request=request, kwargs=kwargs).get_object()
        self.section = cast(Section, section)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        task = cast(Task, form.instance)
        user = cast(User, self.request.user)
        task.creator = user
        task.section = self.section
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Create task for section: {self.section.name}'
        return context

    def get_success_url(self) -> str:
        task = cast(Task, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        kwargs = {
            ProjectViewMixin.pk_url_kwarg: task.section.project.pk,
            SectionViewMixin.pk_url_kwarg: task.section.pk,
            self.pk_url_kwarg: task.pk
        }
        return reverse_lazy('task_detail', kwargs=kwargs)


class TaskDetailView(TaskViewMixin, DetailView):
    context_object_name = 'task'
    template_name = 'tasks/detail.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        user = self.request.user
        task = cast(Task, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Detail of task: {task.title}'
        context['user_is_admin'] = user.is_superuser
        context['user_is_project_owner'] = task.section.project.owner == user
        context['user_is_task_creator'] = task.creator == user
        context['user_is_task_executor'] = task.executor == user
        return context


class TaskUpdateView(TaskViewMixin, UpdateView):
    pass


class TaskDeleteView(TaskViewMixin, DeleteView):
    pass
