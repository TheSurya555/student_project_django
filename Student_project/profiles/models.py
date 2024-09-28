from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from tinymce.models import HTMLField
from django_countries.fields import CountryField

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    languages = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    vat_id = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ProjectExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    contribution = models.CharField(max_length=100)
    technologies = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    project_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            # Assign the next project number
            max_project_number = ProjectExperience.objects.filter(user_profile=self.user_profile).aggregate(models.Max('project_number'))['project_number__max']
            self.project_number = (max_project_number or 0) + 1
        super().save(*args, **kwargs)

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()

    def __str__(self):
        return self.title

@receiver(post_delete, sender=ProjectExperience)
def reset_project_numbers(sender, instance, **kwargs):
    user_profile = instance.user_profile
    projects = ProjectExperience.objects.filter(user_profile=user_profile).order_by('id')
    for idx, project in enumerate(projects, start=1):
        project.project_number = idx
        project.save()
