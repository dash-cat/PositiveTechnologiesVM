#!/bin/zsh

# SSH_HOST="localhost"
SSH_HOST="192.168.0.100"

SSH_PORT=2222
SSH_USER="ansible"

# Array of specific files to copy
FILES_TO_COPY=(
  "software_detection/detect.py"
  "software_detection/oval_vars.xml.j2"
  "software_detection/requirements.txt"
)

# Add each JSON file in the data folder to the array
for file in data/*.json; do
  FILES_TO_COPY+=("$file")
done

echo "Will copy $FILES_TO_COPY"

REMOTE_PATH="/home/ansible/"

# Function to echo and execute a command
echoed() {
  echo "# $@"
  "$@"
}

# Copy all files in a single scp command
echoed scp -P $SSH_PORT ${FILES_TO_COPY[@]} $SSH_USER@$SSH_HOST:$REMOTE_PATH




