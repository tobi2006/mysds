from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, BaseDocTemplate, Frame, PageTemplate, Image
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.units import inch
from database.models import *
from feedback.models import *
from anonymous_marking.models import *
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from database.views import is_teacher, is_admin
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date


@login_required
@user_passes_test(is_teacher)
def export_feedback_sheet(request, code, year, assessment_str, student_id):
    module = Module.objects.get(code = code, year = year)
    assessment = int(assessment_str)
    student = Student.objects.get(student_id = student_id)
    performance = Performance.objects.get(student = student, module = module)
    marksheet = Marksheet.objects.get(student = student, module = module, assessment = assessment)
    if assessment == 1:
        assessment_type = module.assessment_1_type
        assessment_title_string = '<b>' + module.assessment_1_title + '</b>'
        wordcount_string = '<b>' + str(module.assessment_1_max_word_count) + ' Words max.</b>'
        mark = str(performance.assessment_1)
    if assessment == 2:
        assessment_type = module.assessment_2_type
        assessment_title_string = '<b>' + module.assessment_2_title + '</b>'
        wordcount_string = '<b>' + module.assessment_2_max_word_count + ' Words max.</b>'
        mark = str(performance.assessment_2)
    if assessment == 3:
        assessment_type = module.assessment_3_type
        assessment_title_string = '<b>' + module.assessment_3_title + '</b>'
        wordcount_string = '<b>' + module.assessment_3_max_word_count + ' Words max.</b>'
        mark = str(performance.assessment_3)
    if assessment == 4:
        assessment_type = module.assessment_4_type
        assessment_title_string = '<b>' + module.assessment_4_title + '</b>'
        wordcount_string = '<b>' + module.assessment_4_max_word_count + ' Words max.</b>'
        mark = str(performance.assessment_4)
    if assessment == 5:
        assessment_type = module.assessment_5_type
        assessment_title_string = '<b>' + module.assessment_5_title + '</b>'
        wordcount_string = '<b>' + module.assessment_5_max_word_count + ' Words max.</b>'
        mark = str(performance.assessment_5)
    if assessment == 6:
        assessment_type = module.assessment_6_type
        assessment_title_string = '<b>' + module.assessment_6_title + '</b>'
        wordcount_string = '<b>' + module.assessment_6_max_word_count + ' Words max.</b>'
        mark = str(performance.assessment_6)
    feedback_category = FeedbackCategories.objects.get(assessment_type = assessment_type) 
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=marksheet.pdf'
    document = SimpleDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    logo = "cccu.jpg"
    im = Image(logo, 2.45*inch, 1*inch)
    elements.append(im)
    elements.append(Spacer(1,5))
    essay = FeedbackCategories.objects.get(assessment_type = 'Essay')
    if assessment_type == essay:
        title = Paragraph('<para alignment="center">Law Undergraduate Assessment Sheet: Essay</para>', styles['Heading2'])
        elements.append(title)
        elements.append(Spacer(1,5))
        last_name_string = '<b>' + student.last_name + '</b>'
        family_name = [Paragraph('Student family name', styles['Normal']), Spacer(1,3), Paragraph(last_name_string, styles['Normal'])]
        first_name_string = '<b>' + student.first_name + '</b>'
        first_name = [Paragraph('First name', styles['Normal']), Spacer(1,3), Paragraph(first_name_string, styles['Normal'])]
        module_title_string = '<b>' + module.title + '</b>'
        module_title = [Paragraph('Module Title', styles['Normal']), Spacer(1,3), Paragraph(module_title_string, styles['Normal'])]
        module_code_string = '<b>' + module.code + '</b>'
        module_code = [Paragraph('Module Code', styles['Normal']), Spacer(1,3), Paragraph(module_code_string, styles['Normal'])]
        submission_date_string = '<b>' + str(marksheet.submission_date.day) + "/" + str(marksheet.submission_date.month) + "/" + str(marksheet.submission_date.year) + '</b>'
        submission_date = [Paragraph('Submission Date', styles['Normal']), Spacer(1,3), Paragraph(submission_date_string, styles['Normal'])]
        assessment_title = [Paragraph('Assessment Title', styles['Normal']), Spacer(1,3), Paragraph(assessment_title_string, styles['Normal'])]
        word_count = [Paragraph('Word Count', styles['Normal']), Spacer(1,3), Paragraph(wordcount_string, styles['Normal'])]
        criteria = Paragraph('Criteria', styles['Normal'])
        r_a_k = Paragraph('Reading and Knowledge', styles['Normal'])
        u_a_a = Paragraph('Understanding and Analysis', styles['Normal'])
        arg = Paragraph('Argument', styles['Normal'])
        o_a_p = Paragraph('Organisation and Presentation', styles['Normal'])
        marked_by_string = '<b>' + marksheet.marker.first_name + ' ' + marksheet.marker.last_name + '</b>'
        marking_date_string = '<b>' + str(marksheet.marking_date.day) + "/" + str(marksheet.marking_date.month) + "/" + str(marksheet.marking_date.year) + '</b>'
        marked_by = [[Paragraph('Marked by', styles['Normal']), Paragraph(marked_by_string, styles['Normal'])], 
                    [Paragraph('Date', styles['Normal']), Paragraph(marking_date_string, styles['Normal'])]]
        marked_table = Table(marked_by)
        mark = [[Paragraph('Mark', styles['Normal']), Paragraph(mark, styles['Heading1'])],
                ['', '']]
        mark_table = Table(mark)
        mark_table.setStyle(TableStyle([('SPAN', (1,0), (1,1))]))
        comments = [Paragraph('<b>General Comments</b>', styles['Normal']), Spacer(1,4)]
        feedbacklist = marksheet.comments.split('\n')
        for line in feedbacklist:
            if line != "":
                paragraph = Paragraph(line, styles['Normal'])
                comments.append(paragraph)
                comments.append(Spacer(1,4))

        data = [[family_name, '', first_name, ''],
                [module_title, '', module_code, submission_date, ''],
                [assessment_title, '', word_count, '', ''],
                [],
                [criteria, r_a_k, u_a_a, arg, o_a_p],
                ['80 +', '', '', '', ''],
                ['70 - 79', '', '', '', '',],
                ['60 - 69', '', '', '', '',],
                ['50 - 59', '', '', '', '',],
                ['40 - 49', '', '', '', '',],
                ['Under 40', '', '', '', '',],
                [],
                [comments, '', '', '', ''],
                [marked_table, '', '', mark_table, '']
                ]

        t = Table(data) 
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('SPAN', (0,0), (1,0)),
                                ('SPAN', (2,0), (-1,0)),
                                ('SPAN', (0,1), (1,1)),
                                ('SPAN', (3,1), (-1,1)),
                                ('SPAN', (0,2), (1,2)),
                                ('SPAN', (2,2), (-1,2)),
                                ('SPAN', (0,3), (-1,3)),
                                ('BACKGROUND', (0,4), (-1,4), colors.lightgrey),
                                ('BACKGROUND', (0,5), (0,10), colors.lightgrey),
                                ('SPAN', (0,11), (-1,11)),
                                ('SPAN', (0,12), (-1,12)),
                                ('SPAN', (0,-1), (2,-1)),
                                ('SPAN', (3,-1), (-1,-1)),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

        elements.append(t)
    document.build(elements)
    return response

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
        last_week = module.last_session + 1
        no_teaching = module.no_teaching_in.split(",")
        for week in range(module.first_session, last_week):
            strweek = str(week)
            if strweek not in no_teaching:
                header.append(strweek)
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
    d = date.today()
    datenow = "Exported from the CCCU Law DB on " + str(d.day) + "/" + str(d.month) + "/" + str(d.year)
    for module in modules_to_use:        
        heading = "Anonymous Marks for " + module.title + " (" + str(module.year) + "/" + str(module.year + 1) + ")"
        elements.append(Paragraph(heading, styles['Heading2']))
        elements.append(Spacer(1,20))
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
        elements.append(Paragraph(datenow, styles['Normal']))
        elements.append(PageBreak())
    doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])
    doc.build(elements)
    return response

