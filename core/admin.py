from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'title',
        'content',
        'author',
        'created_at'
    ]
    list_filter = [
        'created_at',
    ]



