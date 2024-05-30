from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dob', 'phone', 'address', 'role', 'experience', 'skills', 'languages', 'education', 'vat_id']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})  # Update widget attributes
        self.fields['phone'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['address'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['role'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['experience'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['skills'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['languages'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['education'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['vat_id'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
