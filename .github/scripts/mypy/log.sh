#!/usr/bin/env bash

while read -r line; do
  if [[ "$line" =~ ^([^:]+):([0-9]+):\ (\w+):\ (.*)$ ]]; then
    loglevel="notice"
    [[ "${BASH_REMATCH[3]}" == "error" ]] && loglevel="error"
    echo "::${loglevel} file=${BASH_REMATCH[1]},line=${BASH_REMATCH[2]}::${BASH_REMATCH[4]}"
  fi
  echo "$line"
done
