from database.models import Module, MetaData, Student
from database.views import is_admin
from django.contrib.auth.models import Group
from django.template import Context, RequestContext

def menubar(request):
    future = []
    past = []
    current = []
    meta = MetaData.objects.get(data_id=1)
    current_year = meta.current_year
    all_modules = Module.objects.all()
    for module in all_modules:
        if request.user in module.instructors.all() or is_admin(request.user):
            if module.year == current_year:
                current.append(module)
            elif module.year > current_year:
                future.append(module)
            elif module.year < current_year:
                past.append(module)
    current.sort(key = lambda x: x.title)
    future.sort(key = lambda x: x.title)
    past.sort(key = lambda x: x.title)
    admins = Group.objects.get(name="admins").user_set.all()
    if request.user in admins:
        admin = True
    else:
        admin = False
    inactive_students = Student.objects.filter(active=False)
    if len(inactive_students) > 0:
        if admin:
            inactive = True
        else:
            inactive = False
    else:
        inactive = False
    alumni_students = Student.objects.filter(year=9)
    if len(alumni_students) > 0:
        alumni = True
    else:
        alumni = False
    not_assigned = Student.objects.filter(year=None)
    if len(not_assigned) > 0:
        unassigned = True
    else:
        unassigned = False
    module_dict = {'current': current, 'past': past, 'future': future}
    return {
            'module_dict': module_dict, 'admin': admin, 'inactive': inactive,
            'alumni': alumni, 'unassigned': unassigned
            }

