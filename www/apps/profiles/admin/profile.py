from django.contrib import admin
from ..models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
                'id',
                'user', 
                'filled_in', 
                'tier', 
                'business', 
                'slug', 
                'first_name', 
                'last_name', 
                'gender', 
                'country', 
                'website', 
                'age', 
                'about', 
                'employment_type', 
                'account_status',
                'title',
                'is_freelance',
                'employment_option',
                'work_arrangements',
                'hours_per_week',
                'is_available',
                'availability_date',
                'desired_salary',
                'currency',
                'viewed',
                'bookmarked',
                'posted_jobs',
                'posted_skills',
                'created_at',
                'updated_at',
    )

    search_fields = [
                'id',
                'user__email',
                'business',
                'first_name',
                'last_name', 
                'gender', 
                'country',
                'age', 
                'employment_type',
                'account_status',
    ]

    list_per_page = 25






