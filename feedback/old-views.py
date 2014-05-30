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

# Functions

@login_required
@user_passes_test(is_teacher)
def edit_essay_feedback(request, module_id, year, assessment, student_id):
    penalty = LATE_SUBMISSION_PENALTY
    assessment_int = int(assessment)
    module = Module.objects.get(code=module_id, year=year)
    student = Student.objects.get(student_id=student_id)
    performance = Performance.objects.get(module = module, student = student)
    assessment_title = module.get_assessment_title(assessment)
    essay_mark = performance.get_assessment_result(assessment)
    feedback_type = module.get_assessment_type(assessment)
    deadline = module.get_assessment_submission_date(assessment)
    essay_legal_problem = FeedbackCategories.objects.get(assessment_type = 'Essay / Legal Problem')
    online_test_court_report = FeedbackCategories.objects.get(assessment_type = 'Online Test / Court Report')
    negotiation_written = FeedbackCategories.objects.get(assessment_type = 'Negotiation / Written Submission')
    group_mark = False
    group_and_individual = False
    need_average = False
    two_parts = False
    online_court = False
    average_split = False 
    negotiation_written_submission = False
    today = datetime.date.today()
    student_ids = [] # Only needed for the group marksheets
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
    elif feedback_type == negotiation_written:
        negotiation_written_submission = True
        group_mark = True
        group_and_individual = True

    if need_average:
        denominator = average_split[0] + average_split[1]
    else:
        denominator = 1
    if group_mark:
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
            jump_to = "#" + student.student_id
            all_group_members = Performance.objects.filter(module = module, group_assessment_group = group)
            marksheets = {} 
            for performance in all_group_members:
                student_ids.append(performance.student.student_id)
                try:
                    feedback = Marksheet.objects.get(module=module, student=performance.student, assessment=assessment_int)
                    edit = True
                except Marksheet.DoesNotExist:
                    edit = False
                    feedback = Marksheet(
                            student = performance.student,
                            module = module,
                            assessment = assessment_int,
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

    else: # Individual mark
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
                    marking_date = today
                    )
    if request.method == 'POST':
        if group_mark:
            marker_id = request.POST['marker']
            if marker_id == '0':
                marker = None
            else:
                marker = User.objects.get(id=marker_id)
            second_first_marker_id = request.POST['second_first_marker']
            if second_first_marker_id == '0':
                second_first_marker = None
            else:
                second_first_marker = User.objects.get(id=second_first_marker_id)
            #submission_date = request.POST['submission_date']
            marking_date_string = request.POST['marking_date']
            tmp = marking_date_string.split("/")
            marking_date = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
            try:
                presentation_date = request.POST['presentation_date']
                tmp = presentation_date.split("/")
                presentation_date = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
            except (ValidationError, IndexError):
                presentation_date = None
            if negotiation_written_submission:
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
                group_sum = group_mark_1 + group_mark_2 + group_mark_3 + group_mark_4
                group_feedback.group_comments = request.POST['group_comments']
                group_feedback.marker = marker
                group_feedback.second_first_marker = second_first_marker
                group_feedback.marking_date = marking_date
                group_feedback.submission_date = presentation_date
                group_feedback.save()
                for student, marksheet in marksheets.items():
                    marksheet.marker = marker
                    marksheet.second_first_marker = second_first_marker
#                    print student
#                    print marksheet.second_first_marker
#                    print "----"
                    try:
                        tmp = int(request.POST[student.student_id + '_category_mark_1'])
                        if tmp <= 40:
                            individual_mark_1 = tmp
                            marksheet.category_mark_1_free = individual_mark_1
                        else:
                            individual_mark_1 = 0
                    except ValueError:
                        individual_mark_1 = 0
                    try:
                        tmp = int(request.POST[student.student_id + '_category_mark_2'])
                        if tmp <= 10:
                            individual_mark_2 = tmp
                            marksheet.category_mark_2_free = individual_mark_2
                        else:
                            individual_mark_2 = 0
                    except ValueError:
                        individual_mark_2 = 0
                    try:
                        tmp = int(request.POST[student.student_id + '_category_mark_3'])
                        if tmp <= 10:
                            individual_mark_3 = tmp
                            marksheet.category_mark_3_free = individual_mark_3
                        else:
                            individual_mark_3 = 0
                    except ValueError:
                        individual_mark_3 = 0
                    try:
                        tmp = int(request.POST[student.student_id + '_category_mark_4'])
                        if tmp <= 12:
                            deductions = tmp
                            marksheet.category_mark_4_free = deductions
                        else:
                            deductions = 0
                    except ValueError:
                        deductions = 0
                    marksheet.comments = request.POST[student.student_id + '_comments']
                    marksheet.save()
                    mark = group_sum + individual_mark_1 + individual_mark_2 + individual_mark_3
                    mark -= deductions
                    performance = Performance.objects.get(student = student, module = module)
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
    if group_mark:
        if negotiation_written_submission:
            return render_to_response('negotiation_feedback_form.html',
                        {'group_feedback': group_feedback, 'marksheets': marksheets, 'module': module,
                            'categories': feedback_type, 'student_ids': student_ids,
                            'group_no': group, 'assessment': assessment_title, 'teachers': teachers},
                        context_instance = RequestContext(request)
                    )
        else:
            return HttpResponseRedirect('/na')
    else:
        form = forms.EssayForm(instance=feedback)
        return render_to_response('essay_feedback_form.html',
                {'form': form, 'module': module, 'student': student, 'essay_mark': essay_mark,
                    'two_parts': two_parts, 'assessment': assessment_title, 'online_court': online_court,
                    'categories': feedback_type, 'edit': edit, 'average_split': average_split,
                    'denominator': denominator, 'penalty': penalty, 'deadline': deadline},
                context_instance = RequestContext(request)
                )

