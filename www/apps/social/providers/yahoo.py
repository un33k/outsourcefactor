import base64
from django.utils.translation import ugettext as _
from django.conf import settings
from ..models import SocialAuthProvider
from base.oauth1base import Oauth1Base

class YahooSocialConnect(Oauth1Base):
    name = 'Yahoo'

    # required by all twitter provider
    consumer_key = settings.YAHOO_CONSUMER_KEY
    consumer_secret = settings.YAHOO_CONSUMER_SECRET
    oauth_callback = settings.YAHOO_CALLBACK_URL

    # required base url for oauth 1 providers
    request_token_base_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token?' # send initial request 
    authenticate_base_url = 'https://api.login.yahoo.com/oauth/v2/request_auth?'  # send authentication request
    access_token_base_url = 'https://api.login.yahoo.com/oauth/v2/get_token?'  # send access token request & get user data

    user_info = None

    # which request method does this provider requires for request_token request (get or post)
    def get_request_token_request_method(self):
        return self.REQUEST_METHOD_POST

    # which request method does this provider requires for access_token request (get or post)
    def get_access_token_request_method(self):
        return self.REQUEST_METHOD_POST

    # yahoo requires the callback_url to be passed in
    def get_request_token(self, body=''):
        body = 'oauth_callback='+self.oauth_callback
        return super(YahooSocialConnect, self).get_request_token(body.encode('utf-8'))

    # yahoo requires the oauth_verifier to be passed in
    def get_access_token(self, body=''):
        body = 'oauth_verifier='+self.request.GET['oauth_verifier']
        return super(YahooSocialConnect, self).get_access_token(body.encode('utf-8'))

    # no email, so make something up for now
    def get_email(self):
        return self.get_uuid()+'@'+self.name.lower()+'.com'
        
    # we get an id and username but not an email from yahoo        
    def get_uuid(self):
        userid = self.user_info['xoauth_yahoo_guid']
        uuid = base64.encodestring(self.name+userid)
        return uuid







