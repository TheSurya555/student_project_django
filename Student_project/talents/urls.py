from django.urls import path
from . import views

urlpatterns = [
    path('', views.talents_View , name= 'talents'),
]