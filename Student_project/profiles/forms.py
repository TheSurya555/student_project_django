from django import forms
from .models import UserProfile, ProjectExperience
from django.contrib.auth.forms import PasswordChangeForm ,UserChangeForm
from django.contrib.auth import authenticate
from signUp.models import CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dob', 'phone', 'address', 'role', 'position', 'experience', 'skills', 'languages', 'education', 'vat_id', 'profile_image']
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'input', 'autocomplete': 'off'})
        self.fields['phone'].widget.attrs.update({'class': 'input', 'autocomplete': 'off' })
        self.fields['address'].widget.attrs.update({'class': 'input', 'autocomplete': 'off' })
        self.fields['role'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['position'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['experience'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['skills'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['languages'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['education'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['vat_id'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['profile_image'].widget.attrs.update({'class': 'input', 'type': 'file'})

class ProjectExperienceForm(forms.ModelForm):
    class Meta:
        model = ProjectExperience
        fields = ['title', 'contribution', 'technologies', 'duration', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectExperienceForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['contribution'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['technologies'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off' ,'placeholder': 'Enter old password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = authenticate(username=self.user.username, password=old_password)
        if not user:
            raise forms.ValidationError("Invalid old password.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The new passwords do not match.")
        return cleaned_data        
    
    
class EditUserForm(UserChangeForm):
    password = None
    # 'phone': forms.CharField(attrs={'class':'border-b border-black focus:outline-none focus:border-blue-600 text-sm w-full py-2', 'placeholder': 'Phone Number'}),
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email' ,'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email Address'}),
        }
    