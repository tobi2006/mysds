from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import (HttpResponse, HttpResponseRedirect,
                            HttpResponseForbidden)
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.templatetags.static import static
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, BaseDocTemplate, Frame,
                                PageTemplate, Image)
from reportlab.platypus.flowables import PageBreak

from database.views import is_teacher, is_admin, is_student
from database.models import *
from feedback.models import *
from feedback.categories import *
from anonymous_marking.models import *

# Constants

LOGO = "https://cccu.tobiaskliem.de/static/images/cccu.jpg"

# The different marking categories are in feedback/categories.py

# Helper Functions

def bold(string):
    """Adds <b> tags around a string"""
    bold_string = '<b>' + string + '</b>'
    return bold_string

def heading(string, headingstyle = 'Heading2'):
    """Returns a proper paragraph for the header line, defaults to heading2"""
    tmp = '<para alignment = "center">' + string + '</para>'
    result = Paragraph(tmp, styles[headingstyle])
    return result

def formatted_date(raw_date):
    """Returns a proper date string
    
    This returns a string of the date in British Format.
    If the date field was left blank, an empty string is returned.
    """
    if raw_date == None:
        result = ''
    else:
        result = (str(raw_date.day) + '/' + str(raw_date.month) + '/' +
                    str(raw_date.year))
    return result

def two_markers(marker1, marker2):
    """Returns a string containing two markers, sorted alphabetically"""
    marker_1_sort = marker1.last_name + "/" + marker1.first_name
    marker_2_sort = marker2.last_name + "/" + marker2.first_name
    markers = [marker_1_sort, marker_2_sort]
    markers.sort()
    marker_1_list = markers[0].split("/")
    marker_2_list = markers[1].split("/")
    marker_1_return = marker_1_list[1] + marker_1_list[0]
    marker_2_return = marker_2_list[1] + marker_2_list[0]
    result = marker_1_return + ' / ' + marker_2_return
    return result

def paragraph(string):
    """Returns a paragraph with normal style"""
    return Paragraph(string, styles['Normal'])

def bold_paragraph(string):
    """Returns a paragraph with bold formatting"""
    tmp = bold(string)
    return Paragraph(tmp, styles['Normal'])

def get_title(module, assessment):
    assessment_title_string = module.get_assessment_title(assessment)
    assessment_title_string = assessment_title_string.replace("/", "or")
    return assessment_title_string

# Different marksheets

