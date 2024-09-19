from django import forms
from services.models import Service
from talents.models import Skills
from examination.models import *
from aboutUs.models import *
from tinymce.widgets import TinyMCE 


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['icon', 'name', 'description', 'skills']
        widgets = {
            'icon': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter service description'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter required skills'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Add any additional customization or validation
        self.fields['icon'].label = 'Service Icon'
        self.fields['name'].label = 'Service Name'
        self.fields['description'].label = 'Service Description'
        self.fields['skills'].label = 'Required Skills'

    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if not skills:
            raise forms.ValidationError('This field is required.')
        return skills


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

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['score'] 