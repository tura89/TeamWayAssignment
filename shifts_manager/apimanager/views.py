from django.shortcuts import render
from .models import Shift, Worker


# Create your views here.
def dashboard(request):
    shifts = Shift.objects.order_by("-shift_date")
    context = {
        "page_name": "Recent Shifts",
        "items": list(shifts),
        "not_available_message": "No Shifts Available",
    }
    return render(request, "apimanager/index.html", context)


def dashboard_workers(request):
    workers = Worker.objects.order_by("-id")
    context = {
        "page_name": "All Workers",
        "items": list(workers),
        "not_available_message": "No Workers Available",
    }
    return render(request, "apimanager/index.html", context)
