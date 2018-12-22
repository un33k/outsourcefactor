from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, TemplateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect

from ..models import JobPost
from ..forms import JobPostForm
from ..utils.profile import *
from ..utils.job import *

class EmployerJobDeleteView(DeleteView):
    """ Delete a job post """
    model = JobPost
    success_url = reverse_lazy('employer_jobpost_list')
    template_name = 'profiles/employer_job_list.html'

    def get_object(self, queryset=None):
        """ ensure object is owned by request.user. """
        obj = super(EmployerJobDeleteView, self).get_object()
        if not obj.user == self.request.user:
            messages.add_message(self.request, messages.INFO, _("jobpost not found"))
            raise Http404
        
        messages.add_message(self.request, messages.INFO, _("jobpost deleted"))
        return obj
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobDeleteView, self).dispatch(*args, **kwargs)


class EmployerJobAddView(CreateView):
    """ Add new post for employer """
    form_class = JobPostForm
    success_url = reverse_lazy('employer_jobpost_list')
    template_name = 'profiles/employer_job_list.html'

    # we need the request in the form, pass it in
    def get_form_kwargs(self):
        kwargs = super(EmployerJobAddView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.INFO, _('job post added'))
        return super(EmployerJobAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EmployerJobAddView, self).get_context_data(**kwargs)
        context['jobs'] = get_employer_jobpost(self.request.user.get_profile())
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobAddView, self).dispatch(*args, **kwargs)


class EmployerJobUpdateView(UpdateView):
    """
    Job is already there, just update it
    """
    model = JobPost
    form_class = JobPostForm
    template_name = "profiles/employer_job_update.html"
    success_url = reverse_lazy('employer_jobpost_list')

    # we need the request in the form, pass it in
    def get_form_kwargs(self):
        kwargs = super(EmployerJobUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['obj'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.add_message (self.request, messages.INFO, _('Job updated'))
        return HttpResponseRedirect(self.success_url)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobUpdateView, self).dispatch(*args, **kwargs)


class EmployerJobPublicView(TemplateView):
    """
    Public view of a job
    """
    template_name = "portal/job_object_public_view.html"

    def get_object(self, queryset=None):
        """ get the job or 404 """
        pk = self.kwargs['pk'].strip()
        job = get_object_or_404(JobPost, id=pk)
        return job
    
    def get_context_data(self, **kwargs):
        context = super(EmployerJobPublicView, self).get_context_data(**kwargs)
        job = self.get_object()
        if not job.is_public:
            raise Http404
        context['job'] = job
        context['profile'] = get_user_profile(job.user)
        context['is_public_view'] = True
        context['this_user'] = job.user
 
        if self.request.user == job.user:
            if job.user.get_profile().is_publicly_viewable:
                msg = _('your public facing job post')
            else:
                msg = _('job not viewable by the public. reason: your account profile is incomplete')
            messages.add_message (self.request, messages.INFO, msg)
        else:
            pkey = 'job-viewed'+str(job.id)
            try:
                s = self.request.session[pkey]
            except:
                job.just_viewed()
                self.request.session[pkey] = True
                
        return context

    def get(self, request, *args, **kwargs):
        job = self.get_object()
        slug = self.kwargs['slug'].strip()
        if job.slug != slug: # slug has changed, redirect to new link
            return HttpResponsePermanentRedirect(job.get_absolute_url())
        return super(EmployerJobPublicView, self).get(request, *args, **kwargs)
        
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobPublicView, self).dispatch(*args, **kwargs)

class EmployerJobDelBookmarkView(TemplateView):
    """ Remove a job bookmark from within the favorite list """
    success_url = reverse_lazy('bookmark_list')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk', None)
            if pk:
                job = JobPost.objects.get(id=pk)
                del_job_bookmark(self.request.user, job)
        except:
            pass
        return HttpResponseRedirect(self.success_url)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobDelBookmarkView, self).dispatch(*args, **kwargs)

class EmployerJobAddBookmarkAjaxView(TemplateView):
    """ Given a job pk, this view adds the job to user's bookmarks
    """
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        bm_status = [{'bookmark_toggled': False}]
        if request.user.is_authenticated():
            pk = request.POST['pk']
            try:
                job = JobPost.objects.get(id=pk)
                bm = bookmark_job(self.request.user, job)
                if bm:
                    bm_status = [{'bookmark_toggled': True}]
            except:
                pass
        
        bm_status = simplejson.dumps(bm_status)
        return HttpResponse(bm_status, mimetype="application/javascript")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobAddBookmarkAjaxView, self).dispatch(*args, **kwargs)

class EmployerJobDelBookmarkAjaxView(TemplateView):
    """ Given a job pk, this view deletes the job from user's bookmarks
    """
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        bm_status = [{'bookmark_toggled': False}]
        if request.user.is_authenticated():
            pk = request.POST['pk']
            try:
                job = JobPost.objects.get(id=pk)
                del_job_bookmark(self.request.user, job)
                bm_status = [{'bookmark_toggled': True}]
            except:
                pass
        
        bm_status = simplejson.dumps(bm_status)
        return HttpResponse(bm_status, mimetype="application/javascript")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobDelBookmarkAjaxView, self).dispatch(*args, **kwargs)


class EmployerJobsFetchContactInfo(TemplateView):
    """ 
    Given a jobid, return the contact info for that job or:
    if no contact is provided return the primary email address
    """
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request, *args, **kwargs):
        pk = request.POST['jobid'].split('_')[1]
        try:
            job = JobPost.objects.get(id=pk)
            if job.contact:
                contact_info = [{'email': job.contact}]
            else:
                contact_info = [{'email': job.user.email}]
        except:
            contact_info = [{'email': ''}]

        contact_info = simplejson.dumps(contact_info)
        return HttpResponse(contact_info, mimetype="application/javascript")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployerJobsFetchContactInfo, self).dispatch(*args, **kwargs)



