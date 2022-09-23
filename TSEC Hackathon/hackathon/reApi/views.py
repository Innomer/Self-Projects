from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSerializer,RegisterSerializer,ProfCreateUpdateSerializer
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

class EditProfile(generics.UpdateAPIView):
  permission_classes=(IsAuthenticated,)
  serializer_class=ProfCreateUpdateSerializer

  def get_query_set(self,request,*args,**kwargs):
    tok=request.headers['Token']
    user=Token.objects.get(key=tok).user
    user.Profile.edStat=request.headers['edStat']
    user.Profile.abt=request.headers['abt']
    user.Profile.birthDate=request.headers['birthDate']
    user.Profile.city=request.headers['city']
    user.Profile.country=request.headers['country']
    user.Profile.career=request.headers['career']
    user.Profile.interests=request.headers['interests']
    user.Profile.communities=request.headers['communities']
    user.Profile.pp=request.headers['pp']
    user.save()