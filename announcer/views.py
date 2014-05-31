from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import Template, Context, RequestContext
import datetime

from announcer.models import *
from database.strings import *
from database.views import is_teacher, is_student, is_admin


@login_required
def show_homepage(request):
    announcements = []
    admin = False
    if is_student(request.user):
        print "Whoohoo"
        announcements = Announcement.objects.filter(
            Q(announce_to='students') | Q(announce_to='all'))
    else:
        if is_admin(request.user):
            announcements = Announcement.objects.filter(
                Q(announce_to='teachers') | Q(announce_to='all'))
            admin = True
        elif is_teacher(request.user):
            announcements = Announcement.objects.filter(
                Q(announce_to='teachers') | Q(announce_to='all'))

    if request.method == 'POST':
        if request.POST['header'] or request.POST['text']:
            if request.POST['header']:
                header = request.POST['header']
            else:
                header = ''
            if request.POST['text']:
                text = request.POST['text']
            else:
                text = ''
            new_announcement = Announcement(
                author=request.user,
                publishing_date=datetime.datetime.today(),
                headline=header,
                announce_to=request.POST['announce_to'],
                text=text
                )
            new_announcement.save()
    return render_to_response(
        'home.html',
        {
            'announcements': announcements,
            'mdexplanation': MD_EXPLANATION,
            'admin': admin
        },
        context_instance=RequestContext(request)
        )
