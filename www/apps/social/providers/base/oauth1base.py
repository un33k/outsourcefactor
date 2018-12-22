import cgi, json, base64, urllib
import oauth2 as oauth
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, load_backend
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from ...models import SocialAuthProvider

class Oauth1Base(object):
    
    #name - Yahoo, Twitter ... other Oauth1 providers
    name = 'Social1Base'
    
    REQUEST_METHOD_GET = 'GET'
    REQUEST_METHOD_POST = 'POST'
    
    # request we are processing
    request = None
    
    # consumer & client
    consumer = None
    client = None
    
    # required by all oauth1 provider
    app_id = ''
    consumer_key = ''
    consumer_secret = ''
    oauth_callback = ''
    
    # required base url for oauth 1 providers
    request_token_base_url = '' # 
    authenticate_base_url = ''  # 
    access_token_base_url = ''  # 

    request_token_data_format = 'txt'
    access_token_data_format = 'txt'

    # user info (raw)
    user_info = None
    
    def __init__(self, request):
        self.request = request
        self.name = self.name.capitalize()
        self.consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        self.client = oauth.Client(self.consumer)

    # get the base url for the first dialog with the provider 
    def get_request_token_base_url(self):
        return  self.request_token_base_url
    
    # get the base url for the authentication request
    def get_authenticate_base_url(self):
        return  self.authenticate_base_url
    
    # get the base url for the access token request (returns user data here)
    def get_access_token_base_url(self):
        return  self.access_token_base_url

    # which request method does this provider requires for request_token request (get or post)
    def get_request_token_request_method(self):
        return self.REQUEST_METHOD_GET

    # which request method does this provider requires for access_token request (get or post)
    def get_access_token_request_method(self):
        return self.REQUEST_METHOD_GET

    # extract data from response (returns a dict)
    def extract_data_from_response(self, resp, format='json'):
        if format == 'json':
            data = json.loads(resp)
        else:
            data = dict(cgi.parse_qsl(resp))

        return data

    # save the data to later retrieval, storage can be (db, cache, session[default])
    # derived class can override this with their desired storage backend
    def save_data_to_storage(self, key, data):
        self.request.session[key] = data
 
    # get data from storage
    def get_data_from_storage(self, key):
        try:
            data = self.request.session[key]
        except:
            data = None
        return data

    # set new client
    def set_client(self):
        # reterive the request token from storage
        data = self.get_data_from_storage(key='request_token')
        if data:
            # update the client with a new one that knows about the request token
            oauth_token = data['oauth_token']
            oauth_secret = data['oauth_token_secret']
            token = oauth.Token(oauth_token, oauth_secret)
            self.client = oauth.Client(self.consumer, token)
        else:  
            self.client = oauth.Client(self.consumer)

    # get a request token from the provider
    def get_request_token(self, body=''):
        url = self.get_request_token_base_url()
        method = self.get_request_token_request_method()
        if body:
            result, resp = self.client.request(url, method=method, body=body)
        else:
            result, resp = self.client.request(url, method=method)
        
        status = result['status']
        if status != '200':
            return False, resp
        return True, resp

    # get an access token from the provider
    def get_access_token(self, body=''):
        url = self.get_access_token_base_url()
        method = self.get_access_token_request_method()
        if body:
            result, resp = self.client.request(url, method=method, body=body)
        else:
            result, resp = self.client.request(url, method=method)
        status = result['status']
        if status != '200':
            return False, resp
        return True, resp

    # get the user from the provider
    def get_user_info(self):
        msg = ''
        self.user_info = None
        success, resp = self.get_access_token()
        if not success:
            msg = _('[%s] error - access token' % self.name)
        else:
            self.user_info = self.extract_data_from_response(resp, format=self.access_token_data_format)
            if not self.user_info:
                msg = _('[%s] error - no user info' % self.name)
        return success, msg

    # redirect when we fail
    def redirect_on_failure(self, msg=''):
        redirect = settings.LOGIN_URL
        if self.request.user.is_authenticated():
            redirect = reverse('social_provider_list')
        if msg:
            messages.add_message(self.request, messages.INFO, msg)
        return HttpResponseRedirect(redirect)

    # redirect when we fail
    def redirect_on_success(self, msg='', success_url=settings.LOGIN_REDIRECT_URL):
        if msg:
            messages.add_message(self.request, messages.INFO, msg)
        return HttpResponseRedirect(success_url)

    # we have authenticated this user via a social provider, just login'm in
    def socially_login(self, user):
        # use the backend for login from django.contrib.auth
        if not hasattr(user, 'backend'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                if user == load_backend(backend).get_user(user.pk):
                    user.backend = backend
                    break
        if hasattr(user, 'backend'):
            return login(self.request, user)

    # derived class should override this, combo some of user info and base64 it
    def get_uuid(self):
        uuid = base64.encodestring('override me please')
        raise _("get_uuid must be overridden")
        return ''

    # Oauth 1 providers usually don't provide emails, if so, the derived class would know about it
    def get_email(self):
        return ''

    # a locally initiated authentication request was just received, process it
    def initiate_authentication_request(self):
        success, resp = self.get_request_token()
        if success:
            data = self.extract_data_from_response(resp, format=self.request_token_data_format)
            self.save_data_to_storage(key='request_token', data=data) # remember this, need it during the callback
            args ={
                'oauth_token': data['oauth_token'],
            }
            args = urllib.urlencode(args)
            url = self.get_authenticate_base_url()
            return HttpResponseRedirect(url+args) # this should trigger a callback

        else:
            msg = _('[%s] error - request token' % self.name)
            return self.redirect_on_failure(msg)


    # we have requested social authentication and the provider has called us back
    def process_callback(self):
        # refresh the client that is aware of last state
        self.set_client()
        success, msg = self.get_user_info()
        if not success:
            return self.redirect_on_failure(msg) 

        # we got a uuid
        uuid = self.get_uuid()
        email = self.get_email()

        # try to find the provider to login user with
        try:
            sp = SocialAuthProvider.objects.get(name__iexact=self.name, uuid__exact=uuid)
        except SocialAuthProvider.DoesNotExist:
            # no such provider, user must be trying to add it
            sp = SocialAuthProvider()
            sp.name = self.name
            sp.uuid = uuid
            sp.email = email
            sp.is_active = False
        else:
            # provider found, try to login user with
            self.socially_login(sp.user)
            msg = _('you are logged in via %s' % self.name)
            return self.redirect_on_success(msg=msg, success_url=settings.LOGIN_REDIRECT_URL)


        # if user is already authenticated, the they are adding this provider app to their account
        # if user not authenticated, then the are trying to login as they have this provider in their account
        if self.request.user.is_authenticated():
            sp.user = self.request.user
            sp.is_active = True
            sp.save()
            msg = _('%s is now enabled, so from now on, you can login via %s' % (self.name, self.name))
            return self.redirect_on_success(msg=msg, success_url=reverse('social_provider_list'))
        
        # not logged in, so user must be trying to login without having an account or this provider enabled
        msg = _('setup an account or login with password, then enable %s in your account settings for future logins' % self.name)
        return self.redirect_on_failure(msg=msg)




