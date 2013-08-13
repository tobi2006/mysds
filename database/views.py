from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import simplejson

from database import models
from database.models import *
from database import functions
from database.forms import *
from database.strings import *

def is_teacher(user):
    if user:
        if user.groups.filter(name='teachers').count() == 1:
            return True
        else:
            return False
    else:
        return False

def is_admin(user):
    if user:
        if user.groups.filter(name='admins').count() == 1:
            return True
        else:
            return False
    else:
        return False


###############################################################################
###############################################################################
#                       
#                       Module Functions
#
###############################################################################
###############################################################################


#####################################
#          Module View              #
#####################################

@login_required
@user_passes_test(is_teacher)
def module_view(request, module_id, year):
    """
    The overview function for a module.

    Shows a summary of all the students in a module with the performance information.
    """
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    number_of_groups = 1
    performances = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        if performance.seminar_group > number_of_groups:
            number_of_groups = performance.seminar_group
        student_name = student.last_name + ", " + student.first_name
        performances[student_name] = performance
         

    #create string to make it iterable
    groupstring = ''
    for i in range(0, number_of_groups):
        groupstring += str(i+1)

    return render_to_response('module_view.html',
            {'current_module': module, 'performances': performances, 
            'number_of_groups': groupstring},
            context_instance = RequestContext(request)
            )


#####################################
#        Module Overview            #
#####################################

@login_required
@user_passes_test(is_teacher)
def module_overview(request, year):
    """
    Shows all modules for a particular year

    This function is necessary to keep the menu clear of all past and future modules
    """
    modules = Module.objects.filter(year=year)
    return render_to_response('module_overview.html',
            {'modules': modules, 'year': year},
            context_instance = RequestContext(request)
        )



#####################################
#       Edit Module                 #
#####################################

