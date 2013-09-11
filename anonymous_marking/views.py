from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import simplejson

from database.models import *
from database import functions
from database.forms import *
from anonymous_marking.models import *
from database.views import is_teacher, is_admin 


@login_required
@user_passes_test(is_admin)
def anonymous_marking_admin(request):
    years = []
    all_modules = Module.objects.all()
    for module in all_modules:
        if module.exam_value:
            marks = AnonymousMarks.objects.filter(module = module)
            for mark in marks:
                if mark.exam:
                    if module.year not in years:
                        years.append(module.year)
                    break
    years.sort()
    return render_to_response('anonymous_marking_admin.html',
            {'years': years},
            context_instance=RequestContext(request))

@login_required
@user_passes_test(is_admin)
def upload_anon_ids(request):
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
                student = Student.objects.get(student_id = student_id)
                student.exam_id = anon_id
                try:
                    student.save()
                    counter += 1
                except IntegrityError:
                    problems.append(student)
            if problems:
                printstring = '''%s exam IDs imported.<br><br>
                The exam IDs for the following student(s) were already assigned to a different student:<br>
                <ul>
                '''%(counter)
                for problem in problems:
                    printstring += '<li>' + problem.first_name + ' ' + problem.last_name + ' (' + problem.student_id + ')</li>\n'
                printstring += '</ul>'
            else:
                printstring = '%s exam IDs imported' % (counter)
            title = 'CCCU Law DB'
            return render_to_response(
                    'blank.html', 
                    {'printstring': printstring, 'title': title},
                    context_instance = RequestContext(request))
    else:
        form = CSVUploadForm()
    return render_to_response('anon_file_upload.html',
            {'form': form},
            context_instance=RequestContext(request))

@login_required
@user_passes_test(is_admin)
def edit_anon_ids(request):
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
                    problems += '<li>' + student.first_name + ' ' + student.last_name + ' (' + student.student_id + ')</li>\n'
        if len(problems)>0:
            printstring = '''%s exam IDs imported.<br><br>
            The exam IDs for the following student(s) could not be assigned, as they were already assigned to a different student:<br>
            <ul>
            '''%(counter)
            printstring += problems
            printstring += '</ul>'
        else:
            printstring = '%s exam IDs saved' % (counter)
        title = 'CCCU Law DB'
        return render_to_response(
                'blank.html', 
                {'printstring': printstring, 'title': title},
                context_instance = RequestContext(request))
    return render_to_response('anon_ids_edit.html',
            {'students': students},
            context_instance=RequestContext(request))
        

@login_required
@user_passes_test(is_teacher)
def mark_anonymously(request, module_id, year, assessment):

    """
    Function to enter marks according to the exam ID

    With this function, the marks can be added to the corresponding exam ID.
    Before, the exam IDs have to be added with the function edit_anon_ids.
    The marks get stored into a separate model (AnonymousMarks) and can be matched
    to the students DB entries with the function put_anonymous_marks_in_db.
    """

    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    exam_ids = []
    for student in students:
        exam_id = student.exam_id
        exam_ids.append(exam_id)
        print exam_id
    performances = {}
    for exam_id in exam_ids:
        try:
            performance = AnonymousMarks.objects.get(exam_id=exam_id, module=module)
        except ObjectDoesNotExist:
            performance = AnonymousMarks(exam_id = exam_id, module = module)
        performances[exam_id] = performance
    if assessment == "exam":
        to_change = 9
    else:
        tmp = assessment.split("_")
        to_change = int(tmp[1])
    if request.method == 'POST':
        students = module.student_set.all()
        for student in students:
            if student.exam_id in request.POST:
                tmp = request.POST[student.exam_id]
                try:
                    mark = int(tmp)
                    if mark in range(0, 100):
                        print student.exam_id + ": " + str(mark)
                        try:
                            performance = AnonymousMarks.objects.get(exam_id=student.exam_id, module=module)
                        except ObjectDoesNotExist:
                            performance = AnonymousMarks(exam_id = student.exam_id, module = module)
                        if to_change == 1:
                            if mark != performance.assessment_1:
                                performance.assessment_1 = mark
                                performance.assessment_1_modified = datetime.datetime.today()
                        elif to_change == 2:
                            if mark != performance.assessment_2:
                                performance.assessment_2 = mark
                                performance.assessment_2_modified = datetime.datetime.today()
                        elif to_change == 3:
                            if mark != performance.assessment_3:
                                performance.assessment_3 = mark
                                performance.assessment_3_modified = datetime.datetime.today()
                        elif to_change == 4:
                            if mark != performance.assessment_4:
                                performance.assessment_4 = mark
                                performance.assessment_4_modified = datetime.datetime.today()
                        elif to_change == 5:
                            if mark != performance.assessment_5:
                                performance.assessment_5 = mark
                                performance.assessment_5_modified = datetime.datetime.today()
                        elif to_change == 6:
                            if mark != performance.assessment_6:
                                performance.assessment_6 = mark
                                performance.assessment_6_modified = datetime.datetime.today()
                        elif to_change == 9:
                            if mark != performance.exam:
                                performance.exam = mark
                                performance.exam_modified = datetime.datetime.today()
                        performance.save()
                except ValueError:
                    pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
            'anon_mark.html',
            {'current_module': module, 'performances': performances, 'to_mark': to_change},
            context_instance = RequestContext(request)
        )
    
