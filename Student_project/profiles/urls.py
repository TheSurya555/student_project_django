from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles_View , name= 'profiles'),
    path('settings', views.settings_View , name= 'settings'),
    path('messages', views.messages_View , name= 'messages'),
]