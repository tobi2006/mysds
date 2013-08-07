from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapUneditableInput
from database.models import Student, Module, Performance, ACADEMIC_YEARS

from django.contrib.auth.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
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
                'successor_of': forms.Select(attrs={'class': 'successor_of'})
                }


class LSPForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('lsp',)

class NotesForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('notes',)

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
            ('permanent_email', 'Permanent email'),
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

#def generate_mark_form(no_of_assessments, noexam=False, to_mark='all', *args, **kwargs):
#    if to_mark == 'all':
#        use_widgets = {
#                #'student': BootstrapUneditableInput(),
#                'average': BootstrapUneditableInput()
#            }
#    elif to_mark == 'exam':
#        use_widgets = {
#                #'student': BootstrapUneditableInput(),
#                'average': BootstrapUneditableInput(),
#                'assessment_1': BootstrapUneditableInput(),
#                'assessment_2': BootstrapUneditableInput(),
#                'assessment_3': BootstrapUneditableInput(),
#                'assessment_4': BootstrapUneditableInput(),
#                'assessment_5': BootstrapUneditableInput(),
#                'assessment_6': BootstrapUneditableInput()
#            }
#    else:
#        if to_mark == '1':
#            use_widgets = {
#                #    'student': BootstrapUneditableInput(),
#                    'average': BootstrapUneditableInput(),
#                    'assessment_2': BootstrapUneditableInput(),
#                    'assessment_3': BootstrapUneditableInput(),
#                    'assessment_4': BootstrapUneditableInput(),
#                    'assessment_5': BootstrapUneditableInput(),
#                    'assessment_6': BootstrapUneditableInput(),
#                    'exam': BootstrapUneditableInput()
#                }
#        if to_mark == '2':
#            use_widgets = {
#                #    'student': BootstrapUneditableInput(),
#                    'average': BootstrapUneditableInput(),
#                    'assessment_1': BootstrapUneditableInput(),
#                    'assessment_3': BootstrapUneditableInput(),
#                    'assessment_4': BootstrapUneditableInput(),
#                    'assessment_5': BootstrapUneditableInput(),
#                    'assessment_6': BootstrapUneditableInput(),
#                    'exam': BootstrapUneditableInput()
#                }
#        if to_mark == '3':
#            use_widgets = {
#                #    'student': BootstrapUneditableInput(),
#                    'average': BootstrapUneditableInput(),
#                    'assessment_1': BootstrapUneditableInput(),
#                    'assessment_2': BootstrapUneditableInput(),
#                    'assessment_4': BootstrapUneditableInput(),
#                    'assessment_5': BootstrapUneditableInput(),
#                    'assessment_6': BootstrapUneditableInput(),
#                    'exam': BootstrapUneditableInput()
#                }
#        if to_mark == '4':
#            use_widgets = {
#                #    'student': BootstrapUneditableInput(),
#                    'average': BootstrapUneditableInput(),
#                    'assessment_1': BootstrapUneditableInput(),
#                    'assessment_2': BootstrapUneditableInput(),
#                    'assessment_3': BootstrapUneditableInput(),
#                    'assessment_5': BootstrapUneditableInput(),
#                    'assessment_6': BootstrapUneditableInput(),
#                    'exam': BootstrapUneditableInput()
#                }
#        if to_mark == '5':
#            use_widgets = {
#                #    'student': BootstrapUneditableInput(),
#                    'average': BootstrapUneditableInput(),
#                    'assessment_1': BootstrapUneditableInput(),
#                    'assessment_2': BootstrapUneditableInput(),
#                    'assessment_3': BootstrapUneditableInput(),
#                    'assessment_4': BootstrapUneditableInput(),
#                    'assessment_6': BootstrapUneditableInput(),
#                    'exam': BootstrapUneditableInput()
#                }
#        if to_mark == '6':
#            use_widgets = {
#                #    'student': BootstrapUneditableInput(),
#                    'average': BootstrapUneditableInput(),
#                    'assessment_1': BootstrapUneditableInput(),
#                    'assessment_2': BootstrapUneditableInput(),
#                    'assessment_3': BootstrapUneditableInput(),
#                    'assessment_4': BootstrapUneditableInput(),
#                    'assessment_5': BootstrapUneditableInput(),
#                    'exam': BootstrapUneditableInput()
#                }
#    
#    alwaysexclude = ('module', 'seminar_group', 'absences')
#    excluded_assessments = ['assessment_1', 'assessment_2', 'assessment_3', 'assessment_4', 'assessment_5', 'assessment_6']
#    if noexam:
#        excluded_assessments.append('exam')
#    for i in range(no_of_assessments):
#        del excluded_assessments[0]
#    excludes = alwaysexclude + tuple(excluded_assessments)
#
#    class MarkForm(forms.ModelForm):
#        class Meta:
#            model = Performance
#            exclude = excludes
#            widgets = use_widgets
#
#    return MarkForm
