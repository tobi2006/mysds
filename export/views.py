from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseForbidden)
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.templatetags.static import static
from random import shuffle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    BaseDocTemplate, Frame, PageTemplate, Image)
from reportlab.platypus.flowables import PageBreak

from database.views import is_teacher, is_admin, is_student
from database.models import *
from feedback.models import *
from feedback.categories import *
from anonymous_marking.models import *
from mysds.unisettings import *

# The different marking categories are in feedback/categories.py

# Helper Functions


def logo():
    """Returns the university logo, unless it is not available"""
    styles = getSampleStyleSheet()
    url = "https://cccu.tobiaskliem.de/static/images/cccu.jpg"
    try:
        image = Image(url, 2.45*inch, 1*inch)
    except IOError:
        image = Paragraph(
            "Canterbury Christ Church University", styles['Heading1'])
    return image


def bold(string):
    """Adds <b> tags around a string"""
    bold_string = '<b>' + string + '</b>'
    return bold_string


def heading(string, headingstyle='Heading2'):
    """Returns a proper paragraph for the header line"""
    styles = getSampleStyleSheet()
    tmp = '<para alignment = "center">' + string + '</para>'
    result = Paragraph(tmp, styles[headingstyle])
    return result


def formatted_date(raw_date):
    """Returns a proper date string

    This returns a string of the date in British Format.
    If the date field was left blank, an empty string is returned.
    """
    if raw_date is None:
        result = ''
    else:
        result = (
            str(raw_date.day) + '/' + str(raw_date.month) + '/' +
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
    marker_1_return = marker_1_list[1] + ' ' + marker_1_list[0]
    marker_2_return = marker_2_list[1] + ' ' + marker_2_list[0]
    result = marker_1_return + ' / ' + marker_2_return
    return result


def paragraph(string):
    """Returns a paragraph with normal style"""
    styles = getSampleStyleSheet()
    return Paragraph(string, styles['Normal'])


def bold_paragraph(string):
    """Returns a paragraph with bold formatting"""
    styles = getSampleStyleSheet()
    tmp = bold(string)
    return Paragraph(tmp, styles['Normal'])


def get_title(module, assessment):
    assessment_title_string = module.get_assessment_title(assessment)
    assessment_title_string = assessment_title_string.replace("/", "or")
    return assessment_title_string

# Different marksheets


def essay_sheet(student, module, assessment):
    """Marksheet for Essays

    This is the standard marksheet for CCCU Law, including a marking grid
    with four different categories
    """
    styles = getSampleStyleSheet()
    elements = []
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment)
    assessment_title = bold(module.get_assessment_title(assessment))
    mark = str(performance.get_assessment_result(assessment))
    elements.append(logo())
    elements.append(Spacer(1, 5))
    title = heading('Law Undergraduate Assessment Sheet: Essay')
    elements.append(title)
    elements.append(Spacer(1, 5))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph(module.title)]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)]
    tmp = formatted_date(marksheet.submission_date)
    submission_date = [
        paragraph('Submission Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1, 3),
        paragraph(assessment_title)]
    if module.get_assessment_max_wordcount(assessment):
        tmp = (
            str(module.get_assessment_max_wordcount(assessment)) +
            ' Words max.')
    else:
        tmp = ''
    word_count = [
        paragraph('Word Count'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    criteria = paragraph('Criteria')
    category_1 = paragraph(CATEGORIES['ESSAY']['i_1'])
    category_2 = paragraph(CATEGORIES['ESSAY']['i_2'])
    category_3 = paragraph(CATEGORIES['ESSAY']['i_3'])
    category_4 = paragraph(CATEGORIES['ESSAY']['i_4'])
    data = [
        [last_name, '', first_name, ''],
        [module_title, '', module_code, submission_date, ''],
        [assessment_title, '', word_count, '', ''],
        [criteria, category_1, category_2, category_3, category_4]]
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
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (-1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (3, 1), (-1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (2, 2), (-1, 2)),
            ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
            ('BACKGROUND', (0, 4), (0, 9), colors.lightgrey),
            ('ALIGN', (1, 4), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(t)
    comments = [
        bold_paragraph('General Comments'),
        Spacer(1, 4)]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1, 4))
    for comment in comments:
        elements.append(comment)
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker.first_name + ' ' + marker.last_name
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]]
    marked_by_table = Table(marked_by)
    mark = [
        [
            paragraph('Mark'),
            Paragraph(mark, styles['Heading1'])],
        ['', '']]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    last_data = [[marked_by_table, '', '', mark_table, '']]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (2, 0)),
            ('SPAN', (3, -1), (-1, -1))])
        )
    elements.append(last_table)
    return elements


