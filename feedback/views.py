from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import datetime

from feedback.models import *
from database.models import *
from database.views import is_teacher, is_admin
from feedback import forms 
from mysds.unisettings import *

@login_required
@user_passes_test(is_teacher)
def edit_groupwork_feedback(request, module_id, year, assessment, student_id):
    module = Module.objects.get(code=module_id, year=year)
    student = Student.objects.get(student_id=student_id)
    jump_to = "#" + student.student_id
    performance = Performance.objects.get(module = module, student = student)
    assessment_int = int(assessment)
    if assessment == '1':
        assessment_title = module.assessment_1_title
        essay_mark = performance.assessment_1
        feedback_type = module.assessment_1_type
        deadline = module.assessment_1_submission_date
    elif assessment == '2':
        assessment_title = module.assessment_2_title
        essay_mark = performance.assessment_2
        feedback_type = module.assessment_2_type
        deadline = module.assessment_2_submission_date
    elif assessment == '3':
        assessment_title = module.assessment_3_title
        essay_mark = performance.assessment_3
        feedback_type = module.assessment_3_type
        deadline = module.assessment_3_submission_date
    elif assessment == '4':
        assessment_title = module.assessment_4_title
        essay_mark = performance.assessment_4
        feedback_type = module.assessment_4_type
        deadline = module.assessment_4_submission_date
    elif assessment == '5':
        assessment_title = module.assessment_5_title
        essay_mark = performance.assessment_5
        feedback_type = module.assessment_5_type
        deadline = module.assessment_5_submission_date
    elif assessment == '6':
        assessment_title = module.assessment_6_title
        essay_mark = performance.assessment_6
        feedback_type = module.assessment_6_type
        deadline = module.assessment_6_submission_date
    n_w = False
    group_and_individual = False
    negotiation_written = FeedbackCategries.objects.get(assessment_type = 'Negotiation / Written Submission')
    if feedback_type == negotiation_written:
        n_w = True
        group_and_individual = True
    group = performance.group_assessment_group
    try:
        group_feedback = GroupMarksheet.objects.get(module=module, assessment=assessment_int, group_no = group)
    except GroupMarksheet.DoesNotExist:
        group_feedback = GroupMarksheet(
                module = module,
                assessment = assessment_int,
                group_no = group,
                marker = request.user,
                marking_date = datetime.datetime.today
                )
    if group_and_individual:
        all_group_members = Performance.objects.filter(module = module, group_assessment_group = group)
        students = []
        for student in all_group_members:
            try:
                group_feedback = Marksheet.objects.get(module=module, student=student, assessment=assessment_int)
                edit = True
            except Marksheet.DoesNotExist:
                edit = False
                group_feedback = Marksheet(
                        student = student,
                        module = module,
                        assessment = assessment_int,
                        marker = request.user,
                        marking_date = datetime.datetime.today
                        )
            students.append(feedback)
    if n_w:
        return render_to_response('negotiation_feedback_form.html',
                {'group_feedback': group_feedback, 'students': students, 'module': module,
                    'group_no': group_no, 'assessment': assessment_title},
                context_instance = RequestContext(request)
            )
    else:
        return HttpResponseRedirect('/na')


