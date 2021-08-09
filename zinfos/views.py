from django.shortcuts import render

from common.ortc import ORTC
from common.utils import get_orthanc_server


# La page d'accueil
def index(request):
    stats = None

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
                  {'orthanc_name': orthanc_server['name'], 'stats': stats, 'infos': infos})
