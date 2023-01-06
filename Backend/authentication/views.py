from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
# Create your views here.


#LoginAPI
class LoginApi(APIView):


    def post(self, request):
        serializer= LoginSerializer(request.data)
        try:
            username = serializer.data['username']
            password = serializer.data['password']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username, password=password)
        except:
            data={'message':"Username or Password is incorrect."}
            return Response(data=data,status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_token = user.auth_token.key
        except:
            user_token = Token.objects.create(user=user)

        data = {'token': user_token}
        return Response(data=data, status=status.HTTP_200_OK)


#Register API
class RegisterApi(APIView):


    def post(self, request, *args,  **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_token = Token.objects.create(user=user)
            return Response({
                "message":"User created!",
                "access_token": user_token.key,
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
