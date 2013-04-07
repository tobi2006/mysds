from database.models import MetaData, Module

def module_dictionary(module_list):
    module_dict={}
    for item in module_list:
        title = item.title
        if title not in module_dict:
            module_dict[title] = [item]
        else:
            module_dict[title].append(item)
    #module_dict.sort()
    for entry in module_dict:
        module_dict[entry].sort(key = lambda x: x.year)
    return module_dict

def modules_for_menubar():
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
    dict_to_return = {'current': current, 'past': past, 'future': future}
    return dict_to_return

