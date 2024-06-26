from django.db import models

class AboutUsContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about_us/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.name
