from django.urls import path

from sections.views import SectionDeleteView
from sections.views import SectionDetailView
from sections.views import SectionListView
from sections.views import SectionUpdateView


urlpatterns = [
    path(route='', view=SectionListView.as_view(), name='section_list'),
    path(route='<int:section_pk>/', view=SectionDetailView.as_view(), name='section_detail'),
    path(route='<int:section_pk>/update/', view=SectionUpdateView.as_view(), name='section_update'),
    path(route='<int:section_pk>/delete/', view=SectionDeleteView.as_view(), name='section_delete'),
]
