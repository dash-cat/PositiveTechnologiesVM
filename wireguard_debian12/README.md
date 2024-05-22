# Install and Configure WireGuard on Debian 12

This repository contains an Ansible playbook and role to install and configure WireGuard on a Debian 12 system using official packages.

## Requirements

- Ansible installed on the host machine.
- Debian 12-based target machine with SSH access.
- Python 3 installed on the target machine.

## Inventory Setup

Create an `inventory.ini` file with the target machine's details:

```ini
[wireguard_server]
127.0.0.1 ansible_user=ansible ansible_ssh_pass=ansible ansible_sudo_pass=ansible ansible_python_interpreter=/usr/bin/python3
