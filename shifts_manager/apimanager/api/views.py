from django.http import JsonResponse

from ..models import Shift


def all_shifts(request):
    shifts = Shift.objects.order_by('-shift_date')
    response = {
        'shifts': list(shifts.values())
    }
    return JsonResponse(response)

def shift(request, pk):
    pass