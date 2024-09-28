# mixins.py

from notifications.models import Notification

class NotificationMixin:
    def get_notifications(self, request):
        return Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]