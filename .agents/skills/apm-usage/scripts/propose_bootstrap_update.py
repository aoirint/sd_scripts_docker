# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = []
# [tool.uv]
# exclude-newer = "P7D"
# ///
"""Propose or explicitly pin a reviewed APM release from GitHub."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path

MANIFEST_PATH = Path(__file__).parents[1] / "references" / "apm-bootstrap.json"
API_URL = "https://api.github.com/repos/microsoft/apm/releases?per_page=30"


def timestamp(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def semver(tag: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag)
    if not match:
        raise ValueError(f"Unsupported release tag: {tag}")
    return tuple(int(value) for value in match.groups())


def request_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "apm-usage-skill"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def request_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "apm-usage-skill"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def load_manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as file:
        manifest = json.load(file)
    required = {"version", "published_at", "cooldown_days", "eligible_on", "release_url", "download_url_template", "assets"}
    if required.difference(manifest):
        raise ValueError("Bootstrap manifest is missing required fields")
    if manifest["cooldown_days"] < 7:
        raise ValueError("Bootstrap manifest cooldown must be at least seven days")
    return manifest


def candidate_manifest(
    current: dict,
    release: dict,
    cooldown_exception: dict | None = None,
) -> dict:
    assets_by_name = {asset["name"]: asset for asset in release["assets"]}
    assets = []
    for asset in current["assets"]:
        sidecar = assets_by_name.get(f"{asset['archive']}.sha256")
        if sidecar is None:
            raise ValueError(f"Release {release['tag_name']} is missing {asset['archive']}.sha256")
        digest = request_text(sidecar["browser_download_url"]).strip().split()[0]
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"Invalid SHA-256 sidecar for {asset['archive']}")
        assets.append({**asset, "sha256": digest})
    published_at = timestamp(release["published_at"])
    candidate = {
        **{key: value for key, value in current.items() if key != "cooldown_exception"},
        "version": release["tag_name"],
        "published_at": published_at.isoformat().replace("+00:00", "Z"),
        "eligible_on": (published_at + dt.timedelta(days=current["cooldown_days"])).isoformat().replace("+00:00", "Z"),
        "release_url": release["html_url"],
        "assets": assets,
    }
    if cooldown_exception:
        candidate["cooldown_exception"] = cooldown_exception
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--now", help="UTC timestamp for deterministic cooldown evaluation")
    parser.add_argument("--candidate-version", help="Exact newer release selected for a cooldown exception")
    parser.add_argument(
        "--cooldown-exception-reason",
        help="Maintainer-approved reason for waiving only the selected release's time gate",
    )
    parser.add_argument("--write", action="store_true", help="Replace the manifest after explicit version confirmation")
    parser.add_argument("--confirm-version", help="Required with --write; must equal the selected candidate")
    args = parser.parse_args()
    if args.write != bool(args.confirm_version):
        parser.error("--write and --confirm-version must be used together")
    if bool(args.candidate_version) != bool(args.cooldown_exception_reason):
        parser.error("--candidate-version and --cooldown-exception-reason must be used together")
    if args.cooldown_exception_reason and not args.cooldown_exception_reason.strip():
        parser.error("--cooldown-exception-reason must not be blank")
    current = load_manifest()
    now = timestamp(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=current["cooldown_days"])
    releases = request_json(API_URL)
    stable_newer = [
        release for release in releases
        if not release["draft"] and not release["prerelease"]
        and semver(release["tag_name"]) > semver(current["version"])
    ]
    if args.candidate_version:
        release = next(
            (item for item in stable_newer if item["tag_name"] == args.candidate_version),
            None,
        )
        if release is None:
            raise SystemExit("No matching stable newer candidate for cooldown exception")
        if timestamp(release["published_at"]) <= cutoff:
            raise SystemExit("Selected candidate is already cooldown-eligible; omit the exception")
        exception = {
            "approved_at": now.isoformat().replace("+00:00", "Z"),
            "reason": args.cooldown_exception_reason.strip(),
            "scope": "bootstrap-cli-release-time-gate",
        }
    else:
        eligible = [
            release for release in stable_newer
            if timestamp(release["published_at"]) <= cutoff
        ]
        release = max(eligible, key=lambda item: timestamp(item["published_at"]), default=None)
        exception = None
    candidate = candidate_manifest(current, release, exception) if release else None
    if args.write:
        if candidate is None or args.confirm_version != candidate["version"]:
            raise SystemExit("No matching reviewed candidate to write")
        with MANIFEST_PATH.open("w", encoding="utf-8", newline="\n") as file:
            file.write(json.dumps(candidate, indent=2) + "\n")
    print(json.dumps({"current_version": current["version"], "writes_files": args.write, "candidate": candidate}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
