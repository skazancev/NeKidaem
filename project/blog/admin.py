from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date')
    fields = ('user', 'title', 'text')
    search_fields = ('title', )
