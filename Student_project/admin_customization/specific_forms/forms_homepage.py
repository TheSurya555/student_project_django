from django import forms
from admin_customization.models import HeroSection, WorkStep, ContactInfo


class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = ['heading', 'sub_heading', 'description', 'button_text', 'button_url', 'image1', 'image2', 'image3']
        widgets = {
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'button_url': forms.URLInput(attrs={'class': 'form-control'}),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),
        }


class WorkStepForm(forms.ModelForm):
    class Meta:
        model = WorkStep
        fields = ['title', 'description', 'icon']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),  # For icon class input (like 'fa-solid fa-sign-in-alt')
        }

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['name', 'phone', 'email', 'address', 'description', 'button_text', 'contact_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}), 
        }
