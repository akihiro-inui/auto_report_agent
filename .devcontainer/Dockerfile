FROM python:3.12.7
ARG USERNAME=vscode
ARG USER_UID=1010
ARG USER_GID=$USER_UID


WORKDIR /workspace
ENV PIP_NO_CACHE_DIR=off \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    #POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.3\
    PYTHON_VERSION=3.12.7

# Install libraries and tools
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    libasound-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    gcc \
    ca-certificates\
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libffi-dev \
    llvm \
    xz-utils \
    git \
    libsqlite3-dev \
    pre-commit \
    && curl -sSL https://install.python-poetry.org | python3 -\
    && apt-get clean -y\
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (via NodeSource)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && node -v \
    && npm -v

# Clean up
RUN apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p /etc/sudoers.d \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown -R $USERNAME $POETRY_HOME


USER $USERNAME

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb

# Install Node.js

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
RUN poetry install --no-root
