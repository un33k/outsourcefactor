from django.contrib import admin

class SkillAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'category', 
            'name', 
            'priority',
            'is_active',
            'created_at',
            'updated_at',
    )
    search_fields = [
            'category__name', 
            'name',
    ]
    
    list_per_page = 25


class SkillSetAdmin(admin.ModelAdmin):
    
    list_display = (
            'id',
            'user',
            'skill', 
            'level',
            'detail',
            'created_at',
            'updated_at',
    )
    
    search_fields = [
            'id',
            'user__username',
            'skill__name', 
            'level',
    ]

    list_per_page = 25
