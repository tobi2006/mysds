from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User

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

def reset_password(request):
    if 'email' in request.GET and request.GET['email']:
        email = request.GET['email']
        user = User.objects.get(email = email)
        new_password = User.objects.make_random_password()
        user.set_password(new_password)
        user.save()

        message = """
        Dear %s,
        
        You have requested your details from MySDS, the CCCU database. Here they are:

        Username: %s
        Password: %s

        Please be aware that the form is case sensitive, so make sure you use upper- and lowercase correctly.

        After successfully logging in with the above details, please click on "My Account" and change your password to one that is both easy to remember and difficult to guess. Make sure you do not use the same password for many different websites. A good way to ensure password safety and convenience is to use a password manager like KeepassX, Last Pass or One Password. All of them are available for almost all browsers and platforms.

        Best wishes,

        Your friendly MySDS Admin
        """%(user.first_name, user.username, new_password)

        send_mail('MySDS - New login information', message, 'cccu@tobiaskliem.de', [user.email,])
#        print message #Just for local testing (no SMTP server on this machine)

    return HttpResponseRedirect('/')


def na(request):
    printstring = 'This function is not available yet'
    title = 'CCCU Law DB: Not available'
    return render_to_response('blank.html', {'printstring': printstring, 'title': title}, context_instance = RequestContext(request))