@login_required
@user_passes_test(is_admin)
def write_anonymous_marks_to_db (request, confirmation):
    if confirmation == 'confirm':
        printstring = """
            This function will write the anonymous marks entered so far into the database. After this, the marks of all students
            will be visible. 
            <br><br>
            Are you sure you want to go ahead?<br><br>
            <a href="/write_anonymous_marks_to_db/de_anonymise" class="btn btn-primary" type="button">Go ahead</a>
            """
        title = "Confirm De-Anonymisation"
    elif confirmation == 'de_anonymise':
        metadata = MetaData.objects.get(id = 1)
        year = metadata.current_year
        modules = Module.objects.filter(year = year)
        for module in modules:
            all_anonymous_marks = AnonymousMarks.objects.filter(module = module)
            for anonymous_marks in all_anonymous_marks:
                student = Student.objects.get(exam_id = anonymous_marks.exam_id)
                performance = Performance.objects.get(student = student, module = module)

                # Remove the comments if you want to allow anonymous marking for assessments other than the exam

#                if anonymous_marks.assessment_1:
#                    if anonymous_marks.assessment_1 != performance.assessment_1:
#                        if performance.assessment_1_modified:
#                            if anonymous_marks.assessment_1_modified > performance.assessment_1.modified:
#                                performance.assessment_1 = anonymous_marks.assessment_1
#                                performance.assessment_1_modified = anonymous_marks.assessment_1_modified
#                        else:
#                            performance.assessment_1 = anonymous_marks.assessment_1
#                            performance.assessment_1_modified = anonymous_marks.assessment_1_modified
#                if anonymous_marks.assessment_2:
#                    if anonymous_marks.assessment_2 != performance.assessment_2:
#                        if performance.assessment_2_modified:
#                            if anonymous_marks.assessment_2_modified > performance.assessment_2.modified:
#                                performance.assessment_2 = anonymous_marks.assessment_2
#                                performance.assessment_2_modified = anonymous_marks.assessment_2_modified
#                        else:
#                            performance.assessment_2 = anonymous_marks.assessment_2
#                            performance.assessment_2_modified = anonymous_marks.assessment_2_modified
#                if anonymous_marks.assessment_3 != performance.assessment_3:
#                    if performance.assessment_3_modified:
#                        if anonymous_marks.assessment_3_modified > performance.assessment_3.modified:
#                            performance.assessment_3 = anonymous_marks.assessment_3
#                            performance.assessment_3_modified = anonymous_marks.assessment_3_modified
#                    else:
#                        performance.assessment_3 = anonymous_marks.assessment_3
#                        performance.assessment_3_modified = anonymous_marks.assessment_3_modified
#                if anonymous_marks.assessment_4 != performance.assessment_4:
#                    if performance.assessment_4_modified:
#                        if anonymous_marks.assessment_4_modified > performance.assessment_4.modified:
#                            performance.assessment_4 = anonymous_marks.assessment_4
#                            performance.assessment_4_modified = anonymous_marks.assessment_4_modified
#                    else:
#                        performance.assessment_4 = anonymous_marks.assessment_4
#                        performance.assessment_4_modified = anonymous_marks.assessment_4_modified
#                if anonymous_marks.assessment_5 != performance.assessment_5:
#                    if performance.assessment_5_modified:
#                        if anonymous_marks.assessment_5_modified > performance.assessment_5.modified:
#                            performance.assessment_5 = anonymous_marks.assessment_5
#                            performance.assessment_5_modified = anonymous_marks.assessment_5_modified
#                    else:
#                        performance.assessment_5 = anonymous_marks.assessment_5
#                        performance.assessment_5_modified = anonymous_marks.assessment_5_modified
#                if anonymous_marks.assessment_6 != performance.assessment_6:
#                    if performance.assessment_6_modified:
#                        if anonymous_marks.assessment_6_modified > performance.assessment_6.modified:
#                            performance.assessment_6 = anonymous_marks.assessment_6
#                            performance.assessment_6_modified = anonymous_marks.assessment_6_modified
#                    else:
#                        performance.assessment_6 = anonymous_marks.assessment_6
#                        performance.assessment_6_modified = anonymous_marks.assessment_6_modified
                if anonymous_marks.exam:
                    if anonymous_marks.exam != performance.exam:
                        if performance.exam_modified:
                            if anonymous_marks.exam_modified > performance.exam_modified:
                                performance.exam = anonymous_marks.exam
                                performance.exam_modified = anonymous_marks.exam_modified
                        else:
                            performance.exam = anonymous_marks.exam
                            performance.exam_modified = anonymous_marks.exam_modified

