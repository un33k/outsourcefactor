from django import template
from django.core.urlresolvers import reverse
from django.template import Node, TemplateSyntaxError
from django.conf import settings

register = template.Library()

@register.filter
def get_profile_left_menu(request):
    """
    Given a request object, returns a 1st level profile (account) navigation menu
    """
    is_employee = False
    is_employer = False
    if request.user.is_authenticated():
        up = request.user.get_profile()
        is_employee = up.is_employee
        is_employer = up.is_employer

    PROFILE_NAV_MENU = {
        "1": {
            "name": "Summary",
            "reversible": "profile_view_details",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False
        },
        "2": {
            "name": "Profile",
            "reversible": "profile_edit_details",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False if (up.full_name and up.business) or (up.full_name and up.age) else True
        },
        "3": {
            "name": "Employment",
            "reversible": "employee_profile_edit_details",
            "url": "",
            "selected": False,
            "hidden": not is_employee,
            "editable": False if up.title else True
        },
        "4": {
            "name": "Skills",
            "reversible": "employee_skill_list",
            "url": "",
            "selected": False,
            "hidden": not is_employee,
            "editable": False if up.posted_skills else True
        },
        "5": {
            "name": "Post Jobs",
            "reversible": "employer_jobpost_list",
            "url": "",
            "selected": False,
            "hidden": not is_employer,
            "editable": False
        },
        "6": {
            "name": "Social Networks",
            "reversible": "social_provider_list",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False
        },
        "7": {
            "name": "Email",
            "reversible": "emailmgr_email_list",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False
        },
        "8": {
            "name": "Settings",
            "reversible": "profile_change_password",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False
        },
    }

    # sort by level -- indicating the position of the menu
    menu = []
    keys = PROFILE_NAV_MENU.keys()
    keys.sort()
    items = []
    for key in keys:
        items.append(PROFILE_NAV_MENU[key])
    
    for item in items:
        if item['hidden']:
            continue
        try:
            item['url'] = reverse(item['reversible'])
        except:
            item['url'] = item['reversible'] # plain URI (path)
        
        if item['url'] == request.path:
            item['selected'] = True

        menu.append(item)

        # print menu
    return menu



@register.filter
def get_profile_right_menu(request):
    """
    Given a request object, returns a 1st level profile (account) navigation menu for the right side
    """
    is_employee = False
    is_employer = False
    if request.user.is_authenticated():
        up = request.user.get_profile()
        is_employee = up.is_employee
        is_employer = up.is_employer

    PROFILE_NAV_MENU = {
        "1": {
            "name": "Training",
            "reversible": "training_list",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False
        },        
        "2": {
            "name": "Favorites",
            "reversible": "bookmark_list",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False
        },
        "3": {
            "name": "%s" % "Job Search" if is_employee else "Talent Search",
            "reversible": "%s" % "portal_job_search" if is_employee else "portal_talent_search",
            "url": "",
            "selected": False,
            "hidden": False,
            "editable": False
        },
    }

    # sort by level -- indicating the position of the menu
    menu = []
    keys = PROFILE_NAV_MENU.keys()
    keys.sort()
    items = []
    for key in keys:
        items.append(PROFILE_NAV_MENU[key])
    
    for item in items:
        if item['hidden']:
            continue
        try:
            item['url'] = reverse(item['reversible'])
        except:
            item['url'] = item['reversible'] # plain URI (path)
        
        if item['url'] == request.path:
            item['selected'] = True

        menu.append(item)

        # print menu
    return menu





