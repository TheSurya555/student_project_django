# forms.py
from django import forms
from progress_tracker.models import Project, Progress
from signUp.models import CustomUser

class ProjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['user', 'client', 'project_name', 'client_name', 'image', 'stages', 'status', 'project_costing']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Candidate'}),
            'client': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Client'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Project Name'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Client Name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stages': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Stages'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'project_costing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Project Cost'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, you can filter users for specific conditions
        self.fields['user'].queryset = CustomUser.objects.filter(role=CustomUser.CANDIDATE)
        # Filter clients for recruiters
        self.fields['client'].queryset = CustomUser.objects.filter(role=CustomUser.RECRUITER)

