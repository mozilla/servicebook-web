#!/bin/bash
if [ -n "$1" ]; then
  ARG=$(echo $1|tr A-Z a-z)
else
  ARG="start"
fi

case "$ARG" in
  "start")
      supervisord -n -c /etc/supervisor/supervisord.conf
      ;;
  "test")
    export "SERVICEBOOK=http://localhost:5001/api/"
    supervisord -n -c /etc/supervisor/supervisord.conf
    ;;
  "shell"|"admin")
      /bin/bash
      ;;
  *)
      exec $ARG
      ;;
esac
