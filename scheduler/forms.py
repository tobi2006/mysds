from django import forms
from scheduler.models import *
from database.models import Student

class AppointmentForm(forms.Form):
    LENGTHS = ( 
       (5, '5 Minutes'),
       (10, '10 Minutes'),
       (15, '15 Minutes'),
       (20, '20 Minutes'),
       (25, '25 Minutes'),
       (30, '30 Minutes'),
       (35, '35 Minutes'),
       (40, '40 Minutes'),
       (45, '45 Minutes'),
       (50, '50 Minutes'),
       (55, '55 Minutes'),
       (60, '1 Hour')
       )
    message = forms.CharField(widget = forms.Textarea(attrs = {
        'class': 'form-control', 'rows': '6', 
        'placeholder': 'Any Details you want to tell the students - what they need to bring or prepare, location of the meeting etc'
        }))
    slot_1_date = forms.DateField(widget = forms.TextInput(attrs = {
        'data-date-format': 'dd/mm/yyyy', 'class': 'form-control slot_date', 'placeholder': 'Date for the meetings'
        }))
    slot_1_from = forms.TimeField(widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'Start time in 24h format (eg 14:30)'
        }))
    slot_1_until = forms.TimeField(widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'End time in 24h format (eg 18:00)'
        }))
    slot_2_date = forms.DateField(required = False, widget = forms.TextInput(attrs = {
        'data-date-format': 'dd/mm/yyyy', 'class': 'form-control slot_date', 'placeholder': 'Date for the meetings'
        }))
    slot_2_from = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'Start time in 24h format (eg 14:30)'
        }))
    slot_2_until = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'End time in 24h format (eg 18:00)'
        }))
    slot_3_date = forms.DateField(required = False, widget = forms.TextInput(attrs = {
        'data-date-format': 'dd/mm/yyyy', 'class': 'form-control slot_date', 'placeholder': 'Date for the meetings'
        }))
    slot_3_from = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'Start time in 24h format (eg 14:30)'
        }))
    slot_3_until = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'End time in 24h format (eg 18:00)'
        }))
    slot_4_date = forms.DateField(required = False, widget = forms.TextInput(attrs = {
        'data-date-format': 'dd/mm/yyyy', 'class': 'form-control slot_date', 'placeholder': 'Date for the meetings'
        }))
    slot_4_from = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'Start time in 24h format (eg 14:30)'
        }))
    slot_4_until = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'End time in 24h format (eg 18:00)'
        }))
    slot_5_date = forms.DateField(required = False, widget = forms.TextInput(attrs = {
        'data-date-format': 'dd/mm/yyyy', 'class': 'form-control slot_date', 'placeholder': 'Date for the meetings'
        }))
    slot_5_from = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'Start time in 24h format (eg 14:30)'
        }))
    slot_5_until = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'End time in 24h format (eg 18:00)'
        }))
    slot_6_date = forms.DateField(required = False, widget = forms.TextInput(attrs = {
        'data-date-format': 'dd/mm/yyyy', 'class': 'form-control slot_date', 'placeholder': 'Date for the meetings'
        }))
    slot_6_from = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'Start time in 24h format (eg 14:30)'
        }))
    slot_6_until = forms.TimeField(required = False, widget = forms.TextInput(attrs = {
        'class': 'form-control input-sm', 'placeholder': 'End time in 24h format (eg 18:00)'
        }))
    appointment_length = forms.ChoiceField(choices = LENGTHS)
