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

from zcommon.config import params
from zcommon.ortc import ORTC
from zcommon.utils import get_orthanc_server


# La page d'accueil
def index(request):
    # Récupère les statistiques et les informations système du serveur
    orthanc_server = get_orthanc_server()
    o = ORTC(
        orthanc_server['host'],
        orthanc_server['port'],
        orthanc_server['user'],
        orthanc_server['password'],
    )
    stats = o.GetStatistics()
    infos = o.GetSystemInfos()

    return render(request, 'zinfos/index.html',
                  {
                      'orthanc_name': orthanc_server['name'],
                      'stats': stats, 'infos': infos,
                      'menba_version': params['app']['version'],
                  }
                  )
