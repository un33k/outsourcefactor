from django.conf import settings

# what are the available social auth providers (get from settings)
def available_providers(request):
    cxt = {
        'available_providers': getattr(settings, 'SOCIAL_PROVIDERS', []),
    }
    return cxt

# what are the available social auth providers (get from settings)
def enabled_providers(request):
    from models import SocialAuthProvider
    enabled_providers = []
    if request.user.is_authenticated():
        enabled_providers = SocialAuthProvider.objects.filter(user=request.user)
    
    cxt = {
        'enabled_providersz': enabled_providers
    }
    return cxt