#                if anonymous_marks.r_assessment_1:
#                    if anonymous_marks.r_assessment_1 != performance.r_assessment_1:
#                        if performance.r_assessment_1_modified:
#                            if anonymous_marks.r_assessment_1_modified > performance.r_assessment_1.modified:
#                                performance.r_assessment_1 = anonymous_marks.r_assessment_1
#                                performance.r_assessment_1_modified = anonymous_marks.r_assessment_1_modified
#                        else:
#                            performance.r_assessment_1 = anonymous_marks.r_assessment_1
#                            performance.r_assessment_1_modified = anonymous_marks.r_assessment_1_modified
#                if anonymous_marks.r_assessment_2:
#                    if anonymous_marks.r_assessment_2 != performance.r_assessment_2:
#                        if performance.r_assessment_2_modified:
#                            if anonymous_marks.r_assessment_2_modified > performance.r_assessment_2.modified:
#                                performance.r_assessment_2 = anonymous_marks.r_assessment_2
#                                performance.r_assessment_2_modified = anonymous_marks.r_assessment_2_modified
#                        else:
#                            performance.r_assessment_2 = anonymous_marks.r_assessment_2
#                            performance.r_assessment_2_modified = anonymous_marks.r_assessment_2_modified
#                if anonymous_marks.r_assessment_3 != performance.r_assessment_3:
#                    if performance.r_assessment_3_modified:
#                        if anonymous_marks.r_assessment_3_modified > performance.r_assessment_3.modified:
#                            performance.r_assessment_3 = anonymous_marks.r_assessment_3
#                            performance.r_assessment_3_modified = anonymous_marks.r_assessment_3_modified
#                    else:
#                        performance.r_assessment_3 = anonymous_marks.r_assessment_3
#                        performance.r_assessment_3_modified = anonymous_marks.r_assessment_3_modified
#                if anonymous_marks.r_assessment_4 != performance.r_assessment_4:
#                    if performance.r_assessment_4_modified:
#                        if anonymous_marks.r_assessment_4_modified > performance.r_assessment_4.modified:
#                            performance.r_assessment_4 = anonymous_marks.r_assessment_4
#                            performance.r_assessment_4_modified = anonymous_marks.r_assessment_4_modified
#                    else:
#                        performance.r_assessment_4 = anonymous_marks.r_assessment_4
#                        performance.r_assessment_4_modified = anonymous_marks.r_assessment_4_modified
#                if anonymous_marks.r_assessment_5 != performance.r_assessment_5:
#                    if performance.r_assessment_5_modified:
#                        if anonymous_marks.r_assessment_5_modified > performance.r_assessment_5.modified:
#                            performance.r_assessment_5 = anonymous_marks.r_assessment_5
#                            performance.r_assessment_5_modified = anonymous_marks.r_assessment_5_modified
#                    else:
#                        performance.r_assessment_5 = anonymous_marks.r_assessment_5
#                        performance.r_assessment_5_modified = anonymous_marks.r_assessment_5_modified
#                if anonymous_marks.r_assessment_6 != performance.r_assessment_6:
#                    if performance.r_assessment_6_modified:
#                        if anonymous_marks.r_assessment_6_modified > performance.r_assessment_6.modified:
#                            performance.r_assessment_6 = anonymous_marks.r_assessment_6
#                            performance.r_assessment_6_modified = anonymous_marks.r_assessment_6_modified
#                    else:
#                        performance.r_assessment_6 = anonymous_marks.r_assessment_6
#                        performance.r_assessment_6_modified = anonymous_marks.r_assessment_6_modified
                if anonymous_marks.r_exam:
                    if anonymous_marks.r_exam != performance.r_exam:
                        if performance.r_exam_modified:
                            if anonymous_marks.r_exam_modified > performance.r_exam_modified:
                                performance.r_exam = anonymous_marks.r_exam
                                performance.r_exam_modified = anonymous_marks.r_exam_modified
                        else:
                            performance.r_exam = anonymous_marks.r_exam
                            performance.r_exam_modified = anonymous_marks.r_exam_modified
                
