from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_View , name= 'services'),
    path('services/all/', views.all_services, name='all_services'),
    path('service/<int:service_id>/candidates/', views.service_candidates, name='service_candidates'),
    path('candidate/<int:candidate_id>/', views.candidate_profile, name='candidate_profile'),
    path('all-candidates/', views.all_candidates, name='all_candidates'),
    path('candidate/<int:candidate_id>/detail/', views.candidate_detail, name='candidate_detail'),
]
