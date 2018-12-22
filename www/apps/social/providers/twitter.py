import base64
from django.utils.translation import ugettext as _
from django.conf import settings
from ..models import SocialAuthProvider
from base.oauth1base import Oauth1Base

class TwitterSocialConnect(Oauth1Base):
    name = 'Twitter'

    # required by all twitter provider
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET

    # required base url for oauth 1 providers
    request_token_base_url = 'https://api.twitter.com/oauth/request_token?' # send initial request 
    authenticate_base_url = 'https://api.twitter.com/oauth/authenticate?'  # send authentication request
    access_token_base_url = 'https://api.twitter.com/oauth/access_token?'  # send access token request & get user data

    user_info = None

    def get_email(self):
        username = self.user_info['screen_name']
        return username+'@'+self.name.lower()+'.com'
        
    # we get an id and username but not an email from twitter
    def get_uuid(self):
        userid = self.user_info['user_id']
        username = self.user_info['screen_name']
        uuid = base64.encodestring(self.name+userid+username)
        return uuid







