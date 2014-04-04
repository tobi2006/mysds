from django.db import models
from database.models import Module, Student

from django.contrib.auth.models import User

class Marksheet(models.Model):
    MARKS = (
            (39, '0 - 39 %'),
            (49, '40 - 49 %'),
            (59, '50 - 59 %'),
            (69, '60 - 69 %'),
            (79, '70 - 79 %'),
            (80, '80 or more')
            )
    ASSESSMENTS = (
            [(i, 'Assessment ' + str(i)) for i in range(1, 7)]
            )
    module = models.ForeignKey(Module)
    student = models.ForeignKey(Student)
    assessment =  models.IntegerField(choices=ASSESSMENTS)
    marker = models.ForeignKey(User, limit_choices_to={'groups__name': 'teachers'}, blank=True, null=True, related_name="marker")
    second_first_marker = models.ForeignKey(User, limit_choices_to={'groups__name': 'teachers'}, blank=True, null=True, related_name="second_first_marker")
    second_marker = models.ForeignKey(User, limit_choices_to={'groups__name': 'teachers'}, blank=True, null=True, related_name="second_marker")
    marking_date = models.DateField(blank=True, null=True)
    category_mark_1 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_2 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_3 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_4 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_5 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_6 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_7 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_8 = models.IntegerField(choices=MARKS, blank=True, null=True)
    part_1_mark = models.IntegerField(blank=True, null=True)
    part_2_mark = models.IntegerField(blank=True, null=True)
    submission_date = models.DateField()
    comments = models.TextField(blank=True)
    comments_2 = models.TextField(blank=True)
    # Stuff for group marking
    other_group_members = models.ManyToManyField(Student, blank=True, null=True, related_name='group_marked_in')
    group_component_mark = models.IntegerField(blank=True, null=True)
    individual_component_mark = models.IntegerField(blank=True, null=True)
    group_feedback = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'module', 'assessment')

class FeedbackCategories(models.Model):
    ASSESSMENT_TYPES = (
            ('essay', 'Essay'),
            ('presentation', 'Oral Presentation'),
            ('group_presentation', 'Group_presentation'),
            ('legal_problem', 'Legal Problem'),
            ('essay_legal_problem', 'Essay / Legal Problem')
            )
    assessment_type = models.CharField(
            max_length = 30,
            unique = True
            )
    category_1 = models.CharField(max_length = 100, blank=True)
    category_1_helptext = models.TextField(blank=True)
    category_2 = models.CharField(max_length = 100, blank=True)
    category_2_helptext = models.TextField(blank=True)
    category_3 = models.CharField(max_length = 100, blank=True)
    category_3_helptext = models.TextField(blank=True)
    category_4 = models.CharField(max_length = 100, blank=True)
    category_4_helptext = models.TextField(blank=True)
    category_5 = models.CharField(max_length = 100, blank=True)
    category_5_helptext = models.TextField(blank=True)
    category_6 = models.CharField(max_length = 100, blank=True)
    category_6_helptext = models.TextField(blank=True)
    category_7 = models.CharField(max_length = 100, blank=True)
    category_7_helptext = models.TextField(blank=True)
    category_8 = models.CharField(max_length = 100, blank=True)
    category_8_helptext = models.TextField(blank=True)
    group_component = models.BooleanField()
    individual_weight = models.IntegerField(null=True, blank=True)
    group_weight = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.assessment_type