@login_required
@user_passes_test(is_teacher)
def export_marks(request, code, year):
    module = Module.objects.get(code=code, year=year)
    response = HttpResponse(mimetype='application/pdf')
    filename = module.title.replace(" ", "_")
    filename += "_Marks_" + str(module.year) + ".pdf"
    responsestring = 'attachment; filename=' + filename
    #response['Content-Disposition'] = 'attachment; filename=anonymous_exam_marks.pdf'
    response['Content-Disposition'] = responsestring 
    doc = SimpleDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    d = date.today()
    datenow = "Exported from the CCCU Law DB on " + str(d.day) + "/" + str(d.month) + "/" + str(d.year)
    heading = "Marks for " + module.title + " (" + str(module.year) + "/" + str(module.year + 1) + ")"
    elements.append(Paragraph(heading, styles['Heading2']))
    elements.append(Spacer(1,20))
    data = []
    header = ['Student', 'Student ID', 'QLD']
    if module.assessment_1_value:
        header.append(module.assessment_1_title)
    if module.assessment_2_value:
        header.append(module.assessment_2_title)
    if module.assessment_3_value:
        header.append(module.assessment_3_title)
    if module.assessment_4_value:
        header.append(module.assessment_4_title)
    if module.assessment_5_value:
        header.append(module.assessment_5_title)
    if module.assessment_6_value:
        header.append(module.assessment_6_title)
    if module.exam_value:
        header.append('Exam')
    header.append('Module Mark')
    data.append(header)
    performances = Performance.objects.filter(module = module)
    counter = 0
    highlight = []
    for performance in performances:
        counter += 1
        student = performance.student.last_name + ", " + performance.student.first_name
        row = [student, performance.student.student_id]
        if performance.student.qld:
            row.append(u'\u2713')
        else:
            row.append(' ')
        pay_attention = False
        if module.assessment_1_value:
            if performance.assessment_1:
                if performance.assessment_1 < 40:
                    pay_attention = True
                row.append(performance.assessment_1)
            else:
                row.append('-')
        if module.assessment_2_value:
            if performance.assessment_2:
                if performance.assessment_1 < 40:
                    pay_attention = True
                row.append(performance.assessment_2)
            else:
                row.append('-')
        if module.assessment_3_value:
            if performance.assessment_3:
                row.append(performance.assessment_3)
                if performance.assessment_1 < 40:
                    pay_attention = True
            else:
                row.append('-')
        if module.assessment_4_value:
            if performance.assessment_4:
                row.append(performance.assessment_4)
                if performance.assessment_1 < 40:
                    pay_attention = True
            else:
                row.append('-')
        if module.assessment_5_value:
            if performance.assessment_5:
                row.append(performance.assessment_5)
                if performance.assessment_1 < 40:
                    pay_attention = True
            else:
                row.append('-')
        if module.assessment_6_value:
            if performance.assessment_6:
                row.append(performance.assessment_6)
                if performance.assessment_1 < 40:
                    pay_attention = True
            else:
                row.append('-')
        if module.exam_value:
            if performance.exam:
                row.append(performance.exam)
                if performance.exam < 40:
                    pay_attention = True
            else:
                row.append('-')
        if not module.is_foundational:
            pay_attention = False
        if not performance.student.qld:
            pay_attention = False
        if performance.average:
            row.append(performance.average)
            if performance.average < 40:
                pay_attention = True
        else:
            row.append('-')
            pay_attention = True
        data.append(row)
        if pay_attention:
            highlight.append(counter)
    table = Table(data, repeatRows=1)
    tablestyle = [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND',(0,0),(-1,0),colors.grey),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black)]
    for number in highlight:
        tablestyle.append(('BACKGROUND', (0,number), (-1,number), colors.lightgrey))
    table.setStyle(TableStyle(tablestyle))
    elements.append(table)
    elements.append(Spacer(1,20))
    elements.append(Paragraph(datenow, styles['Normal']))
    elements.append(PageBreak())
    doc.build(elements)
    return response


