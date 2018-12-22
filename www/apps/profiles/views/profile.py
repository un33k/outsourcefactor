# coding: utf-8
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, TemplateView, UpdateView
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseNotAllowed, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import simplejson

from www.apps.utils import *
from ..models import UserProfile
from ..forms import *
from ..utils.profile import *
from ..utils.skill import *
from ..utils.job import *
from ..utils.currency import get_to_usd_text

class ProfileDeleteAccountView(DeleteView):
    """ Delete a User Profile """
    model = User
    success_url = reverse_lazy('auth_login')

    def get_object(self, queryset=None):
        """ ensure object is the same as the request.user. """
        obj = super(ProfileDeleteAccountView, self).get_object()
        if not obj == self.request.user:
            messages.add_message(self.request, messages.INFO, _("user account not found"))
            raise Http404
        
        messages.add_message(self.request, messages.INFO, _("your account was deleted!"))
        invalidate_profile_related_cache()
        return obj
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDeleteAccountView, self).dispatch(*args, **kwargs)

class ProfileDetialView(TemplateView):
    template_name = "profiles/profile_private_view.html"

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetialView, self).get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'], context['profile_dict'] = get_user_profile_and_dict_private(profile)
        context['contacts'] = get_user_contact_dict(profile)
        context['employment'], context['employment_dict'] = get_employment_profile_and_dict_private(profile)
        context['skills'] = get_employee_skill(profile)
        context['jobs'] = get_employer_jobpost(profile)
        context['this_user'] = profile.user
        if profile.is_publicly_viewable:
            msg = _('your profile is public and viewable by others')
        elif profile.is_enabled:
            msg = _('your profile is enabled, yet incomplete, therefore it cannot be seen by others')
        else:
            msg = _('your profile is disabled and incomplete, therefore it cannot be seen by others')
        messages.add_message (self.request, messages.INFO, msg)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetialView, self).dispatch(*args, **kwargs)

class ProfileUpdateView(UpdateView):
    """ Profile is already there, just update it """
    model = UserProfile
    template_name = "profiles/profile_edit_details.html"
    success_url = reverse_lazy('profile_edit_details')

    def get_form_class(self):
        profile = get_user_profile(self.request.user)
        if profile.is_employer:
            return UserProfileCommonEmployerForm
        else:
            return UserProfileCommonEmployeeForm

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message (self.request, messages.INFO, _('profile saved'))
        return HttpResponseRedirect(self.get_success_url())
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(*args, **kwargs)


class ProfileEmployeeUpdateView(UpdateView):
    """ Employee specific info in user profile, just update it """
    form_class = UserProfileEmployementEmployeeForm
    template_name = "profiles/employee_profile_edit_details.html"
    success_url = reverse_lazy('employee_profile_edit_details')

    def get_object(self, queryset=None):
        """Get or create an profile here"""
        profile = get_user_profile(self.request.user)
        return profile

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message (self.request, messages.INFO, _('employee profile saved'))
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEmployeeUpdateView, self).dispatch(*args, **kwargs)

class ProfileTypeUpdateView(UpdateView):
    """ Profile is already there, just update the employement type """
    model = UserProfile
    template_name = "profiles/employment_type_form.html"
    success_url = reverse_lazy('profile_edit_details')

    def get_form_class(self):
        return UserProfileTypeSelectForm

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message (self.request, messages.INFO, _('please complete your profile'))
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileTypeUpdateView, self).dispatch(*args, **kwargs)

