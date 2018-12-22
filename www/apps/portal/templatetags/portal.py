from django import template
from django.core.urlresolvers import reverse
from django.template import Node, TemplateSyntaxError
from django.conf import settings
register = template.Library()

@register.filter
def get_left_portal_menu(request):
    """ Return a left aligned sub menu for portal access"""
    is_employee = False
    is_employer = False
    if request.user.is_authenticated():
        up = request.user.get_profile()
        is_employee = up.is_employee
        is_employer = up.is_employer

    PORTAL_NAV_MENU = {
        "1": {
            "name": "Talent Search",
            "reversible": "portal_talent_search",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False,
            "login_required": False
        },
        "2": {
            "name": "Job Search",
            "reversible": "portal_job_search",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False,
            "login_required": False
        },
        "3": {
            "name": "Business Search",
            "reversible": "portal_business_search",
            "url": "",
            "selected": False,
            "hidden": True,
            "editable": False,
            "login_required": False
        },
    }

    # sort by level -- indicating the position of the menu
    menu = []
    keys = PORTAL_NAV_MENU.keys()
    keys.sort()
    items = []
    for key in keys:
        items.append(PORTAL_NAV_MENU[key])
    
    for item in items:
        if item['hidden']:
            continue
        
        if item['login_required']:
            if not request.user.is_authenticated():
                continue
        try:
            item['url'] = reverse(item['reversible'])
        except:
            item['url'] = item['reversible'] # plain URI (path)
        
        if item['url'] in request.path:
            item['selected'] = True

        menu.append(item)

        # print menu
    return menu

@register.filter
def get_right_portal_menu(request):
    """ Return a right aligned sub menu for portal access"""
    is_employee = False
    is_employer = False
    if request.user.is_authenticated():
        up = request.user.get_profile()
        is_employee = up.is_employee
        is_employer = up.is_employer

    PORTAL_NAV_MENU = {
        "1": {
            "name": "Training",
            "reversible": "training_list",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False,
            "login_required": True
        },
        "2": {
            "name": "Favorites",
            "reversible": "bookmark_list",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False,
            "login_required": True
        },
        "3": {
            "name": "How It Works",
            "reversible": "how_it_works",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False,
            "login_required": False
        },
        # "4": {
        #     "name": "Done For You",
        #     "reversible": "/done4you/",
        #     "url": "",
        #     "selected": False,
        #     "hidden": False,
        #     "editable": False,
        #     "login_required": False
        # },
    }

    # sort by level -- indicating the position of the menu
    menu = []
    keys = PORTAL_NAV_MENU.keys()
    keys.sort()
    items = []
    for key in keys:
        items.append(PORTAL_NAV_MENU[key])
    
    for item in items:
        if item['hidden']:
            continue
        
        if item['login_required']:
            if not request.user.is_authenticated():
                continue
        
        try:
            item['url'] = reverse(item['reversible'])
        except:
            item['url'] = item['reversible'] # plain URI (path)
        
        if item['url'] in request.path:
            item['selected'] = True

        menu.append(item)

        # print menu
    return menu




