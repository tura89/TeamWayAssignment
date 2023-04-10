from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Shift, Worker
from .serializer import ShiftSerializer, WorkerSerializer


@api_view(["GET", "POST"])
def all_shifts(request):
    if request.method == "GET":
        shifts = Shift.objects.order_by("-shift_date")
        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ShiftSerializer(data=request.data, context={"is_create": True})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def shift(request, pk):
    _shift = get_object_or_404(Shift, pk=pk)

    if request.method == "GET":
        serializer = ShiftSerializer(_shift)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ShiftSerializer(_shift, data=request.data, context={"is_create": False, "shift_id": pk})
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
    _worker = get_object_or_404(Worker, pk=pk)

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
