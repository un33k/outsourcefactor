from django import template
from django.template import Node, TemplateSyntaxError
from django.utils.translation import ugettext as _
from django.conf import settings
from ..models import SocialAuthProvider, SocialProfileProvider

register = template.Library()

@register.filter
def get_social_providers_for_user(user):
    return SocialAuthProvider.objects.filter(user=user)

@register.filter
def is_social_provider_enabled(name, user):
    try:
        sp = SocialAuthProvider.objects.get(user=user, name__iexact=name)
    except SocialAuthProvider.DoesNotExist:
        return False
    return True

class GetAvailableProviders(Node):
    def __init__(self, context_name):
        self.context_name = context_name

    def render(self, context):
        context[self.context_name] = settings.SOCIAL_PROVIDERS
        return ''
             
@register.tag
def get_available_providers(parser, token):
    """
    Retrieves a list of available social providers
    {% get_available_providers as providers %}
    """
    try:
        bits = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(_('tag requires exactly two arguments'))
    if len(bits) != 3:
        raise TemplateSyntaxError(_('tag requires exactly two arguments'))
    if bits[1] != 'as':
        raise TemplateSyntaxError(_("first argument to tag must be 'as'"))

    return GetAvailableProviders(bits[2])

@register.filter
def get_youtube_video(user):
    try:
        yt = SocialProfileProvider.objects.get(user=user, provider=SocialProfileProvider.SOCIAL_SITE_YOUTUBE)
    except:
        yt = None
    return yt

@register.filter
def get_social_networks(user):
    providers_auth = SocialAuthProvider.objects.filter(user=user)
    social_networks = []
    msg = 'User has a verified %s account'
    for sp in providers_auth:
        social_networks.append({'name':sp.name.capitalize(), 'msg': msg % sp.name})

    msg = 'User has an unverified %s account'
    social_links = SocialProfileProvider.objects.filter(user=user)
    for sl in social_links:
        try:
            name = sl.get_provider_display().split('.')[0]
            for s in social_networks:
                if s.name.capitalize() == name.capitalize():
                    continue
            social_networks.append({'name':name.capitalize(), 'msg': msg % name})
        except:
            pass
    return social_networks






    