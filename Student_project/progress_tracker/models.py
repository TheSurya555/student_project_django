from django.db import models
from signUp.models import CustomUser  # Adjust the import according to your project structure

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('terminated', 'Terminated'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    client = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='client_projects')
    name = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)  # You might want to remove or use this if it's redundant
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    stages = models.TextField(default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    project_costing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New field for project costing

    def get_stages(self):
        return self.stages.split(',')

    def get_cost_per_stage(self):
        stages = self.get_stages()
        num_stages = len(stages)
        if num_stages == 0 or self.project_costing is None:
            return 0
        return self.project_costing / num_stages

    def __str__(self):
        return f"{self.name} (Client: {self.client.username})" if self.client else self.name

class Progress(models.Model):
    project = models.ForeignKey(Project, related_name='progresses', on_delete=models.CASCADE)
    stage = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)  # Use a valid default user ID
    status = models.CharField(max_length=255, blank=True, null=True)  # Add this line

    def __str__(self):
        return f'{self.project.name} - {self.stage}'
