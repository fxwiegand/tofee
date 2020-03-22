# -*- coding:utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag
def percentage(part, total):
    """
    get part percentage of total
    """
    print('part:', part, type(part), 'total:', total, type(total))
    return round(part * 100 / total) if total > 0 else 0