def negotiation_written_sheet(student, module, assessment):                    
    """Marksheet for the assessment 'Negotiation / Written Submission'

    This is an assessment that includes a group component and is therefore
    a little more complex.
    """
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment
    )
    group_no = performance.group_assessment_group
    group_feedback = GroupMarksheet.objects.get(
        module=module, assessment=assessment, group_no=group_no
    )
    mark = str(performance.get_assessment_result(assessment))
    im = Image(LOGO, 2.45*inch, 1*inch)
    elements.append(im)
    elements.append(Spacer(1,3))
    title = heading(
        'Law Undergraduate Assessment Sheet: Negotiation Study', 'Heading3'
    )
    elements.append(title)
    elements.append(Spacer(1,3))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1,3),
        bold_paragraph(student.last_name)
    ]
    first_name = [
        paragraph('First name'),
        Spacer(1,3),
        bold_paragraph(student.first_name)
    ]
    module_title = [
        paragraph('Module Title'),
        Spacer(1,3),
        bold_paragraph('ELIM')
    ]
    module_code = [
        paragraph('Module Code'),
        Spacer(1,3),
        bold_paragraph(module.code)
    ]
    tmp = formatted_date(group_feedback.submission_date)
    submission_date = [
        paragraph('Presentation Date'),
        Spacer(1,3),
        bold_paragraph(tmp)
    ]
    tmp = str(performance.seminar_group) + '/' + str(group_no)
    group_number = [
        paragraph('Seminar/LAU Group'),
        Spacer(1,3),
        bold_paragraph(tmp)
    ]
    individual_category_1 = bold_paragraph(NEGOTIATION_WRITTEN['i-1'])
    individual_category_2 = bold_paragraph(NEGOTIATION_WRITTEN['i-2'])
    individual_category_3 = bold_paragraph(NEGOTIATION_WRITTEN['i-3'])
    individual_category_4 = bold_paragraph(NEGOTIATION_WRITTEN['i-4'])
    deduction_explanation = paragraph(NEGOTIATION_WRITTEN['i-4-helptext'])
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]
    ]
    marked_by_table = Table(marked_by)
    mark = [
        [paragraph('Mark'), 
        Paragraph(mark, styles['Heading1'])],
        ['', '']
    ]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1,0), (1,1))]))
    table_header_1 = bold_paragraph('Part 1: Assessed Negotiation')
    table_header_2 = bold_paragraph('Marks Available')
    table_header_3 = bold_paragraph('Marks Awarded')
    part_1_subheader = bold_paragraph('1. Individual Work')
    part_2_subheader = bold_paragraph('2. Group Work')
    sub_total_1_string = bold_paragraph('Sub-Total Part 1')
    sub_total_1 = (
        marksheet.category_mark_1_free + 
       group_feedback.category_mark_1_free +
       group_feedback.category_mark_2_free
    )
    table_header_4 = bold_paragraph(
            'Part 2: Individual and Written Submission'
    )
    sub_total_2_string = paragraph('Sub-Total Part 2')
    sub_total_2 = (
        marksheet.category_mark_2_free +
        marksheet.category_mark_3_free +
        group_feedback.category_mark_3_free +
        group_feedback.category_mark_4_free
    )
    deductions_h_1 = bold_paragraph('Deductions possible')
    deductions_h_2 = bold_paragraph('Deductions incurred')
    i_mark_1 = str(marksheet.category_mark_1_free)
    i_mark_2 = str(marksheet.category_mark_2_free)
    i_mark_3 = str(marksheet.category_mark_3_free)
    i_mark_4 = str(marksheet.category_mark_4_free)
    g_mark_1 = str(group_feedback.category_mark_1_free)
    g_mark_2 = str(group_feedback.category_mark_2_free)
    g_mark_3 = str(group_feedback.category_mark_3_free)
    g_mark_4 = str(group_feedback.category_mark_4_free)
    data = [[family_name, first_name, group_number, ''],
            [module_title, module_code, submission_date, ''],
            ['', '', '', ''],
            ['', '', table_header_2, table_header_3],
            [table_header_1, '', '', ''],
            [part_1_subheader, '', '', ''],
            [individual_category_1, '', '40', i_mark_1],
            [part_2_subheader, '', '', ''],
            [group_category_1, '', '10', g_mark_1],
            [group_category_2, '', '10', g_mark_2],
            [sub_total_1_string, '', '60', sub_total_1],
            [table_header_4, '', '', ''],
            [part_1_subheader, '', '', ''],
            [individual_category_2, '', '10', i_mark_2],
            [individual_category_3, '', '10', i_mark_3],
            [part_2_subheader, '', '', ''],
            [group_category_3, '', '10', g_mark_3],
            [group_category_4, '', '10', g_mark_4],
            [sub_total_2_string, '', '40', sub_total_2],
            [individual_category_4, '', deductions_h_1, deductions_h_2],
            [deduction_explanation, '', '12', i_mark_4]
        ]
    t = Table(data) 
    t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('SPAN', (-2,0), (-1,0)),
                            ('SPAN', (-2,1), (-1,1)),
                            ('SPAN', (0,2), (-1,2)),
                            ('BOX', (0,0), (-1,1), 0.25, colors.black),
                            ('SPAN', (0,3), (1,3)),
                            ('SPAN', (0,4), (1,4)),
                            ('SPAN', (0,5), (1,5)),
                            ('SPAN', (0,6), (1,6)),
                            ('SPAN', (0,7), (1,7)),
                            ('SPAN', (0,8), (1,8)),
                            ('SPAN', (0,9), (1,9)),
                            ('BACKGROUND', (0,10), (-1,10), colors.lightgrey),
                            ('SPAN', (0,10), (1,10)),
                            ('SPAN', (0,11), (1,11)),
                            ('SPAN', (0,12), (1,12)),
                            ('SPAN', (0,13), (1,13)),
                            ('SPAN', (0,14), (1,14)),
                            ('SPAN', (0,15), (1,15)),
                            ('SPAN', (0,16), (1,16)),
                            ('SPAN', (0,17), (1,17)),
                            ('SPAN', (0,18), (1,18)),
                            ('SPAN', (0,19), (1,19)),
                            ('SPAN', (0,20), (1,20)),
                            ('BACKGROUND', (0,18), (-1,18), colors.lightgrey),
                            ('BOX', (0,3), (-1,-1), 0.25, colors.black)]))
    elements.append(t)
    elements.append(PageBreak())
    # Individual Comments
    individual_comments = [
        bold_paragraph('Comment on <u>Individual</u> Work for part 1 and 2'),
        Spacer(1,4)
    ]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            individual_comments.append(p)
            individual_comments.append(Spacer(1,4))
    # Group Comments
    group_comments = [
        bold_paragraph('Comment on <u>Group</u> Work for part 1 and 2'),
        Spacer(1,4)
    ]
    feedbacklist = group_feedback.group_comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = Paragraph(line)
            group_comments.append(p)
            group_comments.append(Spacer(1,4))
    # Final table
    last_data = [
        [individual_comments, '', '', ''],
        [group_comments, '', '', ''],
        [marked_by_table, '', mark_table, '']
    ]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,1), (-1,1)),
            ('SPAN', (0,2), (1,2)),
            ('SPAN', (2,2), (-1,2)),
            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey)
        ])
    )
    elements.append(last_table)
    return elements

