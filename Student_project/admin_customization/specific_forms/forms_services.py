from django import forms
from services.models import *

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


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = Service_page
        fields = ['titel', 'page_description', 'service_banner_image', 'service_left_image', 'service_right_image']
        widgets = {
            'titel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter page title'}),
            'page_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter page description'}),
            'service_banner_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'service_left_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'service_right_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
# suryaadmin65