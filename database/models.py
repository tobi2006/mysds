from django.db import models
from django.contrib.auth.models import User
import datetime

ACADEMIC_YEARS = (
        (2009, '2009/10'),
        (2010, '2010/11'),
        (2011, '2011/12'),
        (2012, '2012/13'),
        (2013, '2013/14'),
        (2014, '2014/15'),
        (2015, '2015/16'),
        (2016, '2016/17'),
        (2017, '2017/18'),
        (2018, '2018/19'),
        (2019, '2019/20'),
        (2020, '2020/21'),
        (2021, '2021/22'),
        (2022, '2022/23'),
        (2023, '2023/24'),
        (2024, '2024/25'),
        (2025, '2025/26'),
        (2026, '2026/27'),
        (2027, '2027/28'),
        (2028, '2028/29'),
        (2029, '2029/30')
    )

class MetaData(models.Model):
    data_id = models.IntegerField(default = 1, unique = True)
    current_year = models.IntegerField(choices=ACADEMIC_YEARS)

class Course(models.Model):
    title = models.CharField(max_length = 50, unique=True)

    def __unicode__(self):
        return u'%s' % (self.title)

class Module(models.Model):
    ELIGIBLE = (
            ('1', 'Year 1 only'),
            ('2', 'Year 2 only'),
            ('3', 'Year 3 only'),
            ('123', 'All years'),
            ('12', 'Years 1 and 2'),
            ('23', 'Years 2 and 3')
        ) #With these kinds of strings, it should be possible to check "if 1 in eligible:"
    title = models.CharField(max_length = 50)
    code = models.CharField(max_length = 20)
    #Show next year as the default
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if month < 10:
        current_year = year
    else:
        current_year = year + 1
    year = models.IntegerField(choices=ACADEMIC_YEARS, default=current_year)
    is_qld = models.BooleanField(verbose_name="QLD Module")
    is_pg = models.BooleanField(verbose_name="Postgraduate Module")
    credits = models.IntegerField(default=20)
    eligible = models.CharField(
            max_length = 3,
            choices = ELIGIBLE,
            default = '123',
            verbose_name = "Which students can (or have to) take this module?"
        )
    # Add: instructor = USER??
    number_of_sessions = models.IntegerField(default=10, verbose_name = "Number of sessions with attendance record")
    sessions_recorded = models.IntegerField(blank=True, null=True, default=0)
    assessment_1_title = models.CharField(
            max_length = 30,
            verbose_name="Assessment 1: Name",
            blank=True,
            null=True
        )
    assessment_1_value = models.IntegerField(
            verbose_name="Assessment 1: Percentage",
            blank=True,
            null=True,
        )
    assessment_2_title = models.CharField(
            max_length = 30,
            verbose_name="Assessment 2: Name",
            blank=True,
            null=True
        )
    assessment_2_value = models.IntegerField(
            verbose_name="Assessment 2: Percentage",
            blank=True,
            null=True,
        )
    assessment_3_title = models.CharField(
            max_length = 30,
            verbose_name="Assessment 3: Name",
            blank=True,
            null=True
        )
    assessment_3_value = models.IntegerField(
            verbose_name="Assessment 3: Percentage",
            blank=True,
            null=True,
        )
    assessment_4_title = models.CharField(
            max_length = 30,
            verbose_name="Assessment 4: Name",
            blank=True,
            null=True
        )
    assessment_4_value = models.IntegerField(
            verbose_name="Assessment 4: Percentage",
            blank=True,
            null=True,
        )
    assessment_5_title = models.CharField(
            max_length = 30,
            verbose_name="Assessment 5: Name",
            blank=True,
            null=True
        )
    assessment_5_value = models.IntegerField(
            verbose_name="Assessment 5: Percentage",
            blank=True,
            null=True,
        )
    assessment_6_title = models.CharField(
            max_length = 30,
            verbose_name="Assessment 6: Name",
            blank=True,
            null=True
        )
    assessment_6_value = models.IntegerField(
            verbose_name="Assessment 6: Percentage",
            blank=True,
            null=True,
        )
    exam_value = models.IntegerField(verbose_name="Percentage value for the exam", default=60)

    def __unicode__(self):
        next_year = int(self.year) + 1
        return u'%s (%s/%s)' % (self.title, self.year, next_year)

    def get_absolute_url(self):
        return "/module/%s/%s" % (self.code, self.year)

    class Meta:
        unique_together = ('code', 'year')

