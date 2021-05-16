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
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from common.ortc import ORTC
from common.config import params
from common.utils import get_orthanc_server

def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)

# La page d'accueil c'est la liste des patients

# La liste des patients
class Patients(ListView):

    template_name = 'view/patients.html'
    context_object_name = 'patients'

    # Le serveur orthanc
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

        # Récupère les patients
        patients = self.o.GetPatients()

        # Pagination si l'on trouve des patients
        if patients:
            self.paginate_by = params['paginate_by']

        # Retourne les patients
        return patients
    
    # Enrichit le contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Récupère la provenance de l'url et enrichit le contexte
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None            
        
        # Retourne le contexte
        return context

# Un patient
class Patient(ListView):

    template_name = 'view/patient.html'
    context_object_name = 'studies'

    # Le serveur orthanc
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

        # Récupère les études
        if 'patient_id' in self.kwargs:
            studies = self.o.GetPatientStudies(self.kwargs['patient_id'])
        else:
            studies = None

        # Pagination si l'on trouve des études
        if studies:
            self.paginate_by = params['paginate_by']
        
        # Retourne ses études
        return studies

    # Enrichit le contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Récupère le patient et enrichit le contexte
        if 'patient_id' in self.kwargs:
            context['patient'] = self.o.GetPatient(self.kwargs['patient_id'])
        else:
            context['patient'] = None

        # Récupère la provenance de l'url et enrichit le contexte
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None            
        
        # Retourne le contexte
        return context

# Des études
class Studies(ListView):

    template_name = 'view/studies.html'
    context_object_name = 'studies'
    paginate_by = params['paginate_by']
    request = None
    object_list = {'toto': 'toto', 'tata': 'tata',}

    # Le serveur orthanc
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

        # Récupère les études
        if 'patient_id' in self.kwargs:
            studies = self.o.GetPatientStudies(self.kwargs['patient_id'])
        else:
            studies = None

        # Pagination si l'on trouve des études
        if studies:
            self.paginate_by = params['paginate_by']
        
        # Retourne ses études
        return studies

    # Enrichit le contexte
    def get_context_data(self, **kwargs):

        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Récupère la provenance de l'url et enrichit le contexte
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None            
        
        # Retourne le contexte
        return context

# Une étude
class Study(ListView):

    template_name = 'view/study.html'
    context_object_name = 'series'

    # Le serveur orthanc
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

        # Récupère les séries
        if 'study_id' in self.kwargs:
            series = self.o.GetStudySeries(self.kwargs['study_id'])
        else:
            series = None

        # Pagination si l'on trouve des séries
        if series:
            self.paginate_by = params['paginate_by']
        
        # Retourne les séries
        return series

    # Ajout le détail du patient au contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Ajoute l'url du visualiseur de séries au contexte
        item = {}
        item['stone_web_viewer'] = params['stone_web_viewer']
        item['web_viewer'] = params['web_viewer']
        context['params'] = item
        
        # Récupère l'étude et enrichit le contexte
        if 'study_id' in self.kwargs:
            study = self.o.GetStudy(self.kwargs['study_id'])
        else:
            study = None
        context['study'] = study        

        # Récupère le patient et enrichit le contexte
        if study:
            context['patient'] = self.o.GetPatient(study['ParentPatient'])
        else:
            context['patient'] = None

        # Récupère la provenance de l'url et enrichit le contexte
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None
        
        # Retourne le contexte
        return context

# Téléchargement d'une étude
class StudyDownload(LoginRequiredMixin, TemplateView):

    template_name = 'view/study_download.html'

    # Le serveur orthanc
    orthanc_server = get_orthanc_server()
    o = ORTC(orthanc_server['host'],
             orthanc_server['port'],
             orthanc_server['user'],
             orthanc_server['password'],
    )
    
    # Ajout les infos au contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Authentification
        if self.request.user.is_authenticated:
            django_user = User.objects.get(username=self.request.user.username)
            context['django_user'] = django_user
        else:
            context['django_user'] = None

        # Récupère l'étude et enrichit le contexte
        if 'study_id' in self.kwargs:
            study_id = self.kwargs['study_id']
            study = self.o.GetStudy(study_id)
        else:
            study_id = None
            study = None
        context['study'] = study        

        # Récupère le patient et enrichit le contexte
        if study:
            context['patient'] = self.o.GetPatient(study['ParentPatient'])
        else:
            context['patient'] = None

        # Récupère la provenance de l'url et enrichit le contexte
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None

        # Télécharge l'étude
        if study_id is not None:
            self.o.SetNewTransactionID()
            self.o.DownloadStudy(study_id, django_user)
        
        # Retourne le contexte
        return context

# Une série
class Serie(DetailView):

    template_name = 'view/serie.html'
    context_object_name = 'serie'

    # Le serveur orthanc
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

        # La série
        serie = None

        # Retourne la série
        return serie

    # Ajout le détail du patient au contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Récupère l'étude et enrichit le contexte
        if 'study_id' in self.kwargs:
            study = self.o.GetStudy(self.kwargs['study_id'])
        else:
            study = None
        context['study'] = study        

        # Récupère le patient et enrichit le contexte
        if study:
            context['patient'] = self.o.GetPatient(study['ParentPatient'])
        else:
            context['patient'] = None

        # Récupère la provenance de l'url et enrichit le contexte
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None
        
        # Retourne le contexte
        return context

# Téléchargement d'une série
class SerieDownload(LoginRequiredMixin, TemplateView):

    template_name = 'view/serie_download.html'

    # Le serveur orthanc
    orthanc_server = get_orthanc_server()
    o = ORTC(orthanc_server['host'],
             orthanc_server['port'],
             orthanc_server['user'],
             orthanc_server['password'],
    )
    
    # Ajout les infos au contexte
    def get_context_data(self, **kwargs):
        
        # Appel de l'implémentation de base pour obtenir un contexte                                
        context = super().get_context_data(**kwargs)

        # Authentification
        if self.request.user.is_authenticated:
            django_user = User.objects.get(username=self.request.user.username)
            context['django_user'] = django_user
        else:
            context['django_user'] = None

        # Récupère la série et enrichit le contexte
        if 'serie_id' in self.kwargs:
            serie_id = self.kwargs['serie_id']
            serie = self.o.GetSerie(serie_id)
        else:
            serie_id = None
            serie = None
        context['serie'] = serie        

        # Récupère l'étude et enrichit le contexte
        if serie:
            study = self.o.GetStudy(serie['ParentStudy'])
        else:
            study = None
        context['study'] = study

        # Récupère le patient et enrichit le contexte
        if study:
            context['patient'] = self.o.GetPatient(study['ParentPatient'])
        else:
            context['patient'] = None

        # Récupère la provenance de l'url et enrichit le contexte
        if 'ref' in self.kwargs:
            context['ref'] = self.kwargs['ref']
        else:
            context['ref'] = None

        # Télécharge l'étude
        if serie_id is not None:
            self.o.SetNewTransactionID()
            self.o.DownloadSerie(serie_id, django_user)
        
        # Retourne le contexte
        return context
