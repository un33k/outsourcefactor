from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from ..forms import PasswordChangeFormPrivate

class ProfileChangePassword(FormView):
    """
    Change password for existing user
    """
    form_class = PasswordChangeFormPrivate
    success_url = reverse_lazy('profile_view_details')
    template_name = 'profiles/profile_account_settings.html'

    def get_form_kwargs(self):
        kwargs = super(ProfileChangePassword, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, _('profile changed'))
        return super(ProfileChangePassword, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileChangePassword, self).dispatch(*args, **kwargs)





