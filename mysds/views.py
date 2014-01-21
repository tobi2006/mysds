from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

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
        try:
            user = User.objects.get(email = email)
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            first_name = user.first_name.split(" ")[0] # only first forename
            message = """
            Dear %s,
            
    You have requested your details from MySDS, the CCCU database. Here they are:

    Username: %s
    Password: %s

    Please be aware that the form is case sensitive, so make sure you use upper- and lowercase correctly.

    After successfully logging in with the above details, please click on "My Account" and change your password to one that is both easy to remember and difficult to guess. Make sure you do not use the same password for many different websites. A good way to ensure password safety and convenience is to use a password manager like KeepassX, Last Pass or One Password. All of them are available for almost all browsers and platforms.

    Best wishes,

    Your friendly MySDS Admin
            """%(first_name, user.username, new_password)

            send_mail('MySDS - New login information', message, 'cccu@tobiaskliem.de', [user.email,])
        except User.DoesNotExist:
            return HttpResponseRedirect('/wrong_email')
#        print message #Just for local testing (no SMTP server on this machine)

    return HttpResponseRedirect('/')

@login_required
def invite_students(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('selected_student_id')
        student_group = Group.objects.get(name = 'students')
        for student_id in student_ids:
            student = Student.objects.get(student_id = student_id)
            first_part = student.first_name[0] + student.last_name[0]
            first_part = first_part.lower()
            number = 1
            still_searching = True
            while still_searching:
                username = first_part + str(number)
                if User.objects.filter(username = username).exists():
                    number += 1
                else:
                    still_searching = False
            user = User(username = username, email = student.email)
            user.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            student.belongs_to = user
            student.save()
            student_group.user_set.add(user)
            student_group.save()
            first_name = student.first_name.split(" ")[0] # only first forename
            message = """
Dear %s,

You now have access to MySDS, the Student Database for Law at Canterbury Christ Church University.

The database is available at https://cccu.tobiaskliem.de, and you can access it with the following details:

Username: %s
Password: %s

When you log in, you can change your password if you click on 'My Account'.

On the database, you will be able to see your marks, download your marksheets and book meetings with teachers. The first marksheets should be up soon, and your teachers will let you know about this.

More functions are in planning.

If you experience problems, please contact cccu@tobiaskliem.de - thanks a lot!

Enjoy the experience,

Your friendly MySDS admin.
"""%(first_name, user.username, password) 
            send_mail('The Law Database at Canterbury Christ Church', message, 'cccu@tobiaskliem.de', [user.email,])
            #print message #Just for local testing (no SMTP server on the testing machine)
        return HttpResponseRedirect('/')
    else:
        all_students = Student.objects.all()
        students = [] 
        year = {}
        for student in all_students:
            if student.belongs_to == None:
                students.append(student)
                year[student.year] = True
        return render_to_response('invite_students.html',
                {'students': students, 'year': year},
                context_instance = RequestContext(request))

def wrong_email(request):
    printstring = '''<p>You did not provide a valid email address.</p>
                    <p>
                        Please make sure you use your CCCU email address - eg b.bunny123@canterbury.ac.uk.
                    </p>

                    <a href="/" class="btn btn-primary">Please try again</a>'
                '''
    title = "CCCU Law DB - Wrong email"

    return render_to_response('wrong_email.html', {'printstring': printstring, 'title': title}, context_instance = RequestContext(request))



def na(request):
    printstring = 'This function is not available yet'
    title = 'CCCU Law DB: Not available'
    return render_to_response('blank.html', {'printstring': printstring, 'title': title}, context_instance = RequestContext(request))
