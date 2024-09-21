#!/bin/bash

now=$(date)

PIDFILE="$HOME/aicon-runner.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= | ps -p $(cat ${PIDFILE}) > /dev/null); then
  echo "$now: aicon-runner is already running."
  exit
fi

echo "$now: starting aicon-runner..."
cd $HOME/aicon-runner/
. .venv/bin/activate
python -m aicon_runner --concurrency 5 & echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"
