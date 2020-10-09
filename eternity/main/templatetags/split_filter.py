from django import template

register = template.Library()

"""
Добавлен пользовательский фильтр для разделение тегов
через запятую.
"""
@register.filter(name='split')
def split_filter(value):
    return value.split(",")