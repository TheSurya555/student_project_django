from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser ,RecruiterProfile, CandidateProfile

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RecruiterProfile)
admin.site.register(CandidateProfile)
