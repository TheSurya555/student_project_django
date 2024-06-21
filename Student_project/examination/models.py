from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()  # Ensure this field is present

    def __str__(self):
        return self.name

class Question(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.skill.name}: {self.text}"

class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"

class Answer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test.user.username} - {self.question.text}: {self.answer}"
