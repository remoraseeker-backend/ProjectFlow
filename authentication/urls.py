from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path


urlpatterns = [
    path(route='login/', view=LoginView.as_view(), name='login'),
    path(route='logout/', view=LogoutView.as_view(), name='logout'),
]
