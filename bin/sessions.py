#!/usr/bin/env bash

PROJ_NAME=outsourcefactor
SITE_NAME=$PROJ_NAME.com
source /srv/www/$SITE_NAME/venv/bin/activate
cd /srv/www/$SITE_NAME/pri/venv/webroot
bin/manage.py clearsessions

exit

