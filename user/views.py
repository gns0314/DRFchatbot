from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer


# Create your views here.

# 회원 가입
class Registration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# 로그인

class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user:
            # 로그인 성공 시 토큰 생성 및 반환
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': '잘못된 정보입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    

# 로그아웃
class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "로그아웃되었습니다."}, status=status.HTTP_200_OK)