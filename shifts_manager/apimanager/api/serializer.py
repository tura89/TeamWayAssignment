from rest_framework import serializers


class ShiftSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    worker_id = serializers.IntegerField(read_only=True)
    shift_date = serializers.DateField()
    shift_start = serializers.CharField()
    shift_end = serializers.CharField()


    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
