from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
from feedback.categories import AVAILABLE_MARKSHEETS

DEGREES = (
    (1, 'First'),
    (21, '2:1'),
    (22, '2:2'),
    (3, 'Third'),
    (4, 'Fail')
    )

ACADEMIC_YEARS = (
    [(i, str(i) + "/" + str(i+1)) for i in range(2009, 2025)]
    )

TEACHING_WEEKS = (
    [(i, 'Week ' + str(i)) for i in range(1, 53)]
    )

POSSIBLE_YEARS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (7, 'Masters'),
    (8, 'PhD'),
    (9, 'Alumni')
    )


def this_year():
    """Check which academic year we are in"""
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if month < 9:
        current_year = year - 1
    else:
        current_year = year
    return current_year


class MetaData(models.Model):
    """Simple, but ugly hack to make an easily changeable Year"""
    data_id = models.IntegerField(default=1, unique=True)
    current_year = models.IntegerField(choices=ACADEMIC_YEARS)

    def academic_year_string(self):
        next_year = str(self.current_year + 1)
        result = str(self.current_year) + '/' + next_year[-2:]
        return result


class Course(models.Model):
    """Just the courses (LLB / LLB with Sociology / etc"""
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Official Course Title")


###########################################################COMMENT

    short_title = models.CharField(max_length = 30,
           blank=True, null=True, verbose_name="Short Title", default="")
    is_pg = models.BooleanField(
       verbose_name="Postgraduate Course",
       default=False
       )

#ENDCOMMENT#########################################################

    def __unicode__(self):
        return u'%s' % (self.title)
#    all_years = models.BooleanField(verbose_name=
#           "Course extends over all years (for example Erasmus)")