def essay_sheet(student, module, assessment):                    
    """Marksheet for Essays

    This is the standard marksheet for CCCU Law, including a marking grid
    with four different categories
    """
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment
    )
    assessment_title = bold(module.get_assessment_title(assessment))
    mark = str(performance.get_assessment_result(assessment))
    im = Image(LOGO, 2.45*inch, 1*inch)
    elements.append(im)
    elements.append(Spacer(1,3))
    title = heading('Law Undergraduate Assessment Sheet: Essay')
    elements.append(title)
    elements.append(Spacer(1,3))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1,3),
        bold_paragraph(student.last_name)
    ]
    first_name = [
        paragraph('First name'),
        Spacer(1,3),
        bold_paragraph(student.first_name)
    ]
    module_title = [
        paragraph('Module Title'),
        Spacer(1,3),
        bold_paragraph('module.title')
    ]
    module_code = [
        paragraph('Module Code'),
        Spacer(1,3),
        bold_paragraph(module.code)
    ]
    tmp = formatted_date(marksheet.submission_date)
    submission_date = [
        paragraph('Submission Date'),
        Spacer(1,3),
        bold_paragraph(tmp)
    ]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1,3)
        paragraph(assessment_title)
    ]
    if module.get_assessment_max_wordcount(assessment):
        tmp = (
            str(module.get_assessment_max_wordcount(assessment)) + 
            ' Words max.'
        )
    else:
        tmp = ''
    word_count = [
        paragraph('Word Count'),
        Spacer(1,3),
        bold_paragraph(tmp)
    ]
    criteria = paragraph('Criteria')
    category_1 = paragraph(ESSAY['i-1'])
    category_2 = Paragraph(ESSAY['i-2'])
    category_3 = Paragraph(ESSAY['i-3'])
    category_4 = Paragraph(ESSAY['i-4'])
    data = [
        [family_name, '', first_name, ''],
        [module_title, '', module_code, submission_date, ''],
        [assessment_title, '', word_count, '', ''],
        [criteria, category_1, category_2, category_3, category_4]
    ]
    row = ['80 +']
    if marksheet.category_mark_1 == 80:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_2 == 80:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_3 == 80:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_4 == 80:
        row.append('X')
    else:
        row.append(' ')
    data.append(row)
    row = ['70 - 79']
    if marksheet.category_mark_1 == 79:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_2 == 79:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_3 == 79:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_4 == 79:
        row.append('X')
    else:
        row.append(' ')
    data.append(row)
    row = ['60 - 69']
    if marksheet.category_mark_1 == 69:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_2 == 69:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_3 == 69:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_4 == 69:
        row.append('X')
    else:
        row.append(' ')
    data.append(row)
    row = ['50 - 59']
    if marksheet.category_mark_1 == 59:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_2 == 59:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_3 == 59:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_4 == 59:
        row.append('X')
    else:
        row.append(' ')
    data.append(row)
    row = ['40 - 49']
    if marksheet.category_mark_1 == 49:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_2 == 49:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_3 == 49:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_4 == 49:
        row.append('X')
    else:
        row.append(' ')
    data.append(row)
    row = ['Under 40']
    if marksheet.category_mark_1 == 39:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_2 == 39:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_3 == 39:
        row.append('X')
    else:
        row.append(' ')
    if marksheet.category_mark_4 == 39:
        row.append('X')
    else:
        row.append(' ')
    data.append(row)
    t = Table(data) 
    t.setStyle(
        TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('SPAN', (0,0), (1,0)),
            ('SPAN', (2,0), (-1,0)),
            ('SPAN', (0,1), (1,1)),
            ('SPAN', (3,1), (-1,1)),
            ('SPAN', (0,2), (1,2)),
            ('SPAN', (2,2), (-1,2)),
            ('BACKGROUND', (0,3), (-1,3), colors.lightgrey),
            ('BACKGROUND', (0,4), (0,9), colors.lightgrey),
            ('ALIGN', (1,4), (-1,-1), 'CENTER'),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black)
        ])
    )
    comments = [
        bold_paragraph('General Comments'),
        styles['Normal']),
        Spacer(1,4)
    ]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1,4))
    for comment in comments:
        elements.append(comment)
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]
    ]
    marked_by_table = Table(marked_by)
    mark = [
        [paragraph('Mark'), 
        Paragraph(mark, styles['Heading1'])],
        ['', '']
    ]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1,0), (1,1))]))
    last_data = [[marked_table, '', '', mark_table, '']]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('SPAN', (0,0), (2,0)),
            ('SPAN', (3,-1), (-1,-1))
        ])
    )
    elements.append(last_table)
    return elements

