# from django import forms
from django.forms.models import inlineformset_factory

from courses.models import Course, Module

# Since a course is divided into a variable number of modules,
# it makes sense to use formsets to manage them.
# The inlineformset_factory  function allows us to build a model formset
# dynamically for the Module objects related to a Course object.
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)
