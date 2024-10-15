from django.db import models
from django.conf import settings

class Traffic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Optional user field
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    page_visited = models.CharField(max_length=255)  # URL or name of the page visited
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Optional field for storing IP address

    def __str__(self):
        return f"Traffic from {self.user if self.user else 'Guest'} on {self.timestamp} - {self.page_visited}"


class HeroSection(models.Model):
    heading = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255)
    description = models.TextField()
    button_text = models.CharField(max_length=50, default="Connect With Us")
    button_url = models.URLField()
    image1 = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='hero_images/', blank=True, null=True)

    def __str__(self):
        return self.heading
    
    
class WorkStep(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50)  # Store icon class name for flexibility (e.g., 'fa-solid fa-sign-in-alt')

    def __str__(self):
        return self.title    
    
class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True) 
    button_text = models.CharField(max_length=50, default="Contact Us")
    contact_image = models.ImageField(upload_to='contact_images/', blank=True, null=True) 

    def __str__(self):
        return self.name    