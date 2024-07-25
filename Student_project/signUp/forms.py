# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, RecruiterProfile, CandidateProfile, AdminProfile
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password

class CandidateSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'fname', 'autocomplete': 'off'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input', 'id': 'lname', 'autocomplete': 'off'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'input', 'id': 'email', 'autocomplete': 'off'}))
    phone = forms.CharField(max_length=15, required=True, validators=[RegexValidator(r'^\d{10}$', message="Phone number must be exactly 10 digits.")], widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}),
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}),
    )
        
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}),
        }
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
             
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
    phone = forms.CharField(max_length=15, required=True, validators=[RegexValidator(r'^\d{10}$', message="Phone number must be exactly 10 digits.")], widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}),
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}),
    )
    
    class Meta:
        model =  CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2' ,'company')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}),
        }
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2        

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
    professional_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    phone = forms.CharField(max_length=15, required=True, validators=[RegexValidator(r'^\d{10}$', message="Phone number must be exactly 10 digits.")], widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}),
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'off'}),
    )    
    
    class Meta:
        model =  CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2' ,'professional_id')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}),
        }    

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.ADMIN
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
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input password', 'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username:
            if '@' in username:
                cleaned_data['email'] = username
            else:
                cleaned_data['phone'] = username
        return cleaned_data



