from django.urls import path

from app.views import HomeView


urlpatterns = [
    path(
        route='',
        view=HomeView.as_view(template_name='app/home.html', extra_context={'page_title': 'Home'}),
        name='home',
    ),
]
