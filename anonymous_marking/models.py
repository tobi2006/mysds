from django.db import models
from django.contrib.auth.models import User
import datetime
from database.models import *

class AnonymousMarks(models.Model):
    module = models.ForeignKey(Module)
    exam_id = models.CharField(max_length = 15)
    assessment_1 = models.IntegerField(blank=True, null=True)
    assessment_2 = models.IntegerField(blank=True, null=True)
    assessment_3 = models.IntegerField(blank=True, null=True)
    assessment_4 = models.IntegerField(blank=True, null=True)
    assessment_5 = models.IntegerField(blank=True, null=True)
    assessment_6 = models.IntegerField(blank=True, null=True)
    exam = models.IntegerField(blank=True, null=True)
    r_assessment_1 = models.IntegerField(blank=True, null=True)
    r_assessment_2 = models.IntegerField(blank=True, null=True)
    r_assessment_3 = models.IntegerField(blank=True, null=True)
    r_assessment_4 = models.IntegerField(blank=True, null=True)
    r_assessment_5 = models.IntegerField(blank=True, null=True)
    r_assessment_6 = models.IntegerField(blank=True, null=True)
    r_exam = models.IntegerField(blank=True, null=True)
    q_assessment_1 = models.IntegerField(blank=True, null=True)
    q_assessment_2 = models.IntegerField(blank=True, null=True)
    q_assessment_3 = models.IntegerField(blank=True, null=True)
    q_assessment_4 = models.IntegerField(blank=True, null=True)
    q_assessment_5 = models.IntegerField(blank=True, null=True)
    q_assessment_6 = models.IntegerField(blank=True, null=True)
    q_exam = models.IntegerField(blank=True, null=True)
    assessment_1_modified = models.DateTimeField(blank=True, null=True)
    assessment_2_modified = models.DateTimeField(blank=True, null=True)
    assessment_3_modified = models.DateTimeField(blank=True, null=True)
    assessment_4_modified = models.DateTimeField(blank=True, null=True)
    assessment_5_modified = models.DateTimeField(blank=True, null=True)
    assessment_6_modified = models.DateTimeField(blank=True, null=True)
    exam_modified = models.DateTimeField(blank=True, null=True)
    r_assessment_1_modified = models.DateTimeField(blank=True, null=True)
    r_assessment_2_modified = models.DateTimeField(blank=True, null=True)
    r_assessment_3_modified = models.DateTimeField(blank=True, null=True)
    r_assessment_4_modified = models.DateTimeField(blank=True, null=True)
    r_assessment_5_modified = models.DateTimeField(blank=True, null=True)
    r_assessment_6_modified = models.DateTimeField(blank=True, null=True)
    r_exam_modified = models.DateTimeField(blank=True, null=True)
    q_assessment_1_modified = models.DateTimeField(blank=True, null=True)
    q_assessment_2_modified = models.DateTimeField(blank=True, null=True)
    q_assessment_3_modified = models.DateTimeField(blank=True, null=True)
    q_assessment_4_modified = models.DateTimeField(blank=True, null=True)
    q_assessment_5_modified = models.DateTimeField(blank=True, null=True)
    q_assessment_6_modified = models.DateTimeField(blank=True, null=True)
    q_exam_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('module', 'exam_id')
