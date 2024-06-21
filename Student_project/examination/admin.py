from django.contrib import admin
from .models import Skill, Question, Test, Answer

class QuestionInline(admin.TabularInline):
    model = Question

class SkillAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class AnswerInline(admin.TabularInline):
    model = Answer

class TestAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['user', 'skill', 'score', 'completed', 'created_at']
    list_filter = ['completed', 'created_at']

admin.site.register(Skill, SkillAdmin)
admin.site.register(Test, TestAdmin)
