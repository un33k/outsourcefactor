from django import template
project_tags = [
    'www.apps.social.templatetags.social',
]
for t in project_tags: template.add_to_builtins(t)
