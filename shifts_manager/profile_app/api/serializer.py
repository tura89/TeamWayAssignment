from django.contrib.auth.models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"error": "Profile with this email already exists."})

        profile = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        profile.set_password(self.validated_data['password'])
        profile.save()

        return profile
