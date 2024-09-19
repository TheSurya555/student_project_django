from django.contrib import admin
from .models import *

class ConsultingMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    list_filter = ('created_at',)

admin.site.register(ConsultingMessage, ConsultingMessageAdmin)

@admin.register(SupportInfo)
class SupportInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'address')
    search_fields = ('title', 'email')