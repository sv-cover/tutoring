"""This module holds tags for the shuffeling of lists in Django templates.

Taken from https://stackoverflow.com/questions/7162629/django-shuffle-in-templates"""
import random
from django import template
register = template.Library()

@register.filter
def shuffle(arg):
    """A function that returns a shuffled copy of a collection."""
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp
