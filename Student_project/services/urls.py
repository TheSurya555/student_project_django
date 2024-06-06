from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_View , name= 'services'),
    path('service/<int:service_id>/candidates/', views.service_candidates, name='service_candidates'),
]