from django import forms
#from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapUneditableInput
from database.models import *

from django.contrib.auth.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name (username)' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return "%s" % (obj.get_full_name())

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Extend MultipleChoiceField for users so that the choices are
    listed as 'first_name last_name (username)' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return "%s" % (obj.get_full_name())

class StudentForm(forms.ModelForm):

    tutor = UserModelChoiceField(User.objects.filter(groups__name='teachers'))

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'student_id', 'email',
                'active', 'since', 'year', 'is_part_time',
                'tutor', 'course', 'qld', 'nalp', 'address',
                'home_address', 'phone_no', 'permanent_email')
        widgets = {
                'address': forms.Textarea(attrs={'rows': 6, 'cols': 20}),
                'home_address': forms.Textarea(attrs={'rows': 6, 'cols': 20}),
                }

class ModuleForm(forms.ModelForm):

    #SUCCESSOR_OF_CHOICES = [('', 'Select the Predecessor'), (m, m) for m in Module.objects.all()]

    #year = forms.ChoiceField(choices = ACADEMIC_YEARS, widgets=forms.Select(attrs={'class': 'year'}))
    #successor_of = forms.ChoiceField(choices = SUCCESSOR_OF_CHOICES, widgets=forms.Select(attrs={'class': 'successor_of'}))

    class Meta:
        model = Module
        exclude = ('last_recorded_session',)
        widgets = {
                'year': forms.Select(attrs={'class': 'year'}),
                'successor_of': forms.Select(attrs={'class': 'successor_of'}),
                'assessment_1_value': forms.TextInput(attrs={'class': 'assessment_value'}),
                'assessment_2_value': forms.TextInput(attrs={'class': 'assessment_value'}),
                'assessment_3_value': forms.TextInput(attrs={'class': 'assessment_value'}),
                'assessment_4_value': forms.TextInput(attrs={'class': 'assessment_value'}),
                'assessment_5_value': forms.TextInput(attrs={'class': 'assessment_value'}),
                'assessment_6_value': forms.TextInput(attrs={'class': 'assessment_value'}),
                'exam_value': forms.TextInput(attrs={'class': 'input-small'})
                }


class LSPForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('lsp',)

class NotesForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('notes',)

class TuteeForm(forms.ModelForm):
    class Meta:
        model = Tutee_Session
        fields = ('date_of_meet', 'notes', )
        widgets = {
                'date_of_meet': forms.DateInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'input-small'}),
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
