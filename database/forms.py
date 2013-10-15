from django import forms
from database.models import *

from django.contrib.auth.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return "%s" % (obj.get_full_name())

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Extend MultipleChoiceField for users so that the choices are
    listed as 'first_name last_name' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return "%s" % (obj.get_full_name())

class StudentForm(forms.ModelForm):

    tutor = UserModelChoiceField(
            User.objects.filter(groups__name='teachers').order_by('first_name', 'last_name'),
            required = False,
            widget=forms.Select(attrs={'class': 'form-control'})
            )

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'student_id', 'email',
                'active', 'since', 'year', 'is_part_time', 'tier_4',
                'tutor', 'course', 'qld', 'nalp', 'address',
                'home_address', 'phone_no', 'permanent_email')
        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'student_id': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.TextInput(attrs={'class': 'form-control'}),
                'address': forms.Textarea(attrs={'rows': 6, 'cols': 20, 'class': 'form-control'}),
                'home_address': forms.Textarea(attrs={'rows': 6, 'cols': 20, 'class': 'form-control'}),
                'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
                'permanent_email': forms.TextInput(attrs={'class': 'form-control'}),
                'year': forms.Select(attrs={'class': 'form-control'}),
                'since': forms.Select(attrs={'class': 'form-control'}),
                'course': forms.Select(attrs={'class': 'form-control'}),
                'nalp': forms.CheckboxInput(attrs={'class': 'form-control'}),
                'tier_4': forms.CheckboxInput(attrs={'class': 'form-control'}),
                'is_part_time': forms.CheckboxInput(attrs={'class': 'form-control'}),
                'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
                'qld': forms.CheckboxInput(attrs={'class': 'form-control'})
                }

class ModuleForm(forms.ModelForm):

    instructors = UserModelMultipleChoiceField(
            User.objects.filter(groups__name='teachers'),
            widget = forms.CheckboxSelectMultiple
            )

    class Meta:
        model = Module
        exclude = ('last_recorded_session',)
        widgets = {
                'year': forms.Select(attrs={'class': 'year'}),
                'successor_of': forms.Select(attrs={'class': 'form-control'}),
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'code': forms.TextInput(attrs={'class': 'form-control'}),
                'credits': forms.Select(attrs={'class': 'form-control'}),
                'year': forms.Select(attrs={'class': 'form-control'}),
                'first_session': forms.Select(attrs={'class': 'form-control'}),
                'no_teaching_in': forms.TextInput(attrs={'class': 'form-control'}),
                'last_session': forms.Select(attrs={'class': 'form-control'}),
                'number_of_sessions': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_1_title': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_1_value': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_1_type': forms.Select(attrs={'class': 'form-control'}),
                'assessment_1_max_word_count': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_2_title': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_2_value': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_2_type': forms.Select(attrs={'class': 'form-control'}),
                'assessment_2_max_word_count': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_3_title': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_3_value': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_3_type': forms.Select(attrs={'class': 'form-control'}),
                'assessment_3_max_word_count': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_4_title': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_4_value': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_4_type': forms.Select(attrs={'class': 'form-control'}),
                'assessment_4_max_word_count': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_5_title': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_5_value': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_5_type': forms.Select(attrs={'class': 'form-control'}),
                'assessment_5_max_word_count': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_6_title': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_6_value': forms.TextInput(attrs={'class': 'form-control'}),
                'assessment_6_type': forms.Select(attrs={'class': 'form-control'}),
                'assessment_6_max_word_count': forms.TextInput(attrs={'class': 'form-control'}),
                'exam_value': forms.TextInput(attrs={'class': 'form-control'})
                }


class LSPForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('lsp',)
        widgets = {
                'lsp': forms.Textarea(attrs={'class': 'form-control'})
                }

class NotesForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('notes',)
        widgets = {
                'notes': forms.Textarea(attrs={'class': 'form-control'})
                }

class TuteeForm(forms.ModelForm):
    class Meta:
        model = Tutee_Session
        fields = ('date_of_meet', 'notes', )
        widgets = {
                'date_of_meet': forms.DateInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'form-control'}),
                'notes': forms.Textarea(attrs={'class': 'form-control'}),
                }

class CSVUploadForm(forms.Form):
    csvfile = forms.FileField(
            label = 'Select a .csv file',
            help_text = """Simply save the spreadsheet under Excel or LibreOffice as .csv. 
            Make sure it does not contain a header row and no invalid rows either."""    
        )

class CSVParseForm(forms.Form):
    ATTRIBUTES = (
            ('ignore', 'Ignore this Field'),
            ('student_id', 'Student ID'),
            ('first_name', 'First Name'),
            ('last_name', 'Last Name'),
            ('since', 'Studying since'),
            ('year', 'Year of Study'),
            ('email', 'University email'),
            ('course', 'Course'),
            ('tutor', 'Tutor'),
            ('permanent_email', 'Private email'),
            ('achieved_grade', 'Achieved grade'),
            ('address', 'Term time address'),
            ('home_address', 'Home address')
        )
    column_1 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_2 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_3 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_4 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_5 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_6 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_7 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_8 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_9 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_10 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_11 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
    column_12 = forms.ChoiceField(choices=ATTRIBUTES, required = False)
