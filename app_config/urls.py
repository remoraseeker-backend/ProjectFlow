from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path


urlpatterns = [
    path(route='', view=include('app.urls')),
    path(route='projects/', view=include('projects.urls')),
    path(route='accounts/', view=include('authentication.urls')),
    path(route='admin/', view=admin.site.urls),
]


# Required for debugging the SQL queries.
if getattr(settings, 'DEBUG', False):
    import debug_toolbar
    urlpatterns.insert(0, path(route='__debug__/', view=include(debug_toolbar.urls)))
