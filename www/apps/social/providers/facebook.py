import base64
from django.utils.translation import ugettext as _
from django.conf import settings
from ..models import SocialAuthProvider
from base.oauth2base import Oauth2Base

class FacebookSocialConnect(Oauth2Base):
    name = 'Facebook'

    # required by all provider
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_APP_SECRET
    redirect_uri = settings.FACEBOOK_REDIRECT_URL
    scope = 'email'

    dialog_base_url = 'http://www.facebook.com/dialog/oauth?'
    token_base_url = 'https://graph.facebook.com/oauth/access_token?'
    info_base_url = 'https://graph.facebook.com/me?'

    code = ''
    access_token = ''
    user_info = None
    
    access_token_data_format = 'text' # we get it in raw format
    user_info_data_format = 'json' # we get it in json format

    # facbook requires grant_type
    def get_token_args(self):
        extra_args = {
            'grant_type': 'authorization_code'
        }
        args = super(FacebookSocialConnect, self).get_token_args()
        return dict(args.items() + extra_args.items())

    # we get an email address from facebook
    def get_email(self):
        email = ''
        if self.user_info:
            try:
                email = self.user_info['email']
            except:
                pass
        return email

    # we get an id and username as well as an email from facebook
    def get_uuid(self):
        email = self.get_email()
        uuid = base64.encodestring(self.name+email)
        return uuid







