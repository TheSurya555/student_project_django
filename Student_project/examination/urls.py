from django.urls import path
from . import views

urlpatterns = [
    path('choose-skill/', views.choose_skill, name='choose_skill'),
    path('test/', views.test, name='test'),
    path('rules-and-regulations/', views.rules_and_regulations, name='rules_and_regulations'),
    path('start-test/<int:skill_id>/', views.start_test, name='start_test'),
    path('take-test/<int:test_id>/', views.take_test, name='take_test'),
    path('test_completed/<int:test_id>/', views.test_completed, name='test_completed'),
]