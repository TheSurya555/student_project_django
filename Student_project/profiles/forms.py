from django import forms
from .models import UserProfile, ProjectExperience ,SocialLink,EducationDetail
from django.contrib.auth import authenticate
from signUp.models import CustomUser
from datetime import date, timedelta
from tinymce.widgets import TinyMCE

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'dob', 'phone', 'country', 'state', 'city', 'address', 'postal_code', 
            'role', 'position', 'experience', 'skills', 'languages', 
            'vat_id', 'profile_image', 'resume', 'career_objective',
            'current_company', 'current_company_position', 'current_company_start_date',
            'previous_company', 'previous_company_position', 
            'previous_company_start_date', 'previous_company_end_date','preferred_location',
            'expected_salary','current_salary',
        ]
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'input', 'autocomplete': 'off'})
        self.fields['phone'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['country'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['state'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['city'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['address'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['postal_code'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['role'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['position'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['experience'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['skills'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['languages'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['vat_id'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['profile_image'].widget.attrs.update({'class': 'input', 'type': 'file'})
        self.fields['resume'].widget.attrs.update({'class': 'input', 'type': 'file'})
        self.fields['career_objective'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write your career objective'})
        self.fields['current_company'].widget.attrs.update({'class': 'input', 'autocomplete': 'off','placeholder': 'Enter N/A if no current company.'})
        self.fields['current_company_position'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['current_company_start_date'].widget= forms.DateInput(attrs={'type': 'date', 'class': 'input', 'autocomplete': 'off'})
        self.fields['previous_company'].widget.attrs.update({'class': 'input', 'autocomplete': 'off','placeholder': 'Enter N/A if no previous company.'})
        self.fields['previous_company_position'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['previous_company_start_date'].widget= forms.DateInput(attrs={'type': 'date', 'class': 'input', 'autocomplete': 'off'})
        self.fields['previous_company_end_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'input', 'autocomplete': 'off'})
        self.fields['preferred_location'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['expected_salary'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['current_salary'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
    
        
        
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            today = date.today()
            min_age_date = today - timedelta(days=365*27)
            max_age_date = today - timedelta(days=365*18)
            if not (min_age_date <= dob <= max_age_date):
                raise forms.ValidationError("Date of birth must be between 18 and 27 years from today.")
        return dob
      
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('previous_company_start_date')
        end_date = cleaned_data.get('previous_company_end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Previous company's start date cannot be after the end date.")
        
        return cleaned_data      
      
class ProjectExperienceForm(forms.ModelForm):
    class Meta:
        model = ProjectExperience
        fields = ['title', 'contribution', 'technologies', 'duration', 'description']
        widgets = {
            'description': TinyMCE(attrs={'class': 'form-control', 'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectExperienceForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['contribution'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['technologies'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})   
    
    
class SocialLinkForm(forms.ModelForm):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('website', 'Website'),
    ]

    platform = forms.ChoiceField(
        choices=PLATFORM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SocialLink
        fields = ['platform', 'link']
        widgets = {
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter profile link'}),
        }
    
class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Enter old password'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )
    # show_password = forms.BooleanField(label='Show Password', required=False)
    
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

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

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user    
    
    
class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']  # include all relevant fields
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 10 or not phone.isdigit():
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

#eduction field

class EducationDetailForm(forms.ModelForm):
    class Meta:
        model = EducationDetail
        fields = ['education_level', 'degree', 'specialization', 'university', 'college_name', 'start_year', 'end_year']
        widgets = {
            'start_year': forms.NumberInput(attrs={'class': 'input', 'autocomplete': 'off'}),
            'end_year': forms.NumberInput(attrs={'class': 'input', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super(EducationDetailForm, self).__init__(*args, **kwargs)
        
        # Make education_level a dropdown
        self.fields['education_level'].widget = forms.Select(
            choices=EducationDetail.EDUCATION_LEVEL_CHOICES,
            attrs={'class': 'input'}
        )
        
        self.fields['degree'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['university'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['specialization'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})
        self.fields['college_name'].widget.attrs.update({'class': 'input', 'autocomplete': 'off'})

    # Validation: End year must be greater than or equal to start year
    def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get("start_year")
        end_year = cleaned_data.get("end_year")

        if end_year and start_year and end_year < start_year:
            raise forms.ValidationError("End year must be greater than or equal to the start year.")
        
        return cleaned_data    