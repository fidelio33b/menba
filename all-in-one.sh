#! /bin/bash
#
#
# This file is part of Menba.
# Copyright (C) 2021
#
# Menba is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Menba is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Menba.  If not, see <https://www.gnu.org/licenses/>.
#
# Laurent Lavaud <fidelio33b@gmail.com>, 2021.

# Menba - All In One installation
#
# For use on ubuntu systems (bionic and focal tested)

function install_base {
    # Packages
    apt -y update
    apt -y install gettext python3-pip pwgen figlet

    # python modules
    pip3 install markdown2

    # Create menba group and user
    groupadd menba
    useradd -g menba -m -s /bin/bash menba
}

function install_apache {

    figlet "apache"
    
    # Packages
    apt -y install apache2 libapache2-mod-wsgi-py3

    # Add UTF-8 support :
    echo "export LANG='C.UTF-8'" >> /etc/apache2/envvars
    echo "export LC_ALL='C.UTF-8'" >> /etc/apache2/envvars

    # Conf file
    cat <<EOF > /etc/apache2/sites-available/menba.conf
<VirtualHost *:80>

  ServerName $HOST

  ErrorLog \${APACHE_LOG_DIR}/menba-error.log
  CustomLog \${APACHE_LOG_DIR}/menba-access.log combined

  Alias /robots.txt /home/menba/menba/static/robots.txt
  Alias /favicon.ico /home/menba/menba/static/favicon.ico
  Alias /static/ /home/menba/menba/static/
  Alias /media/ /home/menba/menba/media/
  Alias /files/ /var/lib/menba/files/

  WSGIDaemonProcess menba user=menba group=menba threads=25
  WSGIScriptAlias / /home/menba/menba/menba/wsgi.py process-group=menba
  WSGIProcessGroup menba
  WSGIApplicationGroup menba

  <Directory /home/menba/menba/menba>
    <Files wsgi.py>
      Require all granted
    </Files>
  </Directory>

  <Directory /home/menba/menba/static>
    Require all granted
  </Directory>

  <Directory /home/menba/menba/media>
    Require all granted
  </Directory>

  <Location "/">
    Order Deny,Allow
    <RequireAll>
      Require all granted    
    </RequireAll>
  </Location>

  <Location "/admin">
    Order Deny,Allow
    AuthType Basic
    AuthName "Restricted Content"
    AuthUserFile /etc/apache2/private/htpasswd
    Require valid-user
  </Location>

  <Location "/view">
    Order Deny,Allow
    AuthType Basic
    AuthName "Restricted Content"
    AuthUserFile /etc/apache2/private/htpasswd
    Require valid-user
  </Location>

  <Location "/search">
    Order Deny,Allow
    AuthType Basic
    AuthName "Restricted Content"
    AuthUserFile /etc/apache2/private/htpasswd
    Require valid-user
  </Location>

  <Location "/infos">
    Order Deny,Allow
    AuthType Basic
    AuthName "Restricted Content"
    AuthUserFile /etc/apache2/private/htpasswd
    Require valid-user
  </Location>

  <Location "/files">
    Order Deny,Allow
    AuthType Basic
    AuthName "Restricted Content"
    AuthUserFile /etc/apache2/private/htpasswd
    Require valid-user
  </Location>

</VirtualHost>
EOF

    # Activate the configuration
    a2dissite 000-default.conf
    a2ensite menba.conf

    # Create password file and add an account
    mkdir -p /etc/apache2/private
    chmod 700 /etc/apache2/private
    htpasswd -b -c /etc/apache2/private/htpasswd menba $MAIN_PASSWORD
    chmod 600 /etc/apache2/private/htpasswd
    chown -R www-data:www-data /etc/apache2/private
}

function install_django {

    figlet "django"
    
    # Packages
    pip3 install Django
}

