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

import json
import uuid

import requests

from zcommon.tasks import STDownloadStudy, STDownloadSerie

# Timeout for to stop requests waiting for a response after a given number of seconds
#   - https://docs.python-requests.org/en/latest/user/quickstart/#timeouts
TIMEOUT_GET_REQUEST = (2, 120)


#       _
#   ___| | __ _ ___ ___  ___ 
#  / __| |/ _` / __/ __|/ _ \
# | (__| | (_| \__ \__ \  __/
#  \___|_|\__,_|___/___/\___|
#                            

class ORTC:
    #                                       _
    #  _ __   __ _ _ __ __ _ _ __ ___   ___| |_ _ __ ___  ___ 
    # | '_ \ / _` | '__/ _` | '_ ` _ \ / _ \ __| '__/ _ \/ __|
    # | |_) | (_| | | | (_| | | | | | |  __/ |_| | |  __/\__ \
    # | .__/ \__,_|_|  \__,_|_| |_| |_|\___|\__|_|  \___||___/
    # |_|

    host = None
    port = 8042
    user = None
    password = None
    api_url = None
    verify_cert = False
    transaction_id = None
    transaction_user = None

    #                      _                   _                  
    #   ___ ___  _ __  ___| |_ _ __ _   _  ___| |_ ___ _   _ _ __ 
    #  / __/ _ \| '_ \/ __| __| '__| | | |/ __| __/ _ \ | | | '__|
    # | (_| (_) | | | \__ \ |_| |  | |_| | (__| ||  __/ |_| | |   
    #  \___\___/|_| |_|___/\__|_|   \__,_|\___|\__\___|\__,_|_|   
    #

    def __init__(self, host, port, user, password, transaction_id=None, transaction_user=None, verify_cert=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.api_url = 'http://{}:{}'.format(self.host, self.port)
        self.verify_cert = verify_cert
        self.SetTransactionID(transaction_id)
        self.SetTransactionUser(transaction_user)

    #                 _   _               _           
    #  _ __ ___   ___| |_| |__   ___   __| | ___  ___ 
    # | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` |/ _ \/ __|
    # | | | | | |  __/ |_| | | | (_) | (_| |  __/\__ \
    # |_| |_| |_|\___|\__|_| |_|\___/ \__,_|\___||___/
    #

    # G??n??re un nouveau num??ro de transaction (utile dans les logs p.ex.)
    def SetNewTransactionID(self):
        self.transaction_id = str(uuid.uuid4())[:8]

    # Positionne le num??ro de transaction (utile dans les logs p.ex.)
    def SetTransactionID(self, transaction_id):
        if transaction_id is None:
            self.SetNewTransactionID()
        else:
            self.transaction_id = transaction_id

    # R??cup??re le num??ro de transaction (utile dans les logs p.ex.)
    def GetTransactionID(self):
        return self.transaction_id

    # Positionne le username pour la tra??abilit?? notamment dans syslog
    def SetTransactionUser(self, transaction_user=None):
        self.transaction_user = transaction_user

    # R??cup??re le username pour la tra??abilit?? notamment dans syslog
    def GetTransactionUser(self):
        return self.transaction_user

    # R??cup??re les patients
    def GetPatients(self):

        # Pour stocker les donn??es
        patients = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # D??finit les en-t??tes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # D??finit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche des patients
            REST = '/patients'
            full_url = self.api_url + REST
            data = connection.get(full_url, headers=headers, verify=self.verify_cert, timeout=TIMEOUT_GET_REQUEST)
            patients_list = json.loads(data.text)

            # Stocke les donn??es
            patients = []

            # Parcours des patients pour obtenir les d??tails
            for patient_id in patients_list:

                patient = self.GetPatient(patient_id)

                if patient:
                    patients.append(patient)

        except Exception as e:
            print('oops')
            print(e)

        finally:
            return patients

    # R??cup??re un patient
    def GetPatient(self, patient_id):

        # Pour stocker les donn??es
        patient = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # D??finit les en-t??tes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # D??finit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche du patient
            REST = '/patients'
            full_url = self.api_url + REST + '/' + patient_id
            data = connection.get(full_url, headers=headers, verify=self.verify_cert, timeout=TIMEOUT_GET_REQUEST)
            patient_detail = json.loads(data.text)

            # Stocke certaines donn??es
            patient = patient_detail

        except Exception as e:
            print('oops')
            print(e)

        finally:
            return patient

    # R??cup??re une ??tude
    def GetStudy(self, study_id):

        # Pour stocker les donn??es
        study = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # D??finit les en-t??tes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # D??finit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche de l'??tude
            REST = '/studies'
            full_url = self.api_url + REST + '/' + study_id
            data = connection.get(full_url, headers=headers, verify=self.verify_cert, timeout=TIMEOUT_GET_REQUEST)
            study_details = json.loads(data.text)

            # Stocke certaines donn??es
            study = study_details

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return study

    # R??cup??re les ??tudes d'un patient
    def GetPatientStudies(self, patient_id):

        # Pour stocker les donn??es
        studies = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # R??cup??re les donn??es du patient (=> la liste des ??tudes)
            patient = self.GetPatient(patient_id)

            if patient:

                # Stocke les donn??es
                studies = []

                # Parcours des num??ros d'??tudes du patient
                for study_id in patient['Studies']:

                    # R??cup??re l'??tude
                    study = self.GetStudy(study_id)

                    if study:
                        # Stocke les donn??es
                        studies.append(study)

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return studies

    # R??cup??re une s??rie
    def GetSerie(self, serie_id):

        # Pour stocker les donn??es
        serie = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # D??finit les en-t??tes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # D??finit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche de la s??rie
            REST = '/series'
            full_url = self.api_url + REST + '/' + serie_id
            data = connection.get(full_url, headers=headers, verify=self.verify_cert, timeout=TIMEOUT_GET_REQUEST)
            serie_details = json.loads(data.text)

            # Stocke certaines donn??es
            serie = serie_details

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return serie

    # R??cup??re les s??ries d'une ??tude
    def GetStudySeries(self, study_id):

        # Pour stocker les donn??es
        series = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # R??cup??re les donn??es de l'??tude (=> la liste des s??ries)
            study = self.GetStudy(study_id)

            if study:

                # Stocke les donn??es
                series = []

                # Parcours des num??ros des s??ries de l'??tude
                for serie_id in study['Series']:

                    # R??cup??re la s??rie
                    serie = self.GetSerie(serie_id)

                    if serie:
                        # Stocke les donn??es
                        series.append(serie)

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return series

    # R??cup??re les statistiques d'utilisation
    def GetStatistics(self):

        # Pour stocker les donn??es
        stats = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # D??finit les en-t??tes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # D??finit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche des statistiques
            REST = '/statistics'
            full_url = self.api_url + REST
            data = connection.get(full_url, headers=headers, verify=self.verify_cert, timeout=TIMEOUT_GET_REQUEST)
            formatted_data = json.loads(data.text)

            # Stocke les donn??es
            stats = formatted_data

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return stats

    # R??cup??re les informations concernant le serveur
    def GetSystemInfos(self):

        # Pour stocker les donn??es
        infos = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # D??finit les en-t??tes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # D??finit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche des informations
            REST = '/system'
            full_url = self.api_url + REST
            data = connection.get(full_url, headers=headers, verify=self.verify_cert, timeout=TIMEOUT_GET_REQUEST)
            formatted_data = json.loads(data.text)

            # Stocke les donn??es
            infos = formatted_data

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return infos

    # Recherches
    def Search(self, payload):

        # Note : la recherche doit ??tre pass??e en param??tre sous forme json
        #
        # Exemple :
        #
        #   payload = {'Level': 'Study', 'Query': {'RequestedProcedureDescription': 'IRM*'}, 'Expand': True}

        # Pour stocker les donn??es
        results = None

        try:

            # D??sactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # D??finit les en-t??tes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # D??finit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche
            REST = '/tools/find'
            full_url = self.api_url + REST
            data = connection.post(full_url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                                   headers=headers, verify=self.verify_cert, timeout=TIMEOUT_GET_REQUEST)
            results_details = json.loads(data.text)

            # Stocke les donn??es
            results = results_details

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return results

    # T??l??charge une ??tude
    def DownloadStudy(self, study_id, django_user):

        # Donnera le r??sultat de l'op??ration
        success = False

        try:

            # Des d??tails
            study = None
            patient = None

            # R??cup??re les donn??es de la s??rie
            study = self.GetStudy(study_id)
            if study:
                patient = self.GetPatient(study['ParentPatient'])

            # Lance en // la t??che de r??cup??ration de l'??tude
            success = STDownloadStudy.delay(self.api_url, self.verify_cert, self.user, self.password, study_id,
                                            django_user.email, study, patient, self.transaction_id,
                                            self.transaction_user)

        except Exception as e:
            print('zcommon/ortc.py/DownloadStudy')
            print(str(e))

        finally:
            return success

    # T??l??charge une s??rie
    def DownloadSerie(self, serie_id, django_user):

        # Donnera le r??sultat de l'op??ration
        success = False

        try:

            # Des d??tails
            serie = None
            study = None
            patient = None

            # R??cup??re les donn??es de la s??rie
            serie = self.GetSerie(serie_id)
            if serie:
                study = self.GetStudy(serie['ParentStudy'])
                if study:
                    patient = self.GetPatient(study['ParentPatient'])

            # Lance en // la t??che de r??cup??ration de l'??tude
            success = STDownloadSerie.delay(self.api_url, self.verify_cert, self.user, self.password, serie_id,
                                            django_user.email, serie, study, patient, self.transaction_id,
                                            self.transaction_user)

        except Exception as e:
            print('zcommon/ortc.py/DownloadSerie')
            print(str(e))

        finally:
            return success
