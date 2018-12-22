import cgi, urllib, urllib2, json, base64
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, load_backend
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings

from ...models import SocialAuthProvider

class Oauth2Base(object):

    #name - Facebook, Google ... other Oauth2 providers
    name = 'Social2Base'

    # request we are processing
    request = None

    REQUEST_METHOD_GET = 'get'
    REQUEST_METHOD_POST = 'post'

    # required by all oauth2 provider
    client_id = ''
    redirect_uri = ''
    client_secret = ''
    scope = ''

    # provider specific (e.g. required by google)
    response_type = ''
    grant_type = ''
    alt = ''

    dialog_base_url = '' # call to this url + arg will initiate a auth dialog
    token_base_url = ''  # call to this url + arg will request an access token
    info_base_url = ''  # call to this url + arg will request user info

    code = ''
    access_token = ''
    user_info = None

    access_token_data_format = 'json' # format of retrieved access token, (json, or txt)
    user_info_data_format = 'json' # format of retrieved user info, (json, or txt)

    def __init__(self, request):
        self.request = request
        self.name = self.name.capitalize()

    # get the base url for the first dialog with the provider
    def get_dialog_url(self):
        return  self.dialog_base_url

    # get the base url for the access token request
    def get_tocken_url(self):
        return  self.token_base_url

    # get the base url for the data request
    def get_info_url(self):
        return  self.info_base_url


    # get the required args for a dialog with the provider
    def get_dialog_arg(self):
        args =  {
            'client_id':    self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope':        self.scope
        }
        return args

    # get the required args for a token request
    def get_token_args(self):
        args =  {
            'client_id':        self.client_id,
            'client_secret':    self.client_secret,
            'redirect_uri':     self.redirect_uri,
            'code':             self.code
        }
        return  args

    # get the required args for a user info request
    def get_info_args(self):
        args =  {
            'access_token':     self.access_token
        }
        return  args

    # prepare a request
    def build_request(self, req_type='token', req_method=REQUEST_METHOD_GET):
        if req_type == 'token':
            url = self.get_tocken_url()
            args = self.get_token_args()
        else: # must be a user_info request
            url = self.get_info_url()
            args = self.get_info_args()

        args = urllib.urlencode(args)
        if req_method == self.REQUEST_METHOD_POST:
            req = urllib2.Request(url, data=args)
        else:
            req = urllib2.Request(url+args)
        return req

    # make a request and return the response
    def make_request_return_response(self, req):
        try:
            resp = urllib2.urlopen(req)
        except urllib2.URLError, e:
            resp = e
            return False, resp
        return True, resp

    # extract data from response (returns a dict)
    def extract_data_from_response(self, resp, format='json'):
        if format == 'json' or format == 'text':
            data = json.loads(resp.read())
        else:
            data = dict(cgi.parse_qsl(resp.read()))

        return data

    # extract code from callback (return string)
    def extract_code_from_callback(self):
        self.code = ''
        msg = ''
        success = True
        try:
            self.code = self.request.GET['code']
        except:
            msg = _('[%s] authentication failed (!code)' % self.name)

        if not self.code or msg:
            success = False

        return success, msg

    # which request method does this provider requires for access_token request (get or post)
    def get_access_token_request_method(self):
        return self.REQUEST_METHOD_POST

    # which request method does this provider requires for user info request (get or post)
    def get_user_info_request_method(self):
        return self.REQUEST_METHOD_GET

    # get a response for an access token request
    def get_response_for_access_token_request(self):
        req_method = self.get_access_token_request_method()
        req = self.build_request(req_type='token', req_method=req_method)
        success, resp = self.make_request_return_response(req)
        return success, resp

    # get a response for a user data request
    def get_response_for_user_info_request(self):
        req_method = self.get_user_info_request_method()
        req = self.build_request(req_type='user_info', req_method=req_method)
        success, resp = self.make_request_return_response(req)
        return success, resp

    # we are processing a locally initiated social authentication request
    # we are initiating a dialog with the social provider in question
    def initiate_authentication_request(self):
        url = self.get_dialog_url()
        args = self.get_dialog_arg()
        args = urllib.urlencode(args)
        return HttpResponseRedirect(url+args)

    # we are processing the callback from the provider, we need an access token
    # send the access token request to the provider
    def get_access_token(self):
        msg = ''
        self.access_token = ''
        success, resp = self.get_response_for_access_token_request()
        if not success:
            msg = _('[%s] error - access token - (%s)' % (self.name, resp.code))
        else:
            data = self.extract_data_from_response(resp, format=self.access_token_data_format)
            self.access_token = data['access_token']
            if not self.access_token:
                msg = _('[%s] error - empty access token' % self.name)
        return success, msg

    # we are processing the callback from the provider, have an access token already
    # send the access token back and request user data which may be provider specific
    def get_user_info(self):
        msg = ''
        self.user_info = None
        success, resp = self.get_response_for_user_info_request()
        if not success:
            msg = _('[%s] error - user info - (%s) %s' % (self.name, resp.code))
        else:
            self.user_info = self.extract_data_from_response(resp, format=self.user_info_data_format)
            if not self.user_info:
                msg = _('[%s] error - no user info' % self.name)
                success = False
        return success, msg

    # derived class should override this, combo some of user info and base64 it
    def get_uuid(self):
        uuid = base64.encodestring('override me please')
        raise _("get_uuid must be overridden")
        return ''

    # we have the user info, see if we can extract and email address, derived class has to override
    def get_email(self):
        return ''

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


    # we have requested social authentication and the provider has called us back
    def process_callback(self):

        # we called, now called back with a code, go and extract the code (self.code)
        success, msg = self.extract_code_from_callback()
        if not success:
            return self.redirect_on_failure(msg=msg)

        # exchange the code for an access token
        success, msg = self.get_access_token()
        if not success:
            return self.redirect_on_failure(msg=msg)

        # exchange the access token for the user info
        success, msg = self.get_user_info()
        if not success:
            return self.redirect_on_failure(msg=msg)

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




