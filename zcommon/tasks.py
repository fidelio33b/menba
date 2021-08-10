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

import os

import requests
from celery import shared_task
from django.utils.translation import gettext as _

from zcommon.config import params
from zcommon.utils import send_mail, zlog

# Timeout for to stop requests waiting for a response after a given number of seconds
#   - https://docs.python-requests.org/en/latest/user/quickstart/#timeouts
TIMEOUT_GET_REQUEST = (2, 120)


@shared_task
def STDownloadStudy(api_url, verify_cert, orthanc_user, orthanc_password, study_id, user_email, study, patient,
                    transaction_id, transaction_user):
    # Donnera le résultat de l'opération
    success = False

    try:
        # Log
        zlog('downloading study {}'.format(study_id), transaction_id, transaction_user)

        # Désactive les avertissements du module
        if not verify_cert:
            requests.packages.urllib3.disable_warnings()

        # Définit les en-têtes http
        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'
        headers['Accept'] = 'application/json'

        # Définit la session de connexion
        connection = requests.Session()
        connection.auth = (orthanc_user, orthanc_password)

        # Recherche de l'étude
        REST = '/studies'
        full_url = api_url + REST + '/' + study_id + '/archive'
        data = connection.get(full_url, headers=headers, verify=verify_cert, stream=True, timeout=TIMEOUT_GET_REQUEST)

        # Stockage du flux archive dans un fichier
        directory = params['files']['directory'] + '/' + transaction_user + '/studies'
        if not os.path.exists(directory):
            zlog('creating directory {}'.format(directory), transaction_id, transaction_user)
            os.makedirs(directory)
        filename = study_id + '.zip'
        fullpath = directory + '/' + filename
        link = params['files']['link'] + '/' + transaction_user + '/studies/' + filename
        with open(fullpath, 'wb') as fd:
            for chunk in data.iter_content(chunk_size=128):
                fd.write(chunk)

        # Log
        zlog('study succesfully downloaded', transaction_id, transaction_user)

        # Envoi du mail avec le lien de téléchargement
        if user_email is not None:
            subject = '[' + params['app']['name'] + '] - ' + 'Download link'
            sender = params['mail']['sender']
            recipients = []
            recipients.append(user_email)

            # A traduire...
            body_md = _('mail study download pitch %(link)s '
                        '%(study_description)s %(patient)s') % {'link': link,
                                                                'study_description':
                                                                    study['MainDicomTags']['StudyDescription'],
                                                                'patient': patient['MainDicomTags']['PatientName']
                                                                }

            # Envoi du mail
            send_mail(subject, sender, recipients, body_md, transaction_id=transaction_id,
                      transaction_user=transaction_user)

        success = True

    except Exception as e:
        print('zcommon/tasks.py/STDownloadStudy')
        print(str(e))

    finally:
        return success


@shared_task
def STDownloadSerie(api_url, verify_cert, orthanc_user, orthanc_password, serie_id, user_email, serie, study, patient,
                    transaction_id, transaction_user):
    # Donnera le résultat de l'opération
    success = False

    try:
        # Log
        zlog('downloading serie {}'.format(serie_id), transaction_id, transaction_user)

        # Désactive les avertissements du module
        if not verify_cert:
            requests.packages.urllib3.disable_warnings()

        # Définit les en-têtes http
        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'
        headers['Accept'] = 'application/json'

        # Définit la session de connexion
        connection = requests.Session()
        connection.auth = (orthanc_user, orthanc_password)

        # Recherche de l'étude
        REST = '/series'
        full_url = api_url + REST + '/' + serie_id + '/archive'
        data = connection.get(full_url, headers=headers, verify=verify_cert, stream=True, timeout=TIMEOUT_GET_REQUEST)

        # Stockage du flux archive dans un fichier
        directory = params['files']['directory'] + '/' + transaction_user + '/series'
        if not os.path.exists(directory):
            zlog('--> creating directory {}'.format(directory), transaction_id, transaction_user)
            os.makedirs(directory)
        filename = serie_id + '.zip'
        fullpath = directory + '/' + filename
        link = params['files']['link'] + '/' + transaction_user + '/series/' + filename
        with open(fullpath, 'wb') as fd:
            for chunk in data.iter_content(chunk_size=128):
                fd.write(chunk)

        # Log
        zlog('serie succefully downloaded', transaction_id, transaction_user)

        # Envoi du mail avec le lien de téléchargement
        if user_email is not None:
            subject = '[' + params['app']['name'] + '] - ' + 'Download link'
            sender = params['mail']['sender']
            recipients = []
            recipients.append(user_email)

            # A trduire...
            body_md = _(
                'mail serie download pitch %(link)s %(serie_description)s %(study_description)s %(patient)s') % {
                          'link': link, 'serie_description': serie['MainDicomTags']['SeriesDescription'],
                          'study_description': study['MainDicomTags']['StudyDescription'],
                          'patient': patient['MainDicomTags']['PatientName']}
            send_mail(subject, sender, recipients, body_md, transaction_id=transaction_id,
                      transaction_user=transaction_user)

        success = True

    except Exception as e:
        print('zcommon/tasks.py/STDownloadSerie')
        print(str(e))

    finally:
        return success
