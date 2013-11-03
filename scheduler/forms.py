from django import forms
from scheduler.models import *

#class AppointmentForm(forms.ModelForm):
#
#    class Meta:
#        model = student_teacher_appointment
#        widgets = {
#            'start_time': forms.,
#            #      'date_of_meet': forms.DateInput(attrs={'data-datetime-format': 'dd/mm/yyyy', 'class': 'form-control'}), #Check how to
#            #'end_time': forms.DateTimeField()
#            'student': forms.CheckboxSelectMultiple,
#            teacher = models.ForeignKey(User)
#            invited = models.ManyToManyField(Student, blank=True, null=True)
#                }
#
