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

import syslog
import requests

from django.utils.translation import gettext as _

from time import sleep as tsleep
from celery import shared_task

from common.config import params
from common.utils import send_mail

# Timeout for to stop requests waiting for a response after a given number of seconds
#   - https://docs.python-requests.org/en/latest/user/quickstart/#timeouts
TIMEOUT_GET_REQUEST=1

@shared_task
def STDownloadStudy(api_url, verify_cert, user, password, study_id, user_email, study, patient):

    # Donnera le résultat de l'opération
    success = False
        
    try:

        # Désactive les avertissements du module
        if not verify_cert:
            requests.packages.urllib3.disable_warnings()

        # Définit les en-têtes http
        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'
        headers['Accept'] = 'application/json'

        # Définit la session de connexion
        connection = requests.Session()
        connection.auth = (user, password)

        # Recherche de l'étude
        REST = '/studies'
        full_url = api_url + REST + '/' + study_id + '/archive'
        data = connection.get(full_url, headers=headers, verify=verify_cert, stream=True, timeout=TIMEOUT_GET_REQUEST)

        # Stockage du flux archive dans un fichier
        directory = params['files']['directory']['studies']
        filename = directory + '/' + study_id + '.zip'
        link = params['files']['link']['studies'] + '/' + study_id + '.zip'
        with open(filename, 'wb') as fd:
            for chunk in data.iter_content(chunk_size=128):
                fd.write(chunk)

        # Envoi du mail avec le lien de téléchargement
        if user_email is not None:
            subject = '['+ params['app']['name'] + '] - ' + 'Download link'
            sender = params['mail']['sender']
            recipients = []
            recipients.append(user_email)
            body_md = """# Download study

[Download link]({})

Descritption : {}

Patient : {}

""".format(link, study['MainDicomTags']['StudyDescription'], patient['MainDicomTags']['PatientName'])

            # A trduire...
            body_md = _('mail study download pitch %(link)s %(study_description)s %(patient)s') % {'link': link, 'study_description': study['MainDicomTags']['StudyDescription'], 'patient': patient['MainDicomTags']['PatientName']}
            
            send_mail(subject, sender, recipients, body_md)
                
        success = True

    except Exception as e:
        print('common/tasks.py/STDownloadStudy')
        print(str(e))

    finally:
        return success

@shared_task
def STDownloadSerie(api_url, verify_cert, user, password, serie_id, user_email, serie, study, patient):

    # Donnera le résultat de l'opération
    success = False
        
    try:

        # Désactive les avertissements du module
        if not verify_cert:
            requests.packages.urllib3.disable_warnings()

        # Définit les en-têtes http
        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'
        headers['Accept'] = 'application/json'

        # Définit la session de connexion
        connection = requests.Session()
        connection.auth = (user, password)

        # Recherche de l'étude
        REST = '/studies'
        full_url = api_url + REST + '/' + serie_id + '/archive'
        data = connection.get(full_url, headers=headers, verify=verify_cert, stream=True, timeout=TIMEOUT_GET_REQUEST)

        # Stockage du flux archive dans un fichier
        directory = params['files']['directory']['series']
        filename = directory + '/' + serie_id + '.zip'
        link = params['files']['link']['series'] + '/' + serie_id + '.zip'
        with open(filename, 'wb') as fd:
            for chunk in data.iter_content(chunk_size=128):
                fd.write(chunk)

        # Envoi du mail avec le lien de téléchargement
        if user_email is not None:
            subject = '['+ params['app']['name'] + '] - ' + 'Download link'
            sender = params['mail']['sender']
            recipients = []
            recipients.append(user_email)

            # A trduire...
            body_md = _('mail serie download pitch %(link)s %(serie_description)s %(study_description)s %(patient)s') % {'link': link, 'serie_description': serie['MainDicomTags']['SeriesDescription'], 'study_description': study['MainDicomTags']['StudyDescription'], 'patient': patient['MainDicomTags']['PatientName']}
            send_mail(subject, sender, recipients, body_md)
                
        success = True

    except Exception as e:
        print('common/tasks.py/STDownloadSerie')
        print(str(e))

    finally:
        return success