@login_required
@user_passes_test(is_teacher)
def edit_module(request, module_id, year):
    """
    Opens and processes an edit form for an existing module
    """
    module = Module.objects.get(code=module_id, year=year)
    number_of_assessments = functions.get_number_of_assessments(module)
    if request.method == 'POST':
        form = ModuleForm(instance=module, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = ModuleForm(instance=module)
    return render_to_response(
        'module_form.html', 
        {'module_form': form, 'add': False, 'object': module, 
            'assessments': number_of_assessments}, 
        context_instance = RequestContext(request)
    )

    
#####################################
#       Add Module                  #
#####################################

@login_required
@user_passes_test(is_teacher)
def add_module(request):
    """
    Function to add a new module
    """
    assessments = 0
    if request.is_ajax():
        if 'successor_of' not in request.POST:
            year = int(request.POST['year'])
            predecessor_year = year - 1
            predecessor_modules = Module.objects.filter(year=predecessor_year)
            new_options = '<option value="" selected="selected">---------</option>\n'
            for module in predecessor_modules:
                toadd = '<option value="' + str(module.id) +'">' + str(module) + '</option>\n'
                new_options += toadd
            return HttpResponse(new_options)
        else:
            successor_of = int(request.POST['successor_of'])
            predecessor = Module.objects.get(id=successor_of)
            suggestions = {}
            suggestions['title'] = predecessor.title
            suggestions['code'] = predecessor.code
            suggestions['credits'] = predecessor.credits
            suggestions['number_of_sessions'] = predecessor.number_of_sessions
            eligible = ''
            for entry in Module.ELIGIBLE:
                if entry[0] == predecessor.eligible:
                    eligible += '<option value="' + entry[0] + '" selected="selected">' + entry[1] + '</option>\n'
                else:
                    eligible += '<option value="' + entry[0] + '">' + entry[1] + '</option>\n'
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
                assessments += '<tr><td><strong>Assessment ' + count + ':</strong></td>\n <td>Title</td><td>\n <input id="id_assessment_' + count + '_title" maxlength="30" name="assessment_' + count + '_title" type="text" value="' + title + '" /></td>\n <td>Percentage</td><td>\n <input id="id_assessment_' + count + '_value" name="assessment_' + count + '_value" type="text" value="' + value + '" /></tr>'
                counter += 1
            suggestions['number_of_assessments'] = no_of_assessments
            suggestions['assessments'] = assessments
            if predecessor.exam_value:
                suggestions['exam'] = predecessor.exam_value
        json = simplejson.dumps(suggestions)
        return HttpResponse(json, mimetype='application/json')
        #for module in predecessor_modules:
        #    print module.title

    if request.method == 'POST':
        form = ModuleForm(data=request.POST)
        if form.is_valid():
            module = form.save()
            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = ModuleForm()
    return render_to_response(
        'module_form.html', 
        {'module_form': form, 'add': True, 
        'assessments': assessments}, 
        context_instance = RequestContext(request)
    )

#####################################
#       Anonymous Marking           #
#####################################


@login_required
@user_passes_test(is_teacher)
def upload_anon_ids(request):
    module_dict = functions.modules_for_menubar()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['csvfile']
            f.read()
            list_of_ids = []
            for line in f:
                row = line.split(',')
                list_of_ids.append(row)
            request.session['anon_ids'] = csv_list
            return HttpResponseRedirect('/edit')
    else:
        form = CSVUploadForm()
    return render_to_response('enter_anon_ids.html',
            {'form': form},
            context_instance=RequestContext(request))

@login_required
@user_passes_test(is_teacher)
def edit_anon_ids(request):
    try:
        importdata = request.session.get('anon_ids')
    except KeyError:
        noimport = True
    if request.method == 'POST':
        pass
    else:
        pass
    



@login_required
@user_passes_test(is_teacher)
def enter_anonymous_marks(request, module_id, year):

    """
    Function to enter marks according to the exam ID

    With this function, the marks can be added to the corresponding exam ID.
    Before, the exam IDs have to be added with the function XXX.
    The marks get stored into a separate model (AnonymousMarks) and can be matched
    to the students DB entries with the function XXX.
    """

    module = Module.objects.get(code=module_id, year = year)
    exam_ids = AnonymousMarks.objects.filter(module = module)


@login_required
@user_passes_test(is_admin)
def put_anonymous_marks_in_db(request, module_id, year):
    pass

###############################################################################
###############################################################################
#                                                                             #
#                       Student Functions                                     #
#                                                                             #
###############################################################################
###############################################################################

#####################################
#       Student View                #
#####################################

@login_required
@user_passes_test(is_teacher)
def student_view(request, student_id):
    """
    Shows all information about a student.
    """
    student = Student.objects.get(student_id=student_id)
    all_performances = Performance.objects.filter(student = student)
    sorted_performances = {}
    for performance in all_performances:
        year = performance.module.year
        if sorted_performances.get(year):
            sorted_performances[year].append(performance)
        else:
            sorted_performances[year] = [performance,]
            

    return render_to_response('student_view.html',
            {'student': student, 'years_performances': sorted_performances},
            context_instance = RequestContext(request)
        )

#####################################
#       Search Student              #
#####################################

@login_required
@user_passes_test(is_teacher)
def search_student(request):
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
            students = Student.objects.filter(last_name__icontains=last_name, first_name__icontains=first_name)
        if len(students) == 0:
            students = Student.objects.filter(Q(last_name__istartswith=q) | Q(first_name__istartswith=q))
        if len(students) == 1:
            student = students[0]
            return HttpResponseRedirect(student.get_absolute_url())
#            return render_to_response('student_view.html',
#                {'current_student': student},
#                context_instance = RequestContext(request)
#            )
        else:
            return render_to_response('search_results.html',
                    {'students': students, 'query': q},
                    context_instance = RequestContext (request)
                )
    else:
        return HttpResponse('Please submit a search term.')


#####################################
#        Year View                  #
#####################################

@login_required
@user_passes_test(is_teacher)
def year_view(request, year):
    """
    Shows all students in a particular year and allows making changes in bulk
    """
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
            pass
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
                    tutee_sessions = Tutee_Session.objects.filter(tutee=student)
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
    for academic_year in ACADEMIC_YEARS:
        academic_years.append(academic_year[0])
    llb = Course.objects.get(title="LLB (Hons) Bachelor Of Law")
    all_students = len(students)
    llb_students = None
    other_students = None
    if year == "all":
        llb = Course.objects.get(title__contains="LLB")
        llb_students = Student.objects.filter(course=llb).count()
        other_students = all_students - llb_students
    elif ug:
        llb = Course.objects.get(title__contains="LLB")
        llb_students = Student.objects.filter(year=year, course=llb).count()
        other_students = all_students - llb_students
    if ug or alumnus or unassigned or inactive:
        courses = Course.objects.all
    tutors = User.objects.filter(groups__name='teachers')
    
    return render_to_response('year_view.html',
            {'students': students, 'year': year, 
            'ug': ug, 'pg':pg, 'phd': phd, 'alumnus': alumnus, 'llb': llb,
            'more_than_one_year': more_than_one_year, 'tutors': tutors,
            'academic_years': academic_years, 'courses': courses,
            'all_students': all_students, 'llb_students': llb_students,
            'show_inactive': inactive,
            'other_students': other_students},
            context_instance = RequestContext(request)
        )


#####################################
#        Tutor Stuff                #
#####################################


@login_required
@user_passes_test(is_teacher)
def tutee_list(request):
    tutees = Student.objects.filter(tutor=request.user)
    return render_to_response('tutee_list.html',
            {'tutees': tutees},
            context_instance=RequestContext(request)
        )

@login_required
@user_passes_test(is_teacher)
def tutee_edit(request, student_id, meeting_id=None):
    student = Student.objects.get(student_id=student_id)
    if meeting_id:
        tutee_session = Tutee_Session.objects.get(id=meeting_id)
        edit = meeting_id
    else:
        tutee_session = Tutee_Session(tutee=student, tutor=request.user)
        edit = False
    if request.method == 'POST':
        form = TuteeForm(instance = tutee_session, data = request.POST)
        if form.is_valid():
            if meeting_id:
                print "Ja"
                to_delete = Tutee_Session.objects.get(id=meeting_id)
                to_delete.delete()
            form.save()
            url = '/tutee/' + student.student_id
            return HttpResponseRedirect(url)
    else:
        form = TuteeForm(instance=tutee_session)
    all_performances = Performance.objects.filter(student = student)
    sorted_performances = {}
    for performance in all_performances:
        year = performance.module.year
        if sorted_performances.get(year):
            sorted_performances[year].append(performance)
        else:
            sorted_performances[year] = [performance,]
    tutee_sessions = Tutee_Session.objects.filter(tutee=student)

    return render_to_response('tutee_edit.html',
            {'form': form, 'student': student, 'years_performances': sorted_performances,
                'edit': edit, 'meetings': tutee_sessions, 'mdexplanation': MD_EXPLANATION},
            context_instance = RequestContext(request)
        )

@login_required
@user_passes_test(is_teacher)
def delete_tutee_meeting(request, meeting_id):
    meeting = Tutee_Session.objects.get(id=meeting_id)
    if request.user == meeting.tutor or is_admin(request.user):
        tutee = meeting.tutee
        url = '/tutee/' + tutee.student_id
        meeting.delete()
        return HttpResponseRedirect(url)
    else:
        printstring = 'Only the tutor in question or an administrator can delete this.'
        title = 'CCCU Law DB: Not allowed'
        return render_to_response(
                'blank.html', 
                {'printstring': printstring, 'title': title},
                context_instance = RequestContext(request))



#####################################
#        Add Student                #
#####################################

@login_required
@user_passes_test(is_teacher)
def add_student(request):
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
        context_instance = RequestContext(request)
    )


