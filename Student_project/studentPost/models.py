from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    content = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title



class CandidatePreference(models.Model):
    blog_post = models.OneToOneField(BlogPost, on_delete=models.CASCADE)
    service_title = models.CharField(max_length=200)
    description = models.TextField()
    delivery_time = models.CharField(max_length=100)
    revisions = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service_title