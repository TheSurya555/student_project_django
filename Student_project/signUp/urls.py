from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.signUP_View , name= 'signup'),
    path('signup/', views.candidate_SignUp_View , name= 'candidateSignUp'),
]