from django import template
project_tags = [
    'www.apps.bookmark.templatetags.bookmark',
]
for t in project_tags: template.add_to_builtins(t)