#                if anonymous_marks.q_assessment_1:
#                    if anonymous_marks.q_assessment_1 != performance.q_assessment_1:
#                        if performance.q_assessment_1_modified:
#                            if anonymous_marks.q_assessment_1_modified > performance.q_assessment_1.modified:
#                                performance.q_assessment_1 = anonymous_marks.q_assessment_1
#                                performance.q_assessment_1_modified = anonymous_marks.q_assessment_1_modified
#                        else:
#                            performance.q_assessment_1 = anonymous_marks.q_assessment_1
#                            performance.q_assessment_1_modified = anonymous_marks.q_assessment_1_modified
#                if anonymous_marks.q_assessment_2:
#                    if anonymous_marks.q_assessment_2 != performance.q_assessment_2:
#                        if performance.q_assessment_2_modified:
#                            if anonymous_marks.q_assessment_2_modified > performance.q_assessment_2.modified:
#                                performance.q_assessment_2 = anonymous_marks.q_assessment_2
#                                performance.q_assessment_2_modified = anonymous_marks.q_assessment_2_modified
#                        else:
#                            performance.q_assessment_2 = anonymous_marks.q_assessment_2
#                            performance.q_assessment_2_modified = anonymous_marks.q_assessment_2_modified
#                if anonymous_marks.q_assessment_3 != performance.q_assessment_3:
#                    if performance.q_assessment_3_modified:
#                        if anonymous_marks.q_assessment_3_modified > performance.q_assessment_3.modified:
#                            performance.q_assessment_3 = anonymous_marks.q_assessment_3
#                            performance.q_assessment_3_modified = anonymous_marks.q_assessment_3_modified
#                    else:
#                        performance.q_assessment_3 = anonymous_marks.q_assessment_3
#                        performance.q_assessment_3_modified = anonymous_marks.q_assessment_3_modified
#                if anonymous_marks.q_assessment_4 != performance.q_assessment_4:
#                    if performance.q_assessment_4_modified:
#                        if anonymous_marks.q_assessment_4_modified > performance.q_assessment_4.modified:
#                            performance.q_assessment_4 = anonymous_marks.q_assessment_4
#                            performance.q_assessment_4_modified = anonymous_marks.q_assessment_4_modified
#                    else:
#                        performance.q_assessment_4 = anonymous_marks.q_assessment_4
#                        performance.q_assessment_4_modified = anonymous_marks.q_assessment_4_modified
#                if anonymous_marks.q_assessment_5 != performance.q_assessment_5:
#                    if performance.q_assessment_5_modified:
#                        if anonymous_marks.q_assessment_5_modified > performance.q_assessment_5.modified:
#                            performance.q_assessment_5 = anonymous_marks.q_assessment_5
#                            performance.q_assessment_5_modified = anonymous_marks.q_assessment_5_modified
#                    else:
#                        performance.q_assessment_5 = anonymous_marks.q_assessment_5
#                        performance.q_assessment_5_modified = anonymous_marks.q_assessment_5_modified
#                if anonymous_marks.q_assessment_6 != performance.q_assessment_6:
#                    if performance.q_assessment_6_modified:
#                        if anonymous_marks.q_assessment_6_modified > performance.q_assessment_6.modified:
#                            performance.q_assessment_6 = anonymous_marks.q_assessment_6
#                            performance.q_assessment_6_modified = anonymous_marks.q_assessment_6_modified
#                    else:
#                        performance.q_assessment_6 = anonymous_marks.q_assessment_6
#                        performance.q_assessment_6_modified = anonymous_marks.q_assessment_6_modified
                if anonymous_marks.q_exam:
                    if anonymous_marks.q_exam != performance.q_exam:
                        if performance.q_exam_modified:
                            if anonymous_marks.q_exam_modified > performance.q_exam_modified:
                                performance.q_exam = anonymous_marks.q_exam
                                performance.q_exam_modified = anonymous_marks.q_exam_modified
                        else:
                            performance.q_exam = anonymous_marks.q_exam
                            performance.q_exam_modified = anonymous_marks.q_exam_modified

                performance.save_with_avg()
            yearp1 = year + 1
            printstring = "The anonymous marks for %s/%s have been transferred to the database."%(year, yearp1)
            title = "CCCU Law DB"

    return render_to_response(
            'blank.html', 
            {'printstring': printstring, 'title': title},
            context_instance = RequestContext(request))