def legal_problem_sheet(student, module, assessment):
    """Marksheet for Legal Problem Questions

    This is the standard marksheet for CCCU Law, including a marking grid
    with four different categories
    """
    styles = getSampleStyleSheet()
    elements = []
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment)
    assessment_title = bold(module.get_assessment_title(assessment))
    mark = str(performance.get_assessment_result(assessment))
    elements.append(logo())
    elements.append(Spacer(1, 5))
    title = heading('Law Undergraduate Assessment Sheet: Legal Problem')
    elements.append(title)
    elements.append(Spacer(1, 5))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph(module.title)]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)]
    tmp = formatted_date(marksheet.submission_date)
    submission_date = [
        paragraph('Submission Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1, 3),
        paragraph(assessment_title)]
    if module.get_assessment_max_wordcount(assessment):
        tmp = (
            str(module.get_assessment_max_wordcount(assessment)) +
            ' Words max.')
    else:
        tmp = ''
    word_count = [
        paragraph('Word Count'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    criteria = paragraph('Criteria')
    category_1 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_1'])
    category_2 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_2'])
    category_3 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_3'])
    category_4 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_4'])
    data = [
        [last_name, '', first_name, ''],
        [module_title, '', module_code, submission_date, ''],
        [assessment_title, '', word_count, '', ''],
        [criteria, category_1, category_2, category_3, category_4]]
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
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (-1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (3, 1), (-1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (2, 2), (-1, 2)),
            ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
            ('BACKGROUND', (0, 4), (0, 9), colors.lightgrey),
            ('ALIGN', (1, 4), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(t)
    comments = [
        bold_paragraph('General Comments'),
        Spacer(1, 4)]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1, 4))
    for comment in comments:
        elements.append(comment)
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker.first_name + ' ' + marker.last_name
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]]
    marked_by_table = Table(marked_by)
    mark = [
        [
            paragraph('Mark'),
            Paragraph(mark, styles['Heading1'])],
        ['', '']]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    last_data = [[marked_by_table, '', '', mark_table, '']]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (2, 0)),
            ('SPAN', (3, -1), (-1, -1))])
        )
    elements.append(last_table)
    return elements


def presentation_sheet(student, module, assessment):
    """Marksheet for Oral Presentations

    This is the standard marksheet for individual presentations at
    CCCU Law, including a marking grid with X different categories
    """
    styles = getSampleStyleSheet()
    elements = []
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment)
    assessment_title = bold(module.get_assessment_title(assessment))
    mark = str(performance.get_assessment_result(assessment))
    elements.append(logo())
    elements.append(Spacer(1, 5))
    title = heading('Law Undergraduate Assessment Sheet: Oral Presentation')
    elements.append(title)
    elements.append(Spacer(1, 5))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph(module.title)]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)]
    tmp = formatted_date(marksheet.submission_date)
    submission_date = [
        paragraph('Presentation Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1, 3),
        paragraph(assessment_title)]
    criteria = paragraph('Criteria')
    category_1 = paragraph(CATEGORIES['PRESENTATION']['i_1'])
    category_2 = paragraph(CATEGORIES['PRESENTATION']['i_2'])
    category_3 = paragraph(CATEGORIES['PRESENTATION']['i_3'])
    data = [
        [last_name, '', first_name, ''],
        [module_title, '', module_code, submission_date],
        [assessment_title, '', '', ''],
        [criteria, category_1, category_2, category_3]]
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
    data.append(row)
    t = Table(data)
    t.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (-1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (-1, 2)),
            ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
            ('BACKGROUND', (0, 4), (0, 9), colors.lightgrey),
            ('ALIGN', (1, 4), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(t)
    comments = [
        bold_paragraph('General Comments'),
        Spacer(1, 4)]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1, 4))
    for comment in comments:
        elements.append(comment)
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker.first_name + ' ' + marker.last_name
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]]
    marked_by_table = Table(marked_by)
    mark = [
        [
            paragraph('Mark'),
            Paragraph(mark, styles['Heading1'])
        ],
        ['', '']]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    last_data = [[marked_by_table, '', '', mark_table, '']]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (2, 0)),
            ('SPAN', (3, -1), (-1, -1))])
        )
    elements.append(last_table)
    return elements


def essay_legal_problem_sheet(student, module, assessment):
    """Marksheet for a cross between Essay and legal problem

    This consists of the essay marksheet combined with the legal problem grid
    and two different comment sections
    """
    styles = getSampleStyleSheet()
    elements = []
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment)
    assessment_title = bold(module.get_assessment_title(assessment))
    mark = str(performance.get_assessment_result(assessment))
    elements.append(logo())
    elements.append(Spacer(1, 5))
    title = heading(
        'Law Undergraduate Assessment Sheet: Essay / Legal Problem')
    elements.append(title)
    elements.append(Spacer(1, 5))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph(module.title)]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)]
    tmp = formatted_date(marksheet.submission_date)
    submission_date = [
        paragraph('Submission Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1, 3),
        paragraph(assessment_title)]
    if module.get_assessment_max_wordcount(assessment):
        tmp = (
            str(module.get_assessment_max_wordcount(assessment)) +
            ' Words max.')
    else:
        tmp = ''
    word_count = [
        paragraph('Word Count'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    criteria = paragraph('Criteria')
    category_1 = paragraph(CATEGORIES['ESSAY']['i_1'])
    category_2 = paragraph(CATEGORIES['ESSAY']['i_2'])
    category_3 = paragraph(CATEGORIES['ESSAY']['i_3'])
    category_4 = paragraph(CATEGORIES['ESSAY']['i_4'])
    category_5 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_1'])
    category_6 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_2'])
    category_7 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_3'])
    category_8 = paragraph(CATEGORIES['LEGAL_PROBLEM']['i_4'])
    data = [
        [last_name, '', first_name, ''],
        [module_title, '', module_code, submission_date, ''],
        [assessment_title, '', word_count, '', '']]
    t = Table(data)
    t.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (-1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (3, 1), (-1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (2, 2), (-1, 2)),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(t)
    elements.append(Spacer(1, 5))
    subtitle = Paragraph('Feedback for Part (a): Essay', styles['Heading3'])
    elements.append(subtitle)
    elements.append(Spacer(1, 5))
    data = [[criteria, category_1, category_2, category_3, category_4]]
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
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(t)
    elements.append(Spacer(1, 5))
    comments = [
        bold_paragraph('General Comments'),
        Spacer(1, 4)]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1, 4))
    for comment in comments:
        elements.append(comment)
    part_1_mark_data = [[
        Paragraph('Mark for part(a)', styles['Heading4']),
        Paragraph(str(marksheet.part_1_mark), styles['Heading4'])]]
    part_1_mark_table = Table(part_1_mark_data)
    part_1_mark_table.setStyle(
        TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(part_1_mark_table)
    elements.append(PageBreak())
    heading_2 = Paragraph(
        'Feedback for Part (b): Legal Problem', styles['Heading3'])
    elements.append(heading_2)
    elements.append(Spacer(1, 4))
    data_2 = [[criteria, category_5, category_6, category_7, category_8]]
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
    t_2.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('ALIGN', (1, 4), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(t_2)
    elements.append(Spacer(1, 5))
    comments_2 = [
        bold_paragraph('General Comments'),
        Spacer(1, 4)]
    feedbacklist_2 = marksheet.comments_2.split('\n')
    for line in feedbacklist_2:
        if line != "":
            p = paragraph(line)
            comments_2.append(p)
            comments_2.append(Spacer(1, 4))
    for comment in comments_2:
        elements.append(comment)
    part_2_mark_data = [[
        Paragraph('Mark for part(b)', styles['Heading4']),
        Paragraph(str(marksheet.part_2_mark), styles['Heading4'])
        ]]
    part_2_mark_table = Table(part_2_mark_data)
    part_2_mark_table.setStyle(
        TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(part_2_mark_table)
    elements.append(Spacer(1, 10))
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker.first_name + ' ' + marker.last_name
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]]
    marked_by_table = Table(marked_by)
    mark = [
        [
            paragraph('Final Mark for (a) and (b)'),
            Paragraph(mark, styles['Heading1'])
        ],
        ['', '']]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    last_data = [[marked_by_table, '', '', mark_table, '']]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (2, 0)),
            ('SPAN', (3, -1), (-1, -1))])
        )
    elements.append(last_table)
    return elements


