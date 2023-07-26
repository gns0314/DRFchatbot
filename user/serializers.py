from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length= 128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email',None)
        password = data.get('password',None)

        if email is None:
            raise serializers.ValidationError(
                '이메일이 필요합니다'
            )
        if password is None:
            raise serializers.ValidationError(
                '비밀번호가 필요합니다.'
            )
        
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                '잘못된 정보입니다.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                '삭제된 계정입니다.'
            )
        
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return {
            'email':user.email
        }
