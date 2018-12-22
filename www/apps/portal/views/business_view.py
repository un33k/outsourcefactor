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
from ..utils.business import *


# handle search queries (Business)
class BusinessSearchView(TemplateView):
    template_name = "portal/search_business_view.html"
    
    def get(self, request, **kwargs):
        form = SearchBusinessForm()
        return self.render_to_response({'form': form})

    def post(self, request, **kwargs):
        form = SearchBusinessForm(request, request.POST)
        if not form.is_valid():
            return self.render_to_response({'form': form})

        # build query based on form input
        form_data = form.clean()
        query, business_info = get_business_query(request, form_data)
            
        elist_key = get_cache_key_from_post(request.POST)
        business_list = cache.get(elist_key)
        if business_list:
            created = get_or_create_cache_access_key('Business_Search_View')
            if created:
                cache.delete(elist_key)
                business_list = None
        
        if not business_list:
            # search
            business_list = get_business_profile_list(query)
            if business_list:
                cache.set(elist_key, business_list, 8*60) # remember for x min.
            else:
                business_list = []
        
        # cache query for later pagination
        skey = get_unique_random(20)
        remember = [request.POST, form_data]
        cache.set(skey, remember, 24*60*60)
        
        # paginate starting with page one, the rest of the pages are dealt with elsewhere
        if not business_list:
            business_list = []
        
        paginate = Paginator(business_list, 5)
        businesses = paginate.page(1)
        
        search_keywords = request.POST.get('keywords', '')
        # if user has specific search
        specific_search = False
        if business_info or search_keywords:
            specific_search = True
        
        c = RequestContext(request, {
            'form': form,
            'businesses': businesses,
            'business_info': business_info,
            'search_key': skey,
            'search_kw': search_keywords,
            'specific_search': specific_search,
            'total_result': len(business_list)
        })
        return self.render_to_response(c)


# handle pagination of search queries
class BusinessSearchPaginateView(TemplateView):
    template_name = "portal/search_business_view.html"
    from_class = SearchBusinessForm
    
    def _redirect_on_stale(self):
        messages.add_message(self.request, messages.INFO, _("stale search, search again"))
        return HttpResponseRedirect(reverse_lazy('portal_business_search'))

    def get(self, request, **kwargs):
        form = SearchBusinessForm()
        return self.render_to_response({'form': form})
        
    def post(self, request, *args, **kwargs):
        skey = kwargs.get('sk', None)
        if not skey:
            # something went wrong or someone is playing around, skey must be here, but its not
            return self._redirect_on_stale()

        # we are paginating
        remember = cache.get(skey)
        if not remember:
            # cache has expired
            return self._redirect_on_stale()
            
        try:
            # verify cache content
            post_data = remember[0]
            form_data = remember[1]
        except:
            return self._redirect_on_stale()

        # renew the cache
        cache.delete(skey)
        skey = get_unique_random(20)
        cache.set(skey, remember, 24*60*60)
        
        # build query based on form input
        query, business_info = get_business_query(request, form_data)

        elist_key = get_cache_key_from_post(post_data)
        business_list = cache.get(elist_key)
        if business_list:
            created = get_or_create_cache_access_key('Business_Search_View')
            if created:
                cache.delete(elist_key)
                business_list = None
        
        if not business_list:
            # search
            business_list = get_business_profile_list(query)
            cache.set(elist_key, business_list, 8*60) # remember for x min.

        if not business_list:
            business_list = []
        
        spage = kwargs.get('sp', 1)
        paginate = Paginator(business_list, 5)
        try:
            businesses = paginate.page(spage)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            businesses = paginate.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            businesses = paginate.page(paginate.num_pages)

        form = SearchBusinessForm(request, post_data)
        
        search_keywords = post_data.get('keywords', '')
        # if user has specific search
        specific_search = False
        if business_info or search_keywords:
            specific_search = True
            
        c = RequestContext(request, {
            'form': form,
            'businesses': businesses,
            'business_info': business_info,
            'search_key': skey,
            'search_kw': search_keywords,
            'specific_search': specific_search,
            'total_result': len(business_list)
        })
        return self.render_to_response(c)



