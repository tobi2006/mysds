from django.db import models
from database.models import Module, Student

from django.contrib.auth.models import User

class Marksheet(models.Model):
    """The model for a marksheet for an individual performance.

    Make sure to implement setting complete = True in the functions,
    otherwise there will be a warning sign next to the download
    icon in the module view.
    """
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
    completed = models.BooleanField(blank=True, default=False)
    marker = models.ForeignKey(
            User, limit_choices_to={'groups__name': 'teachers'},
            blank=True, null=True, related_name="marker"
            )
    second_first_marker = models.ForeignKey(
            User, limit_choices_to={'groups__name': 'teachers'},
            blank=True, null=True, related_name="second_first_marker"
            )
    second_marker = models.ForeignKey(
            User, limit_choices_to={'groups__name': 'teachers'},
            blank=True, null=True, related_name="second_marker"
            )
    marking_date = models.DateField(blank=True, null=True)
    category_mark_1 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_2 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_3 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_4 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_5 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_6 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_7 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_8 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_1_free = models.IntegerField(blank=True, null=True)
    category_mark_2_free = models.IntegerField(blank=True, null=True)
    category_mark_3_free = models.IntegerField(blank=True, null=True)
    category_mark_4_free = models.IntegerField(blank=True, null=True)
    category_mark_5_free = models.IntegerField(blank=True, null=True)
    category_mark_6_free = models.IntegerField(blank=True, null=True)
    category_mark_7_free = models.IntegerField(blank=True, null=True)
    category_mark_8_free = models.IntegerField(blank=True, null=True)
    deduction = models.IntegerField(blank=True, null=True)
    deduction_explanation = models.TextField(blank=True)
    part_1_mark = models.IntegerField(blank=True, null=True)
    part_2_mark = models.IntegerField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True)
    comments_2 = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'module', 'assessment')

class GroupMarksheet(models.Model):
    """The model for a marksheet for a group performance.

    Make sure to implement setting complete = True in the functions,
    otherwise the Download Marksheet symbol will not be displayed
    in the module view. You could call the test() function for this,
    but it might be easier to do this when validating the form.
    """
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
    assessment =  models.IntegerField(choices=ASSESSMENTS)
    completed = models.BooleanField(blank=True, default=False)
    group_no = models.IntegerField()
    category_mark_1 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_2 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_3 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_4 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_5 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_6 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_7 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_8 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_1_free = models.IntegerField(blank=True, null=True)
    category_mark_2_free = models.IntegerField(blank=True, null=True)
    category_mark_3_free = models.IntegerField(blank=True, null=True)
    category_mark_4_free = models.IntegerField(blank=True, null=True)
    category_mark_5_free = models.IntegerField(blank=True, null=True)
    category_mark_6_free = models.IntegerField(blank=True, null=True)
    category_mark_7_free = models.IntegerField(blank=True, null=True)
    category_mark_8_free = models.IntegerField(blank=True, null=True)
    group_comments = models.TextField(blank=True)
    group_comments_2 = models.TextField(blank=True)
    submission_date = models.DateField(blank=True, null=True)
    marker = models.ForeignKey(
            User, limit_choices_to={'groups__name': 'teachers'},
            blank=True, null=True, related_name="marker-groupwork")
    second_first_marker = models.ForeignKey(
            User, limit_choices_to={'groups__name': 'teachers'}, blank=True,
            null=True, related_name="second_first_marker-groupwork")
    second_marker = models.ForeignKey(
            User, limit_choices_to={'groups__name': 'teachers'}, blank=True,
            null=True, related_name="second_marker-groupwork")
    marking_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('module', 'assessment', 'group_no')


class FeedbackCategories(models.Model):
    """ This model represents the different types of marksheets.

    Hopefully, this will be obsolete soon.
    """
    assessment_type = models.CharField(
            max_length = 60,
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
    group_category_1 = models.CharField(max_length = 100, blank=True)
    group_category_1_helptext = models.TextField(blank=True)
    group_category_2 = models.CharField(max_length = 100, blank=True)
    group_category_2_helptext = models.TextField(blank=True)
    group_category_3 = models.CharField(max_length = 100, blank=True)
    group_category_3_helptext = models.TextField(blank=True)
    group_category_4 = models.CharField(max_length = 100, blank=True)
    group_category_4_helptext = models.TextField(blank=True)
    group_category_5 = models.CharField(max_length = 100, blank=True)
    group_category_5_helptext = models.TextField(blank=True)
    group_category_6 = models.CharField(max_length = 100, blank=True)
    group_category_6_helptext = models.TextField(blank=True)
    group_category_7 = models.CharField(max_length = 100, blank=True)
    group_category_7_helptext = models.TextField(blank=True)
    group_category_8 = models.CharField(max_length = 100, blank=True)
    group_category_8_helptext = models.TextField(blank=True)

    def __unicode__(self):
        return self.assessment_type
