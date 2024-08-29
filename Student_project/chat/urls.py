# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:candidate_id>/', views.start_chat, name='start_chat'),
    path('session/<int:chat_session_id>/', views.chat_session, name='chat_session'),
    path('session/<int:chat_session_id>/messages/', views.get_messages, name='get_messages'),
    path('messages/', views.inbox , name= 'messages'),
    path('send_message/', views.send_message, name='send_message'),  # New URL pattern
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]
