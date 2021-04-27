from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TodoItem

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ["id", "text", "created_at", "created_by"]