from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm

class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = _("Please enter username or email address.")
    username = forms.CharField(
            label=_("Username or Email"), 
            max_length=150,
            help_text = 'Enter your username or the email address associated with your account.'
    )