def online_test_court_report_sheet(student, module, assessment):
    """Marksheet for Online Test / Court Report

    This is a custom marksheet that allows to combine a mark for an online
    test with a court report. Essentially, it is the essay marksheet with
    a few extra points.
    """
    styles = getSampleStyleSheet()
    elements = []
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment)
    assessment_title = bold(module.get_assessment_title(assessment))
    mark = str(performance.get_assessment_result(assessment))
    elements.append(logo())
    elements.append(Spacer(1, 5))
    title = heading(
        'Law Undergraduate Assessment Sheet: Online Test / Court Report')
    elements.append(title)
    elements.append(Spacer(1, 5))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph(module.title)]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)]
    tmp = formatted_date(marksheet.submission_date)
    submission_date = [
        paragraph('Submission Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1, 3),
        paragraph(assessment_title)]
    if module.get_assessment_max_wordcount(assessment):
        tmp = (
            str(module.get_assessment_max_wordcount(assessment)) +
            ' Words max.')
    else:
        tmp = ''
    word_count = [
        paragraph('Word Count'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    criteria = paragraph('Criteria')
    category_1 = paragraph(CATEGORIES['ESSAY']['i_1'])
    category_2 = paragraph(CATEGORIES['ESSAY']['i_2'])
    category_3 = paragraph(CATEGORIES['ESSAY']['i_3'])
    category_4 = paragraph(CATEGORIES['ESSAY']['i_4'])
    data = [
        [last_name, '', first_name, ''],
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
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (-1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (3, 1), (-1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (2, 2), (-1, 2)),
            ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
            ('BACKGROUND', (0, 4), (0, 9), colors.lightgrey),
            ('ALIGN', (1, 4), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
            ])
        )
    elements.append(t)
    comments = [
        bold_paragraph('General Comments'),
        Spacer(1, 4)]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1, 4))
    for comment in comments:
        elements.append(comment)
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker.first_name + ' ' + marker.last_name
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]]
    marked_by_table = Table(marked_by)
    mark = [
        [
            paragraph('Combined Mark'),
            Paragraph(mark, styles['Heading1'])
        ],
        ['', '']
        ]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    court = 'Mark for Court Report: ' + str(marksheet.part_1_mark)
    online = 'Mark for On Line Test: ' + str(marksheet.part_2_mark)
    last_data = [
        ['', '', paragraph(court)],
        ['', '', paragraph(online)],
        [marked_by_table, '', '', mark_table]]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (1, 1)),
            ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (2, 1), (3, 1)),
            ('SPAN', (0, -1), (2, -1))
            ])
        )
    elements.append(last_table)
    return elements


