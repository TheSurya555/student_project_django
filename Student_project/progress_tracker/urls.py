# progress_tracker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:project_id>/', views.project_progress_view, name='project_progress'),
    path('progress/<int:progress_id>/update/', views.update_progress_view, name='update_progress'),
    path('project/<int:project_id>/status/', views.update_project_status_view, name='update_project_status'),
    path('confirm_progress/<int:progress_id>/', views.confirm_progress_view, name='confirm_progress'),
]
