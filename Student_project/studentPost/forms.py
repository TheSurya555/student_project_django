from django import forms
from .models import BlogPost, CandidatePreference ,BlogImage
from tinymce.widgets import TinyMCE

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'publication_date', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the blog title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the author name'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select the publication date'}),
            'content': TinyMCE(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Enter the blog content'}),
        }

class BlogImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BlogImage
        fields = ['image']
        
        
class CandidatePreferenceForm(forms.ModelForm):
    class Meta:
        model = CandidatePreference
        fields = ['service_title', 'description', 'delivery_time', 'revisions', 'price']
        widgets = {
            'service_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the service'}),
            'delivery_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the delivery time'}),
            'revisions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the number of revisions'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the price'}),
        }
