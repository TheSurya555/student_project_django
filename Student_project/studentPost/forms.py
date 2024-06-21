from django import forms
from .models import BlogPost
from tinymce.widgets import TinyMCE

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'publication_date', 'content', 'blog_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control' ,'type': 'date'}),
            'content': TinyMCE(attrs={'class': 'form-control', 'rows': 8}),
            'blog_image': forms.FileInput(attrs={'class': 'form-control' ,'type':'file' }),
        }