@login_required
def export_feedback_sheet(request, code, year, assessment, student_id):
    """Will export either one or multiple feedback sheets.

    This needs to be given the student id or the string 'all' if
    you want all marksheets for the assessment. It will only work if
    the person requesting is a teacher, an admin or the student the
    marksheet is about.
    """
    module = Module.objects.get(code=code, year=year)
    assessment_title = get_title(module, assessment)
    assessment_type = module.get_assessment_type(assessment)

    # Replace this part!
    essay = FeedbackCategories.objects.get(assessment_type = 'Essay')
    legal_problem = FeedbackCategories.objects.get(
        assessment_type = 'Legal Problem'
    )
    oral_presentation = FeedbackCategories.objects.get(
        assessment_type = 'Oral Presentation'
    )
    essay_legal_problem = FeedbackCategories.objects.get(
        assessment_type = 'Essay / Legal Problem'
    )
    online_test_court_report = FeedbackCategories.objects.get(
        assessment_type = 'Online Test / Court Report'
    )
    negotiation_written = FeedbackCategories.objects.get(
        assessment_type = 'Negotiation / Written Submission'
    )
    if student_id == 'all':
        if is_teacher(request.user) or is_admin(request.user):
            response = HttpResponse(mimetype='application/pdf')
            first_part = module.title.replace(' ', '_')
            second_part = assessment_title.replace(' ', '_')
            filename_string = ('attachment; filename=' + first_part +
                    '_' + second_part + '_-_all_marksheets.pdf')
            all_students = module.student_set.all()
            documentlist = []
            students = [] # Only the students where feedback has been entered
            for student in all_students:
                try:
                    performance = Marksheet.objects.get(
                        student=student, module=module, assessment=assessment
                    )
                    students.append(student)
                except Marksheet.DoesNotExist:
                    pass
            for student in students:
                #This needs to be changed to take the database out
                if assessment_type == essay:
                    elements = essay_sheet(student, module, assessment)
                elif assessment_type == legal_problem:
                    pass
                elif assessment_type == oral_presentation:
                    pass
                elif assessment_type == essay_legal_problem:
                    pass
                elif assessment_type == online_test_court_report:
                    pass
                elif assessment_type == negotiation_written:
                    elements = negotiation_written_sheet(
                        student, module, assessment
                    )
                for element in elements:
                    documentlist.append(element)
                documentlist.append(PageBreak())
            response['Content-Disposition'] = filename_string
            document = SimpleDocTemplate(response)
            document.setAuthor = 'Canterbury Christ Church University'
            document.build(documentlist)
            return response
        else:
            return HttpResponseForbidden()
    else:
        student = Student.objects.get(student_id = student_id)
        own_marksheet = False # Just for the filename
        allowed = False
        if is_teacher(request.user) or is_admin(request.user):
            allowed = True
        elif is_student(request.user):
            if student.belongs_to == request.user:
                own_marksheet = True
                allowed = True
        if allowed:
            module = Module.objects.get(code = code, year = year)
            response = HttpResponse(mimetype='application/pdf')
            assessment_title_string = get_title(module, assessment)
            if own_marksheet:
                first_part = module.title.replace(' ', '_')
                second_part = assessment_title_string.replace(' ', '_')
                filename_string = (
                    'attachment; filename=' + first_part + '_' + 
                    second_part + '_Marksheet.pdf'
                )
            else:
                ln = student.last_name.replace(' ', '_')
                fn = student.first_name.replace(' ', '_')
                filename_string = (
                    'attachment; filename=' + ln + '_' + fn + '.pdf'
                )
            response['Content-Disposition'] = filename_string
            document = SimpleDocTemplate(response)
            document.setAuthor = 'Canterbury Christ Church University'
            elements = get_one_feedback_sheet(student, module, assessment)
            document.build(elements)
            return response
        else:
            return HttpResponseForbidden()

