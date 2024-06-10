from django.urls import path
from . import views

urlpatterns = [
    path('', views.talent_view , name= 'talents'),
    path('talents/<int:skill_id>/', views.fetch_skill_data, name='fetch_skill_data'),
    path('talents/skill-candidates/<int:service_id>/', views.skill_service_candidates, name='skill_service_candidates'),
]
