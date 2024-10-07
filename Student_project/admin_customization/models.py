from django.db import models
from django.conf import settings

class Traffic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Optional user field
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    page_visited = models.CharField(max_length=255)  # URL or name of the page visited
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Optional field for storing IP address

    def __str__(self):
        return f"Traffic from {self.user if self.user else 'Guest'} on {self.timestamp} - {self.page_visited}"