@login_required
@user_passes_test(is_teacher)
def export_attendance_sheet(request, code, year):
    """Returns attendance sheets for a module."""
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename=attendance_sheet.pdf'
    )
    document = SimpleDocTemplate(response)
    elements = []
    module = Module.objects.get(code=code, year=year)
    styles = getSampleStyleSheet()
    next_year = str(module.year + 1)
    heading = (
        module.title + " (" + module.code + ") " + str(module.year) +
        "/" + next_year
    )
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
        performances = Performance.objects.filter(
            module=module, seminar_group=counter
        )
        for performance in performances:
            row = [performance.student,]
            for week in performance.attendance:
                if week == '1':
                    row.append(u'\u2713')
                elif week == 'e':
                    row.append('e')
                else:
                    row.append(' ')
            data.append(row)
        table = Table(data)
        table.setStyle(
            TableStyle([
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black)
            ])
        )
        elements.append(table)
        elements.append(PageBreak())
    document.build(elements)
    return response
     
@login_required
@user_passes_test(is_admin)
def export_anonymous_exam_marks(request, year):
    """Gives an overview of all anonymous marks in the year"""
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
    response['Content-Disposition'] = (
        'attachment; filename=anonymous_exam_marks.pdf'
    )
    doc = BaseDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    frame1 = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width/2-6,
        doc.height, id='col1'
    )
    frame2 = Frame(
        doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
        doc.height, id='col2'
    )
    d = formatted_date(date.today())
    datenow = "Exported from MySDS, the CCCU Law DB on " + d 
    for module in modules_to_use:        
        heading = (
            "Anonymous Marks for " + module.title + " (" +
            str(module.year) + "/" + str(module.year + 1) + ")"
        )
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
        table.setStyle(
            TableStyle([
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black)
            ])
        )
        elements.append(table)
        elements.append(paragraph(datenow)
        elements.append(PageBreak())
    doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])
    doc.build(elements)
    return response

@login_required
@user_passes_test(is_teacher)
def export_marks(request, code, year):
    """Gives a useful sheet of all marks for the module.

    Students will be highlighted if they failed the module, or if a QLD
    student failed a component in a Foundational module"""
    module = Module.objects.get(code=code, year=year)
    response = HttpResponse(mimetype='application/pdf')
    filename = module.title.replace(" ", "_")
    filename += "_Marks_" + str(module.year) + ".pdf"
    responsestring = 'attachment; filename=' + filename
    response['Content-Disposition'] = responsestring 
    doc = SimpleDocTemplate(response)
    doc.pagesize = landscape(A4)
    elements = []
    styles = getSampleStyleSheet()
    d = formatted_date(date.today())
    datenow = "Exported from MySDS, the CCCU Law DB on " + d
    heading = "Marks for " + module
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
        student = (
            performance.student.last_name + ", " + 
            performance.student.first_name
        )
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
    tablestyle = [
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black)
    ]
    for number in highlight:
        tablestyle.append(
            ('BACKGROUND', (0,number), (-1,number), colors.lightgrey)
        )
    table.setStyle(TableStyle(tablestyle))
    elements.append(table)
    elements.append(Spacer(1,20))
    elements.append(paragraph(datenow)
    elements.append(PageBreak())
    doc.build(elements)
    return response
