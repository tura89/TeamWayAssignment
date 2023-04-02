from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Shift, Worker
from .serializer import ShiftSerializer, WorkerSerializer


@api_view(["GET", "POST"])
def all_shifts(request):
    if request.method == "GET":
        shifts = Shift.objects.order_by("-shift_date")
        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def shift(request, pk):
    try:
        _shift = Shift.objects.get(pk=pk)
    except Shift.DoesNotExist:
        return Response({"Error: Shift not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ShiftSerializer(_shift)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ShiftSerializer(_shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == "DELETE":
        _shift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def all_workers(request):
    if request.method == "GET":
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def worker(request, pk):
    try:
        _worker = Worker.objects.get(pk=pk)
    except Worker.DoesNotExist:
        return Response({"Error: Worker not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WorkerSerializer(_worker)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = WorkerSerializer(_worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == "DELETE":
        _worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def all_worker_shifts(request, pk):
    if request.method == "GET":
        shifts = Shift.objects.filter(worker_id=pk).order_by("-shift_date")
        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
