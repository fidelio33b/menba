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

from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext as _

import syslog
import uuid
import markdown2

from common.config import params

# Récupère les infos nécessaires à la connexion au serveur orthanc
def get_orthanc_server():
    
    orthanc_server = {}

    orthanc_server['name'] = params['orthanc_server']
    orthanc_server['host'] = params['orthanc_servers'][params['orthanc_server']]['host']
    orthanc_server['port'] = params['orthanc_servers'][params['orthanc_server']]['port']
    orthanc_server['user'] = params['orthanc_servers'][params['orthanc_server']]['user']
    orthanc_server['password'] = params['orthanc_servers'][params['orthanc_server']]['password']

    return orthanc_server

# Log
def zlog(msg, prefix=None, transaction_user=None, facility=None):

    # Definit les paramètres
    ident = params['app']['name']
    msg = '[{}] ({}) {}'.format(prefix, transaction_user, msg)
    if facility == None or facility == 'INFO':
        facility = syslog.LOG_INFO
    elif facility == 'WARNING':
        facility = syslog.LOG_WARNING
    elif facility == 'ERR':
        facility = syslog.LOG_ERR
    else:
        facility = syslog.LOG_WARNING

    # Positionne syslog
    syslog.openlog(ident=ident, logoption=syslog.LOG_PID, facility=syslog.LOG_INFO)

    # Log !
    syslog.syslog(msg)

    # Ferme le log
    syslog.closelog()    

#
# Envoi d'un mail
#
def send_mail(subject, sender, recipients, body, body_html=None, recipients_cc=None, attach=None, transaction_id=None, transaction_user=None):

    succes = False

    try:

        # Génère le corps au format html si nécessaire
        if body_html is None:

            body_html='''<html>
            <head>
            <META http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>test</title>
            </head>
            <body><div style="font-family:Arial, Helvetica, sans-serif; font-size:14px;">
            {}
'''.format(markdown2.markdown(body, extras=["break-on-newline", 'tables',])) + '''</div></body>
</html>
'''

        # Double format : texte et html
        email = EmailMultiAlternatives(subject, body, sender, recipients, cc=recipients_cc)
        email.attach_alternative(body_html, 'text/html')
        
        # Une pièce jointe ?     
        if attach:
            email.attach_file(attach)

        # On log l'envoi
        zlog('sending mail from {} to {}'.format(sender, recipients), transaction_id, transaction_user)

        # Envoi du mail
        email.send()

        # Est-ce ok ?
        success = True

        # Log de confirmation
        if success is True:
            zlog('success', transaction_id, transaction_user)
            
    except Exception as e:
        msg = 'common/utils.py/send_mail : {}'.str(e)
        zlog(msg, transaction_id, transaction_user, 'ERR')

    return success
