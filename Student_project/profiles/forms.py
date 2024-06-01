from django import forms
from .models import UserProfile, ProjectExperience

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dob', 'phone', 'address', 'role', 'position', 'experience', 'skills', 'languages', 'education', 'vat_id', 'profile_image']
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['address'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['role'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['position'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['experience'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['skills'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['languages'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['education'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['vat_id'].widget.attrs.update({'class': 'form-control input', 'autocomplete': 'off'})
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control input', 'type': 'file'})

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
