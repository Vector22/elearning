from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    # Used in the CourseDetailView to let user enrol in a course
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
