from django.contrib import messages
from django.http import HttpResponsePermanentRedirect

KEYWORDS_FILTER = "undefined cache" 

class Prevent404(object):
    """ Middleware class to redirect to the referrer page if it is a bogus 404 caused by bots. """
    
    def process_request(self, request):
        try:
            url = request.META['HTTP_REFERER']
        except:
            url = request.build_absolute_uri().replace(request.path, '') # this is human
        
        keywords = KEYWORDS_FILTER.split(' ')
        for word in keywords:
            if word in request.path:
                # bogus word, redirect to referrer if its from our site, else send to main page
                messages.add_message(request, messages.ERROR, 'Invalid operation. Please try again!')
                return HttpResponsePermanentRedirect(url)

        return None
