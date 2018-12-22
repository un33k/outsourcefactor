from django.contrib import admin
from models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    
    list_display = (
            'id',
            'user',
            'content_type',
            'object_id',
            'content_object',
            'created_at',
            'updated_at',
    )
    
    search_fields = [
            'id',
            'user',
            'content_type',
            'object_id',
            'content_object'
    ]

    list_per_page = 25

admin.site.register(Bookmark, BookmarkAdmin)