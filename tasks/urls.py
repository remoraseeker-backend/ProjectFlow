from django.urls import path

from tasks.views import TaskCreateView
from tasks.views import TaskDeleteView
from tasks.views import TaskDetailView
from tasks.views import TaskListView
from tasks.views import TaskUpdateView


urlpatterns = [
    path(route='', view=TaskListView.as_view(), name='task_list'),
    path(route='create/', view=TaskCreateView.as_view(), name='task_create'),
    path(route='<int:task_pk>/', view=TaskDetailView.as_view(), name='task_detail'),
    path(route='<int:task_pk>/update/', view=TaskUpdateView.as_view(), name='task_update'),
    path(route='<int:task_pk>/delete/', view=TaskDeleteView.as_view(), name='task_delete'),
]
