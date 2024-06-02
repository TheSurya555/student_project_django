from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    CANDIDATE = 'candidate'
    RECRUITER = 'recruiter'

    ROLE_CHOICES = (
        (CANDIDATE, 'Candidate'),
        (RECRUITER, 'Recruiter'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES ,default=CANDIDATE)
    phone = models.CharField(max_length=15,null=True , unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username
    

class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.username} - {self.company}"    
    
    
class CandidateProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate_profile')

    def __str__(self):
        return self.user.username    
