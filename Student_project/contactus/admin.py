from django.contrib import admin
from .models import ConsultingMessage

class ConsultingMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    list_filter = ('created_at',)

admin.site.register(ConsultingMessage, ConsultingMessageAdmin)