function install_rabbitmq {

    figlet "rabbitmq"

    # Packages
    apt-get install curl gnupg debian-keyring debian-archive-keyring apt-transport-https -y

    ## Team RabbitMQ's main signing key
    apt-key adv --keyserver "hkps://keys.openpgp.org" --recv-keys "0x0A9AF2115F4687BD29803A206B73A36E6026DFCA"
    ## Launchpad PPA that provides modern Erlang releases
    apt-key adv --keyserver "keyserver.ubuntu.com" --recv-keys "F77F1EDA57EBB1CC"
    ## PackageCloud RabbitMQ repository
    apt-key adv --keyserver "keyserver.ubuntu.com" --recv-keys "F6609E60DC62814E"

    ## Add apt repositories maintained by Team RabbitMQ
    tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Provides modern Erlang/OTP releases
##
## "bionic" as distribution name should work for any reasonably recent Ubuntu or Debian release.
## See the release to distribution mapping table in RabbitMQ doc guides to learn more.
deb http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu ${DISTRO} main
deb-src http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu ${DISTRO} main

## Provides RabbitMQ
##
## "bionic" as distribution name should work for any reasonably recent Ubuntu or Debian release.
## See the release to distribution mapping table in RabbitMQ doc guides to learn more.
deb https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ ${DISTRO} main
deb-src https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ ${DISTRO} main
EOF

    ## Update package indices
    apt-get update -y
    
    ## Install Erlang packages
    apt-get install -y erlang-base \
            erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
            erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
            erlang-runtime-tools erlang-snmp erlang-ssl \
            erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

    ## Install rabbitmq-server and its dependencies
    apt-get install rabbitmq-server -y --fix-missing

    # Create user, vhost and associated permissions :
    rabbitmqctl add_user menba $RABBITMQ_PASSWORD
    rabbitmqctl add_vhost menba
    rabbitmqctl set_user_tags menba administrator
    rabbitmqctl set_permissions -p menba menba ".*" ".*" ".*"
}

function install_menba {

    figlet "menba"

    # Create download repository
    mkdir -p /var/lib/menba/files
    chown -R menba:menba /var/lib/menba

    # Get code
    su - menba -c "git clone https://github.com/fidelio33b/menba.git"

    # settings.py
    cat << EOF > /home/menba/menba/menba/settings.py
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

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '${DJANGO_PASSWORD}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['${HOST}']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'zhome.apps.ZHomeConfig',
    'zview.apps.ZViewConfig',
    'zsearch.apps.ZSearchConfig',
    'zinfos.apps.ZInfosConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.RemoteUserBackend',
)

ROOT_URLCONF = 'menba.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'menba.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.sqlite3',
	'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LOCALE_PATHS = [ os.path.join(BASE_DIR, 'locale'), ]
LANGUAGE_CODE = 'en-US'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

# Pour les médias
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Permissions à l'écriture des fichiers dans le répertoire média
FILE_UPLOAD_PERMISSIONS = 0o644

# Pour s'authentifier
LOGIN_URL = '/admin/login/'

# Pour les mails
EMAIL_HOST = '$EMAIL_HOST'
EMAIL_PORT = $EMAIL_PORT
EMAIL_USE_TLS = $EMAIL_USE_TLS
EMAIL_HOST_USER = '$EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = '$EMAIL_HOST_PASSWORD'

# Celery
CELERY_BROKER_URL = 'amqp://menba:${RABBITMQ_PASSWORD}@localhost:5672/menba'
CELERY_TIMEZONE = "America/New_York"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
EOF

    # wsgi.py
    cat << EOF > /home/menba/menba/menba/wsgi.py
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

path1 = '/home/menba/menba'
if path1 not in mpath:
    mpath.append(path1)

from django.core.wsgi import get_wsgi_application

menviron.setdefault('DJANGO_SETTINGS_MODULE', 'menba.settings')

application = get_wsgi_application()

