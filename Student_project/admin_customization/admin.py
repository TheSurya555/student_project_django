from django.contrib import admin
from .models import Traffic

@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'page_visited', 'ip_address')
    search_fields = ('user__username', 'page_visited', 'ip_address')
    list_filter = ('timestamp',)
