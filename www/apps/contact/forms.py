import textwrap
from django import forms
from contact_form.forms import ContactForm
from django.forms import Textarea
from django.conf import settings
from django.utils.translation import ugettext as _
from django.conf import settings

attrs = {'class': 'required'}

class WebPortalContactForm(ContactForm):
    message_subject = forms.CharField(max_length=120, widget=forms.TextInput(attrs=attrs), label=u'Message subject')

    def __init__(self, *args, **kwargs):
        super(WebPortalContactForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['rows'] = 25
        self.fields['name'].label = _("Name")
        self.fields['email'].label = _("Email")
        self.fields['message_subject'].label = _("Message Subject")
        self.fields['body'].label = _("Your Message")
        self.fields.keyOrder = ['name', 'email', 'message_subject', 'body']

    def subject(self):
        project_name = getattr(settings, 'PROJECT_NAME', 'Web')
        from_msg = "[Contact via %s Portal]: " % project_name
        return from_msg + self.cleaned_data["message_subject"]

    def message(self):
        return "From: %(name)s <%(email)s>\n\n%(body)s" % self.cleaned_data