#####################################
#       Edit Student                #
#####################################

@login_required
@user_passes_test(is_teacher)
def edit_student(request, student_id):
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
        context_instance = RequestContext(request)
    )



#####################################
#            Mark                   #
#####################################

@login_required
@user_passes_test(is_teacher)
def mark(request, module_id, year, assessment):
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    performances = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        student_name = student.last_name + ", " + student.first_name 
        performances[student_name] = performance
    if assessment == "exam":
        to_change = 9
    else:
        tmp = assessment.split("_")
        to_change = int(tmp[1])
    if request.method == 'POST':
        students = module.student_set.all()
        for student in students:
            if student.student_id in request.POST:
                tmp = request.POST[student.student_id]
                try:
                    mark = int(tmp)
                    if mark in range(0, 100):
                        performance = Performance.objects.get(student=student, module=module)
                        if to_change == 1:
                            performance.assessment_1 = mark
                        elif to_change == 2:
                            performance.assessment_2 = mark
                        elif to_change == 3:
                            performance.assessment_3 = mark
                        elif to_change == 4:
                            performance.assessment_4 = mark
                        elif to_change == 5:
                            performance.assessment_5 = mark
                        elif to_change == 6:
                            performance.assessment_6 = mark
                        elif to_change == 9:
                            performance.exam = mark
                    performance.save_with_avg()
                except ValueError:
                    pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
            'mark.html',
            {'current_module': module, 'performances': performances, 'to_mark': to_change},
            context_instance = RequestContext(request)
        )


