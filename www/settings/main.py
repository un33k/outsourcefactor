# -*- coding: utf-8 -*-
import os, random, string, time, json
from django.utils.hashcompat import sha_constructor
from unipath import FSPath as Path

SERVER_ROOT_DIR = '/srv/www/'


# site object associated with theh project (rememeber: development != production)
SITE_ID = 1
APPEND_SLASH = True

# entrance to this project -- think of it as the front door to a building
ROOT_URLCONF = 'www.urls.main'
LANGUAGE_CODE = 'en-US'
SECRET_KEY = "localz"

SITE_PROTOCOL = 'http'
# Path to the main project containing PROJ_SITE_NAME
#######################################
PROJ_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Path to the template directory(ies)
#######################################
TEMPLATE_DIRS = ['%s' % os.path.abspath(os.path.join(PROJ_ROOT_DIR, 'www', 'templates')),]

# Assets configs
#######################################
# locale directory
LOCALE_PATHS =  os.path.abspath(os.path.join(PROJ_ROOT_DIR, 'locale'))
# asset root
ASSETS_DIR =  os.path.abspath(os.path.join(PROJ_ROOT_DIR, 'asset'))
# Static directories to look at during the development
STATICFILES_DIRS = ['%s' % os.path.abspath(os.path.join(ASSETS_DIR, 'static')),]
# Path to the static directory (collectstatic copies static assets to for deployment)
STATIC_ROOT = os.path.abspath(os.path.join(ASSETS_DIR, 'collect'))
# Path to the dynamic directory for user uploaded data
MEDIA_ROOT = os.path.abspath(os.path.join(ASSETS_DIR, 'upload'))
# URL to the static assets
STATIC_URL = '/s/'
# URL to the user uploaded assets
MEDIA_URL = '/m/'


USE_I18N = False
USE_L10N = False

DEFAULT_FILE_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'www.apps.portal.middleware.Prevent404',
    'www.apps.auth.middleware.SessionIdleTimeout',
    'www.apps.profiles.middleware.ProfileTypeMiddleware',
    
    # last resort, keep last
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages",
    'www.apps.utils.context_processors.common',
    'www.apps.profiles.context_processors.employement_settings',
    'www.apps.social.context_processors.available_providers',
    'www.apps.social.context_processors.enabled_providers',
]

AUTHENTICATION_BACKENDS = [
    'www.apps.auth.backends.ModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'gravatar',
    'registration',
    'aweber',
    'bootup',
    'contact_form',
    'www.contrib.emailmgr',
    'www.apps.aweber',
    'www.apps.utils',
    'www.apps.profiles',
    'www.apps.bookmark',
    'www.apps.social',
    'www.apps.portal',
]

try:
    import south
    INSTALLED_APPS.append('south')
    SOUTH_TESTS_MIGRATE = False
except:
    pass

try:
    import rosetta
    INSTALLED_APPS.append('rosetta')
except:
    pass

# logout after 1 hour of inactivity
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_IDLE_TIMEOUT = 5*60*60 # X hours

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# django-profiles
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 4

# Account activities
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'

LANGUAGES = []

SERVICE_PROVIDERS =  []

PASSWORD_MINIMUM_LENGHT = 6

# email management template director is shared with profile directory
EMAIL_MGR_TEMPLATE_PATH = "profiles"

# social provider template directory for the provider listing
SOCIAL_PROVIDERS_TEMPLATE_PATH = "profiles"

# ignore few request by robots
import re
IGNORABLE_404_URLS = (
    re.compile(r'^/blog/'),
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'^/beta/'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

# a unique per project-load number to be used as css and js extentions
STATIC_RANDOM_EXTENTION = None
if not STATIC_RANDOM_EXTENTION:
    length = 20
    randtime = str(time.time()).split('.')[0]
    rand = ''.join([random.choice(randtime+string.letters+string.digits) for i in range(length)])
    STATIC_RANDOM_EXTENTION = sha_constructor(rand).hexdigest()[:length]

JOB_COUNTRIES = {
    'PH': 'the Philippines',
    'PK': 'Pakistan',
    'IN': 'India',
    'BD': 'Bangladesh',
    'ID': 'Indonesia',
    'CN': 'China',
    'IR': 'Iran',
}

BUSINESS_COUNTRIES = {
    'US': 'United States',
    'CA': 'Canada',
    'AU': 'Australia',
    'NZ': 'New Zealand',
    'GB': 'United Kingdom',
}

# allow social settings
try:
    from .social import *
except ImportError:
    pass

# allow per user extra setting overwrite
try:
    from .private import *
except ImportError:
    pass




