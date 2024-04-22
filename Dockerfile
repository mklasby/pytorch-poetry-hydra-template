FROM nvcr.io/nvidia/pytorch:24.02-py3

ARG USERNAME=<<user>>
ARG WORKING_DIR=<<working-dir>>
ARG POETRY_VERSION=<<poetry-version>>

SHELL ["/bin/bash", "-c"]

# Install git/ssh/tmux
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y git ssh curl unzip

# Install poetry
# https://python-poetry.org/docs/configuration/#using-environment-variables
USER ${USERNAME}
ENV POETRY_VERSION="${POETRY_VERSION}" \
    POETRY_HOME="/home/${USERNAME}/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    WORKING_DIR=${WORKING_DIR} \
    PATH="/home/${USERNAME}/poetry/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 - && exec bash

# Install project requirements without dev dep.
RUN mkdir -p ${WORKING_DIR}
WORKDIR ${WORKING_DIR} 
COPY ./ ./
RUN pip install --upgrade pip && \
    poetry install -vvv --without dev --no-cache

WORKDIR $WORKING_DIR
