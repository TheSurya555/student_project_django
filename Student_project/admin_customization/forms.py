from django import forms
from talents.models import Skills
from examination.models import Skill ,Question ,Answer,Test,ExamRule
from aboutUs.models import *
from payment.models import Subscription
from tinymce.widgets import TinyMCE 
import json


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
        fields = ['skill', 'type', 'text', 'options', 'correct_answer']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter question'}),
            'options': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter options as a JSON array (e.g., ["Option 1", "Option 2"])'
            }),
            'correct_answer': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the correct answer or solution'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('type')
        options = cleaned_data.get('options')
        correct_answer = cleaned_data.get('correct_answer')

        # Parse and validate options field for MCQ
        if question_type == 'MCQ':
            if not options:
                raise forms.ValidationError("Options are required for MCQ questions.")
            if isinstance(options, str):
                try:
                    options = json.loads(options)  # Parse options as JSON
                except json.JSONDecodeError:
                    raise forms.ValidationError("Options must be a valid JSON array in the format: [\"Option 1\", \"Option 2\"].")
            if not isinstance(options, list) or len(options) < 2:
                raise forms.ValidationError("Options must be a valid JSON array with at least two items.")
            cleaned_data['options'] = options  # Save the parsed list
            
            # Validate correct_answer for CODE
            if not correct_answer:
                raise forms.ValidationError("Code-based questions require a correct solution.")

        return cleaned_data
 

#exam answer review form        
class AnswerCorrectionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = []  # Dynamically set fields based on question type

    def __init__(self, *args, **kwargs):
        question_type = kwargs.pop('question_type', None)  # Pass question type when initializing the form
        super().__init__(*args, **kwargs)

        if question_type == 'MCQ':
            self.fields['is_correct'] = forms.ChoiceField(
                choices=[(True, 'Yes'), (False, 'No')],
                widget=forms.RadioSelect,
                label="Is Correct"
            )
        elif question_type == 'coding':
            self.fields['score'] = forms.DecimalField(
                max_digits=5,
                decimal_places=2,
                label="Score",
                widget=forms.NumberInput(attrs={'min': 0, 'step': 0.1}),
            )     
        
        
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


class ExamRulesForm(forms.ModelForm):
    class Meta:
        model = ExamRule
        fields = ['title','description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Rules title'}),
            'description': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Write Your Rules here'}), 
        }         