#!/bin/bash
  set -e
  LOGFILE=/var/www/pman/data/www/allvbgru/hello.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=3
  # user/group to run as
  test -d $LOGDIR || mkdir -p $LOGDIR
  exec gunicorn_django -w $NUM_WORKERS --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE
