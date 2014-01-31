from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, BaseDocTemplate, Frame, PageTemplate, Image
from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait 
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.units import inch
from database.models import *
from feedback.models import *
from anonymous_marking.models import *
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.templatetags.static import static
from database.views import is_teacher, is_admin, is_student
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from datetime import date

def get_one_feedback_sheet(student, module, assessment):
    performance = Performance.objects.get(student = student, module = module)
    marksheet = Marksheet.objects.get(student = student, module = module, assessment = assessment)
    if assessment == 1:
        assessment_type = module.assessment_1_type
        assessment_title_string = '<b>' + module.assessment_1_title + '</b>'
        if module.assessment_1_max_word_count:
            wordcount_string = '<b>' + str(module.assessment_1_max_word_count) + ' Words max.</b>'
        else:
            wordcount_string = ''
        mark = str(performance.assessment_1)
    if assessment == 2:
        assessment_type = module.assessment_2_type
        assessment_title_string = '<b>' + module.assessment_2_title + '</b>'
        if module.assessment_2_max_word_count:
            wordcount_string = '<b>' + str(module.assessment_2_max_word_count) + ' Words max.</b>'
        else:
            wordcount_string = ''
        mark = str(performance.assessment_2)
    if assessment == 3:
        assessment_type = module.assessment_3_type
        assessment_title_string = '<b>' + module.assessment_3_title + '</b>'
        if module.assessment_3_max_word_count:
            wordcount_string = '<b>' + str(module.assessment_3_max_word_count) + ' Words max.</b>'
        else:
            wordcount_string = ''
        mark = str(performance.assessment_3)
    if assessment == 4:
        assessment_type = module.assessment_4_type
        assessment_title_string = '<b>' + module.assessment_4_title + '</b>'
        if module.assessment_4_max_word_count:
            wordcount_string = '<b>' + str(module.assessment_4_max_word_count) + ' Words max.</b>'
        else:
            wordcount_string = ''
        mark = str(performance.assessment_4)
    if assessment == 5:
        assessment_type = module.assessment_5_type
        assessment_title_string = '<b>' + module.assessment_5_title + '</b>'
        if module.assessment_5_max_word_count:
            wordcount_string = '<b>' + str(module.assessment_5_max_word_count) + ' Words max.</b>'
        else:
            wordcount_string = ''
        mark = str(performance.assessment_5)
    if assessment == 6:
        assessment_type = module.assessment_6_type
        assessment_title_string = '<b>' + module.assessment_6_title + '</b>'
        if module.assessment_6_max_word_count:
            wordcount_string = '<b>' + str(module.assessment_6_max_word_count) + ' Words max.</b>'
        else:
            wordcount_string = ''
        mark = str(performance.assessment_6)
    feedback_category = FeedbackCategories.objects.get(assessment_type = assessment_type) 
    elements = []
    styles = getSampleStyleSheet()
    logo = "https://cccu.tobiaskliem.de/static/images/cccu.jpg"
    im = Image(logo, 2.45*inch, 1*inch)
    elements.append(im)
    elements.append(Spacer(1,5))
    essay = FeedbackCategories.objects.get(assessment_type = 'Essay')
    legal_problem = FeedbackCategories.objects.get(assessment_type = 'Legal Problem')
    oral_presentation = FeedbackCategories.objects.get(assessment_type = 'Oral Presentation')
    essay_legal_problem = FeedbackCategories.objects.get(assessment_type = 'Essay / Legal Problem')
    online_test_court_report = FeedbackCategories.objects.get(assessment_type = 'Online Test / Court Report')
    essay_or_legal_problem = False
    essay_and_legal_problem = False
    online_court = False
    if assessment_type == essay:
        title = Paragraph('<para alignment="center">Law Undergraduate Assessment Sheet: Essay</para>', styles['Heading2'])
        essay_or_legal_problem = True
    elif assessment_type == legal_problem:
        title = Paragraph('<para alignment="center">Law Undergraduate Assessment Sheet: Legal Problem</para>', styles['Heading2'])
        essay_or_legal_problem = True
    elif assessment_type == oral_presentation:
        title = Paragraph('<para alignment="center">Law Undergraduate Assessment Sheet: Oral Presentation</para>', styles['Heading2'])
        presentation = True
    elif assessment_type == essay_legal_problem:
        title = Paragraph('<para alignment="center">Law Undergraduate Assessment Sheet: Essay / Legal Problem</para>', styles['Heading2'])
        essay_or_legal_problem = True
        essay_and_legal_problem = True
    elif assessment_type == online_test_court_report:
        title = Paragraph('<para alignment="center">Law Undergraduate Assessment Sheet: Assessment 1</para>', styles['Heading2'])
        essay_or_legal_problem = True
        online_court = True
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
    if marksheet.submission_date == None:
        submission_date_string = '   '
    else:
        submission_date_string = '<b>' + str(marksheet.submission_date.day) + "/" + str(marksheet.submission_date.month) + "/" + str(marksheet.submission_date.year) + '</b>'
    submission_date = [Paragraph('Submission Date', styles['Normal']), Spacer(1,3), Paragraph(submission_date_string, styles['Normal'])]
    assessment_title = [Paragraph('Assessment Title', styles['Normal']), Spacer(1,3), Paragraph(assessment_title_string, styles['Normal'])]
    if essay_or_legal_problem:
        word_count = [Paragraph('Word Count', styles['Normal']), Spacer(1,3), Paragraph(wordcount_string, styles['Normal'])]
    criteria = Paragraph('Criteria', styles['Normal'])
    r_a_k = Paragraph(assessment_type.category_1, styles['Normal'])
    u_a_a = Paragraph(assessment_type.category_2, styles['Normal'])
    arg = Paragraph(assessment_type.category_3, styles['Normal'])
    if essay_or_legal_problem:
        o_a_p = Paragraph(assessment_type.category_4, styles['Normal'])
    if essay_and_legal_problem:
        category_5 = Paragraph(assessment_type.category_5, styles['Normal'])
        category_6 = Paragraph(assessment_type.category_6, styles['Normal'])
        category_7 = Paragraph(assessment_type.category_7, styles['Normal'])
        category_8 = Paragraph(assessment_type.category_8, styles['Normal'])

    if marksheet.second_first_marker:
        marker1 = marksheet.marker.first_name + " " + marksheet.marker.last_name
        marker2 = marksheet.second_first_marker.first_name + " " + marksheet.second_first_marker.last_name
        markers = [marker1, marker2] # To make sure they don't appear in different orders
        markers.sort()
        marked_by_string = '<b>' + markers[0] + ' / ' + markers[1] + '</b>'
    else:
        marked_by_string = '<b>' + marksheet.marker.first_name + ' ' + marksheet.marker.last_name + '</b>'
    marking_date_string = '<b>' + str(marksheet.marking_date.day) + "/" + str(marksheet.marking_date.month) + "/" + str(marksheet.marking_date.year) + '</b>'

    marked_by = [[Paragraph('Marked by', styles['Normal']), Paragraph(marked_by_string, styles['Normal'])], 
                [Paragraph('Date', styles['Normal']), Paragraph(marking_date_string, styles['Normal'])]]
    marked_table = Table(marked_by)
    if essay_and_legal_problem:
        mark = [[Paragraph('Final Mark for (a) and (b)', styles['Normal']), Paragraph(mark, styles['Heading1'])],
                ['', '']]
    elif online_court:
        mark = [[Paragraph('Combined Mark', styles['Normal']), Paragraph(mark, styles['Heading1'])],
                ['', '']]
    else:
        mark = [[Paragraph('Mark', styles['Normal']), Paragraph(mark, styles['Heading1'])],
                ['', '']]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1,0), (1,1))]))

    if essay_or_legal_problem:
        data = [[family_name, '', first_name, ''],
                [module_title, '', module_code, submission_date, ''],
                [assessment_title, '', word_count, '', '']]
        if not essay_and_legal_problem:
            data.append([criteria, r_a_k, u_a_a, arg, o_a_p])
    elif presentation:
        data = [[family_name, '', first_name, ''],
                [module_title, '', module_code, submission_date],
                [assessment_title, '', '', ''],
                [criteria, r_a_k, u_a_a, arg]]
    if essay_and_legal_problem:
        t = Table(data) 
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('SPAN', (0,0), (1,0)),
                                ('SPAN', (2,0), (-1,0)),
                                ('SPAN', (0,1), (1,1)),
                                ('SPAN', (3,1), (-1,1)),
                                ('SPAN', (0,2), (1,2)),
                                ('SPAN', (2,2), (-1,2)),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
        elements.append(t)
        elements.append(Spacer(1,5))

        subtitle = Paragraph('Feedback for Part (a): Essay', styles['Heading3'])
        elements.append(subtitle)
        elements.append(Spacer(1,5))

        data=[[criteria, r_a_k, u_a_a, arg, o_a_p]]

    # Fill marking grid
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
    if essay_or_legal_problem:
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
    if essay_or_legal_problem:
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
    if essay_or_legal_problem:
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
    if essay_or_legal_problem:
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
    if essay_or_legal_problem:
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
    if essay_or_legal_problem:
        if marksheet.category_mark_4 == 39:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    t = Table(data) 
    if essay_or_legal_problem:
        if not essay_and_legal_problem:
            t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                    ('SPAN', (0,0), (1,0)),
                                    ('SPAN', (2,0), (-1,0)),
                                    ('SPAN', (0,1), (1,1)),
                                    ('SPAN', (3,1), (-1,1)),
                                    ('SPAN', (0,2), (1,2)),
                                    ('SPAN', (2,2), (-1,2)),
                                    ('BACKGROUND', (0,3), (-1,3), colors.lightgrey),
                                    ('BACKGROUND', (0,4), (0,9), colors.lightgrey),
                                    ('ALIGN', (1,4), (-1,-1), 'CENTER'),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
        else:
            t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                                    ('BACKGROUND', (0,1), (0,-1), colors.lightgrey),
                                    ('ALIGN', (1,1), (-1,-1), 'CENTER'),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
    elif presentation:
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('SPAN', (0,0), (1,0)),
                                ('SPAN', (2,0), (-1,0)),
                                ('SPAN', (0,1), (1,1)),
                                ('SPAN', (0,2), (-1,2)),
                                ('BACKGROUND', (0,3), (-1,3), colors.lightgrey),
                                ('BACKGROUND', (0,4), (0,9), colors.lightgrey),
                                ('ALIGN', (1,4), (-1,-1), 'CENTER'),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

    elements.append(t)
    elements.append(Spacer(1,5))
    comments = [Paragraph('<b>General Comments</b>', styles['Normal']), Spacer(1,4)]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            paragraph = Paragraph(line, styles['Normal'])
            comments.append(paragraph)
            comments.append(Spacer(1,4))
    for comment in comments:
        elements.append(comment)

    if essay_and_legal_problem:
        part_1_mark_data = [[Paragraph('Mark for part(a)', styles['Heading4']), Paragraph(str(marksheet.part_1_mark), styles['Heading4'])]]
        part_1_mark_table = Table(part_1_mark_data)
        elements.append(part_1_mark_table)
        elements.append(PageBreak())
        heading_2 = Paragraph('Feedback for Part (b): Legal Problem', styles['Heading3'])
        elements.append(heading_2)
        elements.append(Spacer(1,4))


        data_2 = [[criteria, category_5, category_6, category_7, category_8]]

        # Fill marking grid for the second part
        row = ['80 +']
        if marksheet.category_mark_5 == 80:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_6 == 80:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_7 == 80:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_8 == 80:
            row.append('X')
        else:
            row.append(' ')
        data_2.append(row)
        row = ['70 - 79']
        if marksheet.category_mark_5 == 79:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_6 == 79:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_7 == 79:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_8 == 79:
            row.append('X')
        else:
            row.append(' ')
        data_2.append(row)
        row = ['60 - 69']
        if marksheet.category_mark_5 == 69:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_6 == 69:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_7 == 69:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_8 == 69:
            row.append('X')
        else:
            row.append(' ')
        data_2.append(row)
        row = ['50 - 59']
        if marksheet.category_mark_5 == 59:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_6 == 59:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_7 == 59:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_8 == 59:
            row.append('X')
        else:
            row.append(' ')
        data_2.append(row)
        row = ['40 - 49']
        if marksheet.category_mark_5 == 49:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_6 == 49:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_7 == 49:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_8 == 49:
            row.append('X')
        else:
            row.append(' ')
        data_2.append(row)
        row = ['Under 40']
        if marksheet.category_mark_5 == 39:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_6 == 39:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_7 == 39:
            row.append('X')
        else:
            row.append(' ')
        if marksheet.category_mark_8 == 39:
            row.append('X')
        else:
            row.append(' ')
        data_2.append(row)
        t_2 = Table(data_2) 
        t_2.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                                ('BACKGROUND', (0,1), (0,-1), colors.lightgrey),
                                ('ALIGN', (1,4), (-1,-1), 'CENTER'),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
        elements.append(t_2)
        elements.append(Spacer(1,5))
        comments_2 = [Paragraph('<b>General Comments</b>', styles['Normal']), Spacer(1,4)]
        feedbacklist_2 = marksheet.comments_2.split('\n')
        for line in feedbacklist_2:
            if line != "":
                paragraph = Paragraph(line, styles['Normal'])
                comments_2.append(paragraph)
                comments_2.append(Spacer(1,4))
        for comment in comments_2:
            elements.append(comment)
        part_2_mark_data = [[Paragraph('Mark for part(b)', styles['Heading4']), Paragraph(str(marksheet.part_2_mark), styles['Heading4'])]]
        part_2_mark_table = Table(part_2_mark_data)
        elements.append(part_2_mark_table)
        elements.append(Spacer(1,10))
    if online_court:
        court = 'Mark for Court Report: ' + str(marksheet.part_1_mark)
        online = 'Mark for On Line Test: ' + str(marksheet.part_2_mark)
        last_data = [['', '', Paragraph(court, styles['Normal'])],
                    ['', '', Paragraph(online, styles['Normal'])],
                    #[Paragraph('Mark for Online Test', styles['Heading4']), Paragraph(str(marksheet.part_2_mark), styles['Heading4'])],
                    #[Paragraph('Mark for Court Report', styles['Heading4']), Paragraph(str(marksheet.part_1_mark), styles['Heading4'])],
                        [marked_table, '', '', mark_table]]
        last_table = Table(last_data)
        last_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('SPAN', (0,0), (1,1)),
                                ('SPAN', (2,0), (3,0)),
                                ('SPAN', (2,1), (3,1)),
                                ('SPAN', (0,-1), (2,-1))
                                ]))
    else:
        last_data = [[marked_table, '', '', mark_table, '']]
        last_table = Table(last_data)
        last_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('SPAN', (0,0), (2,0)),
                                ('SPAN', (3,-1), (-1,-1))]))
    elements.append(last_table)
    return elements

