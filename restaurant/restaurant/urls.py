"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path, include, re_path
from restaurant.admin import admin_site

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="H&Q Restaurant API",
        default_version="v1",
        description="APIs for RestaurantApp",
        contact=openapi.Contact(email="2351050141quang@ou.edu.vn"),
        license=openapi.License(name="Nguyễn Hữu Quang@2026"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("apis/", include("users.urls")),
    path("apis/", include("products.urls")),
    path("admin/", admin_site.urls),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    re_path(
        r"^apis/swagger(?P<format>\.json|\.yaml)$",  
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^apis/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^apis/redoc/$", 
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
