from django import forms
from feedback.models import *

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



class EssayForm(forms.ModelForm):
    
    marker = UserModelChoiceField(
            User.objects.filter(groups__name='teachers'),
            required = False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            )
    second_first_marker = UserModelChoiceField(
            User.objects.filter(groups__name='teachers'),
            required = False,
            widget=forms.Select(attrs={'class': 'form-control'}),
            )

    class Meta:
        model = Marksheet
        fields = ('category_mark_1', 'category_mark_2', 'category_mark_3', 'category_mark_4',
                'category_mark_5', 'category_mark_6', 'category_mark_7', 'category_mark_8',
                'part_1_mark', 'part_2_mark', 'comments', 'comments_2', 'submission_date',
                'marking_date', 'marker', 'second_first_marker')
        widgets = {
                'comments': forms.Textarea(attrs={'class': 'form-control'}),
                'comments_2': forms.Textarea(attrs={'class': 'form-control'}),
                'part_1_mark': forms.TextInput(attrs={'class': 'form-control'}),
                'part_2_mark': forms.TextInput(attrs={'class': 'form-control'}),
                'category_mark_1': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_2': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_3': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_4': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_5': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_6': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_7': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_8': forms.Select(attrs={'class': 'form-control'}),
                'submission_date': forms.DateInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'form-control'}),
                'marking_date': forms.DateInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'form-control'})
                }
