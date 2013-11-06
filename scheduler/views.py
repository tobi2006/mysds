import datetime
import time

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext

from database.models import Student, Module, MetaData
from database.views import is_admin, is_student, is_teacher
from scheduler.models import *
from scheduler.forms import *

@login_required
@user_passes_test(is_teacher)
def set_up_appointments(request):
    errors = []
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        invitees = request.POST.getlist('selected_student_id') # Do Validation for these in Javascript
        if form.is_valid():
            message = form.cleaned_data['message']
            minutes = int(form.cleaned_data['appointment_length'])
            length = datetime.timedelta(minutes=minutes)
            slots = []
            slot = {}
            slot['date'] = form.cleaned_data['slot_1_date']
            slot['from'] = form.cleaned_data['slot_1_from']
            slot['until'] = form.cleaned_data['slot_1_until']
            slots.append(slot)
            if form.cleaned_data['slot_2_date']:
                slot = {}
                slot['date'] = form.cleaned_data['slot_2_date']
                slot['from'] = form.cleaned_data['slot_2_from']
                slot['until'] = form.cleaned_data['slot_2_until']
                slots.append(slot)
            if form.cleaned_data['slot_3_date']:
                slot = {}
                slot['date'] = form.cleaned_data['slot_3_date']
                slot['from'] = form.cleaned_data['slot_3_from']
                slot['until'] = form.cleaned_data['slot_3_until']
                slots.append(slot)
            if form.cleaned_data['slot_4_date']:
                slot = {}
                slot['date'] = form.cleaned_data['slot_4_date']
                slot['from'] = form.cleaned_data['slot_4_from']
                slot['until'] = form.cleaned_data['slot_4_until']
                slots.append(slot)
            if form.cleaned_data['slot_5_date']:
                slot = {}
                slot['date'] = form.cleaned_data['slot_5_date']
                slot['from'] = form.cleaned_data['slot_5_from']
                slot['until'] = form.cleaned_data['slot_5_until']
                slots.append(slot)
            if form.cleaned_data['slot_6_date']:
                slot = {}
                slot['date'] = form.cleaned_data['slot_6_date']
                slot['from'] = form.cleaned_data['slot_6_from']
                slot['until'] = form.cleaned_data['slot_6_until']
                slots.append(slot)
            for slot in slots:
                date = slot['date']
                slot_start = datetime.datetime.combine(date, slot['from'])
                slot_end = datetime.datetime.combine(date, slot['until'])
                start = slot_start
                while start + length < slot_end:
                    print "From:"
                    print start.time()
                    start += length
                    print "Until:"
                    print start.time()
                    print "---"
            return HttpResponseRedirect('/set_up_appointments')
    else:
        form = AppointmentForm(initial={'appointment_length': 15})
    all_students = Student.objects.filter(active=True)
    meta_stuff = MetaData.objects.get(data_id=1)
    current_year = meta_stuff.current_year
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
        entry['modules'] = modules
        rows.append(entry)

    return render_to_response('set_up_appointment.html',
            {'rows': rows, 'current_modules': current_modules, 'form': form},
            context_instance=RequestContext(request)
        )
