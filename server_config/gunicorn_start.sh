#!/bin/bash

NAME="iuvo_app"                                  # Name of the application
DJANGODIR=/webapps/iuvo/iuvo          # Django project directory
SOCKFILE=/webapps/iuvo/run/gunicorn.sock  # we will communicte using this unix socket
USER=iuvo_user                                        # the user to run as
GROUP=webapps                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=iuvo.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=iuvo.wsgi                     # WSGI module name
DJANGO_CONFIGURATION=Prod

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_CONFIGURATION=$DJANGO_CONFIGURATION

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE