from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, TemplateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed

from ..models import Skill, SkillSet
from ..forms import SkillSetForm
from ..utils.skill import get_employee_skill

class EmployeeDeleteSkillView(DeleteView):
    model = SkillSet
    success_url = reverse_lazy('employee_skill_list')
    template_name = 'profiles/employee_skill_list.html'

    def get_object(self, queryset=None):
        """ ensure object is owned by request.user. """
        obj = super(EmployeeDeleteSkillView, self).get_object()
        if not obj.user == self.request.user:
            messages.add_message(self.request, messages.INFO, _("skill not found"))
            raise Http404
        
        return obj
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployeeDeleteSkillView, self).dispatch(*args, **kwargs)

class EmployeeAddSkillView(FormView):
    """
    Add new skill for user
    """
    form_class = SkillSetForm
    success_url = reverse_lazy('employee_skill_list')
    template_name = 'profiles/employee_skill_list.html'

    # we need the request in the form, pass it in
    def get_form_kwargs(self):
        kwargs = super(EmployeeAddSkillView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, _('skill added'))
        return super(EmployeeAddSkillView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EmployeeAddSkillView, self).get_context_data(**kwargs)
        context['skills'] = get_employee_skill(self.request.user.get_profile())
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployeeAddSkillView, self).dispatch(*args, **kwargs)


class EmployeeUpdateSkillView(UpdateView):
    """
    Profile is already there, just update it
    """
    model = SkillSet
    form_class = SkillSetForm
    success_url = reverse_lazy('employee_skill_list')
    template_name = "profiles/employee_skill_update.html"

    def get_object(self, queryset=None):
        """ ensure object is owned by request.user. """
        obj = super(EmployeeUpdateSkillView, self).get_object()
        if not obj.user == self.request.user:
            messages.add_message(self.request, messages.INFO, _("skill not found"))
            raise Http404
        return obj

    # we need the request in the form, pass it in
    def get_form_kwargs(self):
        kwargs = super(EmployeeUpdateSkillView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['obj'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.add_message (self.request, messages.INFO, _('skill update'))
        return HttpResponseRedirect(self.success_url)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmployeeUpdateSkillView, self).dispatch(*args, **kwargs)


class EmployeeGetSkillSubcategoryView(TemplateView):
    """ Given a skill category, return all its subcategories, internal use"""

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request):
        category = request.POST['cat_id']
        skills = Skill.objects.filter(category=category)
        skill_subcat = [{'id': s.id, 'name': s.name} for s in skills]
        json_subcat = simplejson.dumps( skill_subcat)
        return HttpResponse(json_subcat, mimetype="application/javascript")


class SearchGetSkillSubcategoryView(TemplateView):
    """ Given a skill category, return all its subcategories with 'Any' as first option """

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Method Not Allowed')

    def post(self, request):
        category = request.POST['cat_id']
        if category > 0:
            skills = Skill.objects.filter(category=category)
            skill_subcat = [{'id': s.id, 'name': s.name} for s in skills]
            skill_subcat.insert(0, {'id': 0, 'name': 'Any'})
        else:
            skill_subcat = [{'id': 0, 'name': 'Any'}]
            
        json_subcat = simplejson.dumps( skill_subcat)
        return HttpResponse(json_subcat, mimetype="application/javascript")

