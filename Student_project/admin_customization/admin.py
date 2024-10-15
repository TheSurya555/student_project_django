from django.contrib import admin
from .models import Traffic, HeroSection, WorkStep, ContactInfo

@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'page_visited', 'ip_address')
    search_fields = ('user__username', 'page_visited', 'ip_address')
    list_filter = ('timestamp',)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'description', 'button_text')  # Adjust these based on the fields you want to display
    search_fields = ('heading', 'sub_heading')
    list_filter = ('heading',)

@admin.register(WorkStep)
class WorkStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'icon')  # Adjust these based on the fields you want to display
    search_fields = ('title',)
    list_filter = ('title',)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'description', 'button_text')  # Adjust these based on the fields you want to display
    search_fields = ('name', 'phone', 'email')
    list_filter = ('name',)