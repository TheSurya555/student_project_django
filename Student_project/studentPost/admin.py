from django.contrib import admin
from .models import BlogPost, BlogImage

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1  # Number of empty forms to display for adding images

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'user')
    search_fields = ('title', 'author')
    list_filter = ('publication_date', 'user')
    ordering = ('-publication_date',)
    inlines = [BlogImageInline]  # Add the inline for BlogImage

    def author(self, obj):
        return obj.user.username if obj.user else 'No Author'

    author.admin_order_field = 'user'

admin.site.register(BlogPost, BlogPostAdmin)
