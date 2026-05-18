#!/usr/bin/env bash
set -euo pipefail

project_dir="${PROJECT_DIR:-/tmp/release-test-project}"
sd_scripts_dir="${SD_SCRIPTS_DIR:-/opt/sd-scripts}"

uv sync --project "${project_dir}" --frozen --only-group dev --inexact --no-install-project

cd "${sd_scripts_dir}"

pytest -q \
    tests/test_custom_offloading_utils.py \
    tests/test_expand_unet_to_inpainting.py \
    tests/test_fine_tune.py \
    tests/test_flux_train.py \
    tests/test_flux_train_network.py \
    tests/test_lumina_train_network.py \
    tests/test_mask_generator.py \
    tests/test_sd3_train.py \
    tests/test_sd3_train_network.py \
    tests/test_sdxl_train.py \
    tests/test_sdxl_train_leco.py \
    tests/test_sdxl_train_network.py \
    tests/test_train.py \
    tests/test_train_leco.py \
    tests/test_train_network.py \
    tests/test_train_textual_inversion.py \
    tests/test_validation.py \
    tests/library
