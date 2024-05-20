# Use the official Debian 12 image as the base
FROM debian:12

# Set the root password
RUN echo 'root:testme' | chpasswd

# Update the package list and install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    apt-transport-https \
    ca-certificates \
    procps \
    openssh-server

# Create the privilege separation directory
RUN mkdir -p /run/sshd

# Create the keyrings directory
RUN mkdir -p /etc/apt/keyrings

# Add the SaltStack repository key
RUN curl -fsSL -o /etc/apt/keyrings/salt-archive-keyring-2023.gpg https://repo.saltproject.io/salt/py3/debian/12/amd64/SALT-PROJECT-GPG-PUBKEY-2023.gpg

# Add the SaltStack repository
RUN echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring-2023.gpg arch=amd64] https://repo.saltproject.io/salt/py3/debian/12/amd64/latest bookworm main" > /etc/apt/sources.list.d/salt.list

# Update the package list and install Salt Master
RUN apt-get update && apt-get install -y salt-master

# Expose the necessary ports
EXPOSE 4505 4506 22

# Copy SSH server configuration
COPY sshd_config /etc/ssh/sshd_config

# Copy startup script
COPY start_services.sh /usr/local/bin/start_services.sh

# Set execute permission for the startup script
RUN chmod +x /usr/local/bin/start_services.sh

# Start SSH and Salt Master services using the startup script
CMD ["/usr/local/bin/start_services.sh"]
