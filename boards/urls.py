from django.urls import path

from boards.views import BoardsView


urlpatterns = [
    path(route='', view=BoardsView.as_view(), name='boards')
]
