from django import forms
from django.utils.translation import gettext as _

class PatientForm(forms.Form):

     # La méthode de recherche
     STARTS_WITH='STARTS'
     CONTAINS='CONTAINS'
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
     patient_tag = forms.ChoiceField(choices=PATIENT_TAG_CHOICES, required=True, widget=forms.Select(attrs={'class': 'custom-select'}))
     patient_search_text = forms.CharField(min_length=2, max_length=100, required=True)

class StudyForm(forms.Form):

     # La méthode de recherche
     STARTS_WITH='STARTS'
     CONTAINS='CONTAINS'
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
     study_tag = forms.ChoiceField(choices=STUDY_TAG_CHOICES, required=True, widget=forms.Select(attrs={'class': 'custom-select'}))
     study_search_text = forms.CharField(min_length=2, max_length=100, required=True)