def negotiation_written_sheet(student, module, assessment):
    """Marksheet for the assessment 'Negotiation / Written Submission'

    This is an assessment that includes a group component and is therefore
    a little more complex.
    """
    elements = []
    styles = getSampleStyleSheet()
    performance = Performance.objects.get(student=student, module=module)
    marksheet = Marksheet.objects.get(
        student=student, module=module, assessment=assessment
    )
    group_no = performance.group_assessment_group
    group_feedback = GroupMarksheet.objects.get(
        module=module, assessment=assessment, group_no=group_no
    )
    mark = str(performance.get_assessment_result(assessment))
    elements.append(logo())
    elements.append(Spacer(1, 3))
    title = heading(
        'Law Undergraduate Assessment Sheet: Negotiation Study', 'Heading3'
    )
    elements.append(title)
    elements.append(Spacer(1, 3))
    last_name = [
        bold_paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph('ELIM')]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)]
    tmp = formatted_date(group_feedback.submission_date)
    submission_date = [
        paragraph('Presentation Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    tmp = str(performance.seminar_group) + '/' + str(group_no)
    group_number = [
        paragraph('Seminar/LAU Group'),
        Spacer(1, 3),
        bold_paragraph(tmp)]
    individual_category_1 = bold_paragraph(
        CATEGORIES['NEGOTIATION_WRITTEN']['i_1'])
    individual_category_2 = bold_paragraph(
        CATEGORIES['NEGOTIATION_WRITTEN']['i_2'])
    individual_category_3 = bold_paragraph(
        CATEGORIES['NEGOTIATION_WRITTEN']['i_3'])
    individual_category_4 = bold_paragraph(
        CATEGORIES['NEGOTIATION_WRITTEN']['i_4'])
    group_category_1 = bold_paragraph(CATEGORIES['NEGOTIATION_WRITTEN']['g_1'])
    group_category_2 = bold_paragraph(CATEGORIES['NEGOTIATION_WRITTEN']['g_2'])
    group_category_3 = bold_paragraph(CATEGORIES['NEGOTIATION_WRITTEN']['g_3'])
    group_category_4 = bold_paragraph(CATEGORIES['NEGOTIATION_WRITTEN']['g_4'])
    deduction_explanation = (
        paragraph(CATEGORIES['NEGOTIATION_WRITTEN']['i_4_helptext']))
    marker = marksheet.marker
    if marksheet.second_first_marker:
        marker2 = marksheet.second_first_marker
        tmp = two_markers(marker, marker2)
    else:
        tmp = marker.first_name + ' ' + marker.last_name
    marking_date = formatted_date(marksheet.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(tmp)],
        [paragraph('Date'), bold_paragraph(marking_date)]]
    marked_by_table = Table(marked_by)
    mark = [
        [
            paragraph('Mark'),
            Paragraph(mark, styles['Heading1'])
        ],
        ['', '']]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    table_header_1 = bold_paragraph('Part 1: Assessed Negotiation')
    table_header_2 = bold_paragraph('Marks Available')
    table_header_3 = bold_paragraph('Marks Awarded')
    part_1_subheader = bold_paragraph('1. Individual Work')
    part_2_subheader = bold_paragraph('2. Group Work')
    sub_total_1_string = bold_paragraph('Sub-Total Part 1')
    sub_total_1 = 0
    if marksheet.category_mark_1_free is not None:
        sub_total_1 += marksheet.category_mark_1_free
    if group_feedback.category_mark_1_free is not None:
        sub_total_1 += group_feedback.category_mark_1_free
    if group_feedback.category_mark_2_free is not None:
        sub_total_1 += group_feedback.category_mark_2_free
    table_header_4 = bold_paragraph(
        'Part 2: Individual and Written Submission'
        )
    sub_total_2_string = paragraph('Sub-Total Part 2')
    sub_total_2 = 0
    if marksheet.category_mark_2_free is not None:
        sub_total_2 += marksheet.category_mark_2_free
    if marksheet.category_mark_3_free is not None:
        sub_total_2 += marksheet.category_mark_3_free
    if group_feedback.category_mark_3_free is not None:
        sub_total_2 += group_feedback.category_mark_3_free
    if group_feedback.category_mark_4_free is not None:
        sub_total_2 += group_feedback.category_mark_4_free
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
    data = [[last_name, first_name, group_number, ''],
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
    t.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0),  (-1, -1), 0.25, colors.black),
            ('SPAN', (-2, 0), (-1, 0)),
            ('SPAN', (-2, 1), (-1, 1)),
            ('SPAN', (0, 2), (-1, 2)),
            ('BOX', (0, 0), (-1, 1), 0.25, colors.black),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (0, 4), (1, 4)),
            ('SPAN', (0, 5), (1, 5)),
            ('SPAN', (0, 6), (1, 6)),
            ('SPAN', (0, 7), (1, 7)),
            ('SPAN', (0, 8), (1, 8)),
            ('SPAN', (0, 9), (1, 9)),
            ('BACKGROUND', (0, 10), (-1, 10), colors.lightgrey),
            ('SPAN', (0, 10), (1, 10)),
            ('SPAN', (0, 11), (1, 11)),
            ('SPAN', (0, 12), (1, 12)),
            ('SPAN', (0, 13), (1, 13)),
            ('SPAN', (0, 14), (1, 14)),
            ('SPAN', (0, 15), (1, 15)),
            ('SPAN', (0, 16), (1, 16)),
            ('SPAN', (0, 17), (1, 17)),
            ('SPAN', (0, 18), (1, 18)),
            ('SPAN', (0, 19), (1, 19)),
            ('SPAN', (0, 20), (1, 20)),
            ('BACKGROUND', (0, 18), (-1, 18), colors.lightgrey),
            ('BOX', (0, 3), (-1, -1), 0.25, colors.black)])
        )
    elements.append(t)
    elements.append(PageBreak())
    # Individual Comments
    individual_comments = [
        bold_paragraph('Comment on <u>Individual</u> Work for part 1 and 2'),
        Spacer(1, 4)]
    feedbacklist = marksheet.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            individual_comments.append(p)
            individual_comments.append(Spacer(1, 4))
    # Group Comments
    group_comments = [
        bold_paragraph('Comment on <u>Group</u> Work for part 1 and 2'),
        Spacer(1, 4)]
    feedbacklist = group_feedback.group_comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            group_comments.append(p)
            group_comments.append(Spacer(1, 4))
    # Final table
    last_data = [
        [individual_comments, '', '', ''],
        [group_comments, '', '', ''],
        [marked_by_table, '', mark_table, '']
        ]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPAN', (0, 0), (-1, 0)),
            ('SPAN', (0, 1), (-1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (2, 2), (-1, 2)),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey)])
        )
    elements.append(last_table)
    return elements

