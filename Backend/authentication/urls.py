from django.urls import path, include
from .views import LoginApi ,RegisterApi
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
      path('api/auth/register', RegisterApi.as_view()),
      path('api/auth/login', LoginApi.as_view()),
]