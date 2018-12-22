from django.contrib import admin
from models import SocialAuthProvider, SocialProfileProvider

class SocialAuthProviderAdmin(admin.ModelAdmin):
    
    list_display = (
            'id',
            'user',
            'name',
            'email',
            'uuid',
            'is_active',
            'created_at',
            'updated_at',
    )
    
    search_fields = [
            'id',
            'user',
            'name',
            'email'
    ]

    list_per_page = 25

admin.site.register(SocialAuthProvider, SocialAuthProviderAdmin)

class SocialProfileProviderAdmin(admin.ModelAdmin):

    list_display = (
            'id',
            'user', 
            'provider', 
            'website',
            'created_at',
            'updated_at',
    )

    search_fields = [
                'id',
                'user__email',
                'provider',
                'website',
    ]

    list_per_page = 25



admin.site.register(SocialProfileProvider, SocialProfileProviderAdmin)