class Module(models.Model):
    """The class representing a module"""
    ELIGIBLE = (
        ('1', 'Year 1 only'),
        ('2', 'Year 2 only'),
        ('3', 'Year 3 only'),
        ('123', 'All years'),
        ('12', 'Years 1 and 2'),
        ('23', 'Years 2 and 3')
        )  # With these kinds of strings, we can check "if '1' in eligible:"
    CREDITS = (
        (20, '20'),
        (40, '40')
        )
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    instructors = models.ManyToManyField(
        User,
        limit_choices_to={'groups__name': 'teachers'},
        blank=True,
        null=True
        )
    current_year = this_year()
    year = models.IntegerField(choices=ACADEMIC_YEARS, default=current_year)
    successor_of = models.ForeignKey('self', blank=True, null=True)
    is_foundational = models.BooleanField(verbose_name="Foundational Module")
    is_pg = models.BooleanField(verbose_name="Postgraduate Module")
    is_nalp = models.BooleanField(
        verbose_name="Module is required for the NALP Qualification")
    credits = models.IntegerField(default=20, choices=CREDITS)
    eligible = models.CharField(
        max_length=3,
        choices=ELIGIBLE,
        default='1',
        verbose_name="Which students can (or have to) take this module?"
        )
    first_session = models.IntegerField(
        default=5,
        verbose_name="Week of first seminar",
        choices=TEACHING_WEEKS
        )
    no_teaching_in = models.CharField(max_length=100, blank=True)
    last_session = models.IntegerField(
        default=15,
        verbose_name="Week of last seminar",
        choices=TEACHING_WEEKS
        )
    sessions_recorded = models.IntegerField(blank=True, null=True, default=0)
    assessment_1_title = models.CharField(
        max_length=100,
        verbose_name="Assessment 1: Name",
        blank=True,
        null=True
        )
    assessment_1_value = models.IntegerField(
        verbose_name="Assessment 1: Percentage",
        blank=True,
        null=True,
        )
    assessment_1_type = models.ForeignKey(
        'feedback.FeedbackCategories',
        blank=True,
        null=True,
        related_name="assessment_1"
        )
    assessment_1_marksheet_type = models.CharField(
        max_length=50,
        verbose_name="Marksheet Type",
        blank=True,
        null=True,
        choices=AVAILABLE_MARKSHEETS
        )
    assessment_1_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback"
        )
    assessment_1_submission_date = models.DateField(blank=True, null=True)
    assessment_1_max_word_count = models.IntegerField(blank=True, null=True)
    assessment_2_title = models.CharField(
        max_length=100,
        verbose_name="Assessment 2: Name",
        blank=True,
        null=True
        )
    assessment_2_value = models.IntegerField(
        verbose_name="Assessment 2: Percentage",
        blank=True,
        null=True,
        )
    assessment_2_type = models.ForeignKey(
        'feedback.FeedbackCategories',
        blank=True,
        null=True,
        related_name="assessment_2"
        )
    assessment_2_marksheet_type = models.CharField(
        max_length=50,
        verbose_name="Marksheet Type",
        blank=True,
        null=True,
        choices=AVAILABLE_MARKSHEETS
        )
    assessment_2_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback")
    assessment_2_submission_date = models.DateField(blank=True, null=True)
    assessment_2_max_word_count = models.IntegerField(blank=True, null=True)
    assessment_3_title = models.CharField(
        max_length=100,
        verbose_name="Assessment 3: Name",
        blank=True,
        null=True
        )
    assessment_3_value = models.IntegerField(
        verbose_name="Assessment 3: Percentage",
        blank=True,
        null=True,
        )
    assessment_3_type = models.ForeignKey(
        'feedback.FeedbackCategories',
        blank=True,
        null=True,
        related_name="assessment_3"
        )
    assessment_3_marksheet_type = models.CharField(
        max_length=50,
        verbose_name="Marksheet Type",
        blank=True,
        null=True,
        choices=AVAILABLE_MARKSHEETS
        )
    assessment_3_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback")
    assessment_3_submission_date = models.DateField(blank=True, null=True)
    assessment_3_max_word_count = models.IntegerField(blank=True, null=True)
    assessment_4_title = models.CharField(
        max_length=100,
        verbose_name="Assessment 4: Name",
        blank=True,
        null=True
        )
    assessment_4_value = models.IntegerField(
        verbose_name="Assessment 4: Percentage",
        blank=True,
        null=True,
        )
    assessment_4_type = models.ForeignKey(
        'feedback.FeedbackCategories',
        blank=True,
        null=True,
        related_name="assessment_4"
        )
    assessment_4_marksheet_type = models.CharField(
        max_length=50,
        verbose_name="Marksheet Type",
        blank=True,
        null=True,
        choices=AVAILABLE_MARKSHEETS
        )
    assessment_4_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback")
    assessment_4_submission_date = models.DateField(blank=True, null=True)
    assessment_4_max_word_count = models.IntegerField(blank=True, null=True)
    assessment_5_title = models.CharField(
        max_length=100,
        verbose_name="Assessment 5: Name",
        blank=True,
        null=True
        )
    assessment_5_value = models.IntegerField(
        verbose_name="Assessment 5: Percentage",
        blank=True,
        null=True,
        )
    assessment_5_type = models.ForeignKey(
        'feedback.FeedbackCategories',
        blank=True,
        null=True,
        related_name="assessment_5"
        )
    assessment_5_marksheet_type = models.CharField(
        max_length=50,
        verbose_name="Marksheet Type",
        blank=True,
        null=True,
        choices=AVAILABLE_MARKSHEETS
        )
    assessment_5_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback")
    assessment_5_submission_date = models.DateField(blank=True, null=True)
    assessment_5_max_word_count = models.IntegerField(blank=True, null=True)
    assessment_6_title = models.CharField(
        max_length=100,
        verbose_name="Assessment 6: Name",
        blank=True,
        null=True
        )
    assessment_6_value = models.IntegerField(
        verbose_name="Assessment 6: Percentage",
        blank=True,
        null=True,
        )
    assessment_6_type = models.ForeignKey(
        'feedback.FeedbackCategories',
        blank=True,
        null=True,
        related_name="assessment_6"
        )
    assessment_6_marksheet_type = models.CharField(
        max_length=50,
        verbose_name="Marksheet Type",
        blank=True,
        null=True,
        choices=AVAILABLE_MARKSHEETS
        )
    assessment_6_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback")
    assessment_6_submission_date = models.DateField(blank=True, null=True)
    assessment_6_max_word_count = models.IntegerField(blank=True, null=True)
    exam_value = models.IntegerField(
        verbose_name="Percentage value for the exam",
        default=60,
        blank=True,
        null=True
        )
    exam_available = models.BooleanField(
        verbose_name="Students can see the exam mark",
        blank=True,
        default=False
        )

    def __unicode__(self):
        next_year = int(self.year) + 1
        return u'%s (%s/%s)' % (self.title, self.year, next_year)

    def clean(self):
        self.code = self.code.strip()

    def get_number_of_sessions(self):
        number_of_sessions = self.last_session - self.first_session
        number_of_sessions += 1
        if self.no_teaching_in != "":
            no_t_in = self.no_teaching_in.strip()  # Remove trailing Commas
            if no_t_in[-1] == ",":
                no_t_in = no_t_in[:-1]
            number_of_sessions -= len(no_t_in.split(","))
        return number_of_sessions

    def get_assessment_title(self, assessment):
        assessment = str(assessment)
        if assessment == '1':
            returnvalue = self.assessment_1_title
        elif assessment == '2':
            returnvalue = self.assessment_2_title
        elif assessment == '3':
            returnvalue = self.assessment_3_title
        elif assessment == '4':
            returnvalue = self.assessment_4_title
        elif assessment == '5':
            returnvalue = self.assessment_5_title
        elif assessment == '6':
            returnvalue = self.assessment_6_title
        elif assessment == 'exam':
            returnvalue = 'Exam'
        return returnvalue

    def get_assessment_value(self, assessment):
        assessment = str(assessment)
        if assessment == '1':
            returnvalue = self.assessment_1_value
        elif assessment == '2':
            returnvalue = self.assessment_2_value
        elif assessment == '3':
            returnvalue = self.assessment_3_value
        elif assessment == '4':
            returnvalue = self.assessment_4_value
        elif assessment == '5':
            returnvalue = self.assessment_5_value
        elif assessment == '6':
            returnvalue = self.assessment_6_value
        elif assessment == 'exam':
            returnvalue = self.exam_value
        return returnvalue

    def get_assessment_type(self, assessment):
        assessment = str(assessment)
        if assessment == '1':
            returnvalue = self.assessment_1_type
        elif assessment == '2':
            returnvalue = self.assessment_2_type
        elif assessment == '3':
            returnvalue = self.assessment_3_type
        elif assessment == '4':
            returnvalue = self.assessment_4_type
        elif assessment == '5':
            returnvalue = self.assessment_5_type
        elif assessment == '6':
            returnvalue = self.assessment_6_type
        else:
            returnvalue = 'Exam'
        return returnvalue

    def get_marksheet_type(self, assessment):
        try:
            number = int(assessment)
        except ValueError:
            return False
        if number == 1:
            returnvalue = self.assessment_1_marksheet_type
        elif number == 2:
            returnvalue = self.assessment_2_marksheet_type
        elif number == 3:
            returnvalue = self.assessment_3_marksheet_type
        elif number == 4:
            returnvalue = self.assessment_4_marksheet_type
        elif number == 5:
            returnvalue = self.assessment_5_marksheet_type
        elif number == 6:
            returnvalue = self.assessment_6_marksheet_type
        return returnvalue

    def get_assessment_max_wordcount(self, assessment):
        number = int(assessment)
        if number == 1:
            returnvalue = self.assessment_1_max_word_count
        elif number == 2:
            returnvalue = self.assessment_2_max_word_count
        elif number == 3:
            returnvalue = self.assessment_3_max_word_count
        elif number == 4:
            returnvalue = self.assessment_4_max_word_count
        elif number == 5:
            returnvalue = self.assessment_5_max_word_count
        elif number == 6:
            returnvalue = self.assessment_6_max_word_count
        return returnvalue

    def get_assessment_submission_date(self, assessment):
        number = int(assessment)
        if number == 1:
            returnvalue = self.assessment_1_submission_date
        elif number == 2:
            returnvalue = self.assessment_2_submission_date
        elif number == 3:
            returnvalue = self.assessment_3_submission_date
        elif number == 4:
            returnvalue = self.assessment_4_submission_date
        elif number == 5:
            returnvalue = self.assessment_5_submission_date
        elif number == 6:
            returnvalue = self.assessment_6_submission_date
        return returnvalue

    def get_assessment_range(self):
        """Returns a list of all assessments"""
        assessment_range = []
        if self.assessment_1_title:
            assessment_range.append('1')
        if self.assessment_2_title:
            assessment_range.append('2')
        if self.assessment_3_title:
            assessment_range.append('3')
        if self.assessment_4_title:
            assessment_range.append('4')
        if self.assessment_5_title:
            assessment_range.append('5')
        if self.assessment_6_title:
            assessment_range.append('6')
        if self.exam_value:
            assessment_range.append('exam')
        return assessment_range

    def get_number_of_assessments(self):
        number = 0
        if self.assessment_1_title:
            number += 1
        if self.assessment_2_title:
            number += 1
        if self.assessment_3_title:
            number += 1
        if self.assessment_4_title:
            number += 1
        if self.assessment_5_title:
            number += 1
        if self.assessment_6_title:
            number += 1
        if self.exam_value:
            number += 1
        return number

    def get_absolute_url(self):
        return reverse('module_view', args=[self.code, str(self.year)])

    def get_edit_url(self):
        return reverse('edit_module', args=[self.code, str(self.year)])

    def get_mark_url(self):
        return reverse('mark_no', args=[self.code, str(self.year)])

    def get_anonymous_mark_url(self):
        return reverse('mark_anon', args=[self.code, str(self.year)])

    def get_de_anonymize_url(self):
        return reverse('de_anonymize_no', args=[self.code, str(self.year)])

    def get_attendance_url(self):
        return reverse('attendance_no', args=[self.code, str(self.year)])

    def get_seminar_groups_url(self):
        return reverse('seminar_groups', args=[self.code, str(self.year)])

    def get_assessment_groups_url(self):
        return reverse('assessment_groups', args=[self.code, str(self.year)])

    def get_add_students_url(self):
        return reverse(
            'add_students_to_module', args=[self.code, str(self.year)])

    def get_address_nines_url(self):
        return reverse('address_nines', args=[self.code, str(self.year)])

    def get_concessions_url(self):
        return reverse('concessions', args=[self.code, str(self.year)])

    def get_attendance_sheet_url(self):
        return reverse(
            'export_attendance_sheet', args=[self.code, str(self.year)])

    def get_sample_pack_url(self):
        return reverse(
            'sample_pack', args=[self.code, str(self.year)])

    def get_seminar_group_overview_url(self):
        return reverse(
            'seminar_group_overview', args=[self.code, str(self.year)])

    def get_remove_student_url(self):
        return reverse(
            'generic_remove_student_from_module',
            args=[self.code, str(self.year)]
            )

    def get_export_marks_url(self):
        return reverse('export_marks', args=[self.code, str(self.year)])

    def get_export_anonymous_marks_url(self):
        return reverse('export_anonymous_marks_no', args=[self.code, str(self.year)])

    def get_toggle_assessment_availability_url(self):
        return reverse('toggle_assessment', args=[self.code, str(self.year)])

    class Meta:
        unique_together = ('code', 'year')


