from django.urls import path
from . import views

urlpatterns = [
    path('', views.consulting_View , name= 'contactus'),
]