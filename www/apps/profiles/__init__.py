from django import template
project_tags = [
    'www.apps.profiles.templatetags.profile',
    'www.apps.profiles.templatetags.job',
    'www.apps.profiles.templatetags.skill',
]
for t in project_tags: template.add_to_builtins(t)
