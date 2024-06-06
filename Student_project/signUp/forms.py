# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm ,PasswordChangeForm
from .models import CustomUser ,RecruiterProfile, CandidateProfile ,AdminProfile
from django.contrib.auth import authenticate

class CandidateSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'fname', 'autocomplete': 'off'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'lname', 'autocomplete': 'off'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'input', 'id': 'email', 'autocomplete': 'off'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.CANDIDATE
        if commit:
            user.save()
            CandidateProfile.objects.create(user=user)
        return user        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone

class RecruiterSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'fname', 'autocomplete': 'off'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'lname', 'autocomplete': 'off'}))
    company = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'company', 'autocomplete': 'off'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'input', 'id': 'email', 'autocomplete': 'off'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}))

    class Meta:
        model =  CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2' ,'company')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.RECRUITER
        if commit:
            user.save()
            RecruiterProfile.objects.create(user=user, company=self.cleaned_data.get('company'))
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone


class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'fname', 'autocomplete': 'off'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'lname', 'autocomplete': 'off'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'input', 'id': 'email', 'autocomplete': 'off'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    professional_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    
    
    class Meta:
        model =  CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2' ,'professional_id')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}),
        }    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.ADMIN
        user.professional_id = self.cleaned_data['professional_id']  # Save professional_id to user
        user.is_staff = True  # Grant staff access
        user.is_superuser = True  # Grant superuser access
        if commit:
            user.save()
            AdminProfile.objects.create(user=user, professional_id=self.cleaned_data.get('professional_id'))
        return user
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone



class EmailOrPhoneLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username:
            if '@' in username:
                cleaned_data['email'] = username
            else:
                cleaned_data['phone'] = username
        return cleaned_data



