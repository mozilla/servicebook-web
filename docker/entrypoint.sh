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
  "shell"|"admin")
      /bin/bash
      ;;
  *)
      exec $ARG
      ;;
esac
