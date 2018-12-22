from django import template
from django.core.urlresolvers import reverse
from django.template import Node, TemplateSyntaxError
from django.conf import settings

register = template.Library()

@register.filter
def get_navigation_menu(request):
    """
    Given a request object, returns a 1st level navigation menu
    """
    loggedin = request.user.is_authenticated()

    NAV_MENU = {
        "100": {
            "name": "home",
            "reversible": "home_page",
            "url": "",
            "pre_login_visible": True,
            "post_login_visible": True,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        },
        # "101": {
        #     "name": "Blog",
        #     "reversible": "http://blog.outsourcefactor.com",
        #     "url": "",
        #     "pre_login_visible": True,
        #     "post_login_visible": True,
        #     "superuser_required": False,
        #     "staff_required": False,
        #     "selected": False
        # },
        # "102": {
        #     "name": "Forum",
        #     "reversible": "http://forum.outsourcefactor.com",
        #     "url": "",
        #     "pre_login_visible": True,
        #     "post_login_visible": True,
        #     "superuser_required": False,
        #     "staff_required": False,
        #     "selected": False
        # },
        # "103": {
        #     "name": "Contact Us",
        #     "reversible": "contact_form",
        #     "url": "",
        #     "pre_login_visible": True,
        #     "post_login_visible": True,
        #     "superuser_required": False,
        #     "staff_required": False,
        #     "selected": False
        # },
        "104": {
            "name": "Login",
            "reversible": "auth_login",
            "url": "",
            "pre_login_visible": True,
            "post_login_visible": False,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        },
        "105": {
            "name": "Signup",
            "reversible": "registration_register",
            "url": "",
            "pre_login_visible": True,
            "post_login_visible": False,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        },
        "106": {
            "name": "Account",
            "reversible": "profile_view_details",
            "url": "",
            "pre_login_visible": False,
            "post_login_visible": True,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        },
        # "107": {
        #     "name": "Admin",
        #     "reversible": "admin:index",
        #     "url": "",
        #     "pre_login_visible": False,
        #     "post_login_visible": True,
        #     "superuser_required": False, # superuser should be set as staff as well 
        #     "staff_required": True,
        #     "selected": False
        # },
        "108": {
            "name": "Logout",
            "reversible": "auth_logout",
            "url": "",
            "pre_login_visible": False,
            "post_login_visible": True,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        }
    }

    # sort by level -- indicating the position of the menu
    menu = []
    keys = NAV_MENU.keys()
    keys.sort()
    items = []
    for key in keys:
        items.append(NAV_MENU[key])
    
    for item in items:
        if item['pre_login_visible'] and item['post_login_visible']:
            pass # show all the time, include in menu
        elif item['post_login_visible'] and loggedin:
            pass # show only when user logs in, include in menu
        elif item['pre_login_visible'] and not loggedin:
            pass # show only when user is not logged in, include in menu
        else:
            continue # not to be shown at this time, don't incud

        if item['superuser_required'] and not request.user.is_superuser:
            continue # not a superuser, don't include

        if item['staff_required'] and not request.user.is_staff:
            continue # not a staff, don't include

        try:
            item['url'] = reverse(item['reversible'])
        except:
            item['url'] = item['reversible']

        if item['url'] == request.path:
            item['selected'] = True

        # if this is a submenu call, we still want to have the menu selected
        if (len(item['url']) >= 2):
            if item['url'] in request.path:
                item['selected'] = True

        menu.append(item)

    return menu

@register.filter
def get_footer_menu(request):
    """
    Given a request object, returns the footer menu
    """
    FOOTER_MENU = {

        # "101": {
        #     "name": "Blog",
        #     "reversible": "http://blog.outsourcefactor.com",
        #     "url": "",
        #     "pre_login_visible": True,
        #     "post_login_visible": True,
        #     "superuser_required": False,
        #     "staff_required": False,
        #     "selected": False
        # },
        # "102": {
        #     "name": "Forum",
        #     "reversible": "http://forum.outsourcefactor.com",
        #     "url": "",
        #     "pre_login_visible": True,
        #     "post_login_visible": True,
        #     "superuser_required": False,
        #     "staff_required": False,
        #     "selected": False
        # },
        "103": {
            "name": "Contact Us",
            "reversible": "contact_form",
            "url": "",
            "pre_login_visible": True,
            "post_login_visible": True,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        },
        "105": {
            "name": "Terms of Service",
            "reversible": "terms_of_service",
            "url": "",
            "pre_login_visible": True,
            "post_login_visible": True,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        },
        "106": {
            "name": "Privacy Policy",
            "reversible": "privacy_policy",
            "url": "",
            "pre_login_visible": True,
            "post_login_visible": True,
            "superuser_required": False,
            "staff_required": False,
            "selected": False
        },
        "107": {
            "name": "Admin",
            "reversible": "admin:index",
            "url": "",
            "pre_login_visible": False,
            "post_login_visible": True,
            "superuser_required": False, # superuser should be set as staff as well 
            "staff_required": True,
            "selected": False
        },
    }

    # sort by level -- indicating the position of the menu
    menu = []
    keys = FOOTER_MENU.keys()
    keys.sort()
    items = []
    for key in keys:
        items.append(FOOTER_MENU[key])
    
    loggedin = request.user.is_authenticated()
    for item in items:
        if item['pre_login_visible'] and item['post_login_visible']:
            pass # show all the time, include in menu
        elif item['post_login_visible'] and loggedin:
            pass # show only when user logs in, include in menu
        elif item['pre_login_visible'] and not loggedin:
            pass # show only when user is not logged in, include in menu
        else:
            continue # not to be shown at this time, don't incud

        if item['superuser_required'] and not request.user.is_superuser:
            continue # not a superuser, don't include

        if item['staff_required'] and not request.user.is_staff:
            continue # not a staff, don't include

        try:
            item['url'] = reverse(item['reversible'])
        except:
            item['url'] = item['reversible']

        if item['url'] == request.path:
            item['selected'] = True

        # if this is a submenu call, we still want to have the menu selected
        if (len(item['url']) >= 2):
            if item['url'] in request.path:
                item['selected'] = True

        menu.append(item)

    return menu