class Student(models.Model):
    student_id = models.CharField(max_length=25, primary_key=True)
    exam_id = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True,
        default=None
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    belongs_to = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': 'students'},
        blank=True,
        null=True)
    since = models.IntegerField(choices=ACADEMIC_YEARS, blank=True, null=True)
    year = models.IntegerField(choices=POSSIBLE_YEARS, blank=True, null=True)
    is_part_time = models.BooleanField(verbose_name="Part Time")
    second_part_time_year = models.BooleanField()
    # This box has to be ticked when a part time student is in
    # the second half of a "year": student x might be in her second
    # year, but still takes year 1 modules for example
    email = models.CharField(max_length=100, blank=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    qld = models.BooleanField(verbose_name="QLD Status", default=True)
    tutor = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': 'teachers'},
        blank=True,
        null=True,
        related_name="tutee"
        )
    modules = models.ManyToManyField(Module, blank=True)
    notes = models.TextField(blank=True)
    highlighted = models.BooleanField()
    active = models.BooleanField(default=True)
    lsp = models.TextField(blank=True)
    permanent_email = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True, verbose_name="Term Time Address")
    phone_no = models.CharField(max_length=100, blank=True)
    home_address = models.TextField(blank=True)
    nalp = models.BooleanField(verbose_name="Paralegal Pathway")
    tier_4 = models.BooleanField(verbose_name="Tier 4 Student")
    achieved_degree = models.IntegerField(
        choices=DEGREES, blank=True, null=True)
    problems = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s, %s' % (self.last_name, self.first_name)

    def clean(self):
        self.student_id = self.student_id.strip()

    def get_absolute_url(self):
        return reverse('student_view', args=[self.student_id])

    def short_first_name(self):
        first_names = self.first_name.split(" ")
        return first_names[0]

    def short_name(self):
        name = self.last_name + ', ' + self.short_first_name()
        return name

    def get_edit_url(self):
        return reverse('edit_student', args=[self.student_id])

    def get_lsp_view_url(self):
        return reverse('lsp_view', args=[self.student_id])

    def get_lsp_edit_url(self):
        return reverse('lsp_edit', args=[self.student_id])

    def get_notes_edit_url(self):
        return reverse('notes_edit', args=[self.student_id])

    def html_address(self):
        address = self.address.replace("\n", "<br>")
        return address

    def html_home_address(self):
        address = self.home_address.replace("\n", "<br>")
        return address

    def year_1_average(self):
        performances = Performance.objects.filter(
            student=self, part_of_average=1)
        marks = []
        for performance in performances:
            if performance.module.credits == 20:
                marks.append(performance.real_average)
            elif performance.module.credits == 40:
                marks.append(performance.real_average)
                marks.append(performance.real_average)
        while len(marks) > 5:
            marks.remove(min(marks))
        all_marks = sum(marks)
        all_marks += 0.0
        average = all_marks / 5
        return average

    def year_2_average(self):
        performances = Performance.objects.filter(
            student=self, part_of_average=2)
        marks = []
        for performance in performances:
            if performance.module.credits == 20:
                marks.append(performance.real_average)
            elif performance.module.credits == 40:
                marks.append(performance.real_average)
                marks.append(performance.real_average)
        while len(marks) > 5:
            marks.remove(min(marks))
        all_marks = sum(marks)
        all_marks += 0.0
        average = all_marks / 5
        return average

    def year_3_average(self):
        performances = Performance.objects.filter(
            student=self, part_of_average=3)
        marks = []
        for performance in performances:
            if performance.module.credits == 20:
                marks.append(performance.real_average)
            elif performance.module.credits == 40:
                marks.append(performance.real_average)
                marks.append(performance.real_average)
        while len(marks) > 5:
            marks.remove(min(marks))
        all_marks = sum(marks)
        all_marks += 0.0
        average = all_marks / 5
        return average

    class Meta:
        ordering = ['last_name', 'first_name', 'year']


