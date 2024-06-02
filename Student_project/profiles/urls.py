from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles_View , name= 'profiles'),
    path('settings', views.settings_View , name= 'settings'),
    path('messages', views.messages_View , name= 'messages'),
    path('profile_edit', views.edit_profile_View , name= 'profile_edit'),
    path('add_project/', views.add_project, name='add_project'), 
    # path('change_password/', views.change_password, name='change_password'),
    
]