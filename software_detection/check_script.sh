#!/bin/bash

# Убедитесь, что скрипт запускается с правами суперпользователя
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit
fi

# Переменные
ARCHIVE_NAME="wireguard_from_official_packages_on_debian_12.tar.gz"
DIRECTORY_NAME="wireguard_from_official_packages_on_debian_12"
REQUIREMENTS_FILE="$DIRECTORY_NAME/requirements.txt"
DETECT_SCRIPT="$DIRECTORY_NAME/detect.py"

# Установите необходимые зависимости
apt-get update
apt-get install -y python3-pip

# Убедитесь, что pip обновлен
pip3 install --upgrade pip

# Перейдите в домашнюю директорию
cd ~

# Разверните архив
tar -xzf "$ARCHIVE_NAME"

# Установите зависимости
pip3 install -r "$REQUIREMENTS_FILE"

# Запустите скрипт detect.py
python3 "$DETECT_SCRIPT"

# Проверьте вывод
if [ -f "$DIRECTORY_NAME/oval_vars.xml" ]; then
  echo "WireGuard detection completed successfully."
else
  echo "WireGuard detection failed."
fi
ansible
