from django.urls import path
from .views import all_shifts, shift

urlpatterns = [
    path('shifts/', all_shifts, name='all-shifts'),
    path('shifts/<int:pk>', shift, name='all-shifts'),
]
