from django.contrib import admin

class JobPostAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user', 
            'title',
            'slug',
            'employment_option',
            'wage_salary',
            'start_date',
            'bookmarked',
            'bookmarked',
            'is_active',
            'keywords',
            'created_at',
            'updated_at',
    )

    search_fields = [
            'id',
            'user__username', 
            'employment_option', 
            'start_date', 
            'is_active',
            'keywords',
    ]

    list_per_page = 25

