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

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView

from common.ortc import ORTC
from common.config import params
from common.utils import get_orthanc_server

from .forms import PatientForm, StudyForm

def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)

# La page d'accueil                                                                                 
class Index(TemplateView):
    template_name = 'zsearch/index.html'

    # Le serveur orthanc
    orthanc_server = get_orthanc_server()
    o = ORTC(orthanc_server['host'],
             orthanc_server['port'],
             orthanc_server['user'],
             orthanc_server['password'],
    )       
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({'patientform': PatientForm(prefix='patientform_pre'), 'studyform': StudyForm(prefix='studyform_pre')})
    
    # Si c'est POST alors on fait des trucs
    def post(self, request, *args, **kwargs):

        patientform = _get_form(request, PatientForm, 'patientform_pre')
        studyform = _get_form(request, StudyForm, 'studyform_pre')

        return self.render_to_response({'patientform': patientform, 'studyform': studyform})

# Des études
class Studies(ListView):

    template_name = 'view/studies.html'
    context_object_name = 'studies'
    paginate_by = params['paginate_by']    

    orthanc_server = get_orthanc_server()
    o = ORTC(orthanc_server['host'],
             orthanc_server['port'],
             orthanc_server['user'],
             orthanc_server['password'],
    )

    # Surcharge queryset parce que l'on ne positionne pas de modèle
    # et que l'on veut juste bénéficier des facilités de gestion et d'affichage
    # offertes par la classe ListView sur un jeu de données
    # issues non pas de la base mais de requêtes REST
    def get_queryset(self):

        # Appel de l'implémentation de base pour obtenir un contexte
        request = self.request

        # Récupère les études qui correspondent à la recherche
        if 'studies' not in request.session:
            studies = None
        else:
            studies = request.session['studies']

        # Retourne les études
        return studies

    # Enrichit le contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Récupère la provenance de l'url
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None            
        
        # Retourne le contexte
        return context

    # Si c'est POST alors on fait des trucs
    def post(self, request, *args, **kwargs):
        
        studyform = _get_form(request, StudyForm, 'studyform_pre')

        if studyform.is_bound and studyform.is_valid():
            # Process studyform and render response
            print(studyform.cleaned_data)

            # Lance la recherche
            # Ce qui aura pour effet de positionner le payload
            self.Search(studyform.cleaned_data)

            # Récupère le contexte
            context = super().get_context_data(**kwargs)

            # Positionne la provenance de l'url
            context['ref'] = 'search'

            # Rendu de la page
            return self.render_to_response(context)
        else:
            print('oops')

    # La recherche proprement dite
    def Search(self, cleaned_data):
            
        # Pour le payload REST
        payload = {}

        # Quel tag est cherché ?
        if cleaned_data['study_tag'] == 'REQPD':
            study_tag = 'RequestedProcedureDescription'
        elif cleaned_data['study_tag'] == 'INAME':
            study_tag = 'InstitutionName'

        # Construction de l'expression de recherche
        query_expression = 'oops'
        if cleaned_data['search_scope'] == 'STARTS':
            query_expression = cleaned_data['study_search_text'] + '*'
        elif cleaned_data['search_scope'] == 'CONTAINS':
            query_expression = '*' + cleaned_data['study_search_text'] + '*'

        # Construit le payload
        payload['Level'] = 'Study'
        payload['Expand'] = True
        payload['Query'] = {}
        payload['Query'][study_tag] = query_expression

        print(payload)

        # Récupère les études
        studies = self.o.Search(payload)

        # On met le payload dans la session
        # Ce qui servira pour la pagination par exemple
        request = self.request
        request.session['studies'] = studies

        # Hyper important
        self.queryset = studies
        self.object_list = self.queryset

        return studies

# Des patients
class Patients(ListView):

    template_name = 'view/patients.html'
    context_object_name = 'patients'
    paginate_by = params['paginate_by']    

    orthanc_server = get_orthanc_server()
    o = ORTC(orthanc_server['host'],
             orthanc_server['port'],
             orthanc_server['user'],
             orthanc_server['password'],
    )

    # Surcharge queryset parce que l'on ne positionne pas de modèle
    # et que l'on veut juste bénéficier des facilités de gestion et d'affichage
    # offertes par la classe ListView sur un jeu de données
    # issues non pas de la base mais de requêtes REST
    def get_queryset(self):

        # Appel de l'implémentation de base pour obtenir un contexte
        request = self.request

        # Récupère les études qui correspondent à la recherche
        if 'patients' not in request.session:
            patients = None
        else:
            patients = request.session['patients']

        # Retourne les études
        return patients

    # Enrichit le contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Récupère la provenance de l'url
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None            
        
        # Retourne le contexte
        return context

    # Si c'est POST alors on fait des trucs
    def post(self, request, *args, **kwargs):
        
        patientform = _get_form(request, PatientForm, 'patientform_pre')

        if patientform.is_bound and patientform.is_valid():
            # Process patientform and render response
            print(patientform.cleaned_data)

            # Lance la recherche
            # Ce qui aura pour effet de positionner le payload
            self.Search(patientform.cleaned_data)

            # Récupère le contexte
            context = super().get_context_data(**kwargs)

            # Positionne la provenance de l'url
            context['ref'] = 'search'

            # Rendu de la page
            return self.render_to_response(context)
        else:
            print('oops')

    # La recherche proprement dite
    def Search(self, cleaned_data):
            
        # Pour le payload REST
        payload = {}

        # Quel tag est cherché ?
        patient_tag = None
        if cleaned_data['patient_tag'] == 'PNAME':
            patient_tag = 'PatientName'
            
        # Construction de l'expression de recherche
        query_expression = 'oops'
        if cleaned_data['search_scope'] == 'STARTS':
            query_expression = cleaned_data['patient_search_text'] + '*'
        elif cleaned_data['search_scope'] == 'CONTAINS':
            query_expression = '*' + cleaned_data['patient_search_text'] + '*'

        # Construit le payload
        payload['Level'] = 'Patient'
        payload['Expand'] = True
        payload['Query'] = {}
        payload['Query'][patient_tag] = query_expression
            
        print(payload)

        # Récupère les patients
        patients = self.o.Search(payload)

        # On met le payload dans la session
        # Ce qui servira pour la pagination par exemple
        request = self.request
        request.session['patients'] = patients

        # Hyper important
        self.queryset = patients
        self.object_list = self.queryset

        return patients
