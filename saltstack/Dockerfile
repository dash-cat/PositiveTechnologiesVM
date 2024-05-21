# Use the official Debian 12 image as the base
FROM debian:12

# Set the root password
RUN echo 'root:testme' | chpasswd

# Update the package list and install dependencies, including Python
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    apt-transport-https \
    ca-certificates \
    procps \
    openssh-server \
    sudo \
    sshpass \
    python3 \
    python3-pip

# Create the privilege separation directory
RUN mkdir -p /run/sshd

# Create a user for Ansible with sudo privileges
RUN useradd -m -s /bin/bash ansible && echo 'ansible:ansible' | chpasswd && adduser ansible sudo

# Expose the necessary ports
EXPOSE 22

# Copy SSH server configuration
COPY sshd_config /etc/ssh/sshd_config

# Copy startup script
COPY start_services.sh /usr/local/bin/start_services.sh

# Set execute permission for the startup script
RUN chmod +x /usr/local/bin/start_services.sh

# Start SSH service using the startup script
CMD ["/usr/local/bin/start_services.sh"]
