from django.urls import path

from boards.views import BoardCreateView
from boards.views import BoardDetailView
from boards.views import BoardListView


urlpatterns = [
    path(
        route='',
        view=BoardListView.as_view(template_name='boards/list.html', extra_context={'page_title': 'Boards'}),
        name='board_list',
    ),
    path(
        route='new/',
        view=BoardCreateView.as_view(template_name='boards/create.html', extra_context={'page_title': 'Create board'}),  # noqa E501
        name='board_create'
    ),
    path(
        route='<int:board_pk>',
        view=BoardDetailView.as_view(template_name='boards/detail.html', extra_context={'page_title': 'Board detail'}),
        name='board_detail',
    )
]
