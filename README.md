# sd-scripts-docker

Dockerfile for [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts).

## Requirements

- Docker Engine >= 27.0
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Usage

- Replace `accelerate launch` with `sudo docker run --rm --gpus all aoirint/sd_scripts`.
- Training command will run in the container by a general user (UID=1000).

### WD14 Captioning (ONNX)

```shell
mkdir -p "./cache/wd14_tagger_model_cache"
sudo chown -R 1000:1000 "./cache/wd14_tagger_model_cache"

# If your cache is broken, execute
# rm -rf ./cache/wd14_tagger_model_cache/wd14_tagger_model

sudo docker run --rm --gpus all \
  -v "./work:/work" \
  -v "./cache/wd14_tagger_model_cache:/wd14_tagger_model_cache" \
  aoirint/sd_scripts \
  finetune/tag_images_by_wd14_tagger.py \
  --model_dir "/wd14_tagger_model_cache/wd14_tagger_model" \
  --onnx \
  /work/my_dataset-20230715.1/img
```

### Training LoRA-LierLa U-Net only with `DreamBooth、キャプション方式` for Animagine XL 4.0 Zero (Stable Diffusion XL)

Create permanent directories to mount on container.

```shell
mkdir -p "./base_model" "./work" "./cache/huggingface/hub"
sudo chown -R 1000:1000 "./base_model" "./work" "./cache/huggingface/hub"
```

Download `animagineXL40_v4Zero.safetensors` from [Animagine XL 4.0 Zero](https://civitai.com/models/1188071?modelVersionId=1409042).

```shell
wget -O "animagineXL40_v4Zero.safetensors" "https://civitai.com/api/download/models/1409042?type=Model&format=SafeTensor&size=full&fp=fp16"
echo "f15812e65c2ea7f4e19ce37fb2a8445eb65c64da450a508dd9c8f237c73f6bb8  animagineXL40_v4Zero" | sha256sum -c -
```

Prepare a dataset directory `work/my_dataset-20230715.1` and a config file `work/my_dataset-20230715.1/config.toml` following [train_README](https://github.com/kohya-ss/sd-scripts/blob/206adb643848ff27894f1e72b6987fa66db99378/docs/train_README-ja.md#dreambooth%E3%82%AD%E3%83%A3%E3%83%97%E3%82%B7%E3%83%A7%E3%83%B3%E6%96%B9%E5%BC%8F%E6%AD%A3%E5%89%87%E5%8C%96%E7%94%BB%E5%83%8F%E4%BD%BF%E7%94%A8%E5%8F%AF).

Set file ownership `UID:GID = 1000:1000` (`sudo chown -R 1000:1000 "./work"`).

You can also choose another directory structure to modify `config.toml` and the training command.

- work/my_dataset-20230715.1/
    - config.toml
    - img/
        - 0001.png
        - 0001.txt
        - 0002.png
        - 0002.txt
        - ...
    - reg_img/
        - transparent_1.png
        - transparent_2.png
        - ...
    - sample_prompts.txt
    - output/
    - logs/

This is an example `sample_prompts.txt`. Use the output of WD14 tagger as reference. Add new lines for multiple samples.

```plain
shs 1girl, 1girl, solo, simple background, white background, masterpiece, high score, great score, absurdres --w 1024 --h 1024 --d 42 --s 28 --l 5 --ss euler_a --n lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry
```

This is an example `config.toml`.

```toml
[general]
enable_bucket = true

[[datasets]]
resolution = 1024
batch_size = 1

  [[datasets.subsets]]
  image_dir = '/work/my_dataset-20230715.1/img'
  caption_extension = '.txt'
  num_repeats = 20

  [[datasets.subsets]]
  is_reg = true
  image_dir = '/work/my_dataset-20230715.1/reg_img'
  class_tokens = '1girl'
  num_repeats = 1
```

Execute training.

```shell
sudo docker run \
  --rm \
  --gpus all \
  -v "./base_model:/base_model" \
  -v "./work:/work" \
  -v "./cache/huggingface/hub:/home/user/.cache/huggingface/hub" \
  aoirint/sd_scripts \
  --num_cpu_threads_per_process=1 \
  sdxl_train_network.py \
  --seed=42 \
  --pretrained_model_name_or_path="/base_model/animagineXL40_v4Zero.safetensors" \
  --dataset_config="/work/my_dataset-20230715.1/config.toml" \
  --output_dir="/work/my_dataset-20230715.1/output" \
  --output_name="my_dataset-20230715.1" \
  --save_model_as="safetensors" \
  --logging_dir="/work/my_dataset-20230715.1/logs" \
  --prior_loss_weight=1.0 \
  --max_train_epochs=5 \
  --learning_rate=1e-4 \
  --optimizer_type="AdaFactor" \
  --xformers \
  --mixed_precision="fp16" \
  --cache_latents \
  --cache_text_encoder_outputs  \
  --gradient_checkpointing \
  --save_every_n_epochs=1 \
  --sample_at_first \
  --sample_every_n_epochs=1 \
  --sample_prompts="/work/my_dataset-20230715.1/sample_prompts.txt" \
  --sample_sampler="euler_a" \
  --network_module="networks.lora" \
  --network_train_unet_only
```

## Release procedure

Releases are driven by the root `VERSION` file and the Git tags on GitHub.

1. Update `VERSION` to the version to publish.
   - Stable releases use SemVer without a prerelease suffix, such as `0.1.0`.
   - Prereleases use SemVer with a prerelease suffix, such as `0.1.0-rc.1`.
2. Commit the `VERSION` change and merge it to `main`.
3. The build workflow checks whether `v<VERSION>` already exists on GitHub.
   - If the tag does not exist and `VERSION` is stable, it creates a latest GitHub Release and publishes Docker images tagged `v<VERSION>` and `latest`.
   - If the tag does not exist and `VERSION` is a prerelease, it creates a prerelease GitHub Release and publishes the Docker image tagged `edge`.
   - If the tag already exists, the push is treated as an edge build and only the `edge` Docker image is updated.
