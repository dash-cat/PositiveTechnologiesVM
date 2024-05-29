#!/bin/zsh

SSH_HOST="localhost"
SSH_PORT=2222
SSH_USER="ansible"

FILES_TO_COPY=(
  "detect.py"
  "oval_vars.xml.j2"
  "requirements.txt"
  "../data/strongswan_from_tar_on_debian.json"
)
REMOTE_PATH="/home/ansible/"

echoed() {
  echo "# $@"
  "$@"
}

echoed scp -P $SSH_PORT ${FILES_TO_COPY[@]} $SSH_USER@$SSH_HOST:$REMOTE_PAT
