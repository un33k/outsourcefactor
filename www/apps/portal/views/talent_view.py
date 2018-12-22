# coding: utf-8
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView, TemplateView, View
from django.http import HttpResponseRedirect 
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from www.apps.profiles.models import UserProfile
from www.apps.utils import *
from ..forms import *
from ..utils.talent import *


# handle search queries
class TalentSearchView(TemplateView):
    template_name = "portal/search_talents_view.html"
    
    def get(self, request, **kwargs):
        form = SearchTalentForm()
        return self.render_to_response({'form': form})

    def post(self, request, **kwargs):
        form = SearchTalentForm(request, request.POST)
        if not form.is_valid():
            return self.render_to_response({'form': form})

        # build query based on form input
        form_data = form.clean()
        query, skill_info = get_employee_query(request, form_data)
        
        request.session['talent_search_params'] = request.POST
        elist_key = get_cache_key_from_post(request.POST)
        employee_list = cache.get(elist_key)
        if not employee_list:
            # search
            employee_list = get_employee_profile_list(query)
            if employee_list:
                cache.set(elist_key, employee_list, 8*60) # remember for x min.
            else:
                employee_list = []

        # paginate starting with page one, the rest of the pages are dealt with elsewhere
        if not employee_list:
            employee_list = []
        paginate = Paginator(employee_list, 4)
        employees = paginate.page(1)

        search_keywords = request.POST.get('keywords', '')
        # if user has specific search
        specific_search = False
        if skill_info or search_keywords:
            specific_search = True
            
        c = RequestContext(request, {
            'form': form,
            'employees': employees,
            'skill_info': skill_info,
            'search_kw': search_keywords,
            'specific_search': specific_search,
            'total_result': len(employee_list)

        })
        return self.render_to_response(c)


# handle pagination of search queries
class TalentSearchPaginateView(TemplateView):
    template_name = "portal/search_talents_view.html"

    def get(self, request, **kwargs):
        form = SearchTalentForm()
        return self.render_to_response({'form': form})
        
    def post(self, request, *args, **kwargs):

        # build query based on form input
        form_data = request.session.get('talent_search_params', {})
        query, skill_info = get_employee_query(request, form_data)
        elist_key = get_cache_key_from_post(form_data)
        employee_list = cache.get(elist_key)
        if not employee_list:
            # search
            employee_list = get_employee_profile_list(query)
            cache.set(elist_key, employee_list, 8*60) # remember for x min.
        if not employee_list:
            employee_list = []
        
        spage = kwargs.get('sp', 1)
        paginate = Paginator(employee_list, 4)
        try:
            employees = paginate.page(spage)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            employees = paginate.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            employees = paginate.page(paginate.num_pages)

        form = SearchTalentForm(request, form_data)
        
        search_keywords = form_data.get('keywords', '')
        # if user has specific search
        specific_search = False
        if skill_info or search_keywords:
            specific_search = True
            
        c = RequestContext(request, {
            'form': form,
            'employees': employees,
            'skill_info': skill_info,
            'search_kw': search_keywords,
            'specific_search': specific_search,
            'total_result': len(employee_list)

        })
        return self.render_to_response(c)



