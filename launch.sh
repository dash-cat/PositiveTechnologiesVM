#!/bin/bash

# Установка переменных
CONTAINER_NAME="debian_container"
IMAGE_NAME="debian_ssh"
ANSIBLE_USER="ansible"
ANSIBLE_PASSWORD="ansible"
SSH_PORT=2222

# Проверка наличия аргумента для плейбука
if [ -z "$1" ]; then
    echo "Пожалуйста, укажите путь к плейбуку."
    echo "Использование: $0 /путь/к/playbook.yaml"
    exit 1
fi

PLAYBOOK_PATH=$1

export ANSIBLE_CONFIG="./ansible.cfg"

# Линтер
ansible-lint ${PLAYBOOK_PATH}

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
ANSIBLE_SUDO_PASS=${ANSIBLE_PASSWORD} ansible-playbook -i inventory.ini ${PLAYBOOK_PATH} -vvv

#  umask 77 && mkdir -p \"` echo /home/ansible/.ansible/tmp `\"&& mkdir \"` echo /home/ansible/.ansible/tmp/ansible-tmp-1716973304.9806573-4129973-70004313624527 `\" && echo ansible-tmp-1716973304.9806573-4129973-70004313624527=\"` echo /home/ansible/.ansible/tmp/ansible-tmp-1716973304.9806573-4129973-70004313624527 `\" 


# # mkdir: cannot create directory '"/home/ansible/.ansible/tmp/ansible-tmp-1716973525.9867811-4136643-126860085612014"': No such file or directory


## ours
# umask 77 \
#   && mkdir -p \"` echo /home/ansible/.ansible/tmp `\" \
#   && mkdir /home/ansible/.ansible/tmp/ansible-tmp-1716973525.9867811-4136643-126860085612014 \
#   && echo ansible-tmp-1716973525.9867811-4136643-126860085612014=\"` echo /home/ansible/.ansible/tmp/ansible-tmp-1716973525.9867811-4136643-126860085612014 `\"

## from stackexchange
# umask 77 \
#   && mkdir -p \"` echo /tmp `\"\
#   && mkdir /tmp/ansible-tmp-1626262883.727861-210-80403864334304 \
#   && echo ansible-tmp-1626262883.727861-210-80403864334304=\"` echo /tmp/ansible-tmp-1626262883.727861-210-80403864334304 `\"


## ours
# umask 77 \
#   && mkdir -p \"` echo /tmp/ `\" \
#   && mkdir \"` echo /tmp/ansible-tmp-1716975908.4795759-13523-256169111411956 `\" \
#   && echo ansible-tmp-1716975908.4795759-13523-256169111411956=\"` echo /tmp/ansible-tmp-1716975908.4795759-13523-256169111411956 `\" 

# ssh -C -o ControlMaster=auto -o ControlPersist=60s -o Port=2222 -o 'User="ansible"' -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o 'ControlPath="/home/griggy/.ansible/cp/1867d46516"' 127.0.0.1  '/bin/sh -c mkdir /tmp/test' 
# ssh -t -C -o ControlMaster=auto -o ControlPersist=60s -o Port=2222 -o 'User="ansible"' -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o 'ControlPath="/home/griggy/.ansible/cp/1867d46516"' 127.0.0.1 /bin/sh
