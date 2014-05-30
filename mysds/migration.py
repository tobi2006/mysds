# These are just functions needed to migrate from the old Database approach
# to feedback categories to the new approach that stores them in the dictionary
# in feedback/categories.py

from database.models import *
from feedback.models import *
from feedback.categories import *

def migrate_assessment_type():
    """Moves everything out of db based system"""
    essay = FeedbackCategories.objects.get(assessment_type = 'Essay')
    legal_problem = FeedbackCategories.objects.get(
            assessment_type = 'Legal Problem')
    oral_presentation = FeedbackCategories.objects.get(
            assessment_type = 'Oral Presentation')
    essay_legal_problem = FeedbackCategories.objects.get(
            assessment_type = 'Essay / Legal Problem')
    online_test_court_report = FeedbackCategories.objects.get(
            assessment_type = 'Online Test / Court Report')
    negotiation_written = FeedbackCategories.objects.get(
            assessment_type = 'Negotiation / Written Submission')
    modules = Module.objects.all()
    for module in modules:
        if module.assessment_1_type:
            if module.assessment_1_type == essay:
                module.assessment_1_marksheet_type = 'ESSAY'
            elif module.assessment_1_type == legal_problem:
                module.assessment_1_marksheet_type = 'LEGAL_PROBLEM'
            elif module.assessment_1_type == oral_presentation:
                module.assessment_1_marksheet_type = 'PRESENTATION'
            elif module.assessment_1_type == essay_legal_problem:
                module.assessment_1_marksheet_type = 'ESSAY_LEGAL_PROBLEM'
            elif module.assessment_1_type == online_test_court_report:
                module.assessment_1_marksheet_type = 'ONLINE_TEST_COURT_REPORT'
            elif module.assessment_1_type == negotiation_written:
                module.assessment_1_marksheet_type = 'NEGOTIATION_WRITTEN'
        if module.assessment_2_type:
            if module.assessment_2_type == essay:
                module.assessment_2_marksheet_type = 'ESSAY'
            elif module.assessment_2_type == legal_problem:
                module.assessment_2_marksheet_type = 'LEGAL_PROBLEM'
            elif module.assessment_2_type == oral_presentation:
                module.assessment_2_marksheet_type = 'PRESENTATION'
            elif module.assessment_2_type == essay_legal_problem:
                module.assessment_2_marksheet_type = 'ESSAY_LEGAL_PROBLEM'
            elif module.assessment_2_type == online_test_court_report:
                module.assessment_2_marksheet_type = 'ONLINE_TEST_COURT_REPORT'
            elif module.assessment_2_type == negotiation_written:
                module.assessment_2_marksheet_type = 'NEGOTIATION_WRITTEN'
        if module.assessment_3_type:
            if module.assessment_3_type == essay:
                module.assessment_3_marksheet_type = 'ESSAY'
            elif module.assessment_3_type == legal_problem:
                module.assessment_3_marksheet_type = 'LEGAL_PROBLEM'
            elif module.assessment_3_type == oral_presentation:
                module.assessment_3_marksheet_type = 'PRESENTATION'
            elif module.assessment_3_type == essay_legal_problem:
                module.assessment_3_marksheet_type = 'ESSAY_LEGAL_PROBLEM'
            elif module.assessment_3_type == online_test_court_report:
                module.assessment_3_marksheet_type = 'ONLINE_TEST_COURT_REPORT'
            elif module.assessment_3_type == negotiation_written:
                module.assessment_3_marksheet_type = 'NEGOTIATION_WRITTEN'
        if module.assessment_4_type:
            if module.assessment_4_type == essay:
                module.assessment_4_marksheet_type = 'ESSAY'
            elif module.assessment_4_type == legal_problem:
                module.assessment_4_marksheet_type = 'LEGAL_PROBLEM'
            elif module.assessment_4_type == oral_presentation:
                module.assessment_4_marksheet_type = 'PRESENTATION'
            elif module.assessment_4_type == essay_legal_problem:
                module.assessment_4_marksheet_type = 'ESSAY_LEGAL_PROBLEM'
            elif module.assessment_4_type == online_test_court_report:
                module.assessment_4_marksheet_type = 'ONLINE_TEST_COURT_REPORT'
            elif module.assessment_4_type == negotiation_written:
                module.assessment_4_marksheet_type = 'NEGOTIATION_WRITTEN'
        if module.assessment_5_type:
            if module.assessment_5_type == essay:
                module.assessment_5_marksheet_type = 'ESSAY'
            elif module.assessment_5_type == legal_problem:
                module.assessment_5_marksheet_type = 'LEGAL_PROBLEM'
            elif module.assessment_5_type == oral_presentation:
                module.assessment_5_marksheet_type = 'PRESENTATION'
            elif module.assessment_5_type == essay_legal_problem:
                module.assessment_5_marksheet_type = 'ESSAY_LEGAL_PROBLEM'
            elif module.assessment_5_type == online_test_court_report:
                module.assessment_5_marksheet_type = 'ONLINE_TEST_COURT_REPORT'
            elif module.assessment_5_type == negotiation_written:
                module.assessment_5_marksheet_type = 'NEGOTIATION_WRITTEN'
        if module.assessment_6_type:
            if module.assessment_6_type == essay:
                module.assessment_6_marksheet_type = 'ESSAY'
            elif module.assessment_6_type == legal_problem:
                module.assessment_6_marksheet_type = 'LEGAL_PROBLEM'
            elif module.assessment_6_type == oral_presentation:
                module.assessment_6_marksheet_type = 'PRESENTATION'
            elif module.assessment_6_type == essay_legal_problem:
                module.assessment_6_marksheet_type = 'ESSAY_LEGAL_PROBLEM'
            elif module.assessment_6_type == online_test_court_report:
                module.assessment_6_marksheet_type = 'ONLINE_TEST_COURT_REPORT'
            elif module.assessment_6_type == negotiation_written:
                module.assessment_6_marksheet_type = 'NEGOTIATION_WRITTEN'
        module.save()

