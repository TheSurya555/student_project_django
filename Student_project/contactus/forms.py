from django import forms
from .models import ConsultingMessage

class ConsultingForm(forms.ModelForm):
    class Meta:
        model = ConsultingMessage
        fields = ('name', 'email', 'phone', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'autocomplete': 'off', 
                'placeholder': 'Enter your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'id': 'email', 
                'autocomplete': 'off', 
                'placeholder': 'Enter your email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'phone', 
                'autocomplete': 'off', 
                'placeholder': 'Enter your phone number'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter your message'
            }),
        }
