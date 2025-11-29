from django.urls import path

from app.views import HomeView
from app.views import OnlyAuthenticatedView


urlpatterns = [
    path(route='', view=HomeView.as_view(), name='home'),
    path(route='secret/', view=OnlyAuthenticatedView.as_view(), name='secret')
]
