import syslog
import requests

from django.utils.translation import gettext as _

from time import sleep as tsleep
from celery import shared_task

from common.config import params
from common.utils import send_mail

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
        data = connection.get(full_url, headers=headers, verify=verify_cert, stream=True)

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
        data = connection.get(full_url, headers=headers, verify=verify_cert, stream=True)

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
