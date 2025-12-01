from django.urls import include
from django.urls import path

from projects.views import ProjectCreateView
from projects.views import ProjectDeleteView
from projects.views import ProjectDetailView
from projects.views import ProjectListView
from projects.views import ProjectUpdateView


urlpatterns = [
    path(route='', view=ProjectListView.as_view(), name='project_list'),
    path(route='create/', view=ProjectCreateView.as_view(), name='project_create'),
    path(route='<int:project_pk>/', view=ProjectDetailView.as_view(), name='project_detail'),
    path(route='<int:project_pk>/sections/', view=include('sections.urls')),
    path(route='<int:project_pk>/update/', view=ProjectUpdateView.as_view(), name='project_update'),
    path(route='<int:project_pk>/delete/', view=ProjectDeleteView.as_view(), name='project_delete'),
]
