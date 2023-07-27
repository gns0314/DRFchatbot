from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.utils import timezone
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
