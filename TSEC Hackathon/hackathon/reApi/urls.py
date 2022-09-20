from email.mime import base
from xml.etree.ElementInclude import include
from django.urls import path
from reApi import views
urlpatterns = [
    path("get-details",views.UserDetailAPI.as_view()),
    path('register',views.RegisterUserAPIView.as_view()),
]