import base64
from django.utils.translation import ugettext as _
from django.conf import settings
from ..models import SocialAuthProvider
from base.oauth2base import Oauth2Base

class GoogleSocialConnect(Oauth2Base):
    name = 'Google'

    # required by all provider
    client_id = settings.GOOGLE_APP_ID
    client_secret = settings.GOOGLE_APP_SECRET
    redirect_uri = settings.GOOGLE_REDIRECT_URL
    scope = 'https://www.googleapis.com/auth/userinfo#email'

    dialog_base_url = 'https://accounts.google.com/o/oauth2/auth?'
    token_base_url = 'https://accounts.google.com/o/oauth2/token?'
    info_base_url = 'https://www.googleapis.com/userinfo/email?'

    code = ''
    access_token = ''
    user_info = None
    
    access_token_data_format = 'json' # we get it in json format
    user_info_data_format = 'json' # we get it in json format
    
    # google requires response_type
    def get_dialog_arg(self):
        extra_args = {
            'response_type': 'code'
        }
        args = super(GoogleSocialConnect, self).get_dialog_arg()
        return dict(args.items() + extra_args.items())

    # google requires grant_type
    def get_token_args(self):
        extra_args = {
            'grant_type': 'authorization_code'
        }
        args = super(GoogleSocialConnect, self).get_token_args()
        return dict(args.items() + extra_args.items())

    # google requires alt
    def get_info_args(self):
        extra_args = {
            'alt': 'json'
        }
        args = super(GoogleSocialConnect, self).get_info_args()
        return dict(args.items() + extra_args.items())

    # we get an email address from google
    def get_email(self):
        email = ''
        if self.user_info:
            try:
                email = self.user_info['data']['email']
            except:
                pass
        return email

    # we get an email address from google, should be unique enough for a uuid
    def get_uuid(self):
        email = self.get_email()
        uuid = base64.encodestring(self.name+email)
        return uuid




