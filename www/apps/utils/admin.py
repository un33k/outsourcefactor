from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.conf import settings


class FlatPageAdmin(FlatPageAdminOld):
    class Media:
        STATIC_URL = getattr(settings, 'STATIC_URL', '/static/')
        DEBUG = getattr(settings, 'DEBUG', False)
        if DEBUG:
            js = (STATIC_URL+'js/tiny_mce/tiny_mce.js', STATIC_URL+'js/tiny_mce/textareas_debug.js',)
        else:
            js = (STATIC_URL+'js/tiny_mce/tiny_mce.js', STATIC_URL+'js/tiny_mce/textareas.js',)

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

