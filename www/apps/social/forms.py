from django import forms
from urlparse import urlparse
from django.utils.translation import ugettext_lazy as _
from models import SocialProfileProvider
from utils import *

class SocialProfileProviderForm(forms.ModelForm):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(SocialProfileProviderForm, self).__init__(*args, **kwargs)

    youtube_link = 'http://www.youtube.com/watch?v='
    
    class Meta:
        model = SocialProfileProvider
        exclude = ('user',)

    def clean_provider(self):
        provider = self.cleaned_data.get('provider')
        try:
            sp = SocialProfileProvider.objects.get(user=self.request.user, provider=provider)
        except:
            pass
        else:
            raise forms.ValidationError(_("The provider is already in your list, choose a new one"))
        return provider

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if len(website) < 5:
            raise forms.ValidationError(_("Website too short! minimum length is ")+" [%d]" % 5)
        
        #make sure domain name in website matches the providers domain name
        provider = self.clean_provider()
        if not provider:
            return website
            
        try:
            d = '.'.join(urlparse(website).netloc.split('.')[-2:]).lower()
            p = SocialProfileProvider.SOCIAL_SITE_CHOICES[provider-1][1].lower()
            if d not in p:
                raise forms.ValidationError(_("The link must be from [%s]" % p))
        except IndexError:
            raise forms.ValidationError(_("Invalid link. please verify the link and try again."))
        
        # handle youtube videos
        if p == SocialProfileProvider.SOCIAL_SITE_CHOICES[SocialProfileProvider.SOCIAL_SITE_YOUTUBE-1][1].lower():
            v_arg = clean_youtube_video_arg(website)
            if not v_arg:
                raise forms.ValidationError(_("Invalid youtube link format. Try this format: [youtube.com/watch?v=60zHFpmCXTQ]"))
            website = self.youtube_link+v_arg

        # now make sure we don't have the link already
        try:
            sp = SocialProfileProvider.objects.get(user=self.request.user, website=website)
        except:
            pass
        else:
            raise forms.ValidationError(_("The link already associated with another provider in your list"))
        
        return website