#!/bin/bash

set -eo pipefail

if ! type "faas-cli" &> /dev/null
then
  echo -e "faas-cli not available\n"
  exit
fi

usage() {
  echo -e "Usage: $0 [--file file] [--publish]\n"
}

while [ ! $# -eq 0 ]
do
  case "$1" in
    --file | -f)
      if [ -n "$2" ]; then
        FILE_ARG=$2
        shift
      else
        usage
        exit
      fi
      ;;
    --publish | -p)
      PUBLISH=1
      ;;
    *)
      usage
      exit
  esac
  shift
done

echo "Fetching OpenFaaS templates ...\n"
faas-cli template pull
faas-cli template store pull python3-flask

shopt -s nullglob
for i in ${FILE_ARG:-*}.y*ml; do
  faas-cli build -f "$i"

  if [ "$PUBLISH" == 1 ]; then
    faas-cli publish -f "$i" --platforms linux/arm64,linux/arm,linux/amd64
  fi
done
