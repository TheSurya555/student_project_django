from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'description', 'skills', 'created_at')
    search_fields = ('name', 'skills')
    list_editable = ('name', 'description', 'skills')
    fields = ('icon', 'name', 'description', 'skills', 'created_at')
    readonly_fields = ('created_at',)
