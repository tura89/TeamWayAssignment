import datetime

from rest_framework import serializers
from ..models import Shift, Worker


class ShiftSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    worker_id = serializers.IntegerField()
    shift_date = serializers.DateField()
    shift_start = serializers.CharField()
    shift_end = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.worker_id = validated_data.get('worker_id', instance.worker_id)
        instance.shift_date = validated_data.get('shift_date', instance.shift_date)
        instance.shift_start = validated_data.get('shift_start', instance.shift_start)
        instance.shift_end = validated_data.get('shift_end', instance.shift_end)
        instance.save()
        return instance

    def create(self, validated_data):
        return Shift.objects.create(**validated_data)

    def validate_worker_id(self, value):
        try:
            worker = Worker.objects.get(pk=value)
        except Worker.DoesNotExist:
            raise serializers.ValidationError("Worker ID not found")
        return value

    def validate_shift_start(self, value):
        if value in Shift.StartTimes.values:
            return value
        raise serializers.ValidationError(F"Start date should be one of: {Shift.StartTimes.values}")

    def validate_shift_end(self, value):
        if not value or value in Shift.EndTimes.values:
            return value
        raise serializers.ValidationError(F"End date should be one of: {Shift.StartTimes.values}, or left unspecified")

    def validate(self, data):
        start_time = datetime.datetime.strptime(data['shift_start'], "%H:%M")
        end_time = data.get('shift_end')
        if end_time:
            end_time = datetime.datetime.strptime(end_time, "%H:%M")
            if end_time and start_time + datetime.timedelta(hours=8) != end_time:
                raise serializers.ValidationError(
                    F"End date should be 8 hours ahead of start date, or left unspecified"
                )

        shifts_on_date = Shift.objects.filter(shift_date=data['shift_date'], worker_id=data['worker_id'])

        if shifts_on_date:

            raise serializers.ValidationError(
                F"Worker {data['worker_id']} already has a shift on {data['shift_date']}, ID: {shifts_on_date[0].id}"
            )

        return data
