#!/bin/zsh

SSH_HOST="localhost"
SSH_PORT=2222
SSH_USER="ansible"

FILES_TO_COPY=(
  "software_detection/detect.py"
  "software_detection/oval_vars.xml.j2"
  "software_detection/requirements.txt"
  "data/keycloak_from_zip_on_debian.json"
  "data/strongswan_from_tar_on_debian.json"
  "data/nginx_unit_from_official_package_on_debian.json"
)
REMOTE_PATH="/home/ansible/"

echoed() {
  echo "# $@"
  "$@"
}

echoed scp -P $SSH_PORT ${FILES_TO_COPY[@]} $SSH_USER@$SSH_HOST:$REMOTE_PAT