@login_required
@user_passes_test(is_teacher)
def edit_essay_feedback(request, module_id, year, assessment, student_id):
    penalty = LATE_SUBMISSION_PENALTY
    module = Module.objects.get(code=module_id, year=year)
    student = Student.objects.get(student_id=student_id)
    performance = Performance.objects.get(module = module, student = student)
    assessment_int = int(assessment)
    if assessment == '1':
        assessment_title = module.assessment_1_title
        essay_mark = performance.assessment_1
        feedback_type = module.assessment_1_type
        deadline = module.assessment_1_submission_date
    elif assessment == '2':
        assessment_title = module.assessment_2_title
        essay_mark = performance.assessment_2
        feedback_type = module.assessment_2_type
        deadline = module.assessment_2_submission_date
    elif assessment == '3':
        assessment_title = module.assessment_3_title
        essay_mark = performance.assessment_3
        feedback_type = module.assessment_3_type
        deadline = module.assessment_3_submission_date
    elif assessment == '4':
        assessment_title = module.assessment_4_title
        essay_mark = performance.assessment_4
        feedback_type = module.assessment_4_type
        deadline = module.assessment_4_submission_date
    elif assessment == '5':
        assessment_title = module.assessment_5_title
        essay_mark = performance.assessment_5
        feedback_type = module.assessment_5_type
        deadline = module.assessment_5_submission_date
    elif assessment == '6':
        assessment_title = module.assessment_6_title
        essay_mark = performance.assessment_6
        feedback_type = module.assessment_6_type
        deadline = module.assessment_6_submission_date
    essay_legal_problem = FeedbackCategories.objects.get(assessment_type = 'Essay / Legal Problem')
    online_test_court_report = FeedbackCategories.objects.get(assessment_type = 'Online Test / Court Report')
    need_average = False
    two_parts = False
    online_court = False
    average_split = False 
    if feedback_type == essay_legal_problem:
        need_average = True
        two_parts = True
        average_split = [1,1] # give the split: part 1 is worth 1, part 2 is worth 1 (50/50 split)
    elif feedback_type == online_test_court_report:
        need_average = True
        online_court = True
        average_split = [15,10]
        # I was asked to set this up in a way to make sure that part a is worth 10 % of the module mark
        # and part 2 15 %. Hence the strange numbers...
    if need_average:
        denominator = average_split[0] + average_split[1]
    else:
        denominator = 1
    try:
        feedback = Marksheet.objects.get(module=module, student=student, assessment=assessment_int)
        edit = True
    except Marksheet.DoesNotExist:
        edit = False
        feedback = Marksheet(
                student = student,
                module = module,
                assessment = assessment_int,
                marker = request.user,
                marking_date = datetime.datetime.today
                )
    if request.method == 'POST':
        form = forms.EssayForm(instance=feedback, data=request.POST)
        if form.is_valid():
            form.save()
            entry_error = False
            mark = None
            if need_average:
                if form.cleaned_data['part_1_mark'] and form.cleaned_data['part_2_mark']:
                    part_1 = int(form.cleaned_data['part_1_mark'])
                    part_2 = int(form.cleaned_data['part_2_mark'])
                    part_1 = part_1 * average_split[0]
                    part_2 = part_2 * average_split[1]
                    tmp = float(part_1 + part_2)
                    floatmark = tmp / denominator
                    mark = round(floatmark)
                elif form.cleaned_data['part_1_mark']:
                    tmp = float(form.cleaned_data['part_1_mark'])
                    tmp = tmp * average_split[0]
                    floatmark = tmp / denominator
                    mark = round(floatmark)
                elif form.cleaned_data['part_2_mark']:
                    tmp = float(form.cleaned_data['part_2_mark'])
                    tmp = tmp * average_split[1]
                    floatmark = tmp / denominator
                    mark = round(floatmark)
                else:
                    mark = 0
            elif request.POST['mark']:
                tmp = request.POST['mark']
                try:
                    mark = int(tmp)
                except ValueError:
                    entry_error = True
            if not entry_error:
                if mark in range(0,100):
                    if assessment == '1':
                        performance.assessment_1 = mark
                    elif assessment == '2':
                        performance.assessment_2 = mark
                    elif assessment == '3':
                        performance.assessment_3 = mark
                    elif assessment == '4':
                        performance.assessment_4 = mark
                    elif assessment == '5':
                        performance.assessment_5 = mark
                    elif assessment == '6':
                        performance.assessment_6 = mark
                    performance.save_with_avg()
            
            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = forms.EssayForm(instance=feedback)
    return render_to_response('essay_feedback_form.html',
            {'form': form, 'module': module, 'student': student, 'essay_mark': essay_mark,
                'two_parts': two_parts, 'assessment': assessment_title, 'online_court': online_court,
                'categories': feedback_type, 'edit': edit, 'average_split': average_split,
                'denominator': denominator, 'penalty': penalty, 'deadline': deadline},
            context_instance = RequestContext(request)
            )
