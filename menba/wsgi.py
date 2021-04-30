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

from os import environ as menviron
from sys import path as mpath

path1 = '/home/django/mendev'
if path1 not in mpath:
    mpath.append(path1)

from django.core.wsgi import get_wsgi_application

menviron.setdefault('DJANGO_SETTINGS_MODULE', 'menba.settings')

application = get_wsgi_application()

from django.contrib.auth.handlers.modwsgi import check_password, groups_for_user
