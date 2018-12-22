import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages

SESSION_IDLE_TIMEOUT = getattr(settings, "SESSION_IDLE_TIMEOUT", 2*60*60)

class SessionIdleTimeout(object):
    """ Middleware class to timeout a session after a specified time period. """
    
    def process_request(self, request):
        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            request.user.last_login = current_datetime - datetime.timedelta(seconds=5)
            request.user.save()
            
            # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity'):
               if (current_datetime - request.session['last_activity']).seconds > SESSION_IDLE_TIMEOUT:
                   messages.add_message(request, messages.ERROR, 'Your session has timed out. Please login again.')
                   logout(request)
            # Set last activity time in current session.
            else:
                request.session['last_activity'] = current_datetime
        return None
