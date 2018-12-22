# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpRequest
from django.conf import settings
from django.views.generic import TemplateView

class HomeView(TemplateView):
    """
    This is where everything starts (homepage shall we call it)
    """
    template_name = "landing/main.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        JOB_COUNTRIES = getattr(settings, 'JOB_COUNTRIES', [])
        if 'country_info' in self.request.session:
            cc = self.request.session['country_info']['country_code']
            if cc and cc.upper() in JOB_COUNTRIES:
                # self.template_name = "landing/targeted_countries.html"
                context['targeted_country'] = cc
        return context
 
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

class PhilippinesView(TemplateView):
    """
    Special page for visitors from the Philippines
    """
    template_name = "landing/philippines.html"
    
    def get_context_data(self, **kwargs):
        context = super(PhilippinesView, self).get_context_data(**kwargs)
        return context
 
    def dispatch(self, *args, **kwargs):
        return super(PhilippinesView, self).dispatch(*args, **kwargs)


class PlainTextView(TemplateView):
  def render_to_response(self, context, **kwargs):
    return super(PlainTextView, self).render_to_response(
      context, content_type='text/plain', **kwargs)
