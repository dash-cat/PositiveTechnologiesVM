#!/bin/bash

# DON'T RUN ME, this is for docker image

# Start SSH service
service ssh start

# Keep the container running
tail -f /dev/null

# # Start SSH service in the background
# /usr/sbin/sshd -D &
