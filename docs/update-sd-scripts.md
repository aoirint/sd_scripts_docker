# Updating sd-scripts

This document describes the repeatable process for updating the
`kohya-ss/sd-scripts` version used by this Docker image and verifying that the
resulting image still starts and imports the expected training dependencies.

Use this procedure for routine sd-scripts updates, PyTorch or CUDA refreshes,
dependency lockfile refreshes, and Docker image validation.

## Scope

The update normally touches these files:

- `Dockerfile`
- `pyproject.toml`
- `uv.lock`
- `README.md`

The repository uses `pyproject.toml` as the local dependency declaration, but
the source of truth for sd-scripts runtime dependencies is the upstream
`requirements.txt` at the selected sd-scripts commit.

This image also carries a few local bundled dependencies that may not be active
in upstream `requirements.txt`:

- BLIP captioning dependencies used by `finetune/make_captions.py`.
- WD14 ONNX captioning dependencies used by
  `finetune/tag_images_by_wd14_tagger.py --onnx`.
- `open-clip-torch` for SDXL-related workflows.
- `lycoris-lora` as an additional bundled network package.

Keep those local extras unless the README and supported image behavior are
updated at the same time.

## Prerequisites

Install or make available:

- Git
- Docker Engine with BuildKit
- `uv`
- `hadolint`

The validation commands below assume the image name
`sd-scripts:update-test`. Use another temporary tag if that tag is already
meaningful in your local environment.

## 1. Prepare The Update Worktree

Start from the latest `main` branch and create a focused update worktree:

```shell
git fetch origin main
git worktree add -b update-sd-scripts-vX.Y.Z .agents/worktrees/update-sd-scripts-vX.Y.Z origin/main
cd .agents/worktrees/update-sd-scripts-vX.Y.Z
```

If the branch or worktree already exists, inspect it before reusing it:

```shell
git status --short
git log --oneline --decorate -5
```

Keep the update PR focused on the sd-scripts, dependency, Dockerfile, and
documentation changes needed for the selected version. Do not update `VERSION`
in the same PR unless the PR is intentionally publishing a Docker image
release.

## 2. Select The Target Version

List upstream version tags:

```shell
git ls-remote --tags https://github.com/kohya-ss/sd-scripts.git 'refs/tags/v*'
```

For a candidate tag, fetch the exact commit and release date:

```shell
git clone --filter=blob:none --no-checkout https://github.com/kohya-ss/sd-scripts.git /tmp/sd-scripts-upstream
git -C /tmp/sd-scripts-upstream fetch --tags origin
git -C /tmp/sd-scripts-upstream show --no-patch --format='%H %ci %s' vX.Y.Z
```

Only adopt an sd-scripts release after the repository cooldown window has
passed. The current baseline is a minimum of 7 days after the upstream release
timestamp or tag commit timestamp.

Record the selected commit SHA. Prefer the tag commit for released versions
instead of a branch name.

## 3. Read Upstream Requirements

Print the upstream requirements and relevant installation notes for the
selected version:

```shell
git -C /tmp/sd-scripts-upstream show vX.Y.Z:requirements.txt
git -C /tmp/sd-scripts-upstream show vX.Y.Z:README.md | sed -n '/About requirements.txt and PyTorch/,+20p'
```

Update `pyproject.toml` so its `[project].dependencies` match the active
dependencies in upstream `requirements.txt`, translated to valid PEP 508
strings.

Keep the comment above the first dependency pointed at the exact upstream
commit, for example:

```toml
# https://github.com/kohya-ss/sd-scripts/blob/<commit-sha>/requirements.txt
```

When translating requirements:

- Keep pinned versions exactly pinned.
- Keep lower bounds and compatible-release specifiers as upstream writes them.
- Do not copy `-e .`; the Dockerfile installs sd-scripts itself after the
  source checkout.
- Preserve local extras that this image documents or intentionally bundles.
- If an upstream dependency is commented out, include it only when this image
  still needs it for documented behavior.
- If a local extra conflicts with the refreshed dependency graph, prefer a
  compatible newer version of the local extra over dropping the feature.
- Preserve `[tool.uv] exclude-newer = "P7D"`.

## 4. Choose PyTorch, CUDA, And xformers

sd-scripts does not list PyTorch in `requirements.txt` because the correct
wheel depends on the CUDA target. Read the selected upstream README and choose
the PyTorch stack that matches this image's supported GPU generation.

For RTX 50 series support, use the upstream-recommended PyTorch and CUDA line
when available. For example, PyTorch 2.8.0 with CUDA 12.9 uses:

```toml
"torch==2.8.0+cu129",
"torchvision==0.23.0+cu129",
"xformers==0.0.32.post2",
```

and:

```toml
[[tool.uv.index]]
name = "pytorch-cu129"
url = "https://download.pytorch.org/whl/cu129"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cu129" }
torchvision = { index = "pytorch-cu129" }
xformers = { index = "pytorch-cu129" }
```

Before locking, confirm that the selected wheels exist for Python 3.10 and
Linux x86_64:

```shell
curl -fsSL https://download.pytorch.org/whl/cu129/torch/ | \
  rg 'torch-2\.8\.0\+cu129-cp310-cp310-.*x86_64'

curl -fsSL https://download.pytorch.org/whl/cu129/torchvision/ | \
  rg 'torchvision-0\.23\.0\+cu129-cp310-cp310-.*x86_64'

curl -fsSL https://download.pytorch.org/whl/cu129/xformers/ | \
  rg 'xformers-0\.0\.32\.post2-.*x86_64'
```

If the upstream README recommends a different CUDA line, replace `cu129`,
package versions, and the `pytorch-cu129` index name consistently.

## 5. Update The Dockerfile

Set `SD_SCRIPTS_VERSION` to the selected upstream commit:

```dockerfile
ARG SD_SCRIPTS_VERSION=<commit-sha>
```

Keep base images pinned by digest:

```dockerfile
ARG CUDA_RUNTIME_IMAGE=nvidia/cuda:<tag>@sha256:<digest>
ARG UV_IMAGE=ghcr.io/astral-sh/uv:<tag>@sha256:<digest>
```

To refresh a base image digest, inspect the image:

```shell
docker buildx imagetools inspect nvidia/cuda:<tag>
docker buildx imagetools inspect ghcr.io/astral-sh/uv:<tag>
```

Use the multi-architecture index digest unless the image is intentionally
limited to one platform.

Keep apt packages version-pinned so `hadolint` can verify the Dockerfile. To
find apt candidate versions for the pinned CUDA runtime image:

```shell
docker run --rm 'nvidia/cuda:<tag>@sha256:<digest>' bash -lc \
  'set -euo pipefail; apt-get update >/dev/null; apt-cache policy ca-certificates git libgl1 libglib2.0-0t64 tk'
```

Package names can change between Ubuntu releases. For Ubuntu 24.04, use
`libgl1` and `libglib2.0-0t64` instead of the older Ubuntu 22.04 package names
`libgl1-mesa-glx` and `libglib2.0-0`.

If the CUDA major or minor version changes, verify the `libnvrtc.so` workaround
path before editing it:

```shell
docker run --rm 'nvidia/cuda:<tag>@sha256:<digest>' bash -lc \
  'ls -l /usr/local/cuda-*/targets/x86_64-linux/lib/libnvrtc.so*'
```

Then update both the source and destination paths in the Dockerfile.

## 6. Refresh `uv.lock`

Run lockfile resolution from the repository root or the update worktree:

```shell
uv lock --upgrade
```

After the lockfile update, verify it is consistent:

```shell
uv lock --check
```

Review the resolver output and `uv.lock` diff for unexpected package upgrades.
If a package appears newer than the cooldown policy should allow, stop and
investigate before building the image.

Pay special attention to:

- PyTorch, torchvision, xformers, and NVIDIA CUDA wheel versions.
- `protobuf` constraints, because ONNX and open-clip packages often constrain
  it differently.
- `numpy` major-version changes, because older captioning and ONNX packages may
  not support the selected version.
- Local extras that disappeared because upstream commented them out.

## 7. Update README Links

If README links point at upstream sd-scripts documentation by commit SHA,
update those links to the selected commit. For example:

```markdown
https://github.com/kohya-ss/sd-scripts/blob/<commit-sha>/docs/train_README-ja.md
```

If the update changes the image's supported GPU, CUDA, Python, or Docker
requirements, update the README requirements section in the same PR.

## 8. Run Static Checks

Run Dockerfile linting:

```shell
hadolint Dockerfile
```

Run Docker's build checks:

```shell
docker build --check .
```

Both commands should complete without warnings for routine updates.

If `hadolint` reports `DL3008`, pin the affected apt package versions. If it
reports `DL3003` or `SC2164` around a `cd`, prefer `git -C` or `WORKDIR`
instead of changing directories inside a shell block.

## 9. Build The Image

Build the image:

```shell
docker build --progress=plain -t sd-scripts:update-test .
```

The first build after a dependency update can take several minutes because the
CUDA, PyTorch, xformers, ONNX Runtime, and NVIDIA library wheels are large.

