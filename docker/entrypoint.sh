#!/bin/bash
if [ -n "$1" ]; then
  ARG=$(echo $1|tr A-Z a-z)
else
  ARG="start"
fi

case "$ARG" in
  "start")
      sleep 3 && supervisord -n
      ;;
  "test")
    export "SERVICEBOOK=http://localhost:5001/api/"
    sleep 3 && supervisord -n
    ;;
  "shell"|"admin")
      /bin/bash
      ;;
  *)
      exec $ARG
      ;;
esac
