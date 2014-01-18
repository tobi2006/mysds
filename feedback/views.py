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

@login_required
@user_passes_test(is_teacher)
def edit_essay_feedback(request, module_id, year, assessment, student_id):
    module = Module.objects.get(code=module_id, year=year)
    student = Student.objects.get(student_id=student_id)
    performance = Performance.objects.get(module = module, student = student)
    assessment_int = int(assessment)
    if assessment == '1':
        assessment_title = module.assessment_1_title
        essay_mark = performance.assessment_1
        feedback_type = module.assessment_1_type
    elif assessment == '2':
        assessment_title = module.assessment_2_title
        essay_mark = performance.assessment_2
        feedback_type = module.assessment_2_type
    elif assessment == '3':
        assessment_title = module.assessment_3_title
        essay_mark = performance.assessment_3
        feedback_type = module.assessment_3_type
    elif assessment == '4':
        assessment_title = module.assessment_4_title
        essay_mark = performance.assessment_4
        feedback_type = module.assessment_4_type
    elif assessment == '5':
        assessment_title = module.assessment_5_title
        essay_mark = performance.assessment_5
        feedback_type = module.assessment_5_type
    elif assessment == '6':
        assessment_title = module.assessment_6_title
        essay_mark = performance.assessment_5
        feedback_type = module.assessment_5_type
    essay_legal_problem = FeedbackCategories.objects.get(assessment_type = 'Essay / Legal Problem')
    online_test_court_report = FeedbackCategories.objects.get(assessment_type = 'Online Test / Court Report')
    need_average = False
    two_parts = False
    online_court = False
    if feedback_type == essay_legal_problem:
        need_average = True
        two_parts = True
    elif feedback_type == online_test_court_report:
        need_average = True
        online_court = True
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
                    tmp = float(part_1 + part_2)
                    floatmark = tmp / 2
                    mark = round(floatmark)
                elif form.cleaned_data['part_1_mark']:
                    tmp = float(form.cleaned_data['part_1_mark'])
                    floatmark = tmp / 2
                    mark = round(floatmark)
                elif form.cleaned_data['part_2_mark']:
                    tmp = float(form.cleaned_data['part_2_mark'])
                    floatmark = tmp / 2
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
                'categories': feedback_type, 'edit': edit},
            context_instance = RequestContext(request)
            )
