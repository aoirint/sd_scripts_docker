# /// script
# requires-python = ">=3.11,<3.15"
# dependencies = []
# [tool.uv]
# exclude-newer = "P7D"
# ///
"""Safely inspect wheel and sdist archive paths, types, modes, size, and SHA-256."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
import tarfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath


@dataclass(frozen=True, slots=True)
class Finding:
    """One archive-floor violation."""

    archive: str
    member: str
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class Result:
    """Inspection result for one distribution archive."""

    archive: str
    size: int
    sha256: str
    members: int
    findings: tuple[Finding, ...]


def _path_finding(*, archive: Path, member: str) -> Finding | None:
    normalized = PurePosixPath(member)
    if "\\" in member:
        return Finding(
            archive.name,
            member,
            "non-posix-path",
            "archive member path contains a backslash",
        )
    if normalized.is_absolute() or ".." in normalized.parts:
        return Finding(
            archive.name,
            member,
            "unsafe-path",
            "archive member path is absolute or traverses a parent",
        )
    if not normalized.parts or normalized == PurePosixPath("."):
        return Finding(
            archive.name,
            member,
            "empty-path",
            "archive member path is empty",
        )
    return None


def _inspect_zip(archive: Path) -> tuple[int, list[Finding]]:
    findings: list[Finding] = []
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        for item in members:
            path_finding = _path_finding(archive=archive, member=item.filename)
            if path_finding is not None:
                findings.append(path_finding)
            mode = item.external_attr >> 16
            file_type = stat.S_IFMT(mode)
            if mode and file_type not in {0, stat.S_IFREG, stat.S_IFDIR}:
                findings.append(
                    Finding(
                        archive.name,
                        item.filename,
                        "special-file",
                        "wheel contains a link or unsupported special file",
                    )
                )
            if (
                not item.is_dir()
                and mode
                and mode & 0o111
                and ".data/scripts/" not in item.filename
            ):
                findings.append(
                    Finding(
                        archive.name,
                        item.filename,
                        "unexpected-executable",
                        "wheel member is executable outside the scripts directory",
                    )
                )
    return len(members), findings


def _inspect_tar(archive: Path) -> tuple[int, list[Finding]]:
    findings: list[Finding] = []
    with tarfile.open(archive, mode="r:*") as bundle:
        members = bundle.getmembers()
        for item in members:
            path_finding = _path_finding(archive=archive, member=item.name)
            if path_finding is not None:
                findings.append(path_finding)
            if not (item.isfile() or item.isdir()):
                findings.append(
                    Finding(
                        archive.name,
                        item.name,
                        "special-file",
                        "sdist contains a link or unsupported special file",
                    )
                )
            if item.isfile() and item.mode & 0o111:
                findings.append(
                    Finding(
                        archive.name,
                        item.name,
                        "unexpected-executable",
                        "sdist member has an executable mode",
                    )
                )
    return len(members), findings


def inspect(archive: Path) -> Result:
    """Inspect one archive without extracting it."""
    archive = archive.resolve()
    if not archive.is_file():
        raise FileNotFoundError(archive)
    if archive.suffix == ".whl":
        members, findings = _inspect_zip(archive)
    elif archive.name.endswith((".tar.gz", ".tar.bz2", ".tar.xz")):
        members, findings = _inspect_tar(archive)
    else:
        raise ValueError(f"unsupported distribution archive: {archive.name}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    return Result(
        archive=archive.name,
        size=archive.stat().st_size,
        sha256=digest,
        members=members,
        findings=tuple(findings),
    )


def main() -> int:
    """Run distribution inspection."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        results = [inspect(archive) for archive in args.archives]
    except (
        FileNotFoundError,
        OSError,
        ValueError,
        tarfile.TarError,
        zipfile.BadZipFile,
    ) as exc:
        parser.error(str(exc))
    print(json.dumps([asdict(result) for result in results], indent=2))
    return 1 if any(result.findings for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
