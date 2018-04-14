from django import template

register = template.Library()

@register.filter
def lookup(d, key):
    print d
    print "\n"
    print key
    return d[key]