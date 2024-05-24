from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactus_View , name= 'contactus'),
]