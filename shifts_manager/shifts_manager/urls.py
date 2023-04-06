from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path("", include("apimanager.urls")),
    path("admin", admin.site.urls),
    path("api/", include("apimanager.api.urls")),
    path("api-auth", include("rest_framework.urls"))
]
