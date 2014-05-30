from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError

from feedback.models import *
from database.models import *
from database.views import is_teacher, is_admin
from feedback import forms 
from feedback.categories import *
from mysds.unisettings import *

@login_required
@user_passes_test(is_teacher)
def edit_feedback(request, module_id, year, assessment, student_id):
    """The form for all feedback sheets"""
    module = Module.objects.get(code=module_id, year=year)
    student = Student.objects.get(student_id=student_id)
    performance = Performance.objects.get(module=module, student=student)
    assessment_title = module.get_assessment_title(assessment)
    assessment = int(assessment)
    mark = performance.get_assessment_result(assessment)
    deadline = module.get_assessment_submission_date(assessment)
    penalty = LATE_SUBMISSION_PENALTY
    today = datetime.date.today()
    marksheet_type = module.get_marksheet_type(assessment)
    if marksheet_type == 'NEGOTIATION_WRITTEN':
        categories = CATEGORIES[marksheet_type]
        group = performance.group_assessment_group
        try:
            group_feedback = GroupMarksheet.objects.get(
                    module=module,
                    assessment=assessment,
                    group_no = group
                    )
        except GroupMarksheet.DoesNotExist:
            group_feedback = GroupMarksheet(
                    module = module,
                    assessment = assessment,
                    group_no = group,
                    marker = request.user,
                    marking_date = datetime.datetime.today
                    )
        jump_to = "#" + student.student_id
        all_group_members = Performance.objects.filter(
                module = module, group_assessment_group = group)
        marksheets = {} 
        student_ids = []
        for performance in all_group_members:
            student_ids.append(performance.student.student_id)
            try:
                feedback = Marksheet.objects.get(
                        module=module, 
                        student=performance.student, 
                        assessment=assessment
                        )
                edit = True
            except Marksheet.DoesNotExist:
                edit = False
                feedback = Marksheet(
                        student = performance.student,
                        module = module,
                        assessment = assessment,
                        marker = request.user,
                        marking_date = today
                        )
            marksheets[performance.student] = feedback
        teachers = []
        all_teachers = User.objects.filter(groups__name='teachers')
        for teacher in all_teachers:
            this = {}
            if teacher == group_feedback.marker:
                this['marker'] = True
            else:
                this['marker'] = False
            if teacher == group_feedback.second_first_marker:
                this['second_first_marker'] = True
            else:
                this['second_first_marker'] = False
            this['id'] = teacher.id
            this['name'] = teacher.first_name + " " + teacher.last_name
            teachers.append(this)
        if request.method == 'POST':
            marker_id = request.POST['marker']
            if marker_id == '0':
                marker = None
            else:
                marker = User.objects.get(id=marker_id)
            second_first_marker_id = request.POST['second_first_marker']
            if second_first_marker_id == '0':
                second_first_marker = None
            else:
                second_first_marker = User.objects.get(
                        id=second_first_marker_id)
            marking_date_string = request.POST['marking_date']
            tmp = marking_date_string.split("/")
            marking_date = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
            try:
                presentation_date = request.POST['presentation_date']
                tmp = presentation_date.split("/")
                presentation_date = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
            except (ValidationError, IndexError):
                presentation_date = None
            try:
                tmp = int(request.POST['group_category_mark_1'])
                if tmp <= 10:
                    group_mark_1 = tmp
                    group_feedback.category_mark_1_free = group_mark_1
                else:
                    group_mark_1 = 0
            except ValueError:
                group_mark_1 = 0
            try:
                tmp = int(request.POST['group_category_mark_2'])
                if tmp <= 10:
                    group_mark_2 = tmp
                    group_feedback.category_mark_2_free = group_mark_2
                else:
                    group_mark_2 = 0
            except ValueError:
                group_mark_2 = 0
            try:
                tmp = int(request.POST['group_category_mark_3'])
                if tmp <= 10:
                    group_mark_3 = tmp
                    group_feedback.category_mark_3_free = group_mark_3
                else:
                    group_mark_3 = 0
            except ValueError:
                group_mark_3 = 0
            try:
                tmp = int(request.POST['group_category_mark_4'])
                if tmp <= 10:
                    group_mark_4 = tmp
                    group_feedback.category_mark_4_free = group_mark_4
                else:
                    group_mark_4 = 0
            except ValueError:
                group_mark_4 = 0
            group_sum = (
                    group_mark_1 + group_mark_2 +
                    group_mark_3 + group_mark_4
                    )
            group_feedback.group_comments = request.POST['group_comments']
            group_feedback.marker = marker
            group_feedback.second_first_marker = second_first_marker
            group_feedback.marking_date = marking_date
            group_feedback.submission_date = presentation_date
            group_feedback.save()
            for student, marksheet in marksheets.items():
                marksheet.marker = marker
                marksheet.second_first_marker = second_first_marker
                try:
                    tmp = int(request.POST[
                        student.student_id + '_category_mark_1'])
                    if tmp <= 40:
                        individual_mark_1 = tmp
                        marksheet.category_mark_1_free = individual_mark_1
                    else:
                        individual_mark_1 = 0
                except ValueError:
                    individual_mark_1 = 0
                try:
                    tmp = int(request.POST[
                        student.student_id + '_category_mark_2'])
                    if tmp <= 10:
                        individual_mark_2 = tmp
                        marksheet.category_mark_2_free = individual_mark_2
                    else:
                        individual_mark_2 = 0
                except ValueError:
                    individual_mark_2 = 0
                try:
                    tmp = int(request.POST[
                        student.student_id + '_category_mark_3'])
                    if tmp <= 10:
                        individual_mark_3 = tmp
                        marksheet.category_mark_3_free = individual_mark_3
                    else:
                        individual_mark_3 = 0
                except ValueError:
                    individual_mark_3 = 0
                try:
                    tmp = int(request.POST[
                        student.student_id + '_category_mark_4'])
                    if tmp <= 12:
                        deductions = tmp
                        marksheet.category_mark_4_free = deductions
                    else:
                        deductions = 0
                except ValueError:
                    deductions = 0
                marksheet.comments = request.POST[
                        student.student_id + '_comments']
                marksheet.save()
                mark = (
                        group_sum + individual_mark_1 +
                        individual_mark_2 + individual_mark_3
                        )
                mark -= deductions
                performance = Performance.objects.get(
                        student = student, module = module)
                performance.set_assessment_result(assessment, mark)
            return HttpResponseRedirect(module.get_absolute_url())
        return render_to_response(
                'negotiation_feedback_form.html',
                {
                        'group_feedback': group_feedback,
                        'marksheets': marksheets,
                        'module': module,
                        'mark': mark,
                        'categories': categories,
                        'student_ids': student_ids,
                        'group_no': group,
                        'assessment': assessment_title,
                        'teachers': teachers
                },
                context_instance = RequestContext(request)
                )

    elif marksheet_type == 'ESSAY_LEGAL_PROBLEM':
        categories = CATEGORIES['ESSAY']
        categories_2 = CATEGORIES['LEGAL_PROBLEM']
        average_split = [1,1]
        denominator = 2
        try:
            feedback = Marksheet.objects.get(
                    module=module, student=student, assessment=assessment)
            edit = True
        except Marksheet.DoesNotExist:
            edit = False
            feedback = Marksheet(
                    student = student,
                    module = module,
                    assessment = assessment,
                    marker = request.user,
                    marking_date = today
                    )
        if request.method == 'POST':
            form = forms.EssayForm(instance=feedback, data=request.POST)
            if form.is_valid():
                form.save()
                mark = None
                if (form.cleaned_data['part_1_mark'] 
                        and form.cleaned_data['part_2_mark']):
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
                if mark in range(0,100):
                    performance.set_assessment_result(assessment, mark)
            return HttpResponseRedirect(module.get_absolute_url())
        form = forms.EssayForm(instance=feedback)
        return render_to_response(
                'individual_feedback_form.html',
                {
                    'form': form,
                    'module': module,
                    'student': student,
                    'mark': mark,
                    'two_parts': True,
                    'assessment': assessment_title,
                    'categories': categories,
                    'categories_2': categories_2,
                    'edit': edit,
                    'average_split': average_split,
                    'denominator': denominator,
                    'penalty': penalty,
                    'deadline': deadline
                },
                context_instance = RequestContext(request)
                )

    elif marksheet_type == 'ONLINE_TEST_COURT_REPORT':
        categories = CATEGORIES['ESSAY']
        average_split = [15,10]
        denominator = 25
        try:
            feedback = Marksheet.objects.get(
                    module=module, student=student, assessment=assessment)
            edit = True
        except Marksheet.DoesNotExist:
            edit = False
            feedback = Marksheet(
                    student = student,
                    module = module,
                    assessment = assessment,
                    marker = request.user,
                    marking_date = today
                    )
        if request.method == 'POST':
            form = forms.EssayForm(instance=feedback, data=request.POST)
            if form.is_valid():
                form.save()
                mark = None
                if (form.cleaned_data['part_1_mark'] 
                        and form.cleaned_data['part_2_mark']):
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
                if mark in range(0,100):
                    performance.set_assessment_result(assessment, mark)
            return HttpResponseRedirect(module.get_absolute_url())
        form = forms.EssayForm(instance=feedback)
        return render_to_response(
                'individual_feedback_form.html',
                {
                    'form': form,
                    'module': module,
                    'student': student,
                    'assessment': assessment_title,
                    'mark': mark,
                    'online_court': True,
                    'categories': categories,
                    'edit': edit,
                    'average_split': average_split,
                    'denominator': denominator,
                    'penalty': penalty,
                    'deadline': deadline
                },
                context_instance = RequestContext(request)
                )

    else: # Generic marksheet, fine for Essay, Legal Problem and Presentation
        categories = CATEGORIES[marksheet_type]
        try:
            feedback = Marksheet.objects.get(
                    module=module, student=student, assessment=assessment)
            edit = True
        except Marksheet.DoesNotExist:
            edit = False
            feedback = Marksheet(
                    student = student,
                    module = module,
                    assessment = assessment,
                    marker = request.user,
                    marking_date = today
                    )
        if request.method == 'POST':
            form = forms.EssayForm(instance=feedback, data=request.POST)
            if form.is_valid():
                form.save()
                if request.POST['mark']:
                    tmp = request.POST['mark']
                    try:
                        mark = int(tmp)
                    except ValueError:
                        mark = None
                if mark in range(0,100):
                    performance.set_assessment_result(assessment, mark)
            return HttpResponseRedirect(module.get_absolute_url())
        form = forms.EssayForm(instance=feedback)
        return render_to_response(
                'individual_feedback_form.html',
                {
                    'form': form,
                    'module': module,
                    'student': student,
                    'mark': mark,
                    'assessment': assessment_title,
                    'categories': categories,
                    'edit': edit,
                    'penalty': penalty,
                    'deadline': deadline
                },
                context_instance = RequestContext(request)
                )