class Performance(models.Model):
    NO_CONCESSIONS='N'
    PENDING='P'
    GRANTED='G'
    CONCESSIONS = (
        (NO_CONCESSIONS, 'No concession'),
        (PENDING, 'Concession pending'),
        (GRANTED, 'Concession granted')
        )
    student = models.ForeignKey(Student)
    module = models.ForeignKey(Module)
    seminar_group = models.IntegerField(blank=True, null=True)
    group_assessment_group = models.IntegerField(blank=True, null=True)
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

###########################################################COMMENT

    assessment_1_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=1, 
        blank=True,
        null=True,
        default=NO_CONCESSIONS
        )
    assessment_2_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=2, 
        blank=True,
        null=True,
        default=NO_CONCESSIONS
        )
    assessment_3_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=2, 
        blank=True,
        null=True,
        default=NO_CONCESSIONS
        )
    assessment_4_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=2, 
        blank=True,
        null=True,
        default=NO_CONCESSIONS
        )
    assessment_5_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=2, 
        blank=True,
        null=True,
        default=NO_CONCESSIONS
        )
    assessment_6_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=2, 
        blank=True,
        null=True,
        default=NO_CONCESSIONS
        )
    exam_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=2, 
        blank=True,
        null=True,
        default=NO_CONCESSIONS
        )