def get_title(module, assessment):
    if assessment == 1:
        assessment_title_string = module.assessment_1_title
    if assessment == 2:
        assessment_title_string = module.assessment_2_title
    if assessment == 3:
        assessment_title_string = module.assessment_3_title
    if assessment == 4:
        assessment_title_string = module.assessment_4_title
    if assessment == 5:
        assessment_title_string = module.assessment_5_title
    if assessment == 6:
        assessment_title_string = module.assessment_6_title
    assessment_title_string = assessment_title_string.replace("/", "or")
    return assessment_title_string

@login_required
def export_feedback_sheet(request, code, year, assessment_str, student_id):
    assessment = int(assessment_str)
    if student_id == 'all':
        if is_teacher(request.user) or is_admin(request.user): #Put check in if instructor
            module = Module.objects.get(code = code, year = year)
            response = HttpResponse(mimetype='application/pdf')
            first_part = module.title.replace(' ', '_')
            assessment_title = get_title(module, assessment)
            print assessment_title
            second_part = assessment_title.replace(' ', '_')
            filename_string = 'attachment; filename=' + first_part + '_' + second_part + '_-_all_marksheets.pdf'

            all_students = module.student_set.all()
            documentlist = []
            students = [] # Only the students where feedback has been entered
            for student in all_students:
                try:
                    performance = Marksheet.objects.get(student = student, module = module, assessment = assessment)
                    students.append(student)
                except Marksheet.DoesNotExist:
                    pass
            for student in students:
                elements = get_one_feedback_sheet(student, module, assessment)
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
        allowed = False # Only teachers and admins can access all marksheets, students only their own
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
                filename_string = 'attachment; filename=' + first_part + '_' + second_part + '_Marksheet.pdf'
            else:
                ln = student.last_name.replace(' ', '_')
                fn = student.first_name.replace(' ', '_')
                filename_string = 'attachment; filename=' + ln + '_' + fn + '.pdf'

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
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=attendance_sheet.pdf'
    document = SimpleDocTemplate(response)
    elements = []
    module = Module.objects.get(code=code, year=year)
    styles = getSampleStyleSheet()
    next_year = str(module.year + 1)
    heading = module.title + " (" + module.code + ") " + str(module.year) + "/" + next_year
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
    doc.pagesize = landscape(A4)
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


