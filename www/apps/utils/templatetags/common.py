from django import template
from django.core.urlresolvers import reverse
from django.template import Node, Library, TemplateSyntaxError
from django.conf import settings
import os, base64

register = template.Library()

######## Start: URL Encoded Base64 #############
# Usage: get_base64 'something' as base64thingy
################################################
class Base64Node(Node):
    def __init__(self, input, cxtname):
        self.b64 = base64.urlsafe_b64encode(str(input))
        self.cxtname = cxtname

    def render(self, context):
        context[self.cxtname] = self.b64
        return ''
 
def get_base64(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_base64 tag takes exactly 3 arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "2nd argument to get_base64 tag must be 'as'"
    return Base64Node(bits[1], bits[3])
get_base64 = register.tag(get_base64)
######### End: URL Encoded Base64 #######

######## Start: Settings Attributes Fetch #######
# Example: get_from_settings my_variable as my_context_value
# Example: get_from_settings my_variable my_default as my_context_value
################################################
class SettingsAttrNode(Node):
    def __init__(self, variable, default, as_value):
        self.variable = getattr(settings, variable, default)
        self.cxtname = as_value

    def render(self, context):
        context[self.cxtname] = self.variable
        return ''
 
def get_from_setting(parser, token):
    as_value = variable = default = ''
    bits = token.contents.split()
    if len(bits) == 4 and bits[2] == 'as':
        variable = bits[1]
        as_value = bits[3]
    elif len(bits) == 6 and bits[2] == 'or' and bits[4] == 'as':
        variable = bits[1]
        default  = bits[3]
        as_value = bits[5]
    else:
        raise TemplateSyntaxError, "usage: get_from_settings variable default as value " \
                    "OR: get_from_settings variable as value"

    return SettingsAttrNode(variable=variable, default=default, as_value=as_value)

get_from_setting = register.tag(get_from_setting)
######### End: Settings Attributes Fetch #######