#####################################
#           Attendance              #
#####################################

@login_required
@user_passes_test(is_teacher)
def attendance(request, module_id, year, group):
    module = Module.objects.get(code=module_id, year=year)
    no_of_sessions = range(module.number_of_sessions)
    students = module.student_set.all()
    students.order_by('last_name')
    if group == "all":
        students_in_group = students
        seminar_group = None
    else:
        seminar_group = group
        students_in_group = []
        for student in students:
            performance = Performance.objects.get(student=student, module=module)
            if performance.seminar_group == int(group):
                students_in_group.append(student)

    if request.method == 'POST':
        last_session = 0
        for student in students_in_group:
            performance = Performance.objects.get(student = student, module = module)
            weeks_present = request.POST.getlist(student.student_id)
            counter = 0
            attendance = ""
            while counter < module.number_of_sessions:
                if str(counter) in weeks_present:
                    attendance = attendance + "1"
                    week_number = counter + 1
                    if week_number > last_session:
                        last_session = week_number
                else:
                    attendance = attendance + "0"
                counter += 1
            performance.attendance  = attendance
            performance.save()
        module.sessions_recorded = last_session
        module.save()
        return HttpResponseRedirect(module.get_absolute_url())

    else:
        attendances = {}
        for student in students_in_group:
            performance = Performance.objects.get(student=student, module=module)
            attendance = {}
            counter = 0
            for session in performance.attendance:
                if session == "1":
                    attendance[counter] = True
                else:
                    attendance[counter] = False
                counter += 1
            attendances[student] = attendance

    return render_to_response(
            'attendance.html',
            {'current_module': module, 'attendances': attendances, 'seminar_group': seminar_group,
            'sessions': no_of_sessions},
            context_instance = RequestContext(request)
        )


#####################################
#        Seminar Groups             #
#####################################
    
@login_required
@user_passes_test(is_teacher)
def seminar_groups(request, module_id, year):
    test = "test"
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    student_ids = []
    performances = {}
    for student in students:
        student_ids.append(student.student_id)
        performance = Performance.objects.get(student=student, module=module)
        performances[student] = performance
    random_options={}
    for i in range(1,10): 
        # Up to 10 Seminar groups. Create a dictionary that lists the options
        # and the maximum number of students per group
        all = len(students)
        number = all / i
        left = all % i
        if left > 0:
            number = number + 1
        random_options[i]=number

    if request.method == 'POST':
        for student in students:
            if student.student_id in request.POST:
                tmp = request.POST[student.student_id]
                try:
                    seminar_group = int(tmp)
                    if seminar_group in range(0, 99):
                        performance = Performance.objects.get(student=student, module=module)
                        performance.seminar_group = seminar_group
                        performance.save()
                except ValueError:
                        pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
            'seminar_groups.html',
            {'current_module': module, 'performances': performances, 'random_options': random_options,
                'students': student_ids},
            context_instance = RequestContext(request)
        )


#####################################
#            LSP View               #
#####################################

@login_required
@user_passes_test(is_teacher)
def lsp_view(request, student_id):

    """
    Show the Learning Support Plan for a student
    """

    student = Student.objects.get(student_id=student_id)
    edit = False
    return render_to_response(
            'lsp.html',
            {'student': student, 'edit': edit},
            context_instance = RequestContext(request)
            )


#####################################
#            LSP Edit               #
#####################################

@login_required
@user_passes_test(is_teacher)
def lsp_edit(request, student_id):

    """
    Allows to edit the Learning Support Plan for a student
    """
    student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        form = LSPForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = LSPForm(instance = student)
    return render_to_response(
            'lsp.html',
            {'form': form, 'student': student, 'edit': True, 'mdexplanation': MD_EXPLANATION},
            context_instance = RequestContext(request)
            )

#####################################
#          Notes Edit               #
#####################################

@login_required
@user_passes_test(is_teacher)
def notes_edit(request, student_id):

    """
    Allows to edit the Notes for a student
    """
    student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        form = NotesForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = NotesForm(instance = student)
    return render_to_response(
            'student_notes.html',
            {'form': form, 'student': student, 'edit': True, 'mdexplanation': MD_EXPLANATION},
            context_instance = RequestContext(request)
            )


