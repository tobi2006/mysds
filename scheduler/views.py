from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext

from database.models import Student, Module, MetaData
from database.views import is_admin, is_student, is_teacher
from scheduler.models import *

@login_required
@user_passes_test(is_teacher)
def set_up_appointments(request):
    errors = []
    if request.method == 'POST':
        invitees = request.POST.getlist('selected_student_id')
        if len(invitees) == 0:
            errors.append("No students selected")
        else:
            date_1 = request.POST['slot_1_date']
            if  date_1 == None:
                errors.append("Specify at least one date")
            elif len(date_1.split('/')) != 3:
                errors.append("Enter a valid date")
            else:
                time_from = request.POST['slot_1_from'].split(':')
                hour_from = time_from[0]
                minute_from = time_from[1]

                




            appointment = StudentTeacherAppointment(
                )

        return HttpResponseRedirect()

    all_students = Student.objects.filter(active=True)
    meta_stuff = MetaData.objects.get(data_id=1)
    current_year = meta_stuff.current_year
#    this_years_modules = Module.objects.filter(instructors__in = request.user, year=current_year)
    this_years_modules = request.user.module_set.all()
    rows = []
    current_modules = {} #Only pass the strings for the ones with students on
    for student in all_students:
        entry = {}
        entry['student'] = student
        if student.tutor == request.user:
            entry['tutee'] = True
        modules = ""
        for module in this_years_modules:
            if student in module.student_set.all():
                module_title = module.title + " " + str(module.year)
                module_no_space = module_title.replace(" ", "_")
                module_no_space = module_no_space.lower()
                modules += " " + module_no_space
                module_title += "/" + str(module.year + 1)
                if module_no_space not in current_modules:
                    current_modules[module_no_space] = module_title
                            #                module_string = module.title.replace(" ", "_")
                            #                module_string += "_" + str(module.year)
                            #                modules += " " + module_string
                            #                if module_string not in current_modules:
                            #                    current_modules.append(module_string)
        entry['modules'] = modules
        rows.append(entry)

    return render_to_response('set_up_appointment.html',
            {'rows': rows, 'current_modules': current_modules},
            context_instance=RequestContext(request)
        )
