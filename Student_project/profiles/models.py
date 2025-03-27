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
    vat_id = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    career_objective = models.TextField(verbose_name='Career Objective', null=True, blank=True)
    level = models.CharField(max_length=20, null=True, blank=True)
    current_company = models.CharField(max_length=255, null=True, blank=True, verbose_name="Current Company")
    current_company_position = models.CharField(max_length=255, null=True, blank=True, verbose_name="Current Position")
    current_company_start_date = models.DateField(null=True, blank=True, verbose_name="Start Date at Current Company")
    previous_company = models.CharField(max_length=255, null=True, blank=True, verbose_name="Previous Company")
    previous_company_position = models.CharField(max_length=255, null=True, blank=True, verbose_name="Previous Position")
    previous_company_start_date = models.DateField(null=True, blank=True, verbose_name="Start Date at Previous Company")
    previous_company_end_date = models.DateField(null=True, blank=True, verbose_name="End Date at Previous Company")
    preferred_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Preferred Job Location")
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Expected Salary")
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Current Salary")
   
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

class SocialLink(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=100, verbose_name="Social Media Platform")
    link = models.URLField(max_length=500, verbose_name="Profile Link")

    def __str__(self):
        return f"{self.platform} - {self.user_profile.user.username}"

    class Meta:
        unique_together = ('user_profile', 'platform')  # Ensures each platform link is unique per user.

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


class EducationDetail(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('10th Grade', '10th Grade'),
        ('12th Grade', '12th Grade'),
        ('Graduation', 'Graduation'),
        ('Post Graduation', 'Post Graduation'),
        ('Other', 'Other'),
    ]

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='educations')
    education_level = models.CharField(
        max_length=255,
        choices=EDUCATION_LEVEL_CHOICES,  # Dropdown choices
        null=True, 
        blank=True, 
        verbose_name="Education Level"
    )
    degree = models.CharField(max_length=255, null=True, blank=True, verbose_name="Degree")
    specialization = models.CharField(max_length=255, null=True, blank=True, verbose_name="Specialization/Stream")
    college_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="College Name")
    university = models.CharField(max_length=255, null=True, blank=True, verbose_name="University Name")
    start_year = models.PositiveIntegerField(verbose_name="Start Year")
    end_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="End Year")  # Optional for ongoing degrees

    def __str__(self):
        end_year_display = self.end_year or "Present"
        return f"{self.education_level} - {self.degree} ({self.start_year} - {end_year_display})"
