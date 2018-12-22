from urlparse import urlparse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from models import SocialAuthProvider, SocialProfileProvider
from providers import *

# get all enabled providers for this user
def get_provider_list(user):
    return SocialAuthProvider.objects.filter(user=user).order_by('name', 'uuid', 'is_active')

# get the class name for this provider
def get_provider_class(provider_name=""):
    classname = '%sSocialConnect' % provider_name.capitalize()
    return globals()[classname]

# given a template name, return its path
def get_template(name):
    import os
    return os.path.join(getattr(settings, "SOCIAL_PROVIDERS_TEMPLATE_PATH", "social"), name)

def get_social_profile_provider_list(profile):
    """  """
    sp = None
    sp = SocialProfileProvider.objects.filter(user=profile.user).order_by('provider', 'website',)
    return sp

def clean_youtube_video_arg(link):
    # http://www.youtube.com/watch?v=x3jHnX5KoDw&feature=g-feat&context=G2681172YFAAAAAAAAAg
    # v = x3jHnX5KoDw
    try:
        from urlparse import parse_qs
    except ImportError:
        from cgi import parse_qs

    url_data = urlparse(link)
    query = parse_qs(url_data.query)
    try:
        video = query["v"][0].strip()
    except:
        video = ''

    return video
    