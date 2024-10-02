from django import forms
from talents.models import Skills
from examination.models import Skill ,Question ,Answer,Test
from aboutUs.models import *
from payment.models import Subscription
from tinymce.widgets import TinyMCE 


# Skill form
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skill']  # Adjust fields as necessary
        widgets = {
            'skill': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skill'].label = 'Skill Name'
        
        
        
#exam skill form
class Exam_SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']  # Add other fields as necessary
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter service description'}),
        }

# Exam question form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['skill', 'text', 'correct_answer']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'text': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Enter question'}), 
            'correct_answer': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Enter correct answer'}), 
        }


#exam answer review form        
class AnswerCorrectionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['is_correct']
        widgets = {
            'is_correct': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }        
        
        
#Payment Subscription form        # 
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'price', 'description', 'short_content', 'features']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subscription name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'short_content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Short Description', 'rows': 3}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter features', 'rows': 3}),
        }        

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['score'] 