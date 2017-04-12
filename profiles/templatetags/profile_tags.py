from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def main_nav(context, match_val):
    v = context.get('nav')
    if v == match_val:
        return 'active'
    return ''
