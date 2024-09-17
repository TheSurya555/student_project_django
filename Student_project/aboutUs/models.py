# models.py
from django.db import models

class AboutUsContent(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='about_us/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Default About Us Content"

class Feature(models.Model):
    about_us = models.ForeignKey(AboutUsContent, related_name='features', on_delete=models.CASCADE)
    icon = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class TeamMember(models.Model):
    about_us = models.ForeignKey(AboutUsContent, related_name='team_members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team_photos/')
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

