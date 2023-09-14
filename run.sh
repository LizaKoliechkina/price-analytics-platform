#!/bin/sh

# load variables from .env file
while read -r line; do [[ -n "${line}" ]] && eval 'export ${line}'; done < .env

alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 80

# unset variables from .env file
while read -r line; do [[ -n "${line}" ]] && unset "$(echo "${line}" | awk -F= '{print $1}')"; done < .env
