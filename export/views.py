from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.flowables import PageBreak
from database.models import *
from anonymous_marking.models import *
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from database.views import is_teacher, is_admin
from django.http import HttpResponse, HttpResponseRedirect

@login_required
@user_passes_test(is_teacher)
def export_attendance_sheet(request, code, year):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=attendance_sheet.pdf'
    document = SimpleDocTemplate(response)
    elements = []
    module = Module.objects.get(code=code, year=year)
    styles = getSampleStyleSheet()
    heading = module.title + " (" + str(module.year) + ")"
    performances = Performance.objects.filter(module=module)
    no_of_seminar_groups = 0
    for performance in performances:
        if performance.seminar_group > no_of_seminar_groups:
            no_of_seminar_groups = performance.seminar_group
    counter = 0
    while counter < no_of_seminar_groups:
        counter += 1
        subheading = "Seminar Group " + str(counter)
        elements.append(Paragraph(heading, styles['Heading1']))
        elements.append(Paragraph(subheading, styles['Heading2']))
        elements.append(Spacer(1,20))
        data = []
        header = ['Name',]
        column = 0
        while column < module.number_of_sessions:
            column += 1
            header.append(str(column))
        data.append(header)
        performances = Performance.objects.filter(module=module, seminar_group=counter)
        #performances.sort()
        for performance in performances:
            row = [performance.student,]
            for week in performance.attendance:
                if week == '1':
                    row.append(u'\u2713')
                else:
                    row.append(' ')
            data.append(row)
        table = Table(data)
        table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                        ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
        elements.append(table)
        elements.append(PageBreak())
    document.build(elements)
    return response
     
@login_required
@user_passes_test(is_admin)
def export_anonymous_exam_marks(request, year):
    modules = Module.objects.filter(year=year)
    modules_to_use = []
    for module in modules:
        if module.exam_value:
            marks = AnonymousMarks.objects.filter(module = module)
            for mark in marks:
                if mark.exam:
                    modules_to_use.append(module)
                    break
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=anonymous_exam_marks.pdf'
    doc = BaseDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')
    for module in modules_to_use:        
        heading = module.title + " (" + str(module.year) + ")"
        elements.append(Paragraph(heading, styles['Heading1']))
        data = []
        header = ['Exam ID', 'Exam Mark']
        data.append(header)
        marks = AnonymousMarks.objects.filter(module = module)
        for mark in marks:
            row = [mark.exam_id, mark.exam]
            data.append(row)
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
        elements.append(table)
        elements.append(PageBreak())
    doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])
    doc.build(elements)
    return response
