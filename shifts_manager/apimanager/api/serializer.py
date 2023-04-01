from rest_framework import serializers
from ..models import Shift, Worker
from rest_framework.response import Response
from rest_framework import status


class ShiftSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    worker_id = serializers.IntegerField()
    shift_date = serializers.DateField()
    shift_start = serializers.CharField()
    shift_end = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return Shift.objects.create(**validated_data)
