
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

from projects.models import Project
from projects.views import ProjectDetailView
from projects.views import ProjectUpdateView
from sections.forms import SectionCreateForm
from sections.forms import SectionUpdateForm
from sections.models import Section


class SectionViewMixin(LoginRequiredMixin):
    model = Section

    def get_queryset(self) -> QuerySet[Section]:
        queryset = self.model.objects.all()
        queryset = queryset.select_related('project')
        return queryset.distinct()


class SectionListView(SectionViewMixin, ListView):
    pass


class SectionCreateView(SectionViewMixin, CreateView):
    form_class = SectionCreateForm
    template_name = 'sections/create.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        project_pk = kwargs['project_pk']
        if user.is_superuser:
            self.project = get_object_or_404(Project, pk=project_pk)
        else:
            self.project = get_object_or_404(Project, pk=project_pk, owner=user)
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
            'project_pk': self.project.pk,
            'section_pk': section.pk,
        }
        return reverse_lazy('section_detail', kwargs=kwargs)


class SectionDetailView(SectionViewMixin, DetailView):
    context_object_name = 'section'
    pk_url_kwarg = 'section_pk'
    template_name = 'sections/detail.html'

    def get_object(self, queryset=None) -> Model:
        user = self.request.user
        project_pk = self.kwargs[ProjectDetailView.pk_url_kwarg]
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
        context['user_is_project_owner_or_superuser'] = section.project.owner == user or user.is_superuser
        return context


class SectionUpdateView(SectionViewMixin, UpdateView):
    form_class = SectionUpdateForm
    # context_object_name = 'section'
    pk_url_kwarg = 'section_pk'
    template_name = 'sections/update.html'

    def get_object(self, queryset=None) -> Model:
        queryset = self.get_queryset() if queryset is None else queryset
        user = self.request.user
        project_pk = self.kwargs[ProjectUpdateView.pk_url_kwarg]
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
            'project_pk': section.project.pk,
            'section_pk': section.pk,
        }
        return reverse_lazy('section_detail', kwargs=kwargs)


class SectionDeleteView(DeleteView):
    pass
