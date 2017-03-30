#!/bin/bash
if [ -n "$1" ]; then
  ARG=$(echo $1|tr A-Z a-z)
else
  ARG="start"
fi

case "$ARG" in
  "start")
      supervisord -n
      ;;
  "test")
    export "SERVICEBOOK=http://localhost:5001/api/"
    supervisord -n
    ;;
  "shell"|"admin")
      /bin/bash
      ;;
  *)
      exec $ARG
      ;;
esac