# Functions called from website


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
    assessment_type = module.get_marksheet_type(assessment)
    if student_id == 'all':
        if is_teacher(request.user) or is_admin(request.user):
            response = HttpResponse(mimetype='application/pdf')
            first_part = module.title.replace(' ', '_')
            second_part = assessment_title.replace(' ', '_')
            filename_string = (
                'attachment; filename=' + first_part +
                '_' + second_part + '_-_all_marksheets.pdf')
            all_students = module.student_set.all()
            documentlist = []
            students = []  # Only the students where feedback has been entered
            for student in all_students:
                try:
                    performance = Marksheet.objects.get(
                        student=student, module=module,
                        assessment=assessment)
                    students.append(student)
                except Marksheet.DoesNotExist:
                    pass
            for student in students:
                if assessment_type == 'ESSAY':
                    elements = essay_sheet(student, module, assessment)
                elif assessment_type == 'LEGAL_PROBLEM':
                    elements = legal_problem_sheet(
                        student, module, assessment)
                elif assessment_type == 'PRESENTATION':
                    elements = presentation_sheet(student, module, assessment)
                elif assessment_type == 'ESSAY_LEGAL_PROBLEM':
                    elements = essay_legal_problem_sheet(
                        student, module, assessment)
                elif assessment_type == 'ONLINE_TEST_COURT_REPORT':
                    elements = online_test_court_report_sheet(
                        student, module, assessment)
                elif assessment_type == 'NEGOTIATION_WRITTEN':
                    elements = negotiation_written_sheet(
                        student, module, assessment)
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
        student = Student.objects.get(student_id=student_id)
        own_marksheet = False  # Just for the filename
        allowed = False
        if is_teacher(request.user) or is_admin(request.user):
            allowed = True
        elif is_student(request.user):
            if student.belongs_to == request.user:
                own_marksheet = True
                allowed = True
        if allowed:
            module = Module.objects.get(code=code, year=year)
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
            if assessment_type == 'ESSAY':
                elements = essay_sheet(student, module, assessment)
            elif assessment_type == 'LEGAL_PROBLEM':
                elements = legal_problem_sheet(
                    student, module, assessment
                    )
            elif assessment_type == 'PRESENTATION':
                elements = presentation_sheet(student, module, assessment)
            elif assessment_type == 'ESSAY_LEGAL_PROBLEM':
                elements = essay_legal_problem_sheet(
                    student, module, assessment)
            elif assessment_type == 'ONLINE_TEST_COURT_REPORT':
                elements = online_test_court_report_sheet(
                    student, module, assessment)
            elif assessment_type == 'NEGOTIATION_WRITTEN':
                elements = negotiation_written_sheet(
                    student, module, assessment)

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
        'attachment; filename=attendance_sheet.pdf')
    document = SimpleDocTemplate(response)
    elements = []
    module = Module.objects.get(code=code, year=year)
    styles = getSampleStyleSheet()
    next_year = str(module.year + 1)
    heading = (
        module.title + " (" + module.code + ") " + str(module.year) +
        "/" + next_year)
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
        elements.append(Spacer(1, 20))
        data = []
        header = ['Name']
        column = 0
        last_week = module.last_session + 1
        no_teaching = module.no_teaching_in.split(",")
        for week in range(module.first_session, last_week):
            strweek = str(week)
            if strweek not in no_teaching:
                header.append(strweek)
        data.append(header)
        performances = Performance.objects.filter(
            module=module, seminar_group=counter)
        for performance in performances:
            row = [performance.student]
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
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
            )
        elements.append(table)
        elements.append(PageBreak())
    document.build(elements)
    return response


@login_required
@user_passes_test(is_admin)
def export_all_anonymous_exam_marks(request, year):
    """Gives an overview of all anonymous marks in the year"""
    modules = Module.objects.filter(year=year)
    modules_to_use = []
    for module in modules:
        if module.exam_value:
            marks = AnonymousMarks.objects.filter(module=module)
            for mark in marks:
                if mark.exam:
                    modules_to_use.append(module)
                    break
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename=anonymous_exam_marks.pdf')
    doc = BaseDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    frame1 = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width/2-6,
        doc.height, id='col1')
    frame2 = Frame(
        doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
        doc.height, id='col2')
    d = formatted_date(date.today())
    datenow = "Exported from MySDS, the CCCU Law DB on " + d
    for module in modules_to_use:
        heading = (
            "Anonymous Marks for " + module.title + " (" +
            str(module.year) + "/" + str(module.year + 1) + ")")
        elements.append(Paragraph(heading, styles['Heading2']))
        elements.append(Spacer(1, 20))
        data = []
        header = ['Exam ID', 'Exam Mark']
        data.append(header)
        marks = AnonymousMarks.objects.filter(module=module)
        for mark in marks:
            row = [mark.exam_id, mark.exam]
            data.append(row)
        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
            )
        elements.append(table)
        elements.append(paragraph(datenow))
        elements.append(PageBreak())
    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2])])
    doc.build(elements)
    return response


