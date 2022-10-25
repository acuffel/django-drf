from django import template

register = template.Library()


@register.filter("fieldtype")
def fieldtype(field):
    return field.field.widget.__class__.__name__


@register.filter("get_item")
def get_item(dictionary, key):
    return dictionary.get(key)
