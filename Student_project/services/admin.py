from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'description', 'skills' ,'created_at')
    search_fields = ('name', 'skills')
