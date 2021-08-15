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

from . import views as sviews
from zview import views as zviews

app_name = 'zsearch'

urlpatterns = [
    # Home page
    path('', sviews.Index.as_view(), name='index'),

    # Search results
    path('patients/', sviews.Patients.as_view(), {'ref': 'search',}, name='spatients'),
    path('studies/', sviews.Studies.as_view(), {'ref': 'search',}, name='sstudies'),

    # Search details
    path('patients/<slug:patient_id>/', zviews.Patient.as_view(), {'ref': 'search',}, name='spatient'),
    path('studies/<slug:study_id>/', zviews.Study.as_view(), {'ref': 'search',}, name='sstudy'),
    path('studies/<slug:study_id>/download/', zviews.StudyDownload.as_view(), {'ref': 'search',}, name='sstudydownload'),
    path('series/<slug:serie_id>/', zviews.Serie.as_view(), {'ref': 'search',}, name='sserie'),    
    path('series/<slug:serie_id>/download/', zviews.SerieDownload.as_view(), {'ref': 'search',}, name='sseriedownload'),
]
