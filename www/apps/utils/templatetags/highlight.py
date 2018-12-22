import re
from django import template
from django.template import Node, TemplateSyntaxError
from django.conf import settings
from django.utils.safestring import mark_safe
from www.apps.portal.utils.common import get_tokenize

register = template.Library()

def highlight_word(needles, haystack, cls_name='highlighted'):
    if not needles:
        return haystack
    if not haystack:
        return ''
    regex = re.compile(r"(%s)" % "|".join([re.escape(n) for n in needles]), re.I)
    i = 0; out = ""
    for m in regex.finditer(haystack):
        out += "".join([haystack[i:m.start()],'<span class="%s">'%cls_name,haystack[m.start():m.end()],"</span>"])
        i = m.end()
    return mark_safe(out + haystack[i:])

@register.filter
def highlight(keywords, string):
    """
    given an list of words, this fuction highlights the match words in the given string
    """
    if not keywords:
        return string
    if not string:
        return ''
    include, exclude = get_tokenize(keywords)
    highlighted = highlight_word(include, string)
    return highlighted
