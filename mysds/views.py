from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from database.models import Student, Module, Course
from database import functions


def default_page(request):
    modules = functions.modules_for_menubar() 
    return render_to_response('home.html', {'module_dict': modules})

def na(request):
    modules = functions.modules_for_menubar() 
    printstring = 'This function is not available yet'
    title = 'CCCU Law DB: Not available'
    return render_to_response('blank.html', {'printstring': printstring, 'title': title, 'module_dict': modules})
