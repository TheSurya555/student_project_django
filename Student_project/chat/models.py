# chat/models.py

from django.db import models, IntegrityError, transaction
from signUp.models import CustomUser  # Import the CustomUser model

class ChatSession(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatSession {self.id}"

    @classmethod
    def get_or_create_chat(cls, user1, user2):
        chat_sessions = cls.objects.filter(participants=user1).filter(participants=user2)
        if chat_sessions.exists():
            return chat_sessions.first()
        else:
            with transaction.atomic():
                chat_session = cls.objects.create()
                chat_session.participants.add(user1, user2)
                return chat_session

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} to {self.receiver.username if self.receiver else 'N/A'}"
