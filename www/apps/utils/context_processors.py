import time, os, datetime
from django.conf import settings
from django.contrib.sites.models import Site

from . import get_unique_random
from .utils import get_country_info

# pass to template if we are in debug mode
def common(request):
    IS_DEBUG = getattr(settings, "DEBUG", False)
    if IS_DEBUG:
        STATIC_RANDOM_EXTENTION = get_unique_random(20)
    else:
        STATIC_RANDOM_EXTENTION = getattr(settings, "STATIC_RANDOM_EXTENTION", 'asdajd434343asd')

    now = datetime.datetime.now()

    country_info = get_country_info(request)
    
    cxt = {
            'p_debug': IS_DEBUG,
            'p_time': str(time.time()).split('.')[0],
            'p_static_random': STATIC_RANDOM_EXTENTION,
            'p_random': get_unique_random(20),
            'p_year': now.strftime("%Y"),
            'p_month': now.strftime("%m"),
            'p_day': now.strftime("%d"),
            'p_date': now.strftime("%Y-%m-%d"),
            'p_project_name':  getattr(settings, "PROJECT_NAME", 'OutsourceFactor'),
            'p_project_domain': Site.objects.get_current(),
            'p_domain_base': request.build_absolute_uri().replace(request.path, ''),
            'p_site_title': getattr(settings, "SITE_TITLE", ''),
            'p_site_description': getattr(settings, "SITE_DESCRIPTION", ''),
            'p_site_keywords': getattr(settings, "SITE_KEYWORDS", ''),
            'p_country_name': country_info.get('country_name', ''),
            'p_country_code': country_info.get('country_code', ''),
            'p_country_alt_name': country_info.get('country_alt_name', ''),
            'p_job_countries': getattr(settings, 'JOB_COUNTRIES', []), 
            'p_business_countries': getattr(settings, 'BUSINESS_COUNTRIES', []),
            'COMMON_DOWNLOADABLE_STATIC_URL': settings.COMMON_DOWNLOADABLE_STATIC_URL,
          }
    return cxt
