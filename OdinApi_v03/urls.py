"""OdinApi2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Odin API",
      default_version='v0.1',
      description="Puntos finales de la api ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
admin.site.site_header = 'ODIN'
# admin.site.site_title = 'My Site Title'
# admin.site.index_title = "<your_index_title>"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.autenticacion.urls')),
    path('api/', include('apps.empresa.urls')),
    path('api/', include('apps.taxis.urls')),
    path('api/', include('apps.periodico.urls')),
    path('api/', include('apps.ecommerce.urls')),
    
    # path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docsw/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
