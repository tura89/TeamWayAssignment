from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ShiftSerializer
from ..models import Shift


@api_view()
def all_shifts(request):
    shifts = Shift.objects.order_by('-shift_date')
    serializer = ShiftSerializer(shifts, many=True)
    return Response(serializer.data)


@api_view()
def shift(request, pk):
    try:
        _shift = Shift.objects.get(pk=pk)
    except Shift.DoesNotExist:
        return Response({"Error: Shift not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ShiftSerializer(_shift)
    return Response(serializer.data)
