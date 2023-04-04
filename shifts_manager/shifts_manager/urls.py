from django.urls import include, path

urlpatterns = [
    path("", include("apimanager.urls")),
    path("api/", include("apimanager.api.urls"))
]
