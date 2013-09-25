from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext


from database.models import Student, Module, Course
from database import functions

def is_teacher(user):
    if user:
        if user.groups.filter(name='teachers').count() == 1:
            return True
        else:
            return False
    else:
        return False

@login_required
@user_passes_test(is_teacher)
def default_page(request):
    title = 'CCCU Law DB'
    return render_to_response('home.html',
            {},
            context_instance = RequestContext(request)
            )


def na(request):
    printstring = 'This function is not available yet'
    title = 'CCCU Law DB: Not available'
    return render_to_response('blank.html', {'printstring': printstring, 'title': title}, context_instance = RequestContext(request))
