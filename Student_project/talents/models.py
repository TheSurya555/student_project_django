from django.db import models

class Skills(models.Model):
    skill = models.CharField(max_length=255)

    def __str__(self):
        return self.skill