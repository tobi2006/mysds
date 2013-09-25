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

    class Meta:
        model = Marksheet
        fields = ('category_mark_1', 'category_mark_2', 'category_mark_3', 'category_mark_4',
                'comments', 'submission_date', 'marking_date', 'marker')
        widgets = {
                'comments': forms.Textarea(attrs={'class': 'form-control'}),
                'category_mark_1': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_2': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_3': forms.Select(attrs={'class': 'form-control'}),
                'category_mark_4': forms.Select(attrs={'class': 'form-control'}),
                'submission_date': forms.DateInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'form-control'}),
                'marking_date': forms.DateInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'form-control'})
                }
