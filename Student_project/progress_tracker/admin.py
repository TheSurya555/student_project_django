from django.contrib import admin
from .models import Project, Progress
from notifications.signals import notify
from django.utils.translation import gettext_lazy as _

class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 0  # Adjust the number of empty forms to display

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'client_name', 'status', 'user', 'display_progress_stages')
    list_filter = ('status',)
    search_fields = ('project_name', 'client_name')
    inlines = [ProgressInline]

    def display_progress_stages(self, obj):
        return ", ".join([progress.stage for progress in obj.progresses.all()])

    display_progress_stages.short_description = 'Progress Stages'

    def save_model(self, request, obj, form, change):
        # Save the project instance
        super().save_model(request, obj, form, change)

        # Send notifications
        recruiter = obj.client  # Assuming this is a User instance
        candidate = obj.user  # Assuming this is a User instance

        if recruiter:
            notify.send(
                sender=request.user,
                recipient=recruiter,
                verb=_("Your project '{0}' has been assigned to candidate: {1}").format(obj.project_name, candidate.username),
                description="The candidate will be responsible for executing specific tasks within the project. Please collaborate closely to ensure all objectives are met.",
                target=obj
            )

        if candidate:
            notify.send(
                sender=request.user,
                recipient=candidate,
                verb=_("You have been assigned a new project: {0}").format(obj.project_name),
                description="Your role is critical in achieving the project's goals. Please review the project tasks and communicate with the recruiter to align on expectations and deadlines.",
                target=obj
            )

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('project', 'stage', 'is_completed', 'user')
    list_filter = ('is_completed', 'project__project_name')
    search_fields = ('stage',)
