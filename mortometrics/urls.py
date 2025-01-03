from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# https://drf-yasg.readthedocs.io/en/stable/readme.html#quickstart
# this is used fo setting up swagger api view
schema_view = get_schema_view(
    openapi.Info(
        title="MortoMetrics API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # dispatching user request and serving the genedata app in the root path
    path('', include('mortometricsapp.urls')),
    path('admin/', admin.site.urls),
    # paths to view api lists via swagger and redoc
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
