from django.contrib import admin
from .models import Service ,Service_page

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'description', 'skills', 'created_at')
    list_display_links = ('created_at',)  # Set created_at as the link to the change page
    search_fields = ('name', 'skills')
    list_editable = ('icon', 'name', 'description', 'skills')  # Include icon in editable fields
    fields = ('icon', 'name', 'description', 'skills', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Service_page)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ('titel', 'page_description', 'service_banner_image')
    search_fields = ('titel',)
