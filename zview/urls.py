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

from django.urls import path

from . import views

app_name = 'zview'

urlpatterns = [
    # Toutes les données
    path('all/patients/', views.Patients.as_view(), {'ref': 'all',}, name='apatients'),
    path('all/patients/<slug:patient_id>/', views.Patient.as_view(), {'ref': 'all',}, name='apatient'),
    path('all/studies/', views.Studies.as_view(), {'ref': 'all',}, name='astudies'),
    path('all/studies/<slug:study_id>/', views.Study.as_view(), {'ref': 'all',}, name='astudy'),
    path('all/studies/<slug:study_id>/download/', views.StudyDownload.as_view(), {'ref': 'all',}, name='astudydownload'),
    path('all/series/<slug:serie_id>/', views.Serie.as_view(), {'ref': 'all',}, name='aserie'),    
    path('all/series/<slug:serie_id>/download/', views.SerieDownload.as_view(), {'ref': 'all',}, name='aseriedownload'),
    
    # Les données issues d'une recherche
    #path('search/patients/', views.Patients.as_view(), {'ref': 'search',}, name='spatients'),
    #path('search/patients/<slug:patient_id>/', views.Patient.as_view(), {'ref': 'search',}, name='spatient'),
    #path('search/studies/', views.Studies.as_view(), {'ref': 'search',}, name='sstudies'),
    #path('search/studies/<slug:study_id>/', views.Study.as_view(), {'ref': 'search',}, name='sstudy'),    
    #path('search/studies/<slug:study_id>/download/', views.StudyDownload.as_view(), {'ref': 'search',}, name='sstudydownload'),
    #path('search/series/<slug:serie_id>/', views.Serie.as_view(), {'ref': 'search',}, name='sserie'),    
    #path('search/series/<slug:serie_id>/download/', views.SerieDownload.as_view(), {'ref': 'search',}, name='sseriedownload'),
]
