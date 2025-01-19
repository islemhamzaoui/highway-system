# autoroute_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from autouroute_api import views # added this line


schema_view = get_schema_view(
    openapi.Info(
        title="Highway Management System",
        default_version='v1',
        
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autouroute_api.urls')),  # This includes the login view
    path('admin/', admin.site.urls),
    path('api/', include('autouroute_api.urls')),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]