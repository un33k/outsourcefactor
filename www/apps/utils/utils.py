from django.conf import settings
from django.contrib.gis.geoip import GeoIP
import re

# this is not intended to be an all-knowing IP address regex
IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def get_ip_address(request):
    """
    Method of django-tracking plugin
    
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.
    """

    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address).group(0)
        except:
            ip_address = '127.0.0.1'

    return ip_address

def get_country_info(request):
    
    if not 'geoip' in request.session:
        g = GeoIP()
        ip = get_ip_address(request)
        country_info = g.country(ip)
        if settings.DEBUG:
            country_info = g.country('baidu.cn')
        
        if country_info['country_name'] == None or country_info['country_code'] == None:
            country_info = {'country_name':'', 'country_code':'', 'country_alt_name': ''}
    
        JOB_COUNTRIES = getattr(settings, 'JOB_COUNTRIES', [])
        cc = country_info.get('country_code', '')
        if cc and cc.upper() in JOB_COUNTRIES:
            country_info['country_alt_name'] = JOB_COUNTRIES[cc.upper()]
        else:
            country_info['country_alt_name'] = country_info.get('country_name', '')

        request.session['country_info'] = country_info
        request.session['geoip'] = True
    else:
        country_info = request.session['country_info']

    return country_info




