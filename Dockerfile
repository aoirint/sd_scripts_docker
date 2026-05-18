# syntax=docker/dockerfile:1

ARG CUDA_RUNTIME_IMAGE=nvidia/cuda:12.9.1-cudnn-runtime-ubuntu24.04@sha256:d02c4310b6d57ca0b16cd80298bdb33a74187baafe2eccd8a6a16180ddc90802
ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.11.13@sha256:841c8e6fe30a8b07b4478d12d0c608cba6de66102d29d65d1cc423af86051563
ARG PYTHON_VERSION=3.10.19
ARG SD_SCRIPTS_URL=https://github.com/kohya-ss/sd-scripts
ARG SD_SCRIPTS_VERSION=a1b48df430a3690aeb5c9b6e7b19025afe8fb518

FROM ${UV_IMAGE} AS uv

FROM ${CUDA_RUNTIME_IMAGE} AS builder
SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

ARG PYTHON_VERSION
ARG SD_SCRIPTS_URL
ARG SD_SCRIPTS_VERSION

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_PROGRESS=1 \
    UV_CACHE_DIR=/root/.cache/uv \
    UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_PROJECT_ENVIRONMENT=/opt/python-venv \
    PATH=/opt/python-venv/bin:/opt/python/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked <<'SH'
    apt-get update

    apt-get install -y --no-install-recommends \
        ca-certificates=20240203 \
        git=1:2.43.0-1ubuntu7.3
SH

COPY --from=uv /uv /usr/local/bin/uv

WORKDIR /opt/sd-scripts-venv-build

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked <<SH
    uv python install "${PYTHON_VERSION}"
    uv sync --frozen --no-dev --no-editable --no-install-project --python "${PYTHON_VERSION}"
SH

WORKDIR /opt/sd-scripts

RUN <<SH
    git init
    git remote add origin "${SD_SCRIPTS_URL}"
    git fetch --depth 1 origin "${SD_SCRIPTS_VERSION}"
    git checkout --detach FETCH_HEAD
    git submodule update --init --recursive
SH


FROM ${CUDA_RUNTIME_IMAGE} AS runtime
SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_NO_PROGRESS=1 \
    UV_CACHE_DIR=/root/.cache/uv \
    UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_PROJECT_ENVIRONMENT=/opt/python-venv \
    PATH=/opt/python-venv/bin:/opt/python/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    HF_HOME=/huggingface

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked <<'SH'
    apt-get update

    apt-get install -y --no-install-recommends \
        ca-certificates=20240203 \
        libgl1=1.7.0-1build1 \
        libglib2.0-0t64=2.80.0-6ubuntu3.8 \
        tk=8.6.14build1
SH

COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /opt/python /opt/python
COPY --from=builder /opt/python-venv /opt/python-venv
COPY --from=builder /opt/sd-scripts /opt/sd-scripts

WORKDIR /opt/sd-scripts

# libnvrtc.so workaround
# https://github.com/aoirint/sd-scripts-docker/issues/19
RUN <<'SH'
    ln -s \
        /usr/local/cuda-12.9/targets/x86_64-linux/lib/libnvrtc.so.12 \
        /usr/local/cuda-12.9/targets/x86_64-linux/lib/libnvrtc.so
SH

# Install project and Pre-compile Python bytecode
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked <<'SH'
    uv pip install --editable .
    python -m compileall .
SH

RUN <<'SH'
    groupadd -o -g 1000 trainer
    useradd -m -o -u 1000 -g 1000 -s /bin/bash trainer
    mkdir -p /huggingface
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

    chown -R trainer:trainer /huggingface /opt/sd-scripts
SH

USER trainer

ENTRYPOINT ["accelerate", "launch"]
