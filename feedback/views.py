from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
#from django.db.models import Q
#from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import datetime
#from django.utils import simplejson

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
    elif assessment == '2':
        assessment_title = module.assessment_2_title
        essay_mark = performance.assessment_2
    elif assessment == '3':
        assessment_title = module.assessment_3_title
        essay_mark = performance.assessment_3
    elif assessment == '4':
        assessment_title = module.assessment_4_title
        essay_mark = performance.assessment_4
    elif assessment == '5':
        assessment_title = module.assessment_5_title
        essay_mark = performance.assessment_5
    elif assessment == '6':
        assessment_title = module.assessment_6_title
        essay_mark = performance.assessment_5
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
    feedback_type = FeedbackCategories.objects.get(assessment_type = 'Essay')
    if request.method == 'POST':
        form = forms.EssayForm(instance=feedback, data=request.POST)
        if form.is_valid():
            form.save()
            if request.POST['mark']:
                tmp = request.POST['mark']
                try:
                    mark = int(tmp)
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
                except ValueError:
                    pass

            
            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = forms.EssayForm(instance=feedback)
    return render_to_response('essay_feedback_form.html',
            {'form': form, 'module': module, 'student': student, 'essay_mark': essay_mark,
                'assessment': assessment_title, 'categories': feedback_type, 'edit': edit},
            context_instance = RequestContext(request)
            )
    
@login_required
@user_passes_test(is_teacher)
def add_essay_feedback(request):
    return HttpResponseRedirect('/na')
