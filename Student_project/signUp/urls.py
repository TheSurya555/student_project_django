from django.urls import path
from . import views

urlpatterns = [
    path('', views.signUP_View , name= 'signup'),
    path('candidateSignUp/', views.candidate_SignUp_View , name= 'candidateSignUp'),
    path('requiterSignUp/', views.requiter_SignUp_View, name= 'requiterSignUp'),
]