class Student(models.Model):
    POSSIBLE_YEARS = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'), 
            (7, 'Masters'),
            (8, 'PhD'),
            (9, 'Alumni')
        )#Allowing for a 6 year Part time degree, Masters (7), PhD (8) and Alumni status (9)
    student_id = models.CharField(max_length = 15, unique = True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    since = models.IntegerField(choices=ACADEMIC_YEARS, blank=True, null=True) 
    year = models.IntegerField(choices=POSSIBLE_YEARS, blank=True, null=True)
    is_part_time = models.BooleanField(verbose_name = "Part Time")
    email = models.CharField(max_length = 50, blank=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    qld = models.BooleanField(verbose_name="QLD Status")
    tutor = models.ForeignKey(User, blank=True, null=True)
    modules = models.ManyToManyField(Module, blank=True)
    notes = models.TextField(blank=True)
    highlighted = models.BooleanField()
    active = models.BooleanField(default=True)
    lsp = models.TextField(blank=True)
    permanent_email = models.CharField(max_length = 50, blank=True)
    achieved_grade = models.CharField(editable=False, max_length=50, blank=True)
    address = models.TextField(blank=True, verbose_name="Term Time Address")
    phone_no = models.CharField(max_length=20)
    home_address = models.TextField(blank=True)
    nalp = models.BooleanField(verbose_name = "Paralegal Pathway")


    def __unicode__(self):
        return u'%s, %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return "/student/%s" % (self.student_id)

    class Meta:
        ordering = ['last_name', 'first_name', 'year']


class Performance(models.Model):
    student = models.ForeignKey(Student)
    module = models.ForeignKey(Module)
    seminar_group = models.IntegerField(blank=True, null=True)
    assessment_1 = models.IntegerField(blank=True, null=True)
    assessment_2 = models.IntegerField(blank=True, null=True)
    assessment_3 = models.IntegerField(blank=True, null=True)
    assessment_4 = models.IntegerField(blank=True, null=True)
    assessment_5 = models.IntegerField(blank=True, null=True)
    assessment_6 = models.IntegerField(blank=True, null=True)
    exam = models.IntegerField(blank=True, null=True)
    # Resit Marks
    r_assessment_1 = models.IntegerField(blank=True, null=True)
    r_assessment_2 = models.IntegerField(blank=True, null=True)
    r_assessment_3 = models.IntegerField(blank=True, null=True)
    r_assessment_4 = models.IntegerField(blank=True, null=True)
    r_assessment_5 = models.IntegerField(blank=True, null=True)
    r_assessment_6 = models.IntegerField(blank=True, null=True)
    r_exam = models.IntegerField(blank=True, null=True)
    # Sit means the average is not capped
    assessment_1_is_sit = models.BooleanField()
    assessment_2_is_sit = models.BooleanField()
    assessment_3_is_sit = models.BooleanField()
    assessment_4_is_sit = models.BooleanField()
    assessment_5_is_sit = models.BooleanField()
    assessment_6_is_sit = models.BooleanField()
    exam_is_sit = models.BooleanField()
    # QLD Resit Marks
    q_assessment_1 = models.IntegerField(blank=True, null=True)
    q_assessment_2 = models.IntegerField(blank=True, null=True)
    q_assessment_3 = models.IntegerField(blank=True, null=True)
    q_assessment_4 = models.IntegerField(blank=True, null=True)
    q_assessment_5 = models.IntegerField(blank=True, null=True)
    q_assessment_6 = models.IntegerField(blank=True, null=True)
    q_exam = models.IntegerField(blank=True, null=True)

    average = models.IntegerField(blank=True, null=True)

    attendance = models.CharField(max_length=50, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'module')

    def initial_save(self):
        """ Sets the initial attendance string based on the number of sessions in the module """
        counter = 0
        initial_attendance = ""
        while counter < self.module.number_of_sessions:
            initial_attendance = initial_attendance + "0"
            counter += 1
        self.attendance = initial_attendance
        self.save()

    def save_with_avg(self):
        sum = 0
        if self.q_assessment_1: # Take the last resit mark for the average
            value = self.q_assessment_1 * self.module.assessment_1_value
            sum = sum + value
        elif self.r_assessment_1:
            value = self.r_assessment_1 * self.module.assessment_1_value
            sum = sum + value
        elif self.assessment_1:
            value = self.assessment_1 * self.module.assessment_1_value
            sum = sum + value
        if self.q_assessment_2:
            value = self.q_assessment_2 * self.module.assessment_2_value
            sum = sum + value
        elif self.r_assessment_2:
            value = self.r_assessment_2 * self.module.assessment_2_value
            sum = sum + value
        elif self.assessment_2:
            value = self.assessment_2 * self.module.assessment_2_value
            sum = sum + value
        if self.q_assessment_3:
            value = self.q_assessment_3 * self.module.assessment_3_value
            sum = sum + value
        elif self.r_assessment_3:
            value = self.r_assessment_3 * self.module.assessment_3_value
            sum = sum + value
        elif self.assessment_3:
            value = self.assessment_3 * self.module.assessment_3_value
            sum = sum + value
        if self.q_assessment_4:
            value = self.q_assessment_4 * self.module.assessment_4_value
            sum = sum + value
        elif self.r_assessment_4:
            value = self.r_assessment_4 * self.module.assessment_4_value
            sum = sum + value
        elif self.assessment_4:
            value = self.assessment_4 * self.module.assessment_4_value
            sum = sum + value
        if self.q_assessment_5:
            value = self.q_assessment_5 * self.module.assessment_5_value
            sum = sum + value
        elif self.r_assessment_5:
            value = self.r_assessment_5 * self.module.assessment_5_value
            sum = sum + value
        elif self.assessment_5:
            value = self.assessment_5 * self.module.assessment_5_value
            sum = sum + value
        if self.q_assessment_6:
            value = self.q_assessment_6 * self.module.assessment_6_value
            sum = sum + value
        elif self.r_assessment_6:
            value = self.r_assessment_6 * self.module.assessment_6_value
            sum = sum + value
        elif self.assessment_6:
            value = self.assessment_6 * self.module.assessment_6_value
            sum = sum + value
        if self.q_exam:
            value = self.q_exam * self.module.exam_value
            sum = sum + value
        elif self.r_exam:
            value = self.r_exam * self.module.exam_value
            sum = sum + value
        elif self.exam:
            value = self.exam * self.module.exam_value
            sum = sum + value
        average = float(sum) / 100
        rounded = round(average)
        self.average = int(rounded)
        self.save()
