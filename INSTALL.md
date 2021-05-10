# Menba - All In One installation

You will find an auto-install script `all-in-one.sh`, that let you install automatically an "all in one" server based on :
- apache web server
- rabbitmq amqp broker
- celery
- django

This script is for ubuntu systems only (bionic and focal tested), but may be adapted to work on other distros.

Of course, someone could split some parts of the solution afterwards to distribute load, like rabbitmq server for example.

Last, but not the least, security should be hardened by enabling ssl, but this is out of the scope of this document.