If the build fails while pulling `ghcr.io/astral-sh/uv`, check local Docker
authentication state first. The image may still be publicly readable even when
an expired local credential causes Docker to fail.

## 10. Run Smoke Tests

Check that core Python packages import and report the expected versions:

```shell
docker run --rm --entrypoint python sd-scripts:update-test -c \
  'import torch, torchvision, xformers, onnx, onnxruntime, open_clip, timm, fairscale; import accelerate, transformers, diffusers; print(torch.__version__); print(torch.version.cuda); print(torchvision.__version__); print(xformers.__version__); print(onnx.__version__); print(onnxruntime.__version__); print(open_clip.__version__); print(timm.__version__); print(accelerate.__version__); print(transformers.__version__); print(diffusers.__version__)'
```

Check that a representative training entrypoint can render help:

```shell
docker run --rm sd-scripts:update-test \
  --help

docker run --rm sd-scripts:update-test \
  sdxl_train_network.py --help
```

When an NVIDIA GPU is available, also run a GPU visibility smoke test:

```shell
docker run --rm --gpus all --entrypoint python sd-scripts:update-test -c \
  'import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "no cuda")'
```

For a release that changes PyTorch, CUDA, xformers, or sd-scripts training
behavior, run at least one small project-specific training or captioning
workflow before merging when practical.

## 11. Run Upstream Release Tests

The Docker image includes the selected upstream sd-scripts checkout under
`/opt/sd-scripts`, including the upstream `tests/` directory. Install the
uv-managed dev test dependencies temporarily in a disposable container and run
the same lightweight upstream pytest set that CI uses:

```shell
docker run --rm --user root --entrypoint bash \
  -v "${PWD}/pyproject.toml:/tmp/release-test-project/pyproject.toml:ro" \
  -v "${PWD}/uv.lock:/tmp/release-test-project/uv.lock:ro" \
  sd-scripts:update-test -lc '
  set -euo pipefail
  uv sync --project /tmp/release-test-project --frozen --only-group dev --inexact --no-install-project
  cd /opt/sd-scripts
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
'
```

This set intentionally excludes upstream tests and scripts that need model
checkpoints, local datasets, or dependencies this image does not bundle, such
as `tests/test_optimizer.py` requiring `dadaptation`.

When an NVIDIA GPU and compatible test checkpoint are available, also run at
least one upstream inpainting training smoke test. The scripts generate
synthetic image data automatically when `--data` is omitted:

```shell
docker run --rm --gpus all --entrypoint bash \
  -v /path/to/models:/models:ro \
  sd-scripts:update-test \
  tests/run_sd15_inpainting_test.sh --mode ft --model /models/sd15-inpainting.safetensors --steps 1

docker run --rm --gpus all --entrypoint bash \
  -v /path/to/models:/models:ro \
  sd-scripts:update-test \
  tests/run_sdxl_inpainting_test.sh --mode ft --model /models/sdxl-base-or-inpainting.safetensors --steps 1
```

If GPU or checkpoint coverage is skipped, record the exact reason in the pull
request.

## 12. Review And Record The Change

Review the diff:

```shell
git diff --stat
git diff --check
git diff -- Dockerfile pyproject.toml uv.lock README.md docs/update-sd-scripts.md
```

Confirm:

- `SD_SCRIPTS_VERSION` is an exact commit SHA from the selected tag.
- The `pyproject.toml` upstream requirements comment points at the same commit.
- README upstream documentation links point at the same commit.
- The CUDA base image digest matches the intended CUDA and Ubuntu tag.
- Apt package versions were checked inside the selected CUDA image.
- `uv.lock` resolves the selected PyTorch CUDA index.
- Local extras are intentionally kept, updated, or removed.
- Upstream sd-scripts pytest release tests passed in the built image.
- Upstream inpainting shell tests were run, or GPU/checkpoint coverage was
  explicitly skipped.
- Verification commands and any skipped GPU tests are documented in the PR.

## 13. Open The Pull Request

Create a focused commit, push the branch, and open a pull request.

The PR body should include:

- The selected sd-scripts version and commit SHA.
- Any CUDA, Ubuntu, PyTorch, xformers, or local-extra dependency changes.
- The checks run locally.
- Whether upstream pytest release tests passed in the built image.
- Whether runtime GPU and upstream inpainting training tests were tested or
  skipped.

Do not update `VERSION` as part of the sd-scripts update unless the same PR is
also intentionally publishing a Docker image release. Follow the README release
procedure separately after the update PR is merged.
