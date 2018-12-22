from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.utils.translation import ugettext as _


class PasswordChangeFormPrivate(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1', '')
        password2 = self.cleaned_data.get('new_password2', '')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        
        min_len = getattr(settings, "PASSWORD_MINIMUM_LENGHT", 6)
        if len(password1) < min_len:
            raise forms.ValidationError(_("Password too short! minimum length is ")+" [%d]" % min_len)

        return password2


