from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.utils import simplejson

from database.models import *
from database import functions
from database.forms import *
from anonymous_marking.models import *
from database.views import is_teacher, is_admin


@login_required
@user_passes_test(is_admin)
def anonymous_marking_admin(request):
    """Displays an admin page with the options for anonymous marking"""
    years = []
    all_modules = Module.objects.all()
    for module in all_modules:
        if module.exam_value:
            marks = AnonymousMarks.objects.filter(module=module)
            for mark in marks:
                if mark.exam:
                    if module.year not in years:
                        years.append(module.year)
                    break
    years.sort()
    return render_to_response(
        'anonymous_marking_admin.html',
        {'years': years},
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_admin)
def upload_anon_ids(request):
    """Allows uploading of a CSV with anonymous IDs

    Requires a csv file with student IDs on the left and anonymous
    IDs on the right. Very straight forward and simple, but helpful"""
    module_dict = functions.modules_for_menubar()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['csvfile']
            f.read()
            counter = 0
            problems = []
            for line in f:
                row = line.split(',')
                student_id = row[0]
                anon_id = row[1]
                anon_id = anon_id.rstrip()
                if anon_id == '':
                    anon_id = None
                student = Student.objects.get(student_id=student_id)
                student.exam_id = anon_id
                try:
                    student.save()
                    counter += 1
                except IntegrityError:
                    problems.append(student)
            if problems:
                printstring = '''%s exam IDs imported.<br><br>
                The exam IDs for the following student(s) were already\
 assigned to a different student:<br>
                <ul>
                ''' % (counter)
                for problem in problems:
                    printstring += (
                        '<li>' +
                        problem.first_name +
                        ' ' +
                        problem.last_name +
                        ' (' +
                        problem.student_id +
                        ')</li>\n'
                        )
                printstring += '</ul>'
            else:
                printstring = '%s exam IDs imported' % (counter)
            title = 'CCCU Law DB'
            return render_to_response(
                'blank.html',
                {'printstring': printstring, 'title': title},
                context_instance=RequestContext(request)
                )
    else:
        form = CSVUploadForm()
    return render_to_response(
        'anon_file_upload.html',
        {'form': form},
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_admin)
def edit_anon_ids(request):
    """Allows manual editing of anonymous IDs"""
    students = Student.objects.filter(active=True)
    if request.method == 'POST':
        counter = 0
        problems = ""
        for student in students:
            if student.student_id in request.POST:
                anon_id = request.POST[student.student_id]
                if anon_id == "":
                    anon_id = None
                student.exam_id = anon_id
                try:
                    student.save()
                    counter += 1
                except IntegrityError:
                    problems += (
                        '<li>' +
                        student.first_name +
                        ' ' +
                        student.last_name +
                        ' (' +
                        student.student_id +
                        ')</li>\n'
                        )
        if len(problems) > 0:
            printstring = '''%s exam IDs imported.<br><br>
            The exam IDs for the following student(s) could not be assigned,\
 as they were already assigned to a different student:<br>
            <ul>
            ''' % (counter)
            printstring += problems
            printstring += '</ul>'
        else:
            printstring = '%s exam IDs saved' % (counter)
        title = 'CCCU Law DB'
        return render_to_response(
            'blank.html',
            {'printstring': printstring, 'title': title},
            context_instance=RequestContext(request)
            )
    return render_to_response(
        'anon_ids_edit.html',
        {'students': students},
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def mark_anonymously(request, code, year, assessment):
    """Function to enter marks according to the exam ID

    With this function, the marks can be added to the corresponding
    exam ID. Before, the exam IDs have to be added with the function
    edit_anon_ids. The marks get stored into a separate model
    (AnonymousMarks) and can be matched to the students DB entries
    with the function put_anonymous_marks_in_db.
    """
    module = Module.objects.get(code=code, year=year)
    students = module.student_set.all()
    exam_ids = []
    no_exam_ids = []
    for student in students:
        if student.exam_id:
            exam_id = student.exam_id
            exam_ids.append(exam_id)
        else:
            no_exam_ids.append(student)
    marks = {}
    for exam_id in exam_ids:
        try:
            performance = AnonymousMarks.objects.get(
                exam_id=exam_id, module=module)
        except ObjectDoesNotExist:
            performance = AnonymousMarks(exam_id=exam_id, module=module)
            performance.save()
        mark = performance.get_assessment_result(assessment)
        marks[exam_id] = mark
        # performances[exam_id] = performance
    if request.method == 'POST':
        for exam_id in exam_ids:
            tmp = request.POST[exam_id]
            try:
                mark = int(tmp)
                if mark in range(0, 100):
                    performance = AnonymousMarks.objects.get(
                        exam_id=exam_id, module=module)
                    if (performance.get_assessment_result(assessment) !=
                            mark):
                        # Otherwise, new timestamp would be set
                        performance.set_assessment_result(assessment, mark)
            except ValueError:
                pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
        'anon_mark.html',
        {
            'current_module': module,
            'marks': marks,
            'no_exam_ids': no_exam_ids
        },
        context_instance=RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def de_anonymize(request, code, year, assessment):
    """Goes through a module and de-anonymizes all assessments"""
    module = Module.objects.get(code=code, year=year)
    all_anonymous_marks = AnonymousMarks.objects.filter(module=module)
    for a in all_anonymous_marks:
        student = Student.objects.get(exam_id=a.exam_id)
        p = Performance.objects.get(student=student, module=module)
        if assessment == 'all':
            assessments = ['1', '2', '3', '4', '5', '6', 'exam']
        else:
            assessments = [assessment]
        for i in assessments:
            if a.get_assessment_result(i):
                if (a.get_assessment_result(i) !=
                        p.get_assessment_result(i)):
                    if p.get_assessment_modified(i):
                        if (a.get_assessment_modified(i) >
                                p.get_assessment_modified(i)):
                            p.set_assessment_result(
                                i,
                                a.get_assessment_result(i),
                                a.get_assessment_modified(i)
                                )
                    else:
                        p.set_assessment_result(
                            i,
                            a.get_assessment_result(i),
                            a.get_assessment_modified(i)
                            )
        for i in assessments:
            if a.get_assessment_result(i, r=True):
                if (a.get_assessment_result(i, r=True) !=
                        p.get_assessment_result(i, r=True)):
                    if p.get_assessment_modified(i, r=True):
                        if (a.get_assessment_modified(i, r=True) >
                                p.get_assessment_modified(i, r=True)):
                            p.set_assessment_result(
                                i,
                                a.get_assessment_result(i, r=True),
                                a.get_assessment_modified(i, r=True),
                                r=True
                                )
                    else:
                        p.set_assessment_result(
                            i,
                            a.get_assessment_result(i, r=True),
                            a.get_assessment_modified(i, r=True),
                            r=True
                            )
        for i in assessments:
            if a.get_assessment_result(i, q=True):
                if (a.get_assessment_result(i, q=True) !=
                        p.get_assessment_result(i, q=True)):
                    if p.get_assessment_modified(i, q=True):
                        if (a.get_assessment_modified(i, q=True) >
                                p.get_assessment_modified(i, q=True)):
                            p.set_assessment_result(
                                i,
                                a.get_assessment_result(i, q=True),
                                a.get_assessment_modified(
                                    i, q=True),
                                q=True
                                )
                    else:
                        p.set_assessment_result(
                            i,
                            a.get_assessment_result(i, q=True),
                            a.get_assessment_modified(i, q=True),
                            q=True
                            )
    return HttpResponseRedirect(module.get_absolute_url())
#
# @login_required
# @user_passes_test(is_admin)
# def write_anonymous_marks_to_db(request, confirmation):
#    """De-Anonymises all marks for the current year"""
#    if confirmation == 'confirm':
#        printstring = (
#            'This function will write the anonymous marks ' +
#            'entered so far into the database. After this, the marks of ' +
#            'all students will be visible. <br><br>' +
#            'Are you sure you want to go ahead?<br><br>' +
#            '<a href="/write_anonymous_marks_to_db/de_anonymise" ' +
#            'class="btn btn-primary" type="button">Go ahead</a>'
#            )
#        title = "Confirm De-Anonymisation"
#        return render_to_response(
#            'blank.html',
#            {'printstring': printstring, 'title': title},
#            context_instance=RequestContext(request))
#
#    elif confirmation == 'de_anonymise':
#        metadata = MetaData.objects.get(id=1)
#        year = metadata.current_year
#        year_string = metadata.academic_year_string()
#        modules = Module.objects.filter(year=year)
#        for module in modules:
#            if de_anonymise_module(module):
#                printstring = (
#                    'The anonymous marks for ' +
#                    '%s ' % (year_string) +
#                    'have been transferred to the database.'
#                    )
#            title = "CCCU Law DB"
#
#    return render_to_response(
#        'blank.html',
#        {'printstring': printstring, 'title': title},
#        context_instance=RequestContext(request))
