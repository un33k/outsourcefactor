from __future__ import absolute_import

from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from contact_form.views import contact_form
from .forms import WebPortalContactForm

# right out of djangoproject.com's website
urlpatterns = patterns('',
    url(r'^sent/',
       TemplateView.as_view(template_name='contact_form/contact_message_sent.html'),
       name='contact_form_sent'),

    url(
        regex = r'^$',
        view  = contact_form,
        kwargs = dict(
            form_class = WebPortalContactForm,
            template_name = 'contact_form/contact_form.html',
        ),
        name = 'contact_form',)
)
