from django.urls import path

from boards.views import BoardsView


urlpatterns = [
    path(
        route='',
        view=BoardsView.as_view(template_name='boards/index.html', extra_context={'page_title': 'Boards'}),
        name='boards',
    )
]
