from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path

from authentication.views import RegisterView


urlpatterns = [
    path(route='login/', view=LoginView.as_view(template_name='authentication/login.html', extra_context={'page_title': 'Login'}), name='auth_login'),  # noqa E501
    path(route='logout/', view=LogoutView.as_view(template_name='authentication/logout.html'), name='auth_logout'),
    path(route='register/', view=RegisterView.as_view(), name='auth_register')
]
