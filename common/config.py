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

params = {
    'app': {
        'name': 'Menba',
    },
    'paginate_by': 40,
    'orthanc_server': 'dcm01',
    'orthanc_servers': {
        'dcm01': {
            'host': 'dcm01',
            'port': 8042,
            'user': 'echanges',
            'password': 'sie-n3vuyae4',
        },
        'dcm02': {
            'host': 'dcm02',
            'port': 8042,
            'user': 'echanges',
            'password': 'sie-n3vuyae4',
        },
    },
    'stone_web_viewer': {
        'url': 'http://10.0.17.12:8042/stone-webviewer/index.html?study=',
    },
    'web_viewer': {
        'url': 'http://10.0.17.12:8042/web-viewer/app/viewer.html?series=',
    },
    'files': {
        'directory': {
            'studies' : '/var/lib/mendev/files/studies',
            'series' :  '/var/lib/mendev/files/series',
        },
        'link': {
            'studies' : 'http://10.0.17.18/files/studies',
            'series' :  'http://10.0.17.18/files/series',
        },
    },
    'mail': {
        'sender': 'noreply@orange.fr',
    },
}