from django.contrib.auth.handlers.modwsgi import check_password, groups_for_user
EOF

    # config.py
    cat << EOF > /home/menba/menba/common/config.py
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
        'version': '0.1.7',
    },
    'paginate_by': 40,
    'orthanc_server': 'conf01',
    'orthanc_servers': {
        'conf01': {
            'host': '${ORTHANC_HOST}',
            'port': ${ORTHANC_PORT},
            'user': '${ORTHANC_USER}',
            'password': '${ORTHANC_PASSWORD}',
        },
        'conf02': {
            'host': 'orthanc-server02',
            'port': 8042,
            'user': 'read-only',
            'password': 'super.secret',
        },
    },
    'stone_web_viewer': {
        'url': '${ORTHANC_PROTOCOL}://${ORTHANC_HOST}:${ORTHANC_PORT}/stone-webviewer/index.html?study=',
    },
    'web_viewer': {
        'url': '${ORTHANC_PROTOCOL}://${ORTHANC_HOST}:${ORTHANC_PORT}/web-viewer/app/viewer.html?series=',
    },
    'files': {
        'directory': '/var/lib/menba/files',
        'link': 'http://${HOST}/files',
    },
    'mail': {
        'sender': '$EMAIL_HOST_USER',
    },
}
EOF

    # Launch commands
    chown menba:menba /home/menba/menba/menba/settings.py /home/menba/menba/menba/wsgi.py /home/menba/menba/common/config.py
    su - menba -c "cd /home/menba/menba && python3 manage.py migrate"
    su - menba -c "cd menba && echo \"from django.contrib.auth.models import User; User.objects.create_user('menba', '${EMAIL_HOST_USER}', '${MAIN_PASSWORD}')\" | python3 manage.py shell"
}

function install_celery {

    figlet celery

    # Install via pip
    pip3 install -U Celery
    mkdir -p /var/log/celery /var/run/celery
    chown menba:menba /var/log/celery /var/run/celery

    # Configuration
    mkdir -p /etc/conf.d

    # celery conf
    cat <<EOF > /etc/conf.d/celery
# Name of nodes to start
# here we have a single node
CELERYD_NODES="w1"
# or we could have three nodes:
#CELERYD_NODES="w1 w2 w3"

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/usr/local/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="menba"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# How to call manage.py
CELERYD_MULTI="multi"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"

# you may wish to add these options for Celery Beat
CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
EOF

    # systemd
    cat <<EOF > /etc/systemd/system/celery.service
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=menba
Group=menba
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/home/menba/menba
ExecStartPre=+/usr/bin/mkdir -p /var/run/celery
ExecStartPre=+/usr/bin/chown menba:menba /var/run/celery
ExecStart=/bin/sh -c '\${CELERY_BIN} -A \$CELERY_APP multi start \$CELERYD_NODES \\
    --pidfile=\${CELERYD_PID_FILE} --logfile=\${CELERYD_LOG_FILE} \\
    --loglevel="\${CELERYD_LOG_LEVEL}" \$CELERYD_OPTS'
ExecStop=/bin/sh -c '\${CELERY_BIN} multi stopwait \$CELERYD_NODES \\
    --pidfile=\${CELERYD_PID_FILE} --loglevel="\${CELERYD_LOG_LEVEL}"'
ExecReload=/bin/sh -c '\${CELERY_BIN} -A \$CELERY_APP multi restart \$CELERYD_NODES \\
    --pidfile=\${CELERYD_PID_FILE} --logfile=\${CELERYD_LOG_FILE} \\
    --loglevel="\${CELERYD_LOG_LEVEL}" \$CELERYD_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Activate auto-start service :
    systemctl enable celery.service
}

function intro {
    echo "!!!"
    echo "!!! For use on ubuntu systems (bionic and focal tested) !!!"
    echo "!!!"
}

# Default parameter
DISTRO=focal
HOST=192.168.0.1
MAIN_PASSWORD=
RABBITMQ_PASSWORD=
DJANGO_PASSWORD=
ORTHANC_HOST=orthanc-server01
ORTHANC_PORT=8042
ORTHANC_PROTOCOL=http
ORTHANC_USER=read-only
ORTHANC_PASSWORD=super.secret
EMAIL_HOST=smtp.nodomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=False
EMAIL_HOST_USER=sender@nodomain.com
EMAIL_HOST_PASSWORD=super.secret

