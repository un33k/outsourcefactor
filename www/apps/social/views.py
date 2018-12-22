from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseNotAllowed

from models import SocialAuthProvider, SocialProfileProvider
from forms import SocialProfileProviderForm
from utils import get_provider_class, get_template, get_social_profile_provider_list


class SocialAuthProviderDisableView(TemplateView):
    """ Disable a social auth provider for an authenticated user """

    # don't allow get
    def get(self, request, provider):
        return HttpResponseNotAllowed('Method Not Allowed')
        
    def post(self, request, provider):
        try:
            p = SocialAuthProvider.objects.get(name__iexact=provider, user=request.user)
        except:
            messages.add_message(request, messages.INFO, _("no such social provider"))
        else:
            p.delete()
            messages.add_message(request, messages.INFO, _("social provider disabled"))
        return HttpResponseRedirect(reverse_lazy('social_provider_list'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SocialAuthProviderDisableView, self).dispatch(*args, **kwargs)

class SocialAuthProviderEnableView(TemplateView):
    """ Enable a social auth provider for an authenticated user """

    # don't allow get
    def get(self, request, provider):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, provider):
        # import pdb; pdb.set_trace()
        try:
            ProviderClass = get_provider_class(provider)
            sp = ProviderClass(request)
        except:
            messages.add_message(request, messages.INFO, _("failed or unsupported social provider"))
            return HttpResponseRedirect(reverse_lazy('social_provider_list'))

        # redirect to the provider to authenticaion, we will get a callback which is handles elsewhere
        return sp.initiate_authentication_request()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SocialAuthProviderEnableView, self).dispatch(*args, **kwargs)

class SocialAuthProviderLoginView(TemplateView):
    """ Login a user via a social provider """

    # don't allow get
    def get(self, request, provider):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, provider):
        # authenticated users will redirect to home, without further action
        if self.request.user.is_authenticated():
            redirect = getattr(settings, settings.LOGIN_REDIRECT_URL, '/')
            messages.add_message(request, messages.INFO, _("already logged in"))
            return HttpResponseRedirect(redirect)

        try:
            ProviderClass = get_provider_class(provider)
            sp = ProviderClass(request)
        except:
            messages.add_message(request, messages.INFO, _("failed or unsupported social provider"))
            redirect = getattr(settings, settings.LOGIN_URL, '/')
            return HttpResponseRedirect(redirect)

        # redirect to the provider to authenticaion, we will get a callback which is handles elsewhere
        return sp.initiate_authentication_request()

class SocialAuthProviderCallbackView(TemplateView):
    """ This is a callback to our initial request """

    def get(self, request, provider):
        try:
            ProviderClass = get_provider_class(provider)
            sp = ProviderClass(request)
        except:
            messages.add_message(request, messages.INFO, _("invalid provider, try again"))
            redirect = getattr(settings, settings.LOGIN_URL, '/')
            return HttpResponseRedirect(redirect)

        # authenticated users who have already enabled this provider redirect to home, without further action
        if request.user.is_authenticated():
            try:
                sp.objects.get(user=request.user)
            except:
                pass
            else:
                redirect = getattr(settings, settings.LOGIN_REDIRECT_URL, '/')
                messages.add_message(request, messages.INFO, _("already logged in"))
                return HttpResponseRedirect(redirect)

        # process the callback
        return sp.process_callback()


class SocialProfileProviderDeleteView(DeleteView):
    """ Delete a social link """
    model = SocialProfileProvider
    success_url = reverse_lazy('social_provider_list')
    template_name = 'profiles/social_provider_list.html'

    def get_object(self, queryset=None):
        """ ensure object is owned by request.user. """
        obj = super(SocialProfileProviderDeleteView, self).get_object()
        if not obj.user == self.request.user:
            messages.add_message(self.request, messages.INFO, _("social profile provider not found"))
            raise Http404
        
        self.request.user.get_profile().save()
        messages.add_message(self.request, messages.INFO, _("social profile provider deleted"))
        return obj
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SocialProfileProviderDeleteView, self).dispatch(*args, **kwargs)

class SocialProviderAddListView(CreateView):
    """ 
        List all enabled/disabled social auth providers for an authenticated user
        List all social profile providers, allow add / delete
    """
    form_class = SocialProfileProviderForm
    success_url = reverse_lazy('social_provider_list')
    template_name = 'profiles/social_provider_list.html'

    # we need the request in the form, pass it in
    def get_form_kwargs(self):
        kwargs = super(SocialProviderAddListView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        self.request.user.get_profile().save()
        messages.add_message(self.request, messages.INFO, _('social profile provider added'))
        return super(SocialProviderAddListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SocialProviderAddListView, self).get_context_data(**kwargs)
        context['social_profile_providers'] = get_social_profile_provider_list(self.request.user.get_profile())
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SocialProviderAddListView, self).dispatch(*args, **kwargs)

