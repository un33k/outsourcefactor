from .main import *

# site that debug version is running on, localhost, or internal ip
SITE_ID = 4

# debug password for admin user
BOOTUP_SUPERUSER_PASSWORD = 'hello'

# individual debugging flags
TEMPLATE_DEBUG = True
DEBUG = True
DEBUG_MAIL_SERVER = True
DEBUG_TOOLBAR = True
DEBUG_COMMAND_EXTENSSION = True
DEBUG_USE_SQLITE3 = True
DEBUG_LOGGING_ONLY = True
DEBUG_LOCAL_EMAIL_SERVER = True
DEBUG_SERVE_STATIC_MEDIA = True  # True during development, False to upload asset to S3
SKIP_CSRF_MIDDLEWARE = False
DEV_IP_ADDRESS = '192.168.211.130'


# quick test of project with sqlite3
if DEBUG_USE_SQLITE3:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': MAIN_DOMAIN_NAME.strip().split(".")[0]+'_db',
        }
    }

# remove CSRF if flag is set
if SKIP_CSRF_MIDDLEWARE:
    MIDDLEWARE_CLASSES = tuple([x for x in list(MIDDLEWARE_CLASSES)
                                  if not x.endswith('CsrfMiddleware')])

# debug toolbar would work on the following "internal" IP address (not production ips)
INTERNAL_IPS = ['127.0.0.1', DEV_IP_ADDRESS,]

# debug toolbar
if DEBUG_TOOLBAR:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        # order matters, so insert the debug toolbar app right after the common middleware
        common_index = MIDDLEWARE_CLASSES.index('django.middleware.common.CommonMiddleware')
        MIDDLEWARE_CLASSES.insert(common_index+1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INSTALLED_APPS.append('debug_toolbar')
        DEBUG_TOOLBAR_CONFIG = {
            'SHOW_TOOLBAR_CALLBACK': lambda req: True,
            'INTERCEPT_REDIRECTS': False,
        }

# debug command extesions (lot of goodies)
if DEBUG_COMMAND_EXTENSSION:
    try:
        import django_extensions
    except ImportError:
        pass
    else:
        INSTALLED_APPS.append('django_extensions')


# debug logging
if DEBUG_LOGGING_ONLY:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': lambda r: not DEBUG
            }
        },
        "formatters": {
            "simple": {"format": "[%(name)s] %(levelname)s: %(message)s"},
            "full": {"format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s"}
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        "handlers": {
            "mail_admins": {
                "level": "WARNING",
                "class": "django.utils.log.AdminEmailHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["console"],
                "level": "ERROR",
                "propagate": False,
            },
            "website": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "aweber": {
                "handlers": ["console"],
                "level": "DEBUG",
            }
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# if we are in debug development mode, then we want to point to our local assets
if DEBUG_SERVE_STATIC_MEDIA:
    # Assets overright
    #######################################
    # URL to the static assets
    STATIC_URL = '/s/'
    # URL to the user uploaded assets
    MEDIA_URL = '/m/'


# # setup S3 AWS_BUCKET_NAME name for django_extensions
# if AWS_STORAGE_BUCKET_NAME and AWS_STORAGE_BUCKET_NAME:
#     AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
            

if DEBUG_LOCAL_EMAIL_SERVER:
    ##### EMAIL STUFF #####
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ####### MAIL SERVER ###########################
    # EMAIL SERVER
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 25
    DEFAULT_FROM_EMAIL = '%s <noreply@%s>' % (PROJECT_NAME, MAIN_DOMAIN_NAME)
    # EMAIL_USE_TLS = True
    # EMAIL_HOST_USER = ""
    # EMAIL_HOST_PASSWORD = ""

# Assets overright
#######################################
# URL to the static assets
STATIC_URL = '/s/'
# URL to the user uploaded assets
MEDIA_URL = '/m/'


INSTALLED_APPS.append('devserver')
DEVSERVER_DEFAULT_ADDR = DEV_IP_ADDRESS
DEVSERVER_DEFAULT_PORT = 8080



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

