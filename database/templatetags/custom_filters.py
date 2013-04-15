from django import template

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
