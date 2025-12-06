from typing import Any
from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from projects.models import Project
from projects.views import ProjectDetailView
from projects.views import ProjectViewMixin
from sections.forms import SectionCreateForm
from sections.forms import SectionUpdateForm
from sections.models import Section


class SectionViewMixin(LoginRequiredMixin, View):
    model = Section
    pk_url_kwarg = 'section_pk'

    def get_queryset(self) -> QuerySet[Section]:
        queryset = self.model.objects.all()
        queryset = queryset.select_related('project')
        queryset = queryset.distinct()
        user = self.request.user
        project_pk = self.kwargs[ProjectViewMixin.pk_url_kwarg]

        if isinstance(self, (SectionListView, SectionDetailView)):
            filters = Q(project__owner=user) | Q(project__members=user)
        elif isinstance(self, (SectionUpdateView, SectionDeleteView)):
            filters = Q(project__owner=user)
        else:
            raise Exception()

        if user.is_superuser:
            return queryset
        else:
            return queryset.filter(filters, project__pk=project_pk)


class SectionListView(SectionViewMixin, ListView):
    """User can get the list of the project sections only if he is a owner or member of project or superuser."""
    context_object_name = 'sections'
    template_name = 'sections/list.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        project = ProjectDetailView(request=request, kwargs=kwargs).get_object()
        self.project = cast(Project, project)
        return super().dispatch(request, *args, **kwargs)

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
        project = ProjectDetailView(request=request, kwargs=kwargs).get_object()
        self.project = cast(Project, project)

        # Raise 404 if user try to add the section into the project where he is not a owner.
        user = request.user
        if not user.is_superuser and self.project.owner != user:
            raise Http404(f'No {self.project._meta.object_name} matches the given query.')

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

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        section = cast(Section, self.object)  # pyright: ignore[reportAttributeAccessIssue]
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['page_title'] = f'Detail of section: {section.name}'
        context['can_edit_section'] =  user.is_superuser or (section.project.owner_id == user.id)  # pyright: ignore[reportAttributeAccessIssue] # noqa E501
        context['can_delete_section'] = user.is_superuser or (section.project.owner_id == user.id)  # pyright: ignore[reportAttributeAccessIssue] # noqa E501
        return context


class SectionUpdateView(SectionViewMixin, UpdateView):
    """User can update section of project only if he is a owner of project or superuser."""
    form_class = SectionUpdateForm
    context_object_name = 'section'
    template_name = 'sections/update.html'

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

    def get_success_url(self) -> str:
        kwargs = {
            ProjectViewMixin.pk_url_kwarg: self.kwargs[ProjectViewMixin.pk_url_kwarg]
        }
        return reverse_lazy('section_list', kwargs=kwargs)
