# TODO: Update prod / replica container
FROM nvcr.io/nvidia/pytorch:24.02-py3

ARG USERNAME=<<user>>
ARG WORKING_DIR=<<working-dir>>
ARG USER_UID=<<uid>>
ARG USER_GID=<<gid>>

SHELL ["/bin/bash", "-c"]

# Create the user
RUN groupadd --gid $USER_GID ${USERNAME} \
    && useradd --uid $USER_UID --gid $USER_GID -m ${USERNAME}

# Install git/ssh/tmux
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y git ssh curl unzip

FROM dev-container-base AS poetry-base
# Install poetry
# https://python-poetry.org/docs/configuration/#using-environment-variables
ARG USERNAME
ARG WORKING_DIR
ARG USER_UID
ARG USER_GID
USER ${USERNAME}
ENV POETRY_VERSION="1.6.1" \
    POETRY_HOME="/home/${USERNAME}/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    VENV_PATH="${WORKING_DIR}/.venv" \
    NVIDIA_DRIVER_CAPABILITIES="all" \
    WORKING_DIR=${WORKING_DIR} \
    PATH="/home/${USERNAME}/.local/bin:${PATH}" \
    VIRTUAL_ENV=$VENV_PATH

ENV PATH="$VENV_PATH/bin:$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - && exec bash

# Install project requirements 
RUN mkdir ${WORKING_DIR}/ && \
    chown -R ${USER_UID}:${USER_GID} ${WORKING_DIR} && \
    chmod -R a+rX ${WORKING_DIR}
WORKDIR ${WORKING_DIR}
COPY --chown=${USER_UID}:${USER_GID} . ${WORKING_DIR}
RUN mkdir ${VENV_PATH}/ && \
    chown -R ${USER_UID}:${USER_GID} ${VENV_PATH} && \
    chmod -R a+rX ${VENV_PATH}
RUN python -m venv .venv && \ 
    source .venv/bin/activate && \
    pip install --upgrade pip && \
    poetry install -vvv && \
    pip install sparseprop && \
    echo "source ${VENV_PATH}/bin/activate" >> /home/$USERNAME/.bashrc

# Install TorchLib for cpp dependicies
RUN wget https://download.pytorch.org/libtorch/cu118/libtorch-shared-with-deps-2.0.1%2Bcu118.zip && \
    unzip ./libtorch-shared-with-deps-2.0.1+cu118.zip


# Build coco API  TODO: Figure out why this wont build! 
WORKDIR ${BUILD_PATH}/src/cocoapi/PythonAPI
# RUN sudo ln -s ${VENV_PATH}/bin/python python && sudo make && sudo make install

WORKDIR $WORKING_DIR
CMD bash
