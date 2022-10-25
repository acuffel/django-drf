
FROM ubuntu:22.04 AS builder

# Update aptitude and install some required packages
# a lot of them are required for Bio::DB::BigFile
RUN apt update
RUN apt full-upgrade -y
RUN apt install -y build-essential
RUN apt install -y git

# Python install
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHON_VERSION 3.10
ENV PYTHONIOENCODING UTF-8
RUN apt install -y python3.10-minimal python3.10-venv python3-venv


# Create default user
ARG USER_NAME docker_user
ARG USER_UID 1000
ARG USER_GID 1000
RUN groupadd ${USER_NAME} --non-unique --gid ${USER_GID}
RUN useradd ${USER_NAME} --non-unique --uid ${USER_UID} --gid ${USER_GID} --create-home --shell /bin/bash

# Install usefull tools
RUN apt install -y netcat
RUN apt install -y gettext
RUN apt install -y wget

# Create required directories
RUN mkdir -p /code/services/backend
RUN mkdir /code/services/backend/.tox
RUN mkdir /code/services/backend/media
RUN mkdir /code/services/backend/static
RUN mkdir /code/services/backend/venv
RUN chown -R ${USER_UID}:${USER_GID} /code

# Define environment variables
ENV PYTHONPATH $PATHONPATH:/code/lib

# Copy source code
WORKDIR /code
COPY . .
RUN chown -R ${USER_UID}:${USER_GID} /code

# App install
WORKDIR /code/services/backend
USER ${USER_NAME}
RUN make venv
RUN make install

# Change directory
WORKDIR /code
