from django import forms
from aboutUs.models import AboutUsContent, Feature, TeamMember
from contactus.models import ConsultingMessage, SupportInfo
from tinymce.widgets import TinyMCE 
from profiles.models import PrivacyPolicy

# About Us Forms

class AboutUsContentForm(forms.ModelForm):
    class Meta:
        model = AboutUsContent
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': TinyMCE(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['about_us', 'icon', 'title', 'description']
        widgets = {
            'about_us': forms.Select(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter icon name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter feature title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['about_us', 'name', 'title', 'photo', 'linkedin_url']
        widgets = {
            'about_us': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter member name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter member title'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter LinkedIn URL'}),
        }

# Contact Us Forms

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['about_us', 'name', 'title', 'photo', 'linkedin_url']
        widgets = {
            'about_us': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter member name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter member title'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter LinkedIn URL'}),
        }

# Contact Us Forms

class ConsultingMessageForm(forms.ModelForm):
    class Meta:
        model = ConsultingMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your message'}),
        }

class SupportInfoForm(forms.ModelForm):
    class Meta:
        model = SupportInfo
        fields = ['title', 'description', 'phone', 'email', 'address', 'support_image', 'contatus_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter description'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'support_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'contatus_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
# PrivacyPolicy form        
class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['title', 'content']        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': TinyMCE(attrs={'class': 'form-control', 'rows': 3}),
        }