class ProfileEmployerDetialPublicView(TemplateView):
    template_name = "portal/employer_object_public_view.html"

    def get_object(self, queryset=None):
        """ get profile of the requested profile, not the users own """
        pk = self.kwargs['pk'].strip()
        profile = get_object_or_404(UserProfile, id=pk)
        return profile

    def get_context_data(self, **kwargs):
        context = super(ProfileEmployerDetialPublicView, self).get_context_data(**kwargs)
        profile = self.get_object()
        if not profile.is_employer or not profile.is_enabled:
            if profile.user != self.request.user: # users can always see their own profile
                raise Http404
        context['profile'], context['profile_dict'] = get_user_profile_and_dict_public(profile)
        context['contacts'] = get_user_contact_dict(profile)
        context['jobs'] = get_employer_jobpost_public_view(profile)
        context['is_public_view'] = True
        context['this_user'] = profile.user
        
        if self.request.user == profile.user:
            if profile.is_publicly_viewable:
                msg = _('your profile is public and viewable by others')
            elif profile.is_enabled:
                msg = _('your profile is enabled, yet incomplete, therefore it cannot be seen by others')
            else:
                msg = _('your profile is hidden and/or incomplete, therefore it cannot be seen by others')
            messages.add_message (self.request, messages.INFO, msg)
        else:
            if not profile.is_publicly_viewable:
                raise Http404
            pkey = 'employer-viewed'+str(profile.id)
            try:
                s = self.request.session[pkey]
            except:
                profile.just_viewed()
                self.request.session[pkey] = True
        return context

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        slug = self.kwargs['slug'].strip()
        if profile.slug != slug: # slug has changed, redirect to new link
            return HttpResponsePermanentRedirect(profile.get_absolute_url())
        return super(ProfileEmployerDetialPublicView, self).get(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super(ProfileEmployerDetialPublicView, self).dispatch(*args, **kwargs)

class ProfileEmployeeDetialPublicView(TemplateView):
    template_name = "portal/employee_object_public_view.html"

    def get_object(self, queryset=None):
        """ get profile of the requested profile, not the users own """
        pk = self.kwargs['pk'].strip()
        profile = get_object_or_404(UserProfile, id=pk)
        return profile

    def get_context_data(self, **kwargs):
        context = super(ProfileEmployeeDetialPublicView, self).get_context_data(**kwargs)
        profile = self.get_object()
        if not profile.is_employee or not profile.is_enabled:
            if profile.user != self.request.user: # users can always see their own profile
                raise Http404
        context['profile'], context['profile_dict'] = get_user_profile_and_dict_public(profile)
        context['contacts'] = get_user_contact_dict(profile)
        context['employment'], context['employment_dict'] = get_employment_profile_and_dict_public(profile)
        context['skills'] = get_employee_skill_public_view(profile)
        context['is_public_view'] = True
        context['this_user'] = profile.user

        if self.request.user == profile.user:
            if profile.is_publicly_viewable:
                msg = _('your profile is public and viewable by others')
            elif profile.is_enabled:
                msg = _('your profile is enabled yet incomplete, therefore it cannot be seen by others')
            else:
                msg = _('your profile is hidden and/or incomplete, therefore it cannot be seen by others')
            messages.add_message (self.request, messages.INFO, msg)
        else:
            if not profile.is_publicly_viewable:
                raise Http404
            pkey = 'jobseeker-viewed'+str(profile.id)
            try:
                s = self.request.session[pkey]
            except:
                profile.just_viewed()
                self.request.session[pkey] = True
        return context

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        slug = self.kwargs['slug'].strip()
        if profile.slug != slug: # slug has changed, redirect to new link
            return HttpResponsePermanentRedirect(profile.get_absolute_url())
        return super(ProfileEmployeeDetialPublicView, self).get(request, *args, **kwargs)

        
    def dispatch(self, *args, **kwargs):
        return super(ProfileEmployeeDetialPublicView, self).dispatch(*args, **kwargs)

class ProfileFetchContactInfo(TemplateView):
    """ 
    Given a username, return the contact info for that user:
    for now just the primary email address
    """
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            contact_info = [{'email': user.email}]
        except:
            contact_info = [{'email': 'private'}]
        
        contact_info = simplejson.dumps(contact_info)
        return HttpResponse(contact_info, mimetype="application/javascript")
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileFetchContactInfo, self).dispatch(*args, **kwargs)

class ProfileBookmarkView(TemplateView):
    template_name = "portal/bookmark_view.html"

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProfileBookmarkView, self).get_context_data(**kwargs)
        context['profile'] = self.get_object()
        context['profile_bookmarks'] = get_profile_bookmarks(self.request.user)
        context['job_bookmarks'] = get_job_bookmarks(self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileBookmarkView, self).dispatch(*args, **kwargs)

class ProfileDelBookmarkView(TemplateView):
    """ Remove a bookmark from within the favorite list """
    success_url = reverse_lazy('bookmark_list')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk', None)
            if pk:
                up = UserProfile.objects.get(id=pk)
                del_profile_bookmark(self.request.user, up)
        except:
            pass
        return HttpResponseRedirect(self.success_url)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDelBookmarkView, self).dispatch(*args, **kwargs)
        
class ProfileAddBookmarkAjaxView(TemplateView):
    """ Given an profile pk, this view adds the profile to user's bookmarks
    """
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        bm_status = [{'bookmark_toggled': False}]
        pk = request.POST['pk']
        try:
            profile = UserProfile.objects.get(id=pk)
            bm = bookmark_profile(self.request.user, profile)
            if bm:
                bm_status = [{'bookmark_toggled': True}]
        except:
            pass
        
        bm_status = simplejson.dumps(bm_status)
        return HttpResponse(bm_status, mimetype="application/javascript")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileAddBookmarkAjaxView, self).dispatch(*args, **kwargs)

        
class ProfileDelBookmarkAjaxView(TemplateView):
    """ Given an profile pk, this view deletes the profile from user's bookmarks
    """
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        bm_status = [{'bookmark_toggled': False}]
        pk = request.POST['pk']
        try:
            profile = UserProfile.objects.get(id=pk)
            del_profile_bookmark(self.request.user, profile)
            bm_status = [{'bookmark_toggled': True}]
        except:
            pass
        
        bm_status = simplejson.dumps(bm_status)
        return HttpResponse(bm_status, mimetype="application/javascript")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDelBookmarkAjaxView, self).dispatch(*args, **kwargs)

class ProfileTrainingView(TemplateView):
    template_name = "portal/training_view.html"

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProfileTrainingView, self).get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileTrainingView, self).dispatch(*args, **kwargs)


