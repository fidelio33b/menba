"""
This file is part of Menba.
Copyright (C) 2021

Menba is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Menba is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Menba.  If not, see <https://www.gnu.org/licenses/>.

Laurent Lavaud <fidelio33b@gmail.com>, 2021.
"""

from django import forms
from django.utils.translation import gettext as _


class PatientForm(forms.Form):
    # La méthode de recherche
    STARTS_WITH = 'STARTS'
    CONTAINS = 'CONTAINS'
    SCOPE_CHOICES = [
        (STARTS_WITH, _('starts with')),
        (CONTAINS, _('contains')),
    ]

    # Les tags de recherche possibles
    PATIENT_NAME = 'PNAME'
    PATIENT_TAG_CHOICES = [
        (PATIENT_NAME, 'Patient name'),
    ]

    # Les champs du formulaire
    search_scope = forms.ChoiceField(choices=SCOPE_CHOICES, required=True, widget=forms.RadioSelect)
    patient_tag = forms.ChoiceField(choices=PATIENT_TAG_CHOICES, required=True,
                                    widget=forms.Select(attrs={'class': 'custom-select'}))
    patient_search_text = forms.CharField(min_length=2, max_length=100, required=True)


class StudyForm(forms.Form):
    # La méthode de recherche
    STARTS_WITH = 'STARTS'
    CONTAINS = 'CONTAINS'
    SCOPE_CHOICES = [
        (STARTS_WITH, _('starts with')),
        (CONTAINS, _('contains')),
    ]

    # Les tags de recherche possibles
    REQUESTED_PROCEDURE_DESCRIPTION = 'REQPD'
    INSTITUTION_NAME = 'INAME'
    STUDY_TAG_CHOICES = [
        (REQUESTED_PROCEDURE_DESCRIPTION, 'Requested procedure description'),
        (INSTITUTION_NAME, 'Institution name'),
    ]

    # Les champs du formulaire
    search_scope = forms.ChoiceField(choices=SCOPE_CHOICES, required=True, widget=forms.RadioSelect)
    study_tag = forms.ChoiceField(choices=STUDY_TAG_CHOICES, required=True,
                                  widget=forms.Select(attrs={'class': 'custom-select'}))
    study_search_text = forms.CharField(min_length=2, max_length=100, required=True)
