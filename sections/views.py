from typing import Any
from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from projects.views import ProjectViewMixin
from sections.forms import SectionCreateForm
from sections.forms import SectionUpdateForm
from sections.models import Section


class SectionViewMixin(LoginRequiredMixin):
    model = Section
    pk_url_kwarg = 'section_pk'

    def get_queryset(self) -> QuerySet[Section]:
        queryset = self.model.objects.all()
        queryset = queryset.select_related('project')
        return queryset.distinct()


class SectionListView(SectionViewMixin, ListView):
    """User can get the list of the project sections only if he is a owner or member of project or superuser."""
    context_object_name = 'sections'
    template_name = 'sections/list.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        project_pk = kwargs[ProjectViewMixin.pk_url_kwarg]
        project_qs = ProjectViewMixin().get_queryset()
        if user.is_superuser:
            self.project = get_object_or_404(project_qs, pk=project_pk)
        else:
            self.project = get_object_or_404(project_qs, Q(owner=user) | Q(members=user), pk=project_pk)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Section]:
        queryset = cast(QuerySet[Section], self.project.sections.all())  # pyright: ignore[reportAttributeAccessIssue]
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Sections of project: {self.project.title}'
        context['project'] = self.project
        return context


class SectionCreateView(SectionViewMixin, CreateView):
    """User can create an new section for project only if he is a owner of the project or superuser."""
    form_class = SectionCreateForm
    template_name = 'sections/create.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        project_pk = kwargs[ProjectViewMixin.pk_url_kwarg]
        project_qs = ProjectViewMixin().get_queryset()
        if user.is_superuser:
            self.project = get_object_or_404(project_qs, pk=project_pk)
        else:
            self.project = get_object_or_404(project_qs, pk=project_pk, owner=user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        section = cast(Section, form.instance)
        section.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Create section for project: {self.project.title}'
        return context

    def get_success_url(self) -> str:
        section = cast(Section, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        kwargs = {
            ProjectViewMixin.pk_url_kwarg: self.project.pk,
            self.pk_url_kwarg: section.pk,
        }
        return reverse_lazy('section_detail', kwargs=kwargs)


class SectionDetailView(SectionViewMixin, DetailView):
    """User can see detail of the project section only if he is a member or owner of the project or superuser."""
    context_object_name = 'section'
    template_name = 'sections/detail.html'

    def get_object(self, queryset=None) -> Section:
        user = self.request.user
        project_pk = self.kwargs[ProjectViewMixin.pk_url_kwarg]
        section_pk = self.kwargs[self.pk_url_kwarg]
        queryset = self.get_queryset() if queryset is None else queryset
        pk_filter = Q(pk=section_pk) & Q(project__pk=project_pk)

        if user.is_superuser:
            return get_object_or_404(queryset, pk_filter)
        else:
            return get_object_or_404(queryset, pk_filter, Q(project__owner=user) | Q(project__members=user))

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        section = cast(Section, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['page_title'] = f'Detail of section: {section.name}'
        context['user_is_project_owner_or_superuser'] = section.project.owner_id == user.id or user.is_superuser  # pyright: ignore[reportAttributeAccessIssue] # noqa E501
        return context


class SectionUpdateView(SectionViewMixin, UpdateView):
    """User can update section of project only if he is a owner of project or superuser."""
    form_class = SectionUpdateForm
    context_object_name = 'section'
    template_name = 'sections/update.html'

    def get_object(self, queryset=None) -> Section:
        queryset = self.get_queryset() if queryset is None else queryset
        user = self.request.user
        project_pk = self.kwargs[ProjectViewMixin.pk_url_kwarg]
        section_pk = self.kwargs[self.pk_url_kwarg]
        pk_filter = Q(pk=section_pk) & Q(project__pk=project_pk)

        if user.is_superuser:
            return get_object_or_404(queryset, pk_filter)
        else:
            return get_object_or_404(queryset, pk_filter, project__owner=user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        section = cast(Section, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Update section: {section.name}'
        return context

    def get_success_url(self) -> str:
        section = cast(Section, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        kwargs = {
            ProjectViewMixin.pk_url_kwarg: section.project.pk,
            self.pk_url_kwarg: section.pk,
        }
        return reverse_lazy('section_detail', kwargs=kwargs)


class SectionDeleteView(SectionViewMixin, DeleteView):
    """User can delete section of project only if he is a owner of project or superuser."""
    context_object_name = 'section'
    template_name = 'sections/delete.html'

    def get_object(self, queryset=None) -> Section:
        queryset = self.get_queryset() if queryset is None else queryset
        user = self.request.user
        project_pk = self.kwargs[ProjectViewMixin.pk_url_kwarg]
        section_pk = self.kwargs[self.pk_url_kwarg]
        pk_filter = Q(pk=section_pk) & Q(project__pk=project_pk)

        if user.is_superuser:
            return get_object_or_404(queryset, pk_filter)
        else:
            return get_object_or_404(queryset, pk_filter, project__owner=user)

    def get_success_url(self) -> str:
        kwargs = {
            ProjectViewMixin.pk_url_kwarg: self.kwargs[ProjectViewMixin.pk_url_kwarg]
        }
        return reverse_lazy('section_list', kwargs=kwargs)
