from django.template.loader import render_to_string
import json


def render_to_html_string(template, context=None):
    not_escaped_string = render_to_string(template, context)
    # This will add \ slashes in order to escape double quotas
    return json.dumps(not_escaped_string)