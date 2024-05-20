#!/bin/bash

# DON'T RUN ME, this is for docker image

# Start SSH service in the background
/usr/sbin/sshd -D &

# Start Salt Master service
salt-master -l info