#####################################
#    Add Students to Module         #
#####################################

@login_required
@user_passes_test(is_teacher)
def add_students_to_module(request, module_id, year):
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
        year = int(number) # Find out which students are eligible
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
            student_to_add = Student.objects.get(student_id = student_id)
            student_to_add.modules.add(module)
            # Generate Performance entry for the student
            performance = Performance(
                    student = student_to_add,
                    module = module
                )
            performance.initial_save()

        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
            'add_students_to_module.html',
            {'module': module, 'more_than_one_year': more_than_one_year, 
                'students': students, 'llb': llb, 'eligible': eligible},
            context_instance = RequestContext(request)
        )


#####################################
#       Parse CSV File              #
#####################################

@login_required
@user_passes_test(is_teacher)
def parse_csv(request):
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
            successful_entrys = 0
            for row in table:
                result = {}
                counter = 0
                for entry in row:
                    column = list_of_columns[counter]
                    if column != 'ignore':
                        result[column] = entry
                    counter += 1
                try: # Check if student is already in and add new data / amend existing
                    current = Student.objects.get(student_id=result['student_id'])
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
                    if 'email' in result:
                        current.email = result['email']
                    if 'course' in result:
                        courses = Course.objects.filter(title__icontains = result['course'])
                        if courses:
                            course = courses[0]
                            current.course = course
                        else:
                            new_course = Course(title = result['course'])
                            new_course.save()
                            current.course = new_course
                    if 'qld' in result:
                        current.qld = result['qld']
                    if 'tutor' in result:
                        tutor_results = User.objects.filter(name = result['tutor'])
                        tutor = tutors[0]
                        current.tutor = tutor
                    if 'notes' in result:
                        current.notes = current.notes + '\n' + result['notes']
                    if 'lsp' in result:
                        current.lsp = result['lsp']
                    if 'permanent_email' in result:
                        current.permanent_email = result['permanent_email']
#                    if 'achieved_grade' in result:
#                        current.achieved_grade = result['achieved_grade']
                    if 'address' in result:
                        current.address = result['address']
                    if 'home_address' in result:
                        current.home_address = result['home_address']
                    current.save()

                except Student.DoesNotExist: # Enter new student
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
                    if 'course' not in result:
                        result['course'] = None
                    else:
                        courses = Course.objects.filter(title__icontains = result['course'])
                        if courses:
                            course = courses[0]
                            result['course'] = course
                        else:
                            new_course = Course(title = result['course'])
                            new_course.save()
                            result['course'] = new_course
                    result['modules'] = ""
                    if 'qld' not in result:
                        result['qld'] = False
                    if 'tutor' not in result:
                        result['tutor'] = None
                    else:
                        tutors = User.objects.filter(name = result['tutor'])
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
                    if 'address' not in result:
                        result['address'] = ""
                    if 'home_address' not in result:
                        result['home_address'] = ""
                    new = Student(
                            student_id = result['student_id'],
                            first_name = result['first_name'],
                            last_name = result['last_name'],
                            #since = int(result['since']),
                            year = result['year'],
                            is_part_time = result['is_part_time'],
                            email = result['email'],
                            course = result['course'],
                            qld = result['qld'],
                            notes = result['notes'],
                            highlighted = result['highlighted'],
                            active = result['active'],
                            lsp = result['lsp'],
                            permanent_email = result['permanent_email'],
#                            achieved_grade = result['achieved_grade'],
                            address = result['address'],
                            home_address = result['home_address']
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
            context_instance = RequestContext(request)
        )


#####################################
#       Upload CSV                  #
#####################################

@login_required
@user_passes_test(is_teacher)
def upload_csv(request):
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
    return render_to_response('upload_csv.html',
            {'form': form},
            context_instance=RequestContext(request))


#####################################
#       Import Success              #
#####################################

@login_required
@user_passes_test(is_teacher)
def import_success(request):
    module_dict = functions.modules_for_menubar()
    successful_entrys = request.session.get('number_of_imports')
    printstring = 'CSV File imported successfully: %s students added to the database' % (successful_entrys)
    title = 'CCCU Law DB: Data'
    return render_to_response(
            'blank.html', 
            {'printstring': printstring, 'title': title},
            context_instance = RequestContext(request))

