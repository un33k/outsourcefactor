# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.contrib.sitemaps import views as sitemap_views
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.views.decorators.cache import cache_page

from www.views.main import *
from www.apps.profiles.views import *
from www.apps.portal.utils.sitemaps import BusinessSitemap, JobseekerSitemap, JobSitemap

admin.autodiscover()

from django.conf.urls.defaults import handler500

def my500Handler(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))

handler500 = my500Handler

# we serve the static media when running django debug server
SERVE_STATIC_MEDIA = getattr(settings, 'SERVE_STATIC_MEDIA', False)

sitemaps = {
    'jobseekers':   JobseekerSitemap,
    'businesses':   BusinessSitemap,
    'jobs':         JobSitemap,
    'flatpages':    FlatPageSitemap,
}

# first thing first, let's take care of the homepage of the website first
urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home_page'),     
    url(r'^philippines/$', PhilippinesView.as_view(), name='ph_page'),     
    url(r'^search/', include('www.apps.portal.urls')),     
)

# admin urls
urlpatterns += patterns('',
    url(r'^admino/', include(admin.site.urls), name="admin_index"),
)

# profiles urls
urlpatterns += patterns('',
    url(r'^profiles/', include('www.apps.profiles.urls')),
)

# auth urls
urlpatterns += patterns('',
    url(r'auth/', include('www.apps.auth.urls')),
)

# signup urls
urlpatterns += patterns('',
    url(r'^signup/', include('www.apps.registration.urls')),
)

# communications
urlpatterns += patterns('',
    url(r'^contact/', include('www.apps.contact.urls')),
)

# files that require special attentions if webserver is not serving them
STATIC_URL = getattr(settings, 'STATIC_URL', '/static/')
urlpatterns += patterns('',
    url(r'^robots\.txt$', PlainTextView.as_view(template_name='robots.txt')),
    url(r'^crossdomain\.xml$', PlainTextView.as_view(template_name='crossdomain.xml')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=STATIC_URL+'img/favicon.ico')),
)

# Specific flatpages urls
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^site/about/$', 'flatpage', {'url': '/site/about/'}, name='about_us'),
    url(r'^site/privacy/$', 'flatpage', {'url': 'site/privacy/'}, name='privacy_policy'),
    url(r'^site/terms/$', 'flatpage', {'url': '/site/terms/'}, name='terms_of_service'),
    url(r'^site/how-it-works/$', 'flatpage', {'url': '/site/how-it-works/'}, name='how_it_works'),
)

# static route
if SERVE_STATIC_MEDIA:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
        url(r'^dynamic/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
    urlpatterns += staticfiles_urlpatterns()

# public facing stuff
#job object (item)
urlpatterns += patterns('',
    url(r'^job/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        EmployerJobPublicView.as_view(),
        name='employer_jobs_public_view'
    ),
    url(r'^business/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        ProfileEmployerDetialPublicView.as_view(),
        name='employer_profile_public_view'
    ),
    url(r'^jobseeker/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        ProfileEmployeeDetialPublicView.as_view(),
        name='employee_profile_public_view'
    ),
)

urlpatterns += patterns('',
    url(r'^sitemap.xml$',
        cache_page(60*60*24)(sitemap_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}
    ),
    
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(60*60*24)(sitemap_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'
    ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^403/$', 'django.views.defaults.permission_denied'),
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', handler500),
    )


# # sitemap and rss urls
# urlpatterns += patterns('',
#     url(r'^sitemap\.xml$', cache_page(sitemap_views.sitemap, 60 * 60 * 6), {'sitemaps': sitemaps}),
# )


