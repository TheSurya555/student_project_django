from django.db import models
from django.conf import settings
from django.db.models import JSONField

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('CODE', 'Code-Based'),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='MCQ')
    text = models.TextField()
    options = JSONField(default=list, blank=True)
    correct_answer = models.TextField(help_text="Correct answer or solution")

    def __str__(self):
        return f"{self.skill.name} - {self.get_type_display()}: {self.text}"

class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1 , related_name='tests')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True,default=0)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"

    def calculate_total_score(self):
    # Sum up scores from both MCQ and coding questions
        total_score = sum(
            answer.is_correct * 1  
            for answer in self.answers.filter(question__type='MCQ')
    )
        total_score += sum(
            score.value
            for score in Score.objects.filter(answer__test=self)
    )
        # Convert the total score to a percentage based on max marks
        max_marks = 30
        percentage_score = (total_score / max_marks) * 100
        
        
        self.score = percentage_score
        self.save()
        
    @staticmethod
    def fetch_latest_score(user):
                
        latest_test = Test.objects.filter(user=user, completed=True).order_by('-completed_date').first()
        return latest_test.score if latest_test else None
    

class Answer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.test.user.username} - {self.question.text}: {self.answer}"


class Score(models.Model):
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, related_name='score')
    value = models.DecimalField(max_digits=5, decimal_places=2,default=0)

    def __str__(self):
        return f"Score for {self.answer}: {self.value}"

class ExamRule(models.Model):
    title = models.CharField(max_length=255)  # Title of the rule
    description = models.TextField()  # Detailed description of the rule
    
    def __str__(self):
        return self.title    