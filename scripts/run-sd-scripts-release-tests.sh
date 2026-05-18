#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'USAGE'
Usage:
  scripts/run-sd-scripts-release-tests.sh --image IMAGE
  scripts/run-sd-scripts-release-tests.sh

Options:
  --image IMAGE     Run the release tests inside the given Docker image.
USAGE
}

image=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --image)
            image="${2:-}"
            if [[ -z "${image}" ]]; then
                echo "Error: --image requires a Docker image tag" >&2
                exit 1
            fi
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Error: unknown argument: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [[ -n "${image}" ]]; then
    script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
    repo_dir="$(cd -- "${script_dir}/.." && pwd)"

    # Run the same checked-in script inside the image under test. The
    # repository mount is read-only because the image should provide the
    # sd-scripts checkout, while this repository only provides locked test
    # tooling and the selected pytest target list.
    docker run --rm --user root --entrypoint bash \
        -v "${repo_dir}:/tmp/release-test-project:ro" \
        "${image}" \
        /tmp/release-test-project/scripts/run-sd-scripts-release-tests.sh
    exit 0
fi

project_dir="${PROJECT_DIR:-/tmp/release-test-project}"
sd_scripts_dir="${SD_SCRIPTS_DIR:-/opt/sd-scripts}"

# Keep pytest under this repository's uv lock instead of installing an
# unpinned tool in CI. The Docker image is built with --no-dev, so only the
# dev group is added at test time. --inexact preserves the already-built
# runtime environment in /opt/python-venv instead of pruning sd-scripts
# dependencies that are not part of the dev-only sync target.
uv sync --project "${project_dir}" --frozen --only-group dev --inexact --no-install-project

cd "${sd_scripts_dir}"

# This list is the release gate for tests that can run inside the published
# image without model checkpoints, local datasets, or extra dependencies that
# the image intentionally does not bundle. Keep model-backed inpainting scripts
# and dependency-expansion tests such as test_optimizer.py in the documented
# manual/GPU validation path unless the image starts shipping their inputs.
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
