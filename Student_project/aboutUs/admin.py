from django.contrib import admin
from .models import AboutUsContent, Feature, TeamMember

class FeatureInline(admin.StackedInline):
    model = Feature
    extra = 1

class TeamMemberInline(admin.StackedInline):
    model = TeamMember
    extra = 1

@admin.register(AboutUsContent)
class AboutUsContentAdmin(admin.ModelAdmin):
    inlines = [FeatureInline, TeamMemberInline]
    list_display = ('title', 'created_at', 'updated_at')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'about_us')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'about_us','linkedin_url')
