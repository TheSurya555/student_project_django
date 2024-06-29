# from django import forms
# from .models import BlogPost
# from tinymce.widgets import TinyMCE

# class BlogPostForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'author', 'publication_date', 'content', 'blog_image']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'author': forms.TextInput(attrs={'class': 'form-control'}),
#             'publication_date': forms.DateInput(attrs={'class': 'form-control' ,'type': 'date'}),
#             'content': TinyMCE(attrs={'class': 'form-control', 'rows': 8}),
#             'blog_image': forms.FileInput(attrs={'class': 'form-control' ,'type':'file' }),
#         }


from django import forms
from .models import BlogPost, CandidatePreference
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

class CandidatePreferenceForm(forms.ModelForm):
    class Meta:
        model = CandidatePreference
        fields = ['service_title', 'description', 'delivery_time', 'revisions','price']
        widgets = {
            'service_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': TinyMCE(attrs={'class': 'form-control', 'rows': 8}),
            'delivery_time': forms.TextInput(attrs={'class': 'form-control'}),
            'revisions': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
