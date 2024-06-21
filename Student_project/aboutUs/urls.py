from django.urls import path
from . import views

urlpatterns = [
    path('', views.aboutUs_view, name='aboutUs_view'),
]