@login_required
@user_passes_test(is_teacher)
def export_anonymous_marks(request, code, year, assessment):
    """Gives an overview of anonymous marks for an assessment"""
    module = Module.objects.get(code=code, year=year)
    response = HttpResponse(mimetype='application/pdf')
    module_string = module.title.replace(" ", "_")
    filename_string = 'attachment; filename='
    filename_string += module_string
    filename_string += '.pdf'
    response['Content-Disposition'] = filename_string
    doc = BaseDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    frame1 = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width/2-6,
        doc.height, id='col1')
    frame2 = Frame(
        doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
        doc.height, id='col2')
    d = formatted_date(date.today())
    datenow = "Exported from MySDS, the CCCU Law DB on " + d
    heading = (
        "Anonymous Marks for " + module.title + " (" +
        str(module.year) + "/" + str(module.year + 1) + ") - ")
    if assessment == 'exam':
        heading += "Exam"
    else:
        assessment = int(assessment)
        heading += module.get_assessment_title(assessment)
    elements.append(Paragraph(heading, styles['Heading2']))
    elements.append(Spacer(1, 20))
    data = []
    header = ['Exam ID', 'Mark']
    data.append(header)
    marks = AnonymousMarks.objects.filter(module=module)
    for mark in marks:
        row = [mark.exam_id, mark.get_assessment_result(assessment)]
        data.append(row)
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        )
    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(paragraph(datenow))
    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2])])
    doc.build(elements)
    return response


@login_required
@user_passes_test(is_teacher)
def export_marks(request, code, year):
    """Gives a useful sheet of all marks for the module.

    Students will be highlighted if they failed the module, or if a QLD
    student failed a component in a Foundational module
    """
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
    modulestring = (
        module.title + ' (' + module.code + ') ' + str(module.year) + '/' +
        str(module.year + 1)
        )
    heading = "Marks for " + modulestring
    elements.append(Paragraph(heading, styles['Heading2']))
    elements.append(Spacer(1, 20))
    data = []
    header = ['ID', 'Student', ' Programme', 'QLD']
    assessment_range = []
    if module.assessment_1_value:
        title = (
            module.assessment_1_title.strip() +
            ' (' +
            str(module.assessment_1_value) +
            '%)'
            )
        assessment_range.append('1')
        header.append(paragraph(title))
    if module.assessment_2_value:
        title = (
            module.assessment_2_title.strip() +
            ' (' +
            str(module.assessment_2_value) +
            '%)'
            )
        assessment_range.append('2')
        header.append(paragraph(title))
    if module.assessment_3_value:
        title = (
            module.assessment_3_title.strip() +
            ' (' +
            str(module.assessment_3_value) +
            '%)'
            )
        assessment_range.append('3')
        header.append(paragraph(title))
    if module.assessment_4_value:
        title = (
            module.assessment_4_title.strip() +
            ' (' +
            str(module.assessment_4_value) +
            '%)'
            )
        assessment_range.append('4')
        header.append(paragraph(title))
    if module.assessment_5_value:
        title = (
            module.assessment_5_title.strip() +
            ' (' +
            str(module.assessment_5_value) +
            '%)'
            )
        assessment_range.append('5')
        header.append(paragraph(title))
    if module.assessment_6_value:
        title = (
            module.assessment_6_title.strip() +
            ' (' +
            str(module.assessment_6_value) +
            '%)'
            )
        assessment_range.append('6')
        header.append(paragraph(title))
    if module.exam_value:
        title = (
            'Exam (' +
            str(module.exam_value) +
            '%)'
            )
        assessment_range.append('exam')
        header.append(paragraph(title))
    header.append('Total')
    header.append('Notes')
    data.append(header)
    performances = Performance.objects.filter(module=module)
    counter = 0
    highlight = []
    # This needs to be replaced once model changes
    ls = Course.objects.get(
        title='BSc (Hons) Legal Studies / Sport And Exercise Science')
    llb = Course.objects.get(
        title='LLB (Hons) Bachelor Of Law')
    business = Course.objects.get(
        title='LLB (Hons) Bachelor Of Law With Business Studies')
    ac = Course.objects.get(
        title='LLB (Hons) Bachelor Of Law With Criminology')
    fi = Course.objects.get(
        title='LLB (Hons) Bachelor Of Law With Forensic Investigation')
    ir = Course.objects.get(
        title='LLB (Hons) Bachelor Of Law With International Relations')
    soc = Course.objects.get(
        title='LLB (Hons) Bachelor Of Law With Sociology')
    # <<<
    for performance in performances:
        counter += 1
        student = (
            performance.student.last_name + ", " +
            performance.student.short_first_name()
            )
        row = [performance.student.student_id, paragraph(student)]
        # This needs to be replaced once model changes
        if performance.student.course == llb:
            course = 'LLB'
        elif performance.student.course == business:
            course = 'LLB/Business'
        elif performance.student.course == ac:
            course = 'LLB/AC'
        elif performance.student.course == fi:
            course = 'LLB/FI'
        elif performance.student.course == ir:
            course = 'LLB/IR'
        elif performance.student.course == soc:
            course = 'LLB/Sociology'
        elif performance.student.course == ls:
            course = 'LS/Sport'
        else:
            course = ''
        row.append(course)
        # <<<
        if performance.student.qld:
            row.append(u'\u2713')
        else:
            row.append(' ')
        notes = ''
        if performance.average < PASSMARK:
            highlight_yellow = True
        else:
            highlight_yellow = False
        highlight_red = False
        for assessment in assessment_range:
            concession = performance.get_concession(assessment)
            assessment_title = module.get_assessment_title(assessment)
            assessment_title = assessment_title.strip()
            granted_or_pending = False
            if concession == 'G':
                granted_or_pending = True
                if assessment == 'exam':
                    if len(notes) == 0:
                        notes = 'Sit exam'
                    else:
                        notes += ', sit exam'
                else:
                    if len(notes) == 0:
                        notes = 'Submit ' + assessment_title
                    else:
                        notes += ', submit ' + assessment_title
            if concession == 'P':
                granted_or_pending = True
                if assessment == 'exam':
                    if len(notes) == 0:
                        notes = 'Concession for exam pending'
                    else:
                        notes += ', concession for exam pending'
                else:
                    if len(notes) == 0:
                        notes = (
                            'Concession for ' +
                            assessment_title +
                            ' pending')
                    else:
                        notes += (
                            ', concession for ' +
                            assessment_title +
                            ' pending')
            if performance.get_assessment_result(assessment):
                row.append(performance.get_assessment_result(assessment))
                if module.is_foundational and performance.student.qld:
                    if (performance.get_assessment_result(assessment)
                            < PASSMARK):
                        if not granted_or_pending:
                            if assessment == 'exam':
                                if len(notes) == 0:
                                    notes = 'Resit exam'
                                else:
                                    notes += ', resit exam'
                            else:
                                if len(notes) == 0:
                                    notes = 'Resubmit ' + assessment_title
                                else:
                                    notes += ', resubmit ' + assessment_title
                        if not highlight_yellow:
                            highlight_red = True
                elif performance.average < PASSMARK:
                    if (performance.get_assessment_result(assessment)
                            < PASSMARK):
                        if not granted_or_pending:
                            if assessment == 'exam':
                                if len(notes) == 0:
                                    notes = 'Resit exam'
                                else:
                                    notes += ', resit exam'
                            else:
                                if len(notes) == 0:
                                    notes = 'Reubmit ' + assessment_title
                                else:
                                    notes += ', resubmit ' + assessment_title
            else:
                row.append('-')
                if module.is_foundational and performance.student.qld:
                    if (performance.get_assessment_result(assessment)
                            < PASSMARK):
                        if not granted_or_pending:
                            if assessment == 'exam':
                                if len(notes) == 0:
                                    notes = 'Resit exam'
                                else:
                                    notes += ', resit exam'
                            else:
                                if len(notes) == 0:
                                    notes = 'Resubmit ' + assessment_title
                                else:
                                    notes += ', resubmit ' + assessment_title
                    if not highlight_yellow:
                        highlight_red = True
                elif performance.average < PASSMARK:
                    if (performance.get_assessment_result(assessment)
                            < PASSMARK):
                        if not granted_or_pending:
                            if assessment == 'exam':
                                if len(notes) == 0:
                                    notes = 'Resit exam'
                                else:
                                    notes += ', resit exam'
                            else:
                                if len(notes) == 0:
                                    notes = 'Reubmit ' + assessment_title
                                else:
                                    notes += ', resubmit ' + assessment_title
        if performance.average:
            row.append(performance.average)
        else:
            row.append('-')
            highlight_yellow = True
        notes_paragraph = paragraph(notes)
        row.append(notes_paragraph)
        data.append(row)
        if highlight_yellow:
            highlight.append((counter, 'y'))
        if highlight_red:
            highlight.append((counter, 'r'))
    table = Table(data, repeatRows=1)
    tablestyle = [
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
        ]
    for item in highlight:
        if item[1] == 'r':
            tablestyle.append(
                ('BACKGROUND', (0, item[0]), (-1, item[0]), colors.red)
                )
        if item[1] == 'y':
            tablestyle.append(
                ('BACKGROUND', (0, item[0]), (-1, item[0]), colors.yellow)
                )
    table.setStyle(TableStyle(tablestyle))
    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(paragraph(datenow))
    elements.append(PageBreak())
    doc.build(elements)
    return response


