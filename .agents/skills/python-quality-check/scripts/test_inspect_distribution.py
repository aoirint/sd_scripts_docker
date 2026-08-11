"""Regression tests for safe distribution archive inspection."""

from __future__ import annotations

import io
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from inspect_distribution import inspect


class DistributionInspectionTests(unittest.TestCase):
    """Exercise safe path, type, and mode checks."""

    def test_accepts_regular_wheel_members(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "example-1.0-py3-none-any.whl"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("example/__init__.py", "")
                bundle.writestr("example-1.0.dist-info/METADATA", "Name: example\n")
            result = inspect(archive)
            self.assertEqual((), result.findings)
            self.assertEqual(2, result.members)
            self.assertEqual(64, len(result.sha256))

    def test_rejects_wheel_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "example-1.0-py3-none-any.whl"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("../outside.py", "")
            codes = {finding.code for finding in inspect(archive).findings}
            self.assertIn("unsafe-path", codes)

    def test_rejects_sdist_link_and_executable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "example-1.0.tar.gz"
            with tarfile.open(archive, "w:gz") as bundle:
                executable = tarfile.TarInfo("example-1.0/run.py")
                executable.mode = 0o755
                payload = b"print('ok')\n"
                executable.size = len(payload)
                bundle.addfile(executable, io.BytesIO(payload))
                link = tarfile.TarInfo("example-1.0/link")
                link.type = tarfile.SYMTYPE
                link.linkname = "run.py"
                bundle.addfile(link)
            codes = {finding.code for finding in inspect(archive).findings}
            self.assertIn("unexpected-executable", codes)
            self.assertIn("special-file", codes)


if __name__ == "__main__":
    unittest.main()
