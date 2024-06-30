#!/bin/bash

CONTAINER_NAME="debian_container"
IMAGE_NAME="debian_ssh"
ANSIBLE_USER="ansible"
ANSIBLE_PASSWORD="ansible"
SSH_PORT=2222

if [ -z "$1" ]; then
    echo "Пожалуйста, укажите путь к плейбуку."
    echo "Использование: $0 /путь/к/playbook.yaml [--lint]"
    exit 1
fi

PLAYBOOK_PATH=$1

export ANSIBLE_CONFIG="./ansible.cfg"

if [ "$2" == "--lint" ]; then
    ansible-lint ${PLAYBOOK_PATH}
    exit 0
fi

ansible-lint ${PLAYBOOK_PATH}

HOST_IP="192.168.0.100"
echo "Host IP = $HOST_IP"

cat <<EOL > inventory.ini
[debian_container]
${HOST_IP} ansible_user=${ANSIBLE_USER} ansible_password=${ANSIBLE_PASSWORD} ansible_sudo_pass=${ANSIBLE_PASSWORD} ansible_port=${SSH_PORT} ansible_python_interpreter=/usr/bin/python3 ansible_ssh_common_args='-o StrictHostKeyChecking=no'

[all:vars]
ansible_python_interpreter=/usr/bin/python3
EOL

ANSIBLE_SUDO_PASS=${ANSIBLE_PASSWORD} ansible-playbook -i inventory.ini ${PLAYBOOK_PATH} -vvv
