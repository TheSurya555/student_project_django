from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'user')
    search_fields = ('title', 'author')
    list_filter = ('publication_date', 'user')

admin.site.register(BlogPost, BlogPostAdmin)
