from django.contrib import admin
from django.urls import include
from django.urls import path


urlpatterns = [
    path(route='', view=include('app.urls')),
    path(route='accounts/', view=include('authentication.urls')),
    path(route='admin/', view=admin.site.urls),
]
