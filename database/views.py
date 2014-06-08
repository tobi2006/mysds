import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.utils import simplejson
from django.utils.datastructures import MultiValueDictKeyError

from database import functions
from database.forms import *
from database.models import *
from database.strings import *
from feedback.models import Marksheet
from feedback.categories import AVAILABLE_MARKSHEETS
from mysds.unisettings import *

# Basic functions


def is_teacher(user):
    """Checks if user belongs to group 'teachers'"""
    if user:
        if user.groups.filter(name='teachers').count() == 1:
            return True
        else:
            return False
    else:
        return False


def is_admin(user):
    """Checks if user belongs to group 'admins'"""
    if user:
        if user.groups.filter(name='admins').count() == 1:
            return True
        else:
            return False
    else:
        return False


def is_student(user):
    """Checks if user belongs to group 'students'"""
    if user:
        if user.groups.filter(name='students').count() == 1:
            return True
        else:
            return False
    else:
        return False


def is_pastoral(user):
    """Checks if user belongs to group 'pastoral'"""
    if user:
        if user.groups.filter(name='pastoral').count() == 1:
            return True
        else:
            return False
    else:
        return False


# Module Functions


@login_required
@user_passes_test(is_teacher)
def module_view(request, module_id, year):
    """Displays the overview for the module.

    Shows a summary of all the students in a module with their
    performance information.
    """
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    number_of_groups = 1
    performances = {}
    # Find out which marksheet template for which essay
    feedback = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
    marksheet_exists = {}
    for assessment in range(1, 7):
        marksheet = module.get_marksheet_type(assessment)
        if any(marksheet in available for available in AVAILABLE_MARKSHEETS):
            feedback[assessment] = True
            if (
                    Marksheet.objects.filter(
                        module=module, assessment=assessment).exists()):
                marksheet_exists[assessment] = True
    rows = []
    email_dict = {}
    no_email_addresses = []
    for student in students:
        row = {}
        performance = Performance.objects.get(student=student, module=module)
        if performance.seminar_group > number_of_groups:
            number_of_groups = performance.seminar_group
        row['performance'] = performance
        # Add all email addresses sorted by seminar groups
        if student.email:
            sg = str(performance.seminar_group)
            if sg not in email_dict:
                email_dict[sg] = str(student.email) + ';'
            else:
                email_dict[sg] = email_dict[sg] + str(student.email) + ';'
        else:
            student_name = student.first_name + " " + student.last_name
            no_email_addresses.append(student_name)
        # Check which student did not attend the last session
        last_session = module.sessions_recorded
        row['no_attendance_twice'] = False
        if last_session > 1:
            last_session -= 1
            session_before_last = last_session - 1
            if (performance.attendance[last_session] == '0'
                    and performance.attendance[session_before_last] == '0'):
                row['no_attendance_twice'] = True
        # Check what symbols / links to show next to assessments
        for assessment in range(1, 7):
            row[assessment] = False
            try:
                marksheet = Marksheet.objects.get(
                    student=student, module=module, assessment=assessment)
                if marksheet.comments:
                    row[assessment] = True
            except Marksheet.DoesNotExist:
                pass
        rows.append(row)
    if request.user in module.instructors.all() or is_admin(request.user):
        adminorinstructor = True
    else:
        adminorinstructor = False
    groupstring = ''  # create string of seminar groups to make this iterable
    for i in range(0, number_of_groups):
        groupstring += str(i+1)

    return render_to_response(
        'module_view.html',
        {
            'module': module,
            'rows': rows,
            'email_dict': email_dict,
            'no_email_addresses': no_email_addresses,
            'adminorinstructor': adminorinstructor,
            'feedback': feedback,
            'marksheet_exists': marksheet_exists,
            'number_of_groups': groupstring
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def edit_module(request, module_id, year):
    """Opens and processes an edit form for an existing module"""
    module = Module.objects.get(code=module_id, year=year)
    number_of_assessments = functions.get_number_of_assessments(module)
    if request.method == 'POST':
        form = ModuleForm(instance=module, data=request.POST)
        if form.is_valid():
            form.save()
            assessments_set = int(request.POST['number_of_coursework'])
            if assessments_set < 6:
                module.assessment_6_title = ""
                module.assessment_6_value = None
                if assessments_set < 5:
                    module.assessment_5_title = ""
                    module.assessment_5_value = None
                    if assessments_set < 4:
                        module.assessment_4_title = ""
                        module.assessment_4_value = None
                        if assessments_set < 3:
                            module.assessment_3_title = ""
                            module.assessment_3_value = None
                            if assessments_set < 2:
                                module.assessment_2_title = ""
                                module.assessment_2_value = None
                                if assessments_set < 1:
                                    module.assessment_1_title = ""
                                    module.assessment_1_value = None
                module.sessions_recorded = request.session['sessions_recorded']
                module.save()
                if (request.session['old_number_of_sessions'] !=
                        module.get_number_of_sessions()):
                    performances = Performance.objects.filter(module=module)
                    for performance in performances:
                        attendance = performance.attendance
                        while (len(attendance) <
                                module.get_number_of_sessions()):
                            attendance += '0'
                        while (len(attendance) >
                                module.get_number_of_sessions()):
                            attendance = attendance[:-1]
                        performance.attendance = attendance
                        performance.save()

            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = ModuleForm(instance=module)
        request.session['old_number_of_sessions'] = (
            module.get_number_of_sessions())
        request.session['sessions_recorded'] = (
            module.sessions_recorded)

    return render_to_response(
        'module_form.html',
        {'module_form': form, 'add': False, 'object': module,
            'assessments': number_of_assessments},
        context_instance=RequestContext(request)
    )


@login_required
@user_passes_test(is_teacher)
def add_module(request):
    """Shows a form to add a new module"""
    assessments = 0
    if request.is_ajax():
        if 'successor_of' not in request.POST:
            year = int(request.POST['year'])
            predecessor_year = year - 1
            predecessor_modules = Module.objects.filter(year=predecessor_year)
            new_options = (
                '<option value="" ' +
                'selected="selected">---------</option>\n'
                )
            for module in predecessor_modules:
                toadd = (
                    '<option value="' +
                    str(module.id) +
                    '">' +
                    str(module) +
                    '</option>\n'
                    )
                new_options += toadd
            return HttpResponse(new_options)
        else:
            successor_of = int(request.POST['successor_of'])
            predecessor = Module.objects.get(id=successor_of)
            suggestions = {}
            suggestions['title'] = predecessor.title
            suggestions['code'] = predecessor.code
            suggestions['credits'] = predecessor.credits
            suggestions['first_session'] = predecessor.first_session
            suggestions['last_session'] = predecessor.last_session
            suggestions['no_teaching_in'] = predecessor.no_teaching_in
            eligible = ''
            for entry in Module.ELIGIBLE:
                if entry[0] == predecessor.eligible:
                    eligible += (
                        '<option value="' +
                        entry[0] +
                        '" selected="selected">' +
                        entry[1] +
                        '</option>\n'
                        )
                else:
                    eligible += (
                        '<option value="' +
                        entry[0] +
                        '">' +
                        entry[1] +
                        '</option>\n'
                        )
            suggestions['eligible'] = eligible
            suggestions['is_foundational'] = predecessor.is_foundational
            suggestions['is_pg'] = predecessor.is_pg
            if predecessor.assessment_6_value:
                no_of_assessments = 6
            elif predecessor.assessment_5_value:
                no_of_assessments = 5
            elif predecessor.assessment_4_value:
                no_of_assessments = 4
            elif predecessor.assessment_3_value:
                no_of_assessments = 3
            elif predecessor.assessment_2_value:
                no_of_assessments = 2
            elif predecessor.assessment_1_value:
                no_of_assessments = 1
            else:
                no_of_assessments = 0
            assessments = ""
            endcounter = no_of_assessments + 1
            counter = 1
            while counter < endcounter:
                if counter == 1:
                    title = predecessor.assessment_1_title
                    value = str(predecessor.assessment_1_value)
                elif counter == 2:
                    title = predecessor.assessment_2_title
                    value = str(predecessor.assessment_2_value)
                elif counter == 3:
                    title = predecessor.assessment_3_title
                    value = str(predecessor.assessment_3_value)
                elif counter == 4:
                    title = predecessor.assessment_4_title
                    value = str(predecessor.assessment_4_value)
                elif counter == 5:
                    title = predecessor.assessment_5_title
                    value = str(predecessor.assessment_5_value)
                elif counter == 6:
                    title = predecessor.assessment_6_title
                    value = str(predecessor.assessment_6_value)
                count = str(counter)
                assessments += (
                    '<tr><td><strong>Assessment ' +
                    count +
                    ':</strong></td>\n <td>Title</td><td>\n ' +
                    '<input id="id_assessment_' +
                    count +
                    '_title" maxlength="30" name="assessment_' +
                    count +
                    '_title" type="text" value="' +
                    title +
                    '" /></td>\n <td>Percentage</td><td>\n ' +
                    '<input id="id_assessment_' +
                    count +
                    '_value" name="assessment_' +
                    count +
                    '_value" type="text" value="' +
                    value +
                    '" /></tr>'
                    )
                counter += 1
            suggestions['number_of_assessments'] = no_of_assessments
            suggestions['assessments'] = assessments
            if predecessor.exam_value:
                suggestions['exam'] = predecessor.exam_value
        json = simplejson.dumps(suggestions)
        return HttpResponse(json, mimetype='application/json')
    if request.method == 'POST':
        form = ModuleForm(data=request.POST)
        if form.is_valid():
            module = form.save()
            assessments_set = int(request.POST['number_of_coursework'])
            if assessments_set < 6:
                module.assessment_6_title = ""
                module.assessment_6_value = None
                if assessments_set < 5:
                    module.assessment_5_title = ""
                    module.assessment_5_value = None
                    if assessments_set < 4:
                        module.assessment_4_title = ""
                        module.assessment_4_value = None
                        if assessments_set < 3:
                            module.assessment_3_title = ""
                            module.assessment_3_value = None
                            if assessments_set < 2:
                                module.assessment_2_title = ""
                                module.assessment_2_value = None
                                if assessments_set < 1:
                                    module.assessment_1_title = ""
                                    module.assessment_1_value = None
            module.save()
            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = ModuleForm()
    return render_to_response(
        'module_form.html',
        {'module_form': form, 'add': True,
            'assessments': assessments},
        context_instance=RequestContext(request)
    )


@login_required
@user_passes_test(is_teacher)
def delete_module(request, module_id, year):
    """Deletes a module"""
    module = Module.objects.get(code=module_id, year=year)
    if request.user in module.instructors.all() or is_admin(request.user):
        performances = Performance.objects.filter(module=module)
        for performance in performances:
            performance.delete()
        module.delete()
        printstring = 'Module deleted'
        title = 'Module deleted'
    else:
        printstring = (
            'Only the module instructors or an ' +
            'admin can delete this module'
            )
        title = 'CCCU Law DB: Not allowed'
    return render_to_response(
        'blank.html',
        {'printstring': printstring, 'title': title},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(is_teacher)
def remove_student_from_module(request, module_id, year, student_id):
    """Removes student from module, deletes performance object"""
    module = Module.objects.get(code=module_id, year=year)
    student = Student.objects.get(student_id=student_id)
    performance = Performance.objects.get(module=module, student=student)
    performance.delete()
    student.modules.remove(module)
    return HttpResponseRedirect(module.get_absolute_url())


@login_required
@user_passes_test(is_teacher)
def seminar_group_overview(request, code, year):
    """Gives a nice overview of seminar groups"""
    module = Module.objects.get(code=code, year=year)
    performances = Performance.objects.filter(module=module)
    number_of_groups = 0
    printstring = "<h2>Seminar Group Overview</h2><br><br>"
    title = "Seminar Group Overview"
    for performance in performances:
        if performance.seminar_group > number_of_groups:
            number_of_groups = performance.seminar_group
    for group in range(0, number_of_groups):
        seminar_group = group + 1
        performances = Performance.objects.filter(
            module=module, seminar_group=seminar_group)
        printstring += (
            "<h3>Seminar Group " +
            str(seminar_group) +
            "</h3><br><br>"
            )
        for performance in performances:
            printstring += (
                performance.student.first_name +
                " " +
                performance.student.last_name +
                "<br>"
                )
        printstring += "<br><br>"

    return render_to_response(
        'blank.html',
        {'printstring': printstring, 'title': title},
        context_instance=RequestContext(request))


@login_required
@user_passes_test(is_teacher)
def toggle_assessment_availability(request, code, year, assessment):
    """Allows students to see their marksheets"""
    module = Module.objects.get(code=code, year=year)
    if assessment == '1':
        if module.assessment_1_available:
            module.assessment_1_available = False
        else:
            module.assessment_1_available = True
    elif assessment == '2':
        if module.assessment_2_available:
            module.assessment_2_available = False
        else:
            module.assessment_2_available = True
    elif assessment == '3':
        if module.assessment_3_available:
            module.assessment_3_available = False
        else:
            module.assessment_3_available = True
    elif assessment == '4':
        if module.assessment_4_available:
            module.assessment_4_available = False
        else:
            module.assessment_4_available = True
    elif assessment == '5':
        if module.assessment_5_available:
            module.assessment_5_available = False
        else:
            module.assessment_5_available = True
    elif assessment == '6':
        if module.assessment_6_available:
            module.assessment_6_available = False
        else:
            module.assessment_6_available = True
    module.save()
    return HttpResponseRedirect(module.get_absolute_url())


@login_required
@user_passes_test(is_teacher)
def address_nines(request, code, year):
    """Allows teachers to change marks when the average ends with 9"""
    module = Module.objects.get(code=code, year=year)
    performances_in_module = Performance.objects.filter(module=module)
    performances = []
    for performance in performances_in_module:
        tmp = str(performance.average)
        if tmp[-1] == '9':
            performances.append(performance)
    if request.method == 'POST':
        for performance in performances:
            student_id = performance.student.student_id
            assessment = student_id + '_1'
            if assessment in request.POST:
                try:
                    mark = int(request.POST[assessment])
                    if mark in range(0, 100):
                        performance.assessment_1 = mark
                except ValueError:
                    pass
            assessment = student_id + '_2'
            if assessment in request.POST:
                try:
                    mark = int(request.POST[assessment])
                    if mark in range(0, 100):
                        performance.assessment_2 = mark
                except ValueError:
                    pass
            assessment = student_id + '_3'
            if assessment in request.POST:
                try:
                    mark = int(request.POST[assessment])
                    if mark in range(0, 100):
                        performance.assessment_3 = mark
                except ValueError:
                    pass
            assessment = student_id + '_4'
            if assessment in request.POST:
                try:
                    mark = int(request.POST[assessment])
                    if mark in range(0, 100):
                        performance.assessment_4 = mark
                except ValueError:
                    pass
            assessment = student_id + '_5'
            if assessment in request.POST:
                try:
                    mark = int(request.POST[assessment])
                    if mark in range(0, 100):
                        performance.assessment_5 = mark
                except ValueError:
                    pass
            assessment = student_id + '_6'
            if assessment in request.POST:
                try:
                    mark = int(request.POST[assessment])
                    if mark in range(0, 100):
                        performance.assessment_6 = mark
                except ValueError:
                    pass
            assessment = student_id + '_exam'
            if assessment in request.POST:
                try:
                    mark = int(request.POST[assessment])
                    if mark in range(0, 100):
                        performance.exam = mark
                except ValueError:
                    pass
            performance.save_with_avg()
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
        'address_nines.html',
        {'module': module, 'performances': performances},
        context_instance=RequestContext(request)
    )


# Student Functions


@login_required
@user_passes_test(is_teacher)
def student_view(request, student_id, meeting_id=None):
    """Shows all information about a student.

    If the person looking at this is the personal tutor of the student,
    he / she will also see the meeting records and a form to enter new
    meeting records. Members of the 'pastoral' group responsible for
    the oversight of the tutor system will see the records but will
    not get the form. If a meeting_id is given, this will switch to
    edit that record.
    """
    student = Student.objects.get(student_id=student_id)
    tutor = False
    pastoral = False

    if student.tutor == request.user:
        tutor = True
        tutee_sessions = Tutee_Session.objects.filter(tutee=student)
        if meeting_id:
            tutee_session = Tutee_Session.objects.get(id=meeting_id)
            edit = meeting_id
        else:
            tutee_session = Tutee_Session(tutee=student, tutor=request.user)
            edit = False
        if request.method == 'POST':
            form = TuteeForm(instance=tutee_session, data=request.POST)
            if form.is_valid():
                if meeting_id:
                    to_delete = Tutee_Session.objects.get(id=meeting_id)
                    to_delete.delete()
                form.save()
                url = student.get_absolute_url()
                return HttpResponseRedirect(url)
        else:
            form = TuteeForm(instance=tutee_session)
    elif is_pastoral(request.user):
        pastoral = True
        tutee_sessions = Tutee_Session.objects.filter(tutee=student)

    all_performances = Performance.objects.filter(student=student)
    sorted_performances = {}
    for performance in all_performances:
        use_performance = False
        if performance.module.sessions_recorded is not None:
            use_performance = True
        elif performance.assessment_1:
            use_performance = True
        elif performance.assessment_2:
            use_performance = True
        elif performance.assessment_3:
            use_performance = True
        elif performance.assessment_4:
            use_performance = True
        elif performance.assessment_5:
            use_performance = True
        elif performance.assessment_6:
            use_performance = True
        elif performance.exam:
            use_performance = True
        if use_performance:
            year = performance.module.year
            if sorted_performances.get(year):
                sorted_performances[year].append(performance)
            else:
                sorted_performances[year] = [performance]

    if tutor:
        return render_to_response(
            'student_view.html',
            {
                'form': form,
                'student': student,
                'years_performances': sorted_performances,
                'tutor': True,
                'show_meeting_notes': True,
                'edit': edit,
                'meetings': tutee_sessions,
                'mdexplanation': MD_EXPLANATION
            },
            context_instance=RequestContext(request)
            )
    elif pastoral:
        return render_to_response(
            'student_view.html',
            {
                'student': student,
                'years_performances': sorted_performances,
                'show_meeting_notes': True,
                'meetings': tutee_sessions
            },
            context_instance=RequestContext(request)
            )
    else:
        return render_to_response(
            'student_view.html',
            {
                'student': student,
                'years_performances': sorted_performances
            },
            context_instance=RequestContext(request)
            )


@login_required
@user_passes_test(is_teacher)
def search_student(request):
    """Little search function. Needs to be replaced with AJAX"""
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        students = []
        if len(q) > 1:
            if "," in q:
                search = q.split(",")
                first_name = search[-1].strip()
                last_name = search[0].strip()
            else:
                search = q.split()
                first_name = search[0]
                last_name = search[-1]
            students = Student.objects.filter(
                last_name__icontains=last_name,
                first_name__icontains=first_name
                )
        if len(students) == 0:
            students = Student.objects.filter(
                Q(last_name__istartswith=q) | Q(first_name__istartswith=q))
        if len(students) == 1:
            student = students[0]
            return HttpResponseRedirect(student.get_absolute_url())
        else:
            return render_to_response(
                'search_results.html',
                {'students': students, 'query': q},
                context_instance=RequestContext(request)
                )
    else:
        return HttpResponse('Please submit a search term.')


@login_required
@user_passes_test(is_teacher)
def year_view(request, year):
    """Shows all students in a particular year and allows bulk changes"""
    if request.method == 'POST':
        students_to_add = request.POST.getlist('selected_student_id')
        selected_option = request.POST.__getitem__('modify')
        selected = selected_option.split('_')
        if selected[0] == 'tutor':
            tutor = User.objects.get(id=selected[1])
            for student_id in students_to_add:
                student = Student.objects.get(student_id=student_id)
                student.tutor = tutor
                student.save()
        elif selected[0] == 'qld':
            if selected[1] == 'on':
                for student_id in students_to_add:
                    student = Student.objects.get(student_id=student_id)
                    student.qld = True
                    student.save()
            elif selected[1] == 'off':
                for student_id in students_to_add:
                    student = Student.objects.get(student_id=student_id)
                    student.qld = False
                    student.save()
        elif selected[0] == 'nalp':
            if selected[1] == 'on':
                for student_id in students_to_add:
                    student = Student.objects.get(student_id=student_id)
                    student.nalp = True
                    student.save()
            elif selected[1] == 'off':
                for student_id in students_to_add:
                    student = Student.objects.get(student_id=student_id)
                    student.nalp = False
                    student.save()
        elif selected[0] == 'course':
            course = Course.objects.get(title=selected[1])
            for student_id in students_to_add:
                student = Student.objects.get(student_id=student_id)
                student.course = course
                student.save()
        elif selected[0] == 'since':
            startyear = selected[1]
            for student_id in students_to_add:
                student = Student.objects.get(student_id=student_id)
                student.since = startyear
                student.save()
        elif selected[0] == 'year':
            for student_id in students_to_add:
                student = Student.objects.get(student_id=student_id)
                student.year = selected[1]
                student.save()
        elif selected[0] == 'active':
            if selected[1] == 'yes':
                for student_id in students_to_add:
                    student = Student.objects.get(student_id=student_id)
                    student.active = True
                    student.save()
            elif selected[1] == 'no':
                for student_id in students_to_add:
                    student = Student.objects.get(student_id=student_id)
                    student.active = False
                    student.save()
        elif selected[0] == 'delete':
            if selected[1] == 'yes':
                for student_id in students_to_add:
                    student = Student.objects.get(student_id=student_id)
                    performances = Performance.objects.filter(student=student)
                    for performance in performances:
                        performance.delete()
                    tutee_sessions = Tutee_Session.objects.filter(
                        tutee=student)
                    for tutee_session in tutee_sessions:
                        tutee_session.delete()
                    student.delete()
            if selected[1] == 'no':
                pass
        url = '/year/' + year
        return HttpResponseRedirect(url)

    if year == "all":
        students = Student.objects.all()
    elif year == "unassigned":
        students = Student.objects.filter(year=None)
    elif year == "inactive":
        students = Student.objects.filter(active=False)
    else:
        students = Student.objects.filter(year=year)

    ug = False
    pg = False
    phd = False
    alumnus = False
    more_than_one_year = False
    inactive = False
    unassigned = False
    if year == "all":
        ug = True
        more_than_one_year = True
    elif year == "unassigned":
        unassigned = True
    elif year == "inactive":
        inactive = True
    else:
        if int(year) < 4:
            ug = True
        elif int(year) == 7:
            pg = True
        elif int(year) == 8:
            phd = True
        elif int(year) == 9:
            alumnus = True

    academic_years = []
    meta_stuff = MetaData.objects.get(data_id=1)
    current_year = meta_stuff.current_year
    latest_start_year = current_year + 2
    for academic_year in ACADEMIC_YEARS:
        if academic_year[0] < latest_start_year:
            academic_years.append(academic_year[0])
    llb = Course.objects.get(title="LLB (Hons) Bachelor Of Law")
    all_students = len(students)

    if ug or alumnus or unassigned or inactive:
        courses = Course.objects.all

    tutors = User.objects.filter(groups__name='teachers')
    return render_to_response(
        'year_view.html',
        {
            'students': students,
            'year': year,
            'ug': ug,
            'pg': pg,
            'phd': phd,
            'alumnus': alumnus,
            'llb': llb,
            'more_than_one_year': more_than_one_year,
            'tutors': tutors,
            'academic_years': academic_years,
            'courses': courses,
            'all_students': all_students,
            'show_inactive': inactive
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_admin)
def all_attendances(request, year):
    """Shows all assessments per year."""
    year = int(year)
    students = Student.objects.filter(year=year, active=True)
    all_attendances = {}
    meta_stuff = MetaData.objects.get(data_id=1)
    current_year = meta_stuff.current_year
    all_rows = []
    for student in students:
        modules = student.modules.all()
        for module in modules:
            if module.year == current_year:
                email_string = '<a href="mailto:' + student.email
                email_string += (
                    '?Subject=Attendance for ' + module.title + '">')
                email_string += (
                    '<span class="glyphicon glyphicon-envelope">' +
                    '</span></a>'
                    )
                url = student.get_absolute_url()
                student_string = (
                    '<a href="' +
                    url +
                    '">' +
                    student.last_name +
                    ', ' +
                    student.first_name +
                    '</a>'
                    )
                url = module.get_absolute_url()
                module_string = (
                    '<a href="' +
                    url +
                    '">' +
                    module.title +
                    ' (' +
                    module.code +
                    ')</a>'
                    )
                row = [email_string, student_string, module_string]
                performance = Performance.objects.get(
                    student=student, module=module)
                attendance_list = performance.attendance
                attendance = []
                no_teaching = []
                tmp = module.no_teaching_in.split(',')
                for item in tmp:
                    try:
                        no_teaching.append(int(item))
                    except ValueError:  # Ignore whitespace or wrong entries
                        pass
                first = int(module.first_session)
                counter = 0
                for week in range(5, 30):
                    attendance = 'NT'  # No teaching
                    if week >= first:
                        week_no = counter + 1
                        if week_no <= module.sessions_recorded:
                            if week not in no_teaching:
                                attendance = attendance_list[counter]
                                counter += 1
                    row.append(attendance)
                all_rows.append(row)

    return render_to_response(
        'all_attendances.html',
        {'all_rows': all_rows},
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def tutee_list(request):
    """Lists all tutees with warning info"""
    tutees = Student.objects.filter(tutor=request.user)
    email_addresses = ""
    no_email_addresses = []
    problem_students = {}
    meta_stuff = MetaData.objects.get(data_id=1)
    current_year = meta_stuff.current_year
    for tutee in tutees:
        if tutee.email:
            email_addresses += tutee.email + ";"
        else:
            name = tutee.first_name + " " + tutee.last_name
            no_email_addresses.append(name)
        # Check if there are any issues the tutor should see in the overview
        performances = Performance.objects.filter(student=tutee)
        problems = []
        for performance in performances:
            module = performance.module
            if module.year == current_year:
                last_session = module.sessions_recorded
                if last_session > 1:
                    last_session -= 1
                    session_before_last = last_session - 1
                    if (
                            performance.attendance[last_session] == '0'
                            and performance.attendance[session_before_last] ==
                            '0'
                    ):
                        problemstring = (
                            "Did not attend at least the last two " +
                            "sessions in " +
                            module.title
                            )
                        problems.append(problemstring)
            if module.is_foundational and tutee.qld:
                for assessment in range(1, 7):
                    if (performance.get_assessment_result(assessment)
                            is not None):
                        if (performance.get_assessment_result(assessment) <
                                PASSMARK):
                            problemstring = (
                                "Failed " +
                                module.get_assessment_title(assessment) +
                                " for " +
                                module.title
                                )
                            problems.append(problemstring)
                if performance.exam:
                    if performance.exam < PASSMARK:
                        problemstring = "Failed the exam for " + module.title
                        problems.append(problemstring)
            if performance.average_makes_sense():
                if performance.average:
                    if performance.average < PASSMARK:
                        problemstring = "Failed " + module.title
                        problems.append(problemstring)
        if len(problems) > 0:
            problem_students[tutee] = problems

    return render_to_response(
        'tutee_list.html',
        {
            'tutees': tutees,
            'email_addresses': email_addresses,
            'no_email_addresses': no_email_addresses,
            'problem_students': problem_students
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def delete_tutee_meeting(request, meeting_id):
    """Deletes the record of a meeting"""
    meeting = Tutee_Session.objects.get(id=meeting_id)
    if request.user == meeting.tutor or is_admin(request.user):
        tutee = meeting.tutee
        url = tutee.get_absolute_url()
        meeting.delete()
        return HttpResponseRedirect(url)
    else:
        printstring = (
            'Only the tutor in question or an administrator ' +
            'can delete this.'
            )
        title = 'CCCU Law DB: Not allowed'
        return render_to_response(
            'blank.html',
            {'printstring': printstring, 'title': title},
            context_instance=RequestContext(request))


@login_required
@user_passes_test(is_admin)
def all_tutees(request, year):
    """Gives an overview of all tutee meetings for a year"""
    students = Student.objects.filter(year=year)
    tutee_dict = {}
    most_sessions = 0
    for student in students:
        sessions = []
        try:
            tutee_sessions = Tutee_Session.objects.filter(tutee=student)
            for session in tutee_sessions:
                sessions.append(session)
        except Tutee_Session.DoesNotExist:
            pass
        if len(sessions) > most_sessions:
            most_sessions = len(sessions)
        tutee_dict[student] = sessions
    return render_to_response(
        'all_tutees.html',
        {
            'year': year,
            'tutee_dict': tutee_dict,
            'most_sessions': most_sessions
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def add_student(request):
    """Displays and processes a form to add a student"""
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if form.is_valid():
            student = form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = StudentForm()
    return render_to_response(
        'student_form.html',
        {'student_form': form, 'add': True},
        context_instance=RequestContext(request)
    )


@login_required
@user_passes_test(is_teacher)
def edit_student(request, student_id):
    """Displays and processes a form to edit a student"""
    student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = StudentForm(instance=student)
    return render_to_response(
        'student_form.html',
        {'student_form': form, 'add': False, 'student': student},
        context_instance=RequestContext(request)
    )


@login_required
@user_passes_test(is_teacher)
def mark(request, module_id, year, assessment):
    """Simple mark form (only marks, no feedback)"""
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    performances = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        student_name = student.last_name + ", " + student.first_name
        performances[student_name] = performance
    if request.method == 'POST':
        students = module.student_set.all()
        for student in students:
            if student.student_id in request.POST:
                tmp = request.POST[student.student_id]
                try:
                    mark = int(tmp)
                    if mark in range(0, 100):
                        performance = Performance.objects.get(
                            student=student, module=module)
                        if (mark !=
                                performance.get_assessment_result(assessment)):
                            performance.set_assessment_result(assessment, mark)
                except ValueError:
                    pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
        'mark.html',
        {
            'current_module': module,
            'performances': performances,
            'to_mark': assessment
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def attendance(request, module_id, year, group):
    """Displays and processes attendance record for a group"""
    module = Module.objects.get(code=module_id, year=year)
    no_of_sessions = range(module.get_number_of_sessions())
    students = module.student_set.all()
    if group == "all":
        students_in_group = students
        seminar_group = None
    else:
        seminar_group = group
        students_in_group = []
        for student in students:
            performance = Performance.objects.get(
                student=student, module=module)
            if performance.seminar_group == int(group):
                students_in_group.append(student)
    if request.method == 'POST':
        last_session = 0
        for student in students_in_group:
            performance = Performance.objects.get(
                student=student, module=module)
            counter = 0
            attendance = ""
            while counter < module.get_number_of_sessions():
                key = student.student_id + '_' + str(counter)
                try:
                    session_attendance = request.POST[key]
                    if session_attendance == 'p':
                        attendance = attendance + "1"
                        week_number = counter + 1
                        if week_number > last_session:
                            last_session = week_number
                    elif session_attendance == 'e':
                        attendance = attendance + "e"
                        week_number = counter + 1
                        if week_number > last_session:
                            last_session = week_number
                    else:
                        attendance = attendance + "0"
                except MultiValueDictKeyError:
                    attendance = attendance + "0"
                counter += 1
            performance.attendance = attendance
            performance.save()
        module.sessions_recorded = last_session
        module.save()
        return HttpResponseRedirect(module.get_absolute_url())
    else:
        header = []
        last_week = module.last_session + 1
        no_teaching = module.no_teaching_in.split(",")
        for week in range(module.first_session, last_week):
            strweek = str(week)
            if strweek not in no_teaching:
                header.append(strweek)
        attendances = {}
        for student in students_in_group:
            performance = Performance.objects.get(
                student=student, module=module)
            attendance = {}
            counter = 0
            for session in performance.attendance:
                if session == "1":
                    attendance[counter] = 'p'
                elif session == 'e':
                    attendance[counter] = 'e'
                else:
                    attendance[counter] = 'a'
                counter += 1
            attendances[student] = attendance

    return render_to_response(
        'attendance.html',
        {
            'module': module,
            'attendances': attendances,
            'seminar_group': seminar_group,
            'sessions': no_of_sessions,
            'header': header
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def seminar_groups(request, module_id, year):
    """Form to assign seminar groups"""
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    performances = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        performances[student] = performance
    random_options = {}
    for i in range(1, 10):
        # Up to 10 Seminar groups. Create a dictionary that lists the options
        # and the maximum number of students per group
        all = len(students)
        number = all / i
        left = all % i
        if left > 0:
            number = number + 1
        random_options[i] = number

    if request.method == 'POST':
        for student in students:
            if student.student_id in request.POST:
                tmp = request.POST[student.student_id]
                try:
                    seminar_group = int(tmp)
                    if seminar_group in range(0, 99):
                        performance = Performance.objects.get(
                            student=student, module=module)
                        performance.seminar_group = seminar_group
                        performance.save()
                except ValueError:
                        pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
        'seminar_groups.html',
        {
            'module': module,
            'performances': performances,
            'random_options': random_options
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def assessment_groups(request, module_id, year):
    """Allows to set assessment groups as well"""
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    if request.method == 'POST':
        for student in students:
            tmp = request.POST[student.student_id]
            group = int(tmp)
            performance = Performance.objects.get(
                student=student, module=module)
            if group == 0:
                performance.group_assessment_group = None
            else:
                performance.group_assessment_group = group
            performance.save()
        return HttpResponseRedirect(module.get_absolute_url())
    dictionary = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        if performance.group_assessment_group is None:
            group = "0"
        else:
            group = str(performance.group_assessment_group)
        if group in dictionary:
            dictionary[group].append(performance)
        else:
            dictionary[group] = [performance]
    no_of_students = len(students)
    max_groups = no_of_students / 2
    left = no_of_students % 2
    if left == 1:
        max_groups += 1

    return render_to_response(
        'assessment_groups.html',
        {
            'module': module,
            'dictionary': dictionary,
            'max_groups': max_groups
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def lsp_view(request, student_id):
    """Show the Learning Support Plan for a student"""

    student = Student.objects.get(student_id=student_id)
    edit = False
    return render_to_response(
        'lsp.html',
        {'student': student, 'edit': edit},
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def lsp_edit(request, student_id):
    """Allows to edit the Learning Support Plan for a student"""
    student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        form = LSPForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = LSPForm(instance=student)
    return render_to_response(
        'lsp.html',
        {
            'form': form,
            'student': student,
            'edit': True,
            'mdexplanation': MD_EXPLANATION
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def notes_edit(request, student_id):
    """Allows to edit the Notes for a student """
    student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        form = NotesForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = NotesForm(instance=student)
    return render_to_response(
        'student_notes.html',
        {
            'form': form,
            'student': student,
            'edit': True,
            'mdexplanation': MD_EXPLANATION
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def add_students_to_module(request, module_id, year):
    """Adds students to a module, creates performance"""
    module = Module.objects.get(code=module_id, year=year)
    llb = Course.objects.get(title="LLB (Hons) Bachelor Of Law")
    students_in_module = module.student_set.all()
    if len(module.eligible) > 1:
        more_than_one_year = True
    else:
        more_than_one_year = False
    students = []
    eligible = []
    years = []
    if module.is_pg:
        students_from_db = Student.objects.filter(year__gt=3, year__lt=9)
    else:
        students_from_db = Student.objects.filter(year__lte=3)
    for number in module.eligible:
        year = int(number)  # Find out which students are eligible
        meta_stuff = MetaData.objects.get(data_id=1)
        current_year = meta_stuff.current_year
        time_difference = module.year - current_year
        year = year - time_difference
        years.append(year)
    for student in students_from_db:
        if student not in students_in_module:
            students.append(student)
        if student.year in years:
            eligible.append(student.student_id)

    if request.method == 'POST':
        students_to_add = request.POST.getlist('selected_student_id')
        for student_id in students_to_add:
            student_to_add = Student.objects.get(student_id=student_id)
            student_to_add.modules.add(module)
            # Generate Performance entry for the student
            performance = Performance(
                student=student_to_add,
                module=module
                )
            performance.initial_save()

        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
        'add_students_to_module.html',
        {
            'module': module,
            'more_than_one_year': more_than_one_year,
            'students': students,
            'llb': llb,
            'eligible': eligible
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def parse_csv(request):
    """Parses CSV Files with Student data, creates / amends Students"""
    importdata = request.session.get('csv_data')
    table = []
    for line in importdata:
        row = line.split(',')
        table.append(row)
    first_row = table[0]
    no_of_columns = len(first_row)
    if request.method == "POST":
        form = CSVParseForm(request.POST)
        if form.is_valid():
            list_of_columns = []
            if no_of_columns > 0:
                list_of_columns.append(form.cleaned_data['column_1'])
                if no_of_columns > 1:
                    list_of_columns.append(form.cleaned_data['column_2'])
                if no_of_columns > 2:
                    list_of_columns.append(form.cleaned_data['column_3'])
                if no_of_columns > 3:
                    list_of_columns.append(form.cleaned_data['column_4'])
                if no_of_columns > 4:
                    list_of_columns.append(form.cleaned_data['column_5'])
                if no_of_columns > 5:
                    list_of_columns.append(form.cleaned_data['column_6'])
                if no_of_columns > 6:
                    list_of_columns.append(form.cleaned_data['column_7'])
                if no_of_columns > 7:
                    list_of_columns.append(form.cleaned_data['column_8'])
                if no_of_columns > 8:
                    list_of_columns.append(form.cleaned_data['column_9'])
                if no_of_columns > 9:
                    list_of_columns.append(form.cleaned_data['column_10'])
                if no_of_columns > 10:
                    list_of_columns.append(form.cleaned_data['column_11'])
                if no_of_columns > 11:
                    list_of_columns.append(form.cleaned_data['column_12'])
                if no_of_columns > 12:
                    list_of_columns.append(form.cleaned_data['column_13'])
                if no_of_columns > 13:
                    list_of_columns.append(form.cleaned_data['column_14'])
                if no_of_columns > 14:
                    list_of_columns.append(form.cleaned_data['column_15'])
            successful_entrys = 0
            item_in_table = 0
            ignore_students = request.POST.getlist('exclude')
            for row in table:
                item_in_table += 1
                if str(item_in_table) not in ignore_students:
                    result = {}
                    counter = 0
                    for entry in row:
                        column = list_of_columns[counter]
                        if column != 'ignore':
                            result[column] = entry
                        counter += 1
                    try:
                        current = Student.objects.get(
                            student_id=result['student_id'])
                        if 'first_name' in result:
                            current.first_name = result['first_name']
                        if 'last_name' in result:
                            current.last_name = result['last_name']
                        if 'since' in result:
                            current.since = result['since']
                        if 'year' in result:
                            tmp = result['year']
                            current.year = int(tmp[0])
                        if 'is_part_time' in result:
                            current.is_part_time = result['is_part_time']
                        if 'phone_no' in result:
                            current.phone_no = result['phone_no']
                        if 'email' in result:
                            current.email = result['email']
                        if 'course' in result:
                            parse_result = (
                                result['course'].split("-")[-1].strip())
                            courses = Course.objects.filter(title=parse_result)
                            if courses:
                                course = courses[0]
                                current.course = course
                            else:
                                new_course = Course(title=parse_result)
                                new_course.save()
                                current.course = new_course
                        if 'qld' in result:
                            current.qld = result['qld']
                        if 'tutor' in result:
                            tutor_results = User.objects.filter(
                                name=result['tutor'])
                            tutor = tutors[0]
                            current.tutor = tutor
                        if 'notes' in result:
                            current.notes = (
                                current.notes + '\n' + result['notes'])
                        if 'lsp' in result:
                            current.lsp = result['lsp']
                        if 'permanent_email' in result:
                            current.permanent_email = result['permanent_email']
    #                    if 'achieved_grade' in result:
    #                        current.achieved_grade = result['achieved_grade']
                        change_address = False
                        if 'address1' in result:
                            change_address = True
                        if 'address2' in result:
                            change_address = True
                        if 'address3' in result:
                            change_address = True
                        if 'address4' in result:
                            change_address = True
                        if 'address5' in result:
                            change_address = True
                        if change_address:
                            current.address = ""
                            if 'address1' in result:
                                current.address += result['address1'] + "\n"
                            if 'address2' in result:
                                current.address += result['address2'] + "\n"
                            if 'address3' in result:
                                current.address += result['address3'] + "\n"
                            if 'address4' in result:
                                current.address += result['address4'] + "\n"
                            if 'address5' in result:
                                current.address += result['address5']
                        change_home_address = False
                        if 'home_address1' in result:
                            change_home_address = True
                        if 'home_address2' in result:
                            change_home_address = True
                        if 'home_address3' in result:
                            change_home_address = True
                        if 'home_address4' in result:
                            change_home_address = True
                        if 'home_address5' in result:
                            change_home_address = True
                        if change_home_address:
                            current.home_address = ""
                            if 'home_address1' in result:
                                current.home_address += (
                                    result['home_address1'] + "\n")
                            if 'home_address2' in result:
                                current.home_address += (
                                    result['home_address2'] + "\n")
                            if 'home_address3' in result:
                                current.home_address += (
                                    result['home_address3'] + "\n")
                            if 'home_address3' in result:
                                current.home_address += (
                                    result['home_address4'] + "\n")
                            if 'home_address5' in result:
                                current.home_address += (
                                    result['home_address5'] + "\n")
                        current.save()

                    except Student.DoesNotExist:  # Enter new student
                        if 'first_name' not in result:
                            result['first_name'] = ""
                        if 'last_name' not in result:
                            result['last_name'] = ""
                        if 'since' not in result:
                            result['since'] = ""
                        if 'year' not in result:
                            result['year'] = None
                        else:
                            tmp = result['year']
                            result['year'] = int(tmp[0])
                        if 'is_part_time' not in result:
                            result['is_part_time'] = False
                        if 'email' not in result:
                            result['email'] = ""
                        if 'phone_no' not in result:
                            result['phone_no'] = ""
                        if 'course' not in result:
                            result['course'] = None
                        else:
                            parse_result = (
                                result['course'].split("-")[-1].strip())
                            courses = Course.objects.filter(title=parse_result)
                            if courses:
                                course = courses[0]
                                result['course'] = course
                            else:
                                new_course = Course(title=parse_result)
                                new_course.save()
                                result['course'] = new_course
                        result['modules'] = ""
                        if 'qld' not in result:
                            result['qld'] = False
                        if 'tutor' not in result:
                            result['tutor'] = None
                        else:
                            tutors = User.objects.filter(name=result['tutor'])
                            tutor = tutors[0]
                            result['tutor'] = tutor
                        if 'notes' not in result:
                            result['notes'] = ""
                        result['highlighted'] = False
                        result['active'] = True
                        if 'lsp' not in result:
                            result['lsp'] = ""
                        if 'permanent_email' not in result:
                            result['permanent_email'] = ""
                        address = ""
                        if 'address1' in result:
                            address += result['address1'] + "\n"
                        if 'address2' in result:
                            address += result['address2'] + "\n"
                        if 'address3' in result:
                            address += result['address3'] + "\n"
                        if 'address4' in result:
                            address += result['address4'] + "\n"
                        if 'address5' in result:
                            address += result['address5']
                        home_address = ""
                        if 'home_address1' in result:
                            home_address += result['home_address1'] + "\n"
                        if 'home_address2' in result:
                            home_address += result['home_address2'] + "\n"
                        if 'home_address3' in result:
                            home_address += result['home_address3'] + "\n"
                        if 'home_address3' in result:
                            home_address += result['home_address4'] + "\n"
                        if 'home_address5' in result:
                            home_address += result['home_address5'] + "\n"

                        new = Student(
                            student_id=result['student_id'],
                            first_name=result['first_name'],
                            last_name=result['last_name'],
                            year=result['year'],
                            is_part_time=result['is_part_time'],
                            email=result['email'],
                            course=result['course'],
                            qld=result['qld'],
                            notes=result['notes'],
                            highlighted=result['highlighted'],
                            active=result['active'],
                            lsp=result['lsp'],
                            permanent_email=result['permanent_email'],
                            phone_no=result['phone_no'],
                            address=address,
                            home_address=home_address
                            )
                        new.save()
                        successful_entrys += 1
            request.session['number_of_imports'] = successful_entrys
            return HttpResponseRedirect('/import_success')
    else:
        form = CSVParseForm()
    return render_to_response(
        'parse_csv.html',
        {'form': form, 'csv_list': table, 'first_row': first_row},
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def upload_csv(request):
    """Allows to upload CSV, saves result in session and calls parser"""
    module_dict = functions.modules_for_menubar()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['csvfile']
            f.read()
            csv_list = []
            for line in f:
                csv_list.append(line)
            request.session['csv_data'] = csv_list
            return HttpResponseRedirect('/parse_csv')
    else:
        form = CSVUploadForm()
    return render_to_response(
        'upload_csv.html',
        {'form': form},
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def import_success(request):
    """Displays successful upload / parsing"""
    module_dict = functions.modules_for_menubar()
    successful_entrys = request.session.get('number_of_imports')
    printstring = (
        'CSV File imported successfully: ' +
        '%s students added to the database' % (successful_entrys)
        )
    title = 'CCCU Law DB: Data'
    return render_to_response(
        'blank.html',
        {'printstring': printstring, 'title': title},
        context_instance=RequestContext(request)
        )


# Exam board mode


@login_required
def concessions(request, module_id, year):
    """
    A relatively simple function that lets the admin (or instructor)
    choose a box if a failed part shouldn't be a resit (which would
    mean that the module mark would be capped at a pass.
    """
    module = Module.objects.get(code=module_id, year=year)
    if request.user in module.instructors.all() or is_admin(request.user):
        students = module.student_set.all()
        if request.method == 'POST':
            raw_concessions = request.POST.getlist('concession')
            concessions = {}
            for concession in raw_concessions:
                tmp = concession.split("_")
                student_id = tmp[0]
                assessment = tmp[1]
                if student_id in concessions:
                    concessions[student_id].append(assessment)
                else:
                    concessions[student_id] = [assessment]
            for student in students:
                performance = Performance.objects.get(
                    student=student,
                    module=module
                    )
                if student.student_id in concessions:
                    student_concessions = concessions[student.student_id]
                    if '1' in student_concessions:
                        performance.assessment_1_is_sit = True
                    else:
                        performance.assessment_1_is_sit = False
                    if '2' in student_concessions:
                        performance.assessment_2_is_sit = True
                    else:
                        performance.assessment_2_is_sit = False
                    if '3' in student_concessions:
                        performance.assessment_3_is_sit = True
                    else:
                        performance.assessment_3_is_sit = False
                    if '4' in student_concessions:
                        performance.assessment_4_is_sit = True
                    else:
                        performance.assessment_4_is_sit = False
                    if '5' in student_concessions:
                        performance.assessment_5_is_sit = True
                    else:
                        performance.assessment_5_is_sit = False
                    if '6' in student_concessions:
                        performance.assessment_6_is_sit = True
                    else:
                        performance.assessment_6_is_sit = False
                    if 'e' in student_concessions:
                        performance.exam_is_sit = True
                    else:
                        performance.exam_is_sit = False
                else:
                    performance.assessment_1_is_sit = False
                    performance.assessment_2_is_sit = False
                    performance.assessment_3_is_sit = False
                    performance.assessment_4_is_sit = False
                    performance.assessment_5_is_sit = False
                    performance.assessment_6_is_sit = False
                    performance.exam_is_sit = False
                performance.save()

#            for concession in concessions:
#                tmp = concession.split("_")
#                student_id = tmp[0]
#                assessment = tmp[1]
#                student = Student.objects.get(student_id = student_id)
#                performance = Performance.objects.get(
#                   student = student, module = module)
#                if assessment == '1':
#                    performance.assessment_1_is_sit = True
#                if assessment == '2':
#                    performance.assessment_2_is_sit = True
#                if assessment == '3':
#                    performance.assessment_3_is_sit = True
#                if assessment == '4':
#                    performance.assessment_4_is_sit = True
#                if assessment == '5':
#                    performance.assessment_5_is_sit = True
#                if assessment == '6':
#                    performance.assessment_6_is_sit = True
#                if assessment == 'e':
#                    performance.exam_is_sit = True
#                performance.save()
            return HttpResponseRedirect(module.get_absolute_url())
        else:
            performances = []
            for student in students:
                performance = Performance.objects.get(
                    student=student,
                    module=module)
                performances.append(performance)

            return render_to_response(
                'concessions.html',
                {'module': module, 'performances': performances},
                context_instance=RequestContext(request)
                )
    else:
        printstring = (
            'Only the module instructors or an admin can allow concessions')
        title = 'CCCU Law DB: Not allowed'
        return render_to_response(
            'blank.html',
            {'printstring': printstring, 'title': title},
            context_instance=RequestContext(request))


@login_required
@user_passes_test(is_admin)
def end_of_year_decision(request, year):
    meta_stuff = MetaData.objects.get(data_id=1)
    current_year = meta_stuff.current_year
    students = Student.objects.filter(active=True, year=year)
    all_problem_performances = []
    problem_students = {}
    for student in students:
        performances = Performance.objects.filter(student=student)
        for performance in performances:
            if performance.module.year == current_year:
                bad_performance = False
                if performance.real_average < PASSMARK:
                    bad_performance = True
                else:
                    if student.qld and performance.module.is_foundational:
                        assessments = [1, 2, 3, 4, 5, 6, 'exam']
                        for a in assessments:
                            if performance.module.get_assessment_value(a):
                                if (performance.get_assessment_result(a)
                                        < PASSMARK):
                                    bad_performance = True
                if bad_performance:
                    if student in problem_students:
                        problem_students[student][
                            'bad_performances'].append(performance)
                    else:
                        problem_students[student] = {}
                        problem_students[student][
                            'bad_performances'] = [performance]
    for student in problem_students:
        performances = Performance.objects.filter(student=student)
        problem_students[student]['good_performances'] = []
        problem_students[student]['credits'] = 0
        for performance in performances:
            if performance.module.year == current_year:
                if (performance not in
                        problem_students[student]['bad_performances']):
                    problem_students[student][
                        'good_performances'].append(performance)
                    problem_students[student]['credits'] += (
                        performance.module.credits)
                elif performance.average > PASSMARK:
                    problem_students[student]['credits'] += (
                        performance.module.credits)

    return render_to_response(
        'exam_board_overview.html',
        {'year': year, 'dictionary': problem_students},
        context_instance=RequestContext(request)
        )

# Remember for progression:
#
# if student.is_part_time:
#   if student.second_part_time_year:
#       student.year += 1
#   else:
#       student.second_part_time_year = True
#
# Also think about deleting anonymous mark entries


# Student Accessible Functions


@login_required
@user_passes_test(is_student)
def student_marks(request):
    """Allows student to see their own mark and feedback"""
    student = Student.objects.get(belongs_to=request.user)
    all_performances = Performance.objects.filter(student=student)
    sorted_performances = {}
    for performance in all_performances:
        module = performance.module
        output = {}
        output['module'] = module
        year = module.year
        if module.assessment_1_available:
            output['assessment_1'] = performance.assessment_1
            try:
                marksheet = Marksheet.objects.get(
                    student=student, module=module, assessment=1)
                if marksheet.comments:
                    output['assessment_1_marksheet'] = True
            except Marksheet.DoesNotExist:
                pass
        if module.assessment_2_available:
            output['assessment_2'] = performance.assessment_2
            try:
                marksheet = Marksheet.objects.get(
                    student=student, module=module, assessment=2)
                if marksheet.comments:
                    output['assessment_2_marksheet'] = True
            except Marksheet.DoesNotExist:
                pass
        if module.assessment_3_available:
            output['assessment_3'] = performance.assessment_3
            try:
                marksheet = Marksheet.objects.get(
                    student=student, module=module, assessment=3)
                if marksheet.comments:
                    output['assessment_3_marksheet'] = True
            except Marksheet.DoesNotExist:
                pass
        if module.assessment_4_available:
            output['assessment_4'] = performance.assessment_4
            try:
                marksheet = Marksheet.objects.get(
                    student=student, module=module, assessment=4)
                if marksheet.comments:
                    output['assessment_4_marksheet'] = True
            except Marksheet.DoesNotExist:
                pass
        if module.assessment_5_available:
            output['assessment_5'] = performance.assessment_5
            try:
                marksheet = Marksheet.objects.get(
                    student=student, module=module, assessment=5)
                if marksheet.comments:
                    output['assessment_5_marksheet'] = True
            except Marksheet.DoesNotExist:
                pass
        if module.assessment_6_available:
            output['assessment_6'] = performance.assessment_6
            try:
                marksheet = Marksheet.objects.get(
                    student=student, module=module, assessment=6)
                if marksheet.comments:
                    output['assessment_6_marksheet'] = True
            except Marksheet.DoesNotExist:
                pass
        if module.exam_available:
            output['exam'] = performance.exam
        else:
            output['exam'] = None
        if sorted_performances.get(year):
            sorted_performances[year].append(output)
        else:
            sorted_performances[year] = [output]

    return render_to_response(
        'student_own_marks.html',
        {'student': student, 'sorted_performances': sorted_performances},
        context_instance=RequestContext(request)
        )
