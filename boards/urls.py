from django.urls import path

from boards.views import BoardCreateView
from boards.views import BoardDetailView
from boards.views import BoardListView


urlpatterns = [
    path(route='', view=BoardListView.as_view(), name='board_list'),
    path(route='create/', view=BoardCreateView.as_view(), name='board_create'),
    path(route='<int:board_pk>', view=BoardDetailView.as_view(), name='board_detail')
]