#ENDCOMMENT##################################################

    # Sit means the average is not capped
    assessment_1_is_sit = models.BooleanField(default=False)
    assessment_2_is_sit = models.BooleanField(default=False)
    assessment_3_is_sit = models.BooleanField(default=False)
    assessment_4_is_sit = models.BooleanField(default=False)
    assessment_5_is_sit = models.BooleanField(default=False)
    assessment_6_is_sit = models.BooleanField(default=False)
    exam_is_sit = models.BooleanField(default=False)
    # QLD Resit Marks
    q_assessment_1 = models.IntegerField(blank=True, null=True)
    q_assessment_2 = models.IntegerField(blank=True, null=True)
    q_assessment_3 = models.IntegerField(blank=True, null=True)
    q_assessment_4 = models.IntegerField(blank=True, null=True)
    q_assessment_5 = models.IntegerField(blank=True, null=True)
    q_assessment_6 = models.IntegerField(blank=True, null=True)
    q_exam = models.IntegerField(blank=True, null=True)
    # Time Stamps for anonymous marking (comparing which is more recent)
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

    average = models.IntegerField(blank=True, null=True)
    real_average = models.FloatField(blank=True, null=True)
    part_of_average = models.IntegerField(blank=True, null=True)
    # Belongs to which year's avg

    attendance = models.CharField(max_length=50, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'module')
        ordering = ['module', 'student']

    def initial_save(self):
        """Sets the initial attendance string based on the number of sessions.

        Also sets the part_of_average variable, which is important for the
        student's average.
        """

        counter = 0
        initial_attendance = ""
        number_of_sessions = self.module.get_number_of_sessions()
        while counter < number_of_sessions:
            initial_attendance = initial_attendance + "0"
            counter += 1
        self.attendance = initial_attendance
        meta_stuff = MetaData.objects.get(data_id=1)
        current_year = meta_stuff.current_year
        distance_of_years = self.module.year - current_year
        self.part_of_average = self.student.year + distance_of_years
        self.save()

    def save_with_avg(self):
        sum = 0
        if self.q_assessment_1:  # Take the last resit mark for the average
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
        self.real_average = average
        self.save()

    def average_makes_sense(self):
        """Returns true if there are marks in all categories"""
        result = True
        if self.module.assessment_1_value:
            if self.assessment_1 is None:
                result = False
        if result:
            if self.module.assessment_2_value:
                if self.assessment_2 is None:
                    result = False
        if result:
            if self.module.assessment_3_value:
                if self.assessment_3 is None:
                    result = False
        if result:
            if self.module.assessment_4_value:
                if self.assessment_4 is None:
                    result = False
        if result:
            if self.module.assessment_5_value:
                if self.assessment_5 is None:
                    result = False
        if result:
            if self.module.assessment_6_value:
                if self.assessment_6 is None:
                    result = False
        if result:
            if self.module.exam_value:
                if self.exam is None:
                    result = False
        return result

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

    def get_concession(self, assessment):
        if assessment == '1':
            concession = self.assessment_1_concessions
        if assessment == '2':
            concession = self.assessment_2_concessions
        if assessment == '3':
            concession = self.assessment_3_concessions
        if assessment == '4':
            concession = self.assessment_4_concessions
        if assessment == '5':
            concession = self.assessment_5_concessions
        if assessment == '6':
            concession = self.assessment_6_concessions
        if assessment == 'exam':
            concession = self.exam_concessions
        return concession

    def set_concession(self, assessment, concession):
        if assessment == '1':
            self.assessment_1_concessions = concession
        if assessment == '2':
            self.assessment_2_concessions = concession
        if assessment == '3':
            self.assessment_3_concessions = concession
        if assessment == '4':
            self.assessment_4_concessions = concession
        if assessment == '5':
            self.assessment_5_concessions = concession
        if assessment == '6':
            self.assessment_6_concessions = concession
        if assessment == 'exam':
            self.exam_concessions = concession
        self.save()

    def set_assessment_result(
            self, assessment, mark, timestamp=False, r=False, q=False):
        number = str(assessment)
        safe_mark = int(mark)
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
        self.save_with_avg()
        return


class Tutee_Session(models.Model):
    tutee = models.ForeignKey(Student)
    tutor = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': 'teachers'}
        )
    date_of_meet = models.DateField()
    notes = models.TextField()

    class Meta:
        ordering = ['date_of_meet', 'tutor']

    def get_absolute_url(self):
        tutee_url = reverse('student_view', args=[self.tutee.student_id])
        tutee_url += "#"
        tutee_url += str(self.id)
        return tutee_url
