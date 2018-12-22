# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.conf import settings
from registration.views import activate
from registration.views import register
from .forms import RegistrationForm

### Stright from django-registration default backend, with two modificaitons
### A. RegistrationFormUniqueEmail is given to the backend via register
### B. Remove the registration.auth_urls as it is handled directly

urlpatterns = patterns('',
    url(r'^activated/$',
       TemplateView.as_view(template_name='registration/activated.html'),
       name='registration_activation_complete'),
       
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
       activate,
       {
       'template_name': 'registration/activation_failed.html',
       'backend': 'registration.backends.default.DefaultBackend',
       'extra_context':{'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS},
       },
       name='registration_activate'),
    
    url(r'^activation/sent/$',
       TemplateView.as_view(template_name='registration/activation_sent.html'),
       name='registration_complete'),
    
    url(r'^closed/$',
       TemplateView.as_view(template_name='registration/activation_expired.html'),
       name='registration_disallowed'),
    
    url(r'^$',
        register,
        {
        'template_name': 'registration/account_setup_form.html',
        'backend': 'registration.backends.default.DefaultBackend',
        'form_class': RegistrationForm,
        'extra_context':{'account_setup_button': 'Create an account'},
        },
        name='registration_register'),

)

