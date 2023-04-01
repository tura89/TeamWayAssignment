from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ShiftSerializer
from ..models import Shift


@api_view(['GET', 'POST'])
def all_shifts(request):
    if request.method == 'GET':
        shifts = Shift.objects.order_by('-shift_date')
        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def shift(request, pk):
    try:
        _shift = Shift.objects.get(pk=pk)
    except Shift.DoesNotExist:
        return Response({"Error: Shift not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShiftSerializer(_shift)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ShiftSerializer(_shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    if request.method == 'GET':
        _shift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

