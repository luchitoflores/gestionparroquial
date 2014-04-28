# -*- coding:utf-8 -*-
from django import template


register = template.Library()

@register.filter(is_safe=True)
def label_tag_attrs(value, arg):
    return value.label_tag(attrs={'class': arg})

