from django.contrib import admin
from .models import Project, Progress

class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 0  # Adjust the number of empty forms to display

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_name', 'status', 'user', 'display_progress_stages')
    list_filter = ('status',)
    search_fields = ('name', 'client_name')
    inlines = [ProgressInline]

    def display_progress_stages(self, obj):
        return ", ".join([progress.stage for progress in obj.progresses.all()])

    display_progress_stages.short_description = 'Progress Stages'

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('project', 'stage', 'is_completed', 'user')
    list_filter = ('is_completed', 'project__name')
    search_fields = ('stage',)
    