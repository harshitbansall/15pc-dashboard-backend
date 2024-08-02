import json

from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse, redirect, render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import ConfigUserSerializer, UserSerializer


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = UserSerializer(data={
            'full_name': request.data.get('full_name').title() if request.data.get('full_name') else None,
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'raw_password': request.data.get('password'),
        })
        if serializer.is_valid():
            try:
                created_user = serializer.save()
                refresh = RefreshToken.for_user(created_user)
                return Response(data={"success": "true", "message": "User Created.", "refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={"success": "false", "message": str(e).title()})
        else:
            return Response(data={"success": "false", "message": serializer.errors})


class ObtainAuthToken(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        user_instance = authenticate(email=request.data.get(
            'email'), password=request.data.get('password'))
        if user_instance is not None:
            refresh = RefreshToken.for_user(user_instance)
            return Response(data={"success": "true", "refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response(data={"success": "false", "message": "User Not Found."})


class Config(APIView):
    def get(self, request):
        data = {
            "success": "true",
            "user_details": ConfigUserSerializer(request.user).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
