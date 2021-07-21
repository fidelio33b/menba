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

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # La page d'accueil
    path('', include('zhome.urls')),

    # La visualisation des données
    path('view/', include('zview.urls')),

    # Les recherches
    path('search/', include('zsearch.urls')),

    # Les informations (serveur, statistiques...)
    path('infos/', include('zinfos.urls')),
]
