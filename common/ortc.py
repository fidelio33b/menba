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

import requests
import json

from common.tasks import STDownloadStudy, STDownloadSerie

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

    #                      _                   _                  
    #   ___ ___  _ __  ___| |_ _ __ _   _  ___| |_ ___ _   _ _ __ 
    #  / __/ _ \| '_ \/ __| __| '__| | | |/ __| __/ _ \ | | | '__|
    # | (_| (_) | | | \__ \ |_| |  | |_| | (__| ||  __/ |_| | |   
    #  \___\___/|_| |_|___/\__|_|   \__,_|\___|\__\___|\__,_|_|   
    #
    
    def __init__(self, host, port, user, password, verify_cert=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.api_url = 'http://{}:{}'.format(self.host, self.port)
        self.verify_cert = verify_cert

    #                 _   _               _           
    #  _ __ ___   ___| |_| |__   ___   __| | ___  ___ 
    # | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` |/ _ \/ __|
    # | | | | | |  __/ |_| | | | (_) | (_| |  __/\__ \
    # |_| |_| |_|\___|\__|_| |_|\___/ \__,_|\___||___/
    #                                                 

    # Récupère les patients
    def GetPatients(self):

        # Pour stocker les données
        patients = None

        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Définit les en-têtes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # Définit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche des patients
            REST = '/patients'
            full_url = self.api_url + REST
            donnees = connection.get(full_url, headers=headers, verify=self.verify_cert)
            patients_list = json.loads(donnees.text)
            
            # Stocke les données
            patients = []
            
            # Parcours des patients pour obtenir les détails
            for patient_id in patients_list:

                patient = self.GetPatient(patient_id)

                if patient:
                    patients.append(patient)

        except Exception as e:
            print('oops')
            print(e)

        finally:
            return patients

    # Récupère un patient
    def GetPatient(self, patient_id):

        # Pour stocker les données
        patient = None
        
        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Définit les en-têtes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # Définit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche du patient
            REST = '/patients'
            full_url = self.api_url + REST + '/' + patient_id
            data = connection.get(full_url, headers=headers, verify=self.verify_cert)
            patient_detail = json.loads(data.text)

            # Stocke certaines données
            patient = patient_detail

        except Exception as e:
            print('oops')
            print(e)

        finally:
            return patient

    # Récupère une étude
    def GetStudy(self, study_id):

        # Pour stocker les données
        study = None
        
        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Définit les en-têtes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # Définit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche de l'étude
            REST = '/studies'
            full_url = self.api_url + REST + '/' + study_id
            data = connection.get(full_url, headers=headers, verify=self.verify_cert)
            study_details = json.loads(data.text)

            # Stocke certaines données
            study = study_details
            
        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return study

    # Récupère les études d'un patient
    def GetPatientStudies(self, patient_id):

        # Pour stocker les données
        studies = None
        
        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Récupère les données du patient (=> la liste des études)
            patient = self.GetPatient(patient_id)

            if patient:

                # Stocke les données
                studies = []
            
                # Parcours des numéros d'études du patient
                for study_id in patient['Studies']:

                    # Récupère l'étude
                    study = self.GetStudy(study_id)
                    
                    if study:
                        
                        # Stocke les données
                        studies.append(study)

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return studies

    # Récupère une série
    def GetSerie(self, serie_id):

        # Pour stocker les données
        serie = None
        
        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Définit les en-têtes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # Définit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche de la série
            REST = '/series'
            full_url = self.api_url + REST + '/' + serie_id
            data = connection.get(full_url, headers=headers, verify=self.verify_cert)
            serie_details = json.loads(data.text)

            # Stocke certaines données
            serie = serie_details
            
        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return serie

    # Récupère les séries d'une étude
    def GetStudySeries(self, study_id):

        # Pour stocker les données
        series = None
        
        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Récupère les données de l'étude (=> la liste des séries)
            study = self.GetStudy(study_id)

            if study:

                # Stocke les données
                series = []
            
                # Parcours des numéros des séries de l'étude
                for serie_id in study['Series']:

                    # Récupère la série
                    serie = self.GetSerie(serie_id)
                    
                    if serie:
                        
                        # Stocke les données
                        series.append(serie)

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return series

    # Récupère les statistiques d'utilisation
    def GetStatistics(self):

        # Pour stocker les données
        stats = None
        
        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Définit les en-têtes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # Définit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche de la série
            REST = '/statistics'
            full_url = self.api_url + REST
            data = connection.get(full_url, headers=headers, verify=self.verify_cert)
            stats_details = json.loads(data.text)

            # Stocke les données
            stats = stats_details

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return stats

    # Recherches
    def Search(self, payload):

        # Note : la recherche doit être passée en paramètre sous forme json
        #
        # Exemple :
        #
        #   payload = {'Level': 'Study', 'Query': {'RequestedProcedureDescription': 'IRM*'}, 'Expand': True}

        # Pour stocker les données
        results = None

        try:

            # Désactive les avertissements du module
            if not self.verify_cert:
                requests.packages.urllib3.disable_warnings()

            # Définit les en-têtes http
            headers = {}
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['Accept'] = 'application/json'

            # Définit la session de connexion
            connection = requests.Session()
            connection.auth = (self.user, self.password)

            # Recherche
            REST = '/tools/find'
            full_url = self.api_url + REST
            data = connection.post(full_url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), headers=headers, verify=self.verify_cert)
            results_details = json.loads(data.text)

            # Stocke les données
            results = results_details

        except Exception as e:
            print('oops')
            print(str(e))

        finally:
            return results

    # Télécharge une étude
    def DownloadStudy(self, study_id, django_user):

        # Donnera le résultat de l'opération
        success = False
        
        try:

            # Des détails
            study = None
            patient = None

            # Récupère les données de la série
            study = self.GetStudy(study_id)
            if study:
                patient = self.GetPatient(study['ParentPatient'])

            # Lance en // la tâche de récupération de l'étude
            success = STDownloadStudy.delay(self.api_url, self.verify_cert, self.user, self.password, study_id, django_user.email, study, patient)
            
        except Exception as e:
            print('common/ortc.py/DownloadStudy')
            print(str(e))

        finally:
            return success

    # Télécharge une série
    def DownloadSerie(self, serie_id, django_user):

        # Donnera le résultat de l'opération
        success = False
        
        try:

            # Des détails
            serie = None
            study = None
            patient = None

            # Récupère les données de la série
            serie = self.GetSerie(serie_id)
            if serie:
                study = self.GetStudy(serie['ParentStudy'])                
                if study:
                    patient = self.GetPatient(study['ParentPatient'])

            # Lance en // la tâche de récupération de l'étude
            success = STDownloadSerie.delay(self.api_url, self.verify_cert, self.user, self.password, serie_id, django_user.email, serie, study, patient)
            
        except Exception as e:
            print('common/ortc.py/DownloadSerie')
            print(str(e))

        finally:
            return success
