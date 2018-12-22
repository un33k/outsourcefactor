# -*- coding: utf-8 -*-
from registration.forms import RegistrationFormUniqueEmail
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

MIN_PASS_LEN = getattr(settings, "PASSWORD_MINIMUM_LENGHT", 6)

class RegistrationForm(RegistrationFormUniqueEmail):
    def __init__(self, *args, **kwargs):
        super(RegistrationFormUniqueEmail, self).__init__(*args, **kwargs)
        self.fields['email'].label = _("Email")
        self.fields['email'].help_text = _("A valid email address. Your activation link will be sent to this address. (please avoid typos)")
        self.fields['password2'].label = _("Confirm password")
        self.fields['password1'].help_text = _("Please choose a strong password. (minimum %d characters)" % MIN_PASS_LEN)
        
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        
        if len(password2) < MIN_PASS_LEN:
            raise forms.ValidationError(_("Password too short! minimum length is ")+" [%d]" % MIN_PASS_LEN)

        return password2

        