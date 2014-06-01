from django.db import models
from django.contrib.auth.models import User
import datetime
# from database.models import *
from database.models import Module


class AnonymousMarks(models.Model):
    module = models.ForeignKey(Module)
    exam_id = models.CharField(max_length=15)
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
        ordering = ['module', 'exam_id']

    def get_assessment_result(self, assessment, r=False, q=False):
        number = str(assessment)
        if r:
            if number == '1':
                returnvalue = self.r_assessment_1
            elif number == '2':
                returnvalue = self.r_assessment_2
            elif number == '3':
                returnvalue = self.r_assessment_3
            elif number == '4':
                returnvalue = self.r_assessment_4
            elif number == '5':
                returnvalue = self.r_assessment_5
            elif number == '6':
                returnvalue = self.r_assessment_6
            elif number == 'exam':
                returnvalue = self.r_exam
        elif q:
            if number == '1':
                returnvalue = self.q_assessment_1
            elif number == '2':
                returnvalue = self.q_assessment_2
            elif number == '3':
                returnvalue = self.q_assessment_3
            elif number == '4':
                returnvalue = self.q_assessment_4
            elif number == '5':
                returnvalue = self.q_assessment_5
            elif number == '6':
                returnvalue = self.q_assessment_6
            elif number == 'exam':
                returnvalue = self.q_exam
        else:
            if number == '1':
                returnvalue = self.assessment_1
            elif number == '2':
                returnvalue = self.assessment_2
            elif number == '3':
                returnvalue = self.assessment_3
            elif number == '4':
                returnvalue = self.assessment_4
            elif number == '5':
                returnvalue = self.assessment_5
            elif number == '6':
                returnvalue = self.assessment_6
            elif number == 'exam':
                returnvalue = self.exam
        return returnvalue

    def get_assessment_modified(self, assessment, r=False, q=False):
        number = str(assessment)
        if r:
            if number == '1':
                returnvalue = self.r_assessment_1_modified
            elif number == '2':
                returnvalue = self.r_assessment_2_modified
            elif number == '3':
                returnvalue = self.r_assessment_3_modified
            elif number == '4':
                returnvalue = self.r_assessment_4_modified
            elif number == '5':
                returnvalue = self.r_assessment_5_modified
            elif number == '6':
                returnvalue = self.r_assessment_6_modified
            elif number == 'exam':
                returnvalue = self.r_exam_modified
        elif q:
            if number == '1':
                returnvalue = self.q_assessment_1_modified
            elif number == '2':
                returnvalue = self.q_assessment_2_modified
            elif number == '3':
                returnvalue = self.q_assessment_3_modified
            elif number == '4':
                returnvalue = self.q_assessment_4_modified
            elif number == '5':
                returnvalue = self.q_assessment_5_modified
            elif number == '6':
                returnvalue = self.q_assessment_6_modified
            elif number == 'exam':
                returnvalue = self.q_exam_modified
        else:
            if number == '1':
                returnvalue = self.assessment_1_modified
            elif number == '2':
                returnvalue = self.assessment_2_modified
            elif number == '3':
                returnvalue = self.assessment_3_modified
            elif number == '4':
                returnvalue = self.assessment_4_modified
            elif number == '5':
                returnvalue = self.assessment_5_modified
            elif number == '6':
                returnvalue = self.assessment_6_modified
            elif number == 'exam':
                returnvalue = self.exam_modified
        return returnvalue

    def set_assessment_result(
            self, assessment, mark, timestamp=False, r=False, q=False):
        number = str(assessment)
        safe_mark = int(mark)
        print str(number) + ": " + str(safe_mark)
        if not timestamp:
            timestamp = datetime.datetime.now()
        if r:
            if number == '1':
                self.r_assessment_1 = safe_mark
                self.r_assessment_1_modified = timestamp
            elif number == '2':
                self.r_assessment_2 = safe_mark
                self.r_assessment_2_modified = timestamp
            elif number == '3':
                self.r_assessment_3 = safe_mark
                self.r_assessment_3_modified = timestamp
            elif number == '4':
                self.r_assessment_4 = safe_mark
                self.r_assessment_4_modified = timestamp
            elif number == '5':
                self.r_assessment_5 = safe_mark
                self.r_assessment_5_modified = timestamp
            elif number == '6':
                self.r_assessment_6 = safe_mark
                self.r_assessment_6_modified = timestamp
            elif number == 'exam':
                self.r_exam = safe_mark
                self.r_exam_modified = timestamp
        elif q:
            if number == '1':
                self.q_assessment_1 = safe_mark
                self.q_assessment_1_modified = timestamp
            elif number == '2':
                self.q_assessment_2 = safe_mark
                self.q_assessment_2_modified = timestamp
            elif number == '3':
                self.q_assessment_3 = safe_mark
                self.q_assessment_3_modified = timestamp
            elif number == '4':
                self.q_assessment_4 = safe_mark
                self.q_assessment_4_modified = timestamp
            elif number == '5':
                self.q_assessment_5 = safe_mark
                self.q_assessment_5_modified = timestamp
            elif number == '6':
                self.q_assessment_6 = safe_mark
                self.q_assessment_6_modified = timestamp
            elif number == 'exam':
                self.q_exam = safe_mark
                self.q_exam_modified = timestamp
        else:
            if number == '1':
                self.assessment_1 = safe_mark
                self.assessment_1_modified = timestamp
            elif number == '2':
                self.assessment_2 = safe_mark
                self.assessment_2_modified = timestamp
            elif number == '3':
                self.assessment_3 = safe_mark
                self.assessment_3_modified = timestamp
            elif number == '4':
                self.assessment_4 = safe_mark
                self.assessment_4_modified = timestamp
            elif number == '5':
                self.assessment_5 = safe_mark
                self.assessment_5_modified = timestamp
            elif number == '6':
                self.assessment_6 = safe_mark
                self.assessment_6_modified = timestamp
            elif number == 'exam':
                self.exam = safe_mark
                self.exam_modified = timestamp
        self.save()
        return
