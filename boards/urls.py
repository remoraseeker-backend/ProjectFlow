from django.urls import path

from boards.views import BoardCreateView
from boards.views import BoardsView


urlpatterns = [
    path(
        route='',
        view=BoardsView.as_view(template_name='boards/index.html', extra_context={'page_title': 'Boards'}),
        name='boards',
    ),
    path(
        route='new/',
        view=BoardCreateView.as_view(template_name='boards/board_create.html', extra_context={'page_title': 'Create board'}),  # noqa E501
        name='board_new'
    ),
]
