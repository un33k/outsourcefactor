from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from forms import AuthenticationForm

### copied straight from django-registration registration.auth_urls

urlpatterns = patterns('',
    url(r'^login/$',
       auth_views.login,
       {
            'authentication_form': AuthenticationForm,
            'template_name': 'auth/login.html'
       },
       name='auth_login'),
       
    url(r'^logout/$',
       auth_views.logout,
       {'template_name': 'landing/main.html'},
       name='auth_logout'),
       
    url(r'^password/change/$',
       auth_views.password_change,
       {'template_name': 'auth/password_change_form.html'},
       name='auth_password_change'),
       
    url(r'^password/change/done/$',
       auth_views.password_change_done,
       {'template_name': 'profiles/profile_private_view.html'},
       name='auth_password_change_done'),
       
    # a password reset is requested and the form allows an email address input
    url(r'^password/reset/$',
       auth_views.password_reset,
       {
       'template_name': 'auth/password_reset_form.html',
        'email_template_name': 'auth/password_reset_email.txt',
       },
       name='auth_password_reset'),
    
    # an email has been sent to the provided email address with the link to reset password
    url(r'^password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'auth/password_reset_done.html'},
       name='auth_password_reset_done'),
       
    # password reset link has been clicked on, forms allows for a new password and confirmation   
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'auth/password_reset_confirm.html'},
       name='auth_password_reset_confirm'),
       
    # system has changed the password and redirect to this template for the final success message
    url(r'^password/reset/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'auth/password_reset_complete.html'},
       name='auth_password_reset_complete'),
)


