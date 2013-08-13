from database.models import Module, MetaData
from django.contrib.auth.models import Group

def menubar(request):
    future = []
    past = []
    current = []
    meta = MetaData.objects.get(data_id=1)
    current_year = meta.current_year
    all_modules = Module.objects.all()
    for module in all_modules:
        if module.year == current_year:
            current.append(module)
        elif module.year > current_year:
            if module.year not in future:
                future.append(module.year)
        elif module.year < current_year:
            if module.year not in past:
                past.append(module.year)
    current.sort(key = lambda x: x.title)
    future.sort()
    past.sort()
    admins = Group.objects.get(name="admins").user_set.all()
    if request.user in admins:
        admin = True
    else:
        admin = False
    module_dict = {'current': current, 'past': past, 'future': future}
    return {
            'module_dict': module_dict, 'admin': admin
            }

