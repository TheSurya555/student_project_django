# chat/admin.py
from django.contrib import admin
from .models import ChatSession, Message

class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_participants')
    search_fields = ('participants__username', 'participants__email')

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_session', 'sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')

admin.site.register(ChatSession, ChatSessionAdmin)
admin.site.register(Message, MessageAdmin)