def check_group_marksheets():
    """Only checking for Negotiation / Written!"""
    marksheets = GroupMarksheet.objects.all()
    for marksheet in marksheets:
        completed = True
        if marksheet.category_mark_1_free is None:
            completed = False
        elif marksheet.category_mark_2_free is None:
            completed = False
        elif marksheet.category_mark_3_free is None:
            completed = False
        elif marksheet.category_mark_4_free is None:
            completed = False
        marksheet.completed = completed
        marksheet.save()


def check_marksheets():
    """Goes through all marksheets. RUN GROUP THING FIRST!"""
    marksheets = Marksheet.objects.all()
    for marksheet in marksheets:
        assessment = marksheet.assessment
        completed = True
        marksheet_type = marksheet.module.get_marksheet_type(
                marksheet.assessment)
        performance = Performance.objects.get(
                student = marksheet.student,
                module = marksheet.module
                )
        if marksheet_type == 'ESSAY':
            if performance.get_assessment_result(assessment) is None:
                completed = False
            elif marksheet.category_mark_1 is None:
                completed = False
            elif marksheet.category_mark_2 is None:
                completed = False
            elif marksheet.category_mark_3 is None:
                completed = False
            elif marksheet.category_mark_4 is None:
                completed = False
            elif marksheet.submission_date is None:
                completed = False
            elif marksheet.comments is None:
                completed = False
        elif marksheet_type == 'LEGAL_PROBLEM':
            if performance.get_assessment_result(assessment) is None:
                completed = False
            elif marksheet.category_mark_1 is None:
                completed = False
            elif marksheet.category_mark_2 is None:
                completed = False
            elif marksheet.category_mark_3 is None:
                completed = False
            elif marksheet.category_mark_4 is None:
                completed = False
            elif marksheet.submission_date is None:
                completed = False
            elif marksheet.comments is None:
                completed = False
        elif marksheet_type == 'PRESENTATION':
            if performance.get_assessment_result(assessment) is None:
                completed = False
            elif marksheet.category_mark_1 is None:
                completed = False
            elif marksheet.category_mark_2 is None:
                completed = False
            elif marksheet.category_mark_3 is None:
                completed = False
            elif marksheet.submission_date is None:
                completed = False
            elif marksheet.comments is None:
                completed = False
        elif marksheet_type == 'ESSAY_LEGAL_PROBLEM':
            if performance.get_assessment_result(assessment) is None:
                completed = False
            elif marksheet.category_mark_1 is None:
                completed = False
            elif marksheet.category_mark_2 is None:
                completed = False
            elif marksheet.category_mark_3 is None:
                completed = False
            elif marksheet.category_mark_4 is None:
                completed = False
            elif marksheet.category_mark_5 is None:
                completed = False
            elif marksheet.category_mark_6 is None:
                completed = False
            elif marksheet.category_mark_7 is None:
                completed = False
            elif marksheet.category_mark_8 is None:
                completed = False
            elif marksheet.submission_date is None:
                completed = False
            elif marksheet.comments is None:
                completed = False
            elif marksheet.comments_2 is None:
                completed = False
            elif marksheet.part_1_mark is None:
                completed = False
            elif marksheet.part_2_mark is None:
                completed = False
        elif marksheet_type == 'ONLINE_TEST_COURT_REPORT':
            if performance.get_assessment_result(assessment) is None:
                completed = False
            elif marksheet.category_mark_1 is None:
                completed = False
            elif marksheet.category_mark_2 is None:
                completed = False
            elif marksheet.category_mark_3 is None:
                completed = False
            elif marksheet.category_mark_4 is None:
                completed = False
            elif marksheet.submission_date is None:
                completed = False
            elif marksheet.comments is None:
                completed = False
            elif marksheet.part_1_mark is None:
                completed = False
            elif marksheet.part_2_mark is None:
                completed = False
        elif marksheet_type == 'NEGOTIATION_WRITTEN':
            if performance.get_assessment_result(assessment) is None:
                completed = False
            elif marksheet.category_mark_1_free is None:
                completed = False
            elif marksheet.category_mark_2_free is None:
                completed = False
            elif marksheet.category_mark_3_free is None:
                completed = False
            elif marksheet.category_mark_4_free is None:
                completed = False
            group = performance.group_assessment_group 
            try:
                group_marksheet = GroupMarksheet.objects.get(
                        module = marksheet.module,
                        assessment = marksheet.assessment,
                        group_no = group
                        )
                if not group_marksheet.completed:
                    completed = False
            except:
                completed = False
        if not completed:
            print marksheet.student.student_id + marksheet.module.title
        marksheet.completed = completed
        marksheet.save()
