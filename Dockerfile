# syntax=docker/dockerfile:1
ARG BASE_IMAGE=nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
ARG PYTHON_VERSION=3.10
ARG UV_VERSION=0.9

# Download uv binary stage
FROM "ghcr.io/astral-sh/uv:${UV_VERSION}" AS uv-reference

# Build uv and Python base stage
FROM "${BASE_IMAGE}" AS uv-python-base

ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

ENV PYTHONUNBUFFERED=1

ARG UV_VERSION
COPY --from=uv-reference /uv /uvx /bin/

ENV UV_PYTHON_CACHE_DIR="/uv_python_cache"
ENV UV_PYTHON_INSTALL_DIR="/opt/python"
ENV PATH="${UV_PYTHON_INSTALL_DIR}/bin:${PATH}"

ARG PYTHON_VERSION
RUN --mount=type=cache,target=/uv_python_cache <<EOF
    uv python install "${PYTHON_VERSION}"
EOF

# Download sd-scripts source code stage
FROM "${BASE_IMAGE}" AS download-sd-scripts

ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

RUN --mount=type=cache,sharing=private,target=/var/cache/apt \
    --mount=type=cache,sharing=private,target=/var/lib/apt/lists <<EOF
    apt-get update
    apt-get install -y --no-install-recommends \
        git \
        ca-certificates
EOF

ARG SD_SCRIPTS_URL=https://github.com/kohya-ss/sd-scripts
ARG SD_SCRIPTS_VERSION=206adb643848ff27894f1e72b6987fa66db99378

RUN <<EOF
    mkdir -p /opt/sd-scripts

    cd /opt/sd-scripts
    git init
    git remote add origin "${SD_SCRIPTS_URL}"
    git fetch --depth 1 origin "${SD_SCRIPTS_VERSION}"
    git checkout FETCH_HEAD
    git submodule update --init --recursive
EOF


# Build Python virtual environment stage
FROM uv-python-base AS build-venv

#  uv configuration
# - Generate bytecodes
# - Copy packages into virtual environment
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install Python dependencies
COPY ./pyproject.toml uv.lock /opt/sd-scripts-venv-build/
RUN --mount=type=cache,target=/root/.cache/uv <<EOF
    cd /opt/sd-scripts-venv-build/

    UV_PROJECT_ENVIRONMENT="/opt/python_venv" uv sync --frozen --no-dev --no-editable --no-install-project
EOF


# Runtime stage
FROM uv-python-base AS runtime

RUN --mount=type=cache,sharing=private,target=/var/cache/apt \
    --mount=type=cache,sharing=private,target=/var/lib/apt/lists <<EOF
    apt-get update
    apt-get install -y --no-install-recommends \
        tk \
        libglib2.0-0 \
        libgl1-mesa-glx
EOF

# libnvrtc.so workaround
# https://github.com/aoirint/sd-scripts-docker/issues/19
RUN <<EOF
    ln -s \
        /usr/local/cuda-11.8/targets/x86_64-linux/lib/libnvrtc.so.11.2 \
        /usr/local/cuda-11.8/targets/x86_64-linux/lib/libnvrtc.so
EOF

# Copy Python virtual environment from build stage
COPY --from=build-venv /opt/python_venv /opt/python_venv
ENV PATH="/opt/python_venv/bin:${PATH}"

# Copy application code
COPY --from=download-sd-scripts /opt/sd-scripts /opt/sd-scripts

# Install project and Pre-compile Python bytecode
RUN <<EOF
    cd /opt/sd-scripts

    pip3 install --no-deps .

    python -m compileall .
EOF

# huggingface cache dir
ENV HF_HOME=/huggingface

RUN <<EOF
    # create huggingface cache dir
    mkdir -p /huggingface

    # create accelerate cache dir
    mkdir -p /huggingface/accelerate

    tee /huggingface/accelerate/default_config.yaml <<EOT
command_file: null
commands: null
compute_environment: LOCAL_MACHINE
deepspeed_config: {}
distributed_type: 'NO'
downcast_bf16: 'no'
dynamo_backend: 'NO'
fsdp_config: {}
gpu_ids: all
machine_rank: 0
main_process_ip: null
main_process_port: null
main_training_function: main
megatron_lm_config: {}
mixed_precision: fp16
num_machines: 1
num_processes: 1
rdzv_backend: static
same_network: true
tpu_name: null
tpu_zone: null
use_cpu: false
EOT

    # writable by default execution user
    chown -R "1000:1000" /huggingface
EOF

WORKDIR /opt/sd-scripts
USER "1000:1000"

ENTRYPOINT [ "accelerate", "launch" ]
