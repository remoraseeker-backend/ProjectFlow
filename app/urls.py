from django.urls import path

from app.views import HomeView


urlpatterns = [
    path(route='', view=HomeView.as_view(), name='app_home'),
]
