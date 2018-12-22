from django import template
from django.template import Node, TemplateSyntaxError
from ..models import Bookmark

register = template.Library()

@register.filter
def is_bookmarked(user, obj):
    """ 
    Given a user and an object, 
    Returns: True if object is bookmarked by user, otherwise False
    """
    try:
        bm = Bookmark.objects.get_the_bookmark_for_this_object_for_this_user(user, obj)
    except:
        pass
    else:
        if bm and bm.user == user or bm.content_object == obj:
            return True
    return False



