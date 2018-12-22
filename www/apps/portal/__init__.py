from django import template
project_tags = [
    'www.apps.portal.templatetags.portal',
    'www.apps.portal.templatetags.rounder',
]
for t in project_tags: template.add_to_builtins(t)
