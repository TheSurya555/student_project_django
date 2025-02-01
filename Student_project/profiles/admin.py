from django.contrib import admin
from .models import PrivacyPolicy ,UserProfile, ProjectExperience,EducationDetail
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



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role', 'position')
    search_fields = ('user__username', 'role', 'position')
    list_filter = ('role', 'position')

@admin.register(ProjectExperience)
class ProjectExperienceAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'title', 'contribution', 'project_number')
    search_fields = ('title', 'contribution')
    list_filter = ('user_profile__user__username',)

@admin.register(EducationDetail)
class EducationDetailAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'education_level', 'degree', 'college_name', 'start_year', 'end_year',)  
    