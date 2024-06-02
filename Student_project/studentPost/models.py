from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
