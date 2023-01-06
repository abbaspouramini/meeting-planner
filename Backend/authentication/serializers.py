from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','username')
        extra_kwargs = {
            'password':{'write_only': True},
        }
        def create(self, validated_data):
            user = User(username=validated_data['username'],  email=validated_data['email'])
            user.set_password(validated_data['password'])
            return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password','username')


