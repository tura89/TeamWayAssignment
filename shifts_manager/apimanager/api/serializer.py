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
        instance.worker_id = validated_data.get('worker_id', instance.worker_id)
        instance.shift_date = validated_data.get('shift_date', instance.shift_date)
        instance.shift_start = validated_data.get('shift_start', instance.shift_start)
        instance.shift_end = validated_data.get('shift_end', instance.shift_end)
        instance.save()
        return instance

    def create(self, validated_data):
        return Shift.objects.create(**validated_data)
