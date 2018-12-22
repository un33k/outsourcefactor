from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect 
from ..utils.profile import get_user_profile
from www.apps.utils.utils import get_country_info

class ProfileTypeMiddleware(object):
    """
    Users have to choose a profile type, employee or employer
    """
    
    def process_request(self, request):
        """ User that is authenticated must have chosen to be an empolyer or an employee """
        if request.user.is_authenticated():
            p = get_user_profile(request.user)
            
            # profile already has type, continue
            if p.has_employment_type:
                return

            # profile doesn't have type yet, but is trying to set one, continue
            if request.path == reverse_lazy('profile_type_edit'):
                return

            # user is trying to logout, let it be, continue
            if request.path == reverse_lazy('auth_logout'):
                return
            
            # we need a profile first before can continue, so ask user to set one up now
            messages.add_message (request, messages.INFO, _('choose profile type first'))
            
            # this is the first visit, so try to auto populate their country
            country_info = get_country_info(request)
            country = country_info.get('country_code', '')
            if country:
                p.country = country
                p.save()
            return HttpResponseRedirect(reverse_lazy('profile_type_edit'))
