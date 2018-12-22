import os, random, string, time
from django.utils.hashcompat import sha_constructor
from django import template
from django.core.cache import cache

def model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dict containing the data in the ``instance`` where:
    data = {'lable': 'verbose_name', 'name':name, 'value':value,}
    Verbose_name is capitalized, order of fields is respected.
    
    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned dict.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict, even if they are listed in
    the ``fields`` argument.

    """

    data = []
    if instance:
        opts = instance._meta
        for f in opts.fields:
            if not f.editable:
                continue
            if fields and not f.name in fields:
                continue
            if exclude and f.name in exclude:
                continue

            value = f.value_from_object(instance)

            # load the display name of choice fields
            get_choice = 'get_'+f.name+'_display'
            if hasattr(instance, get_choice):
                value = getattr(instance, get_choice)()

            # only display fields with values and skip the reset
            if value:
                data.append({'lable': f.verbose_name.capitalize(), 'name': f.name, 'value':value, 'help':f.help_text, })

        if fields and data:
            sorted_data = []
            for f in fields:
                for d in data:
                    if f.lower == d['name'].lower:
                        sorted_data.append(d)
            data = sorted_data
    return data

# get a random string of known length
def get_unique_random(length=10):
    randtime = str(time.time()).split('.')[0]
    rand = ''.join([random.choice(randtime+string.letters+string.digits) for i in range(length)])
    return sha_constructor(rand).hexdigest()[:length]

# remove csrf stuff and create a token that is generic
def get_cache_key_from_post(post_data):
    pd = post_data
    try:
        del pd['csrfmiddlewaretoken']
    except:
        pass
    return pd.urlencode()

# get or create cache access key
# if access key created, then the caller should delete their own cache and reset a new one
# if created = False, then the caller's own cache still good and can be used
def get_or_create_cache_access_key(key_type=''):
    created = False
    if key_type:    
        key = 'cache_access_key_%s' % (key_type,)
        access_key = cache.get(key)
        if not access_key:
            cache.set(key, 86400 * 7)
            created = True
    return created

# delete access key signalling that something has changed
def delete_cache_access_key(key_type=''):
    if key_type:    
        key = 'cache_access_key_%s' % (key_type,)
        access_key = cache.get(key)
        if access_key:
            cache.delete(key)



#load templatetags, keep it last in the page
project_tags = [
    # django tags
    'django.templatetags.cache',
    'django.templatetags.future',
    'django.templatetags.i18n',
    'django.templatetags.l10n',
    'django.templatetags.static',
    'django.contrib.humanize.templatetags.humanize',

    # # project tags
    'www.apps.utils.templatetags.common',
    'www.apps.utils.templatetags.email',
    'www.apps.utils.templatetags.highlight',
    'www.apps.utils.templatetags.navigation',
    
    # 3rd party
    'gravatar.templatetags.gravatar',
]
for t in project_tags: template.add_to_builtins(t)
