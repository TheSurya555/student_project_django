from django.contrib import admin
from .models import PrivacyPolicy
from tinymce.widgets import TinyMCE
from django import forms

class PrivacyPolicyAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class PrivacyPolicyAdmin(admin.ModelAdmin):
    form = PrivacyPolicyAdminForm

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