def sample_pack(request, code, year):
    """Prepares a nice sample pack for the external examiner"""
    module = Module.objects.get(code=code, year=year)
    response = HttpResponse(mimetype='application/pdf')
    tmp = module.title.replace(" ", "_")
    filename_string = 'attachment; filename=' + tmp + '_examiners_pack.pdf'
    response['Content-Disposition'] = filename_string
    document = SimpleDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    performances = list(Performance.objects.filter(module=module))
    samplesize = sample_size(len(performances))
    per_range = round(samplesize / 5)  # Fail, 40s, 50s, 60s, 70 +
    sample = {}
    for assessment in module.get_assessment_range():
        shuffle(performances)  # Make sure the marks are from all over
        add = []
        first = []
        two_one = []
        two_two = []
        third = []
        fail = []
        leftover = []  # Needed if there are less than per_range in one
        complete = False
        for performance in performances:
            mark = performance.get_assessment_result(assessment)
            if mark:
                if mark > 69:
                    if len(first) < per_range:
                        first.append(performance)
                    else:
                        leftover.append(performance)
                elif mark > 59:
                    if len(two_one) < per_range:
                        two_one.append(performance)
                    else:
                        leftover.append(performance)
                elif mark > 49:
                    if len(two_two) < per_range:
                        two_two.append(performance)
                    else:
                        leftover.append(performance)
                elif mark > 39:
                    if len(third) < per_range:
                        third.append(performance)
                    else:
                        leftover.append(performance)
                else:
                    if len(fail) < per_range:
                        fail.append(performance)
                    else:
                        leftover.append(performance)
        this_sample = first + two_one + two_two + third + fail
        while len(this_sample) < samplesize:
            this_sample.append(leftover.pop())
        this_sample.sort(
            key=lambda x: x.get_assessment_result(assessment),
            reverse=True)
        sample[assessment] = this_sample
    title = heading('Checklist, not part of the pack')
    elements.append(title)
    assessment_string = (
        'Assessments (at the end, together with the marksheets included in ' +
        'this bundle)')
    data = [
        [
            bold_paragraph('Make sure to add the following to this pack'),
            '', '', ''],
        ['The module handbook (after the title page)', '', '', ''],
        [bold_paragraph(assessment_string), '', '', '']
        ]
    headline = [0, 2]
    only_one = [1]
    counter = 2
    for assessment in module.get_assessment_range():
        if module.get_assessment_title(assessment) == 'Exam':
            blind = True
        else:
            blind = False
        newline = True
        counter += 1
        title = bold_paragraph(module.get_assessment_title(assessment))
        headline.append(counter)
        data.append([title, '', '', ''])
        counter += 1
        title = paragraph(
            'Instructions for ' + module.get_assessment_title(assessment))
        data.append([title, '', '', ''])
        only_one.append(counter)
        this_sample = sample[assessment]
        for performance in this_sample:
            if newline:
                print "True"
                counter += 1
                if blind:
                    first_column = performance.student.exam_id
                    print first_column
                else:
                    first_column = performance.student.__unicode__()
                newline = False
            else:
                if blind:
                    data.append(
                        [
                            first_column,
                            '',
                            performance.student.exam_id,
                            ''
                        ])
                else:
                    data.append(
                        [
                            first_column,
                            '',
                            performance.student.__unicode__(),
                            ''
                        ])
                newline = True
    t = Table(data, colWidths=(200, 20, 200, 20))
    style = [
        ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
        ]
    for line in headline:
        style.append(('SPAN', (0, line), (-1, line)))
    for line in only_one:
        style.append(('SPAN', (0, line), (-2, line)))

