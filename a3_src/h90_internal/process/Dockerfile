# Use the official Ubuntu 22.04 as a parent image
FROM ubuntu:22.04

# Declare a build argument for the username
ARG USERNAME

# Update and install necessary libraries
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    openssh-server \
    git

# Create a new user and switch to it
RUN useradd -m ${USERNAME}
USER ${USERNAME}

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set up SSH for passwordless access to localhost
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -q -N "" \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod og-wx ~/.ssh/authorized_keys

# Set the working directory in the container
WORKDIR /home/${USERNAME}/dev