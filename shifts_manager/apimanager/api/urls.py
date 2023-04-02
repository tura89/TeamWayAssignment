from django.urls import path
from .views import all_shifts, shift, all_workers, worker, all_worker_shifts

urlpatterns = [
    path('shifts/', all_shifts, name='all-shifts'),
    path('shifts/<int:pk>', shift, name='shift'),

    path('workers/', all_workers, name='all-workers'),
    path('workers/<int:pk>', worker, name='worker'),
    path('workers/<int:pk>/shifts', all_worker_shifts, name='all-shifts-by-worker'),
]
