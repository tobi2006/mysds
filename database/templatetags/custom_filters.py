from django import template
from django.utils.datastructures import SortedDict

register = template.Library()

@register.filter
def get_directory_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def count_attendance(attendancestring):
    sum = 0
    for week in attendancestring:
        sum = sum + int(week)
    return sum

@register.filter
def only_first_word(longer_string):
    return longer_string.split()[0]

@register.filter(name='sort')
def listsort(value):
        if isinstance(value, dict):
            new_dict = SortedDict()
            key_list = value.keys()
            key_list.sort()
            for key in key_list:
                new_dict[key] = value[key]
            return new_dict
        elif isinstance(value, list):
            new_list = list(value)
            new_list.sort()
            return new_list
        else:
            return value
        listsort.is_safe = True

@register.filter(name='sort_reverse')
def listsort_reverse(value):
        if isinstance(value, dict):
            new_dict = SortedDict()
            key_list = value.keys()
            key_list.sort()
            key_list.reverse()
            for key in key_list:
                new_dict[key] = value[key]
            return new_dict
        elif isinstance(value, list):
            new_list = list(value)
            new_list.sort()
            new_list.reverse()
            return new_list
        else:
            return value
        listsort.is_safe = True
