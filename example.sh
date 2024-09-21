#!/bin/bash

now=$(date)

echo "---"
echo "$now"

PIDFILE="$HOME/aicon-runner.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= | ps -p $(cat ${PIDFILE}) > /dev/null); then
  echo "aicon-runner is already running."
  exit 99
fi

echo "starting aicon-runner..."
cd $HOME/aicon-runner/
. .venv/bin/activate
python -m aicon_runner --concurrency 5 & echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"
