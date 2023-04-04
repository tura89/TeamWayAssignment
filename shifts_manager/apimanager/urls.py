from django.urls import path

from .views import dashboard, dashboard_workers

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("workers/", dashboard_workers, name="dashboard-workers"),
]
