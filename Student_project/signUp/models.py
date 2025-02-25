from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import RegexValidator

# Validator for Indian phone numbers (10-digit, starting with 6, 7, 8, or 9)
indian_phone_validator = RegexValidator(
    regex=r'^[6789]\d{9}$',
    message="Enter a valid 10-digit Indian phone number starting with 6, 7, 8, or 9."
)

# Validator for proper name format (First letter capital, no numbers/special chars, allows single-word & multi-word names)
name_validator = RegexValidator(
    regex=r'^[A-Z][a-z]*(?:\s[A-Z][a-z]*)*$',
    message="Enter a valid name (Each word should start with an uppercase letter, e.g., 'John Doe')."
)

class CustomUser(AbstractUser):
    CANDIDATE = 'candidate'
    RECRUITER = 'recruiter'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (CANDIDATE, 'Candidate'),
        (RECRUITER, 'Recruiter'),
        (ADMIN, 'Admin'),
    )

    full_name = models.CharField(
        max_length=50, 
        validators=[name_validator],  
        default="Unknown",  # Ensuring existing users have a default value
        help_text="Enter your full name (Each word should start with an uppercase letter)."
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CANDIDATE)
    phone = models.CharField(
        max_length=10, 
        null=False,  
        blank=False, 
        unique=True, 
        validators=[indian_phone_validator]  
    )
    professional_id = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)  

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

    def is_online(self):
        if not self.last_activity:
            return False
        now = timezone.now()
        return now - self.last_activity < datetime.timedelta(minutes=5) 


class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company = models.CharField(max_length=50)  

    def __str__(self):
        return f"{self.user.username} - {self.company}"    
    
    
class CandidateProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate_profile')

    def __str__(self):
        return self.user.username


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    professional_id = models.CharField(max_length=30, unique=True, null=True, blank=True)  

    def __str__(self):
        return f"{self.user.username} - {self.professional_id if self.professional_id else 'No ID'}"
