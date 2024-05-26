#!/bin/bash

# Установка переменных
CONTAINER_NAME="debian_container"
IMAGE_NAME="debian_ssh"
ANSIBLE_USER="ansible"
ANSIBLE_PASSWORD="ansible"
SSH_PORT=2222

# Линтер
ansible-lint playbook.yaml

# Получение IP-адреса контейнера
HOST_IP="127.0.0.1"
echo "Host IP = $HOST_IP"

# Проверка подключения по SSH вручную
echo "Проверка подключения по SSH..."
for i in {1..10}; do
    sshpass -p ${ANSIBLE_PASSWORD} ssh -o StrictHostKeyChecking=no -p ${SSH_PORT} ${ANSIBLE_USER}@${HOST_IP} "echo SSH подключение успешно" && break
    echo "Повторная попытка подключения через 5 секунд..."
    sleep 5
done

# Создание файла инвентаря
cat <<EOL > inventory.ini
[debian_container]
${HOST_IP} ansible_user=${ANSIBLE_USER} ansible_password=${ANSIBLE_PASSWORD} ansible_sudo_pass=${ANSIBLE_PASSWORD} ansible_port=${SSH_PORT} ansible_python_interpreter=/usr/bin/python3 ansible_ssh_common_args='-o StrictHostKeyChecking=no'

[all:vars]
ansible_python_interpreter=/usr/bin/python3
EOL

# Запуск Ansible playbook
ANSIBLE_SUDO_PASS=${ANSIBLE_PASSWORD} ansible-playbook -i inventory.ini ./playbook.yaml -v
