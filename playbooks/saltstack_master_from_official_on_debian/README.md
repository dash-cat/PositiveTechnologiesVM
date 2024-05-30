# Ansible Playbook to Install SaltStack Master on Debian

This repository contains an Ansible playbook to automate the installation of SaltStack Master on a Debian system.

## Requirements

- Ansible installed on the host machine.
- A Debian-based target machine with SSH access.
- Python 3 installed on the target machine.

## Inventory Setup

Create an `inventory.ini` file with the target machine's details:

```ini
[debian_container]
127.0.0.1 ansible_user=ansible ansible_ssh_pass=ansible ansible_sudo_pass=ansible ansible_python_interpreter=/usr/bin/python3