#    for line in checkboxline:
#        style.append(('BOX', (-1, line), (-1, line)))
    t.setStyle(TableStyle(style))
    elements.append(t)
    # Title page
    elements.append(PageBreak())
    elements.append(Spacer(1, 100))
    elements.append(logo())
    elements.append(Spacer(1, 80))
    title = heading(module.__unicode__(), 'Heading1')
    elements.append(title)
    elements.append(Spacer(1, 40))
    if len(module.eligible) == 1:
        tmp = 'Year ' + module.eligible
    elif len(module.eligible) == 2:
        tmp = 'Years ' + module.eligible[0] + ' and ' + module.eligible[1]
    else:
        tmp = (
            'Years ' +
            module.eligible[0] +
            ', ' +
            module.eligible[1] +
            ' and ' +
            module.eligible[2]
            )
    level = heading(tmp)
    elements.append(level)
    elements.append(Spacer(1, 40))
    subtitle = heading('Exam Board Sample Pack')
    elements.append(subtitle)
    elements.append(PageBreak())
    # Statistics page
    title = heading('Module Marks')
    elements.append(title)
    elements.append(Spacer(1, 20))
    no_of_first = 0
    no_of_two_one = 0
    no_of_two_two = 0
    no_of_third = 0
    no_of_fail = 0
    for performance in performances:
        result = performance.average
        if result:
            if result > 69:
                no_of_first += 1
            elif result > 59:
                no_of_two_one += 1
            elif result > 49:
                no_of_two_two += 1
            elif result > 39:
                no_of_third += 1
            else:
                no_of_fail += 1
    first_f = float(no_of_first)
    two_one_f = float(no_of_two_one)
    two_two_f = float(no_of_two_two)
    third_f = float(no_of_third)
    fail_f = float(no_of_fail)
    first_percent = round(((first_f / len(performances)) * 100), 1)
    two_one_percent = round(((two_one_f / len(performances)) * 100), 1)
    two_two_percent = round(((two_two_f / len(performances)) * 100), 1)
    third_percent = round(((third_f / len(performances)) * 100), 1)
    fail_percent = round(((fail_f / len(performances)) * 100), 1)
    data = []
    data.append(['Range', 'Amount', 'Percentage'])
    data.append(['70 +', no_of_first, first_percent])
    data.append(['60-69', no_of_two_one, two_one_percent])
    data.append(['50-59', no_of_two_two, two_two_percent])
    data.append(['40-49', no_of_third, third_percent])
    data.append(['Fail', no_of_fail, fail_percent])
    t = Table(data)
    style = [
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]
    t.setStyle(TableStyle(style))
    elements.append(t)
    elements.append(PageBreak())
    for assessment in module.get_assessment_range():
        this_sample = sample[assessment]
        assessment_type = module.get_marksheet_type(assessment)
        if assessment_type:
            for performance in this_sample:
                student = performance.student
                if assessment_type == 'ESSAY':
                    marksheet = essay_sheet(student, module, assessment)
                elif assessment_type == 'LEGAL_PROBLEM':
                    marksheet = legal_problem_sheet(
                        student, module, assessment)
                elif assessment_type == 'PRESENTATION':
                    marksheet = presentation_sheet(student, module, assessment)
                elif assessment_type == 'ESSAY_LEGAL_PROBLEM':
                    marksheet = essay_legal_problem_sheet(
                        student, module, assessment)
                elif assessment_type == 'ONLINE_TEST_COURT_REPORT':
                    marksheet = online_test_court_report_sheet(
                        student, module, assessment)
                elif assessment_type == 'NEGOTIATION_WRITTEN':
                    marksheet = negotiation_written_sheet(
                        student, module, assessment)
                else:
                    marksheet = False
                if marksheet:
                    for element in marksheet:
                        elements.append(element)
                    elements.append(PageBreak())
    document.build(elements)
    return response
