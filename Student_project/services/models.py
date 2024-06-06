from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255, help_text="Comma-separated skills related to this service")
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='service_icons/', null=True, blank=True)  # Add this line for the icon


    def __str__(self):
        return self.name
