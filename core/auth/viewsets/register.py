from django.shortcuts import render
from core.user import serializers
from core.user.models import User
from rest_framework import viewsets, permissions


class RegisterViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.UserSerializer
    permissions_class = [permissions.AllowAny]
    http_method_names = ['post']
    queryset = User.objects.all()

    