function set_parameters {
    
    # Distribution
    echo
    echo -n "ubuntu distribution (bionic or focal) [$DISTRO] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	DISTRO=$RET
    fi    
    
    # Hostname
    echo
    echo -n "hostname (fqdn or ip) [$HOST] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	HOST=$RET
    fi

    # Orthanc
    echo
    echo -n "orthanc hostname (fqdn or ip) [$ORTHANC_HOST] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	ORTHANC_HOST=$RET
    fi
    
    echo -n "orthanc port [$ORTHANC_PORT] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	ORTHANC_PORT=$RET
    fi
    
    echo -n "orthanc protocol (http or https) [$ORTHANC_PROTOCOL] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	ORTHANC_PROTOCOL=$RET
    fi
    
    echo -n "orthanc user [$ORTHANC_USER] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	ORTHANC_USER=$RET
    fi
    
    echo -n "orthanc password [$ORTHANC_PASSWORD] : "
    read RET
    if [ "$RET" != "" ]
    then
	ORTHANC_PASSWORD=$RET
    fi

    # Email
    echo
    echo -n "email host [$EMAIL_HOST] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	EMAIL_HOST=$RET
    fi

    echo -n "email port [$EMAIL_PORT] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	EMAIL_PORT=$RET
    fi

    echo -n "email use tls (True/False) [$EMAIL_USE_TLS] : "
    read RET
    RET=${RET^}
    if [ "$RET" != "" ]
    then
	EMAIL_USE_TLS=$RET
    fi

    echo -n "email host user [$EMAIL_HOST_USER] : "
    read RET
    RET=`echo $RET | tr '[:upper:]' '[:lower:]'`
    if [ "$RET" != "" ]
    then
	EMAIL_HOST_USER=$RET
    fi

    echo -n "email host password [$EMAIL_HOST_PASSWORD] : "
    read RET
    if [ "$RET" != "" ]
    then
	EMAIL_HOST_PASSWORD=$RET
    fi

    echo
}

function print_parameters {

    echo "Please note"
    echo
    echo "distribution                      $DISTRO"
    echo "hostname                          $HOST"
    echo "password for app menba user       $MAIN_PASSWORD"
    echo "password for rabbitmq menba user  $RABBITMQ_PASSWORD"
    echo
    echo "orthanc server                    $ORTHANC_HOST"
    echo "orthanc port                      $ORTHANC_PORT"
    echo "orthanc protocol                  $ORTHANC_PROTOCOL"
    echo "orthanc user                      $ORTHANC_USER"
    echo "orthanc password                  $ORTHANC_PASSWORD"
    echo
    echo "email host                        $EMAIL_HOST"
    echo "email port                        $EMAIL_PORT"
    echo "email use tls                     $EMAIL_USE_TLS"
    echo "email host user                   $EMAIL_HOST_USER"
    echo "email host password               $EMAIL_HOST_PASSWORD"
}

function generate_passwords {
    # Generate the passwords
    MAIN_PASSWORD=$(pwgen -vBn 12 1)
    RABBITMQ_PASSWORD=$(pwgen -vBn 12 1)
    DJANGO_PASSWORD=$(pwgen -vBn 64 1)
}

#                _ 
#   __ _  ___   | |
#  / _` |/ _ \  | |
# | (_| | (_) | |_|
#  \__, |\___/  (_)
#  |___/           

# Install
intro
set_parameters
install_base
generate_passwords
install_apache
install_django
install_rabbitmq
install_celery
install_menba

# Restart services
systemctl restart apache2
systemctl restart celery.service

figlet "All done !"

echo
print_parameters
echo
echo "Point your browser to http://${HOST}/ and..."

figlet "Enjoy !"
