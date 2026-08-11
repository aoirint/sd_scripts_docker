"""Regression tests for the shared Python project mechanical checker."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_project import Checker


class KeywordOnlyCheckerTests(unittest.TestCase):
    """Exercise zero-positional enforcement and its narrow exceptions."""

    def findings_for_source(self, *, source: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "src" / "package" / "module.py"
            source_file.parent.mkdir(parents=True)
            source_file.write_text(source, encoding="utf-8")
            checker = Checker(root)
            checker._check_keyword_only_definitions(source_file)
            return [finding.code for finding in checker.findings]

    def test_generic_checker_does_not_require_flet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                """
[project]
name = "example"
version = "1.0.0"
description = "Example library"
requires-python = ">=3.11"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
""",
                encoding="utf-8",
            )
            checker = Checker(root)
            checker._check_pyproject(pyproject)
            codes = {finding.code for finding in checker.findings}
            self.assertNotIn("flet-dependency", codes)
            self.assertNotIn("flet-app-path", codes)
            self.assertNotIn("flet-app-module", codes)

    def test_reports_invalid_python_instead_of_skipping_it(self) -> None:
        findings = self.findings_for_source(source="def broken(:\n")
        self.assertIn("invalid-python", findings)

    def test_accepts_keyword_only_definitions_and_real_receivers(self) -> None:
        findings = self.findings_for_source(
            source="""
def function(*, value):
    return value

class Example:
    def method(self, *, value):
        return value

    @classmethod
    def create(cls, *, value):
        return value

    def __new__(cls, *, value):
        return super().__new__(cls)
"""
        )
        self.assertFalse(
            set(findings) & {"keyword-only-definition", "keyword-only-lambda"}
        )

    def test_rejects_false_receivers_variadics_and_lambdas(self) -> None:
        findings = self.findings_for_source(
            source="""
def top_level(self):
    return self

class Example:
    @staticmethod
    def static(cls):
        return cls

    @custom
    @classmethod
    def decorated(cls):
        return cls

def variadic(*args):
    return args

callable_value = lambda value: value
"""
        )
        self.assertIn("keyword-only-definition", findings)
        self.assertIn("keyword-only-lambda", findings)

    def test_rejects_custom_decorators_using_trusted_names(self) -> None:
        findings = self.findings_for_source(
            source="""
from custom import override

class Example:
    @override
    def method(self):
        return None
"""
        )
        self.assertIn("keyword-only-definition", findings)

    def test_rejects_class_local_shadowing_of_a_trusted_decorator(self) -> None:
        findings = self.findings_for_source(
            source="""
class Example:
    property = external_decorator

    @property
    def method(self):
        return None
"""
        )
        self.assertIn("keyword-only-definition", findings)

    def test_nested_import_cannot_reclassify_a_custom_decorator(self) -> None:
        findings = self.findings_for_source(
            source="""
from custom import override

class Example:
    @override
    def method(self):
        return None

def unrelated(*, value):
    from typing import override
    return override(value)
"""
        )
        self.assertIn("keyword-only-definition", findings)

    def test_rejects_assignment_aliases_for_standard_constructors(self) -> None:
        findings = self.findings_for_source(
            source="""
from dataclasses import dataclass

alias = dataclass

@alias
class Record:
    value: int
"""
        )
        self.assertIn("keyword-only-callable-alias", findings)

    def test_accepts_only_a_real_same_line_external_exception(self) -> None:
        findings = self.findings_for_source(
            source="""
def string_marker(value="# keyword-only-exception: fake callback ABI"):
    return value

def external(value):  # keyword-only-exception: framework callback ABI
    return value
"""
        )
        self.assertIn("keyword-only-definition", findings)
        self.assertEqual(
            sum(finding == "keyword-only-definition" for finding in findings),
            1,
        )

    def test_rejects_generated_positional_constructors_and_dataclass_aliases(
        self,
    ) -> None:
        findings = self.findings_for_source(
            source="""
if True:
    from dataclasses import dataclass as dc
    from dataclasses import field as dc_field
from typing import NamedTuple as NT
from collections import namedtuple as nt
from dataclasses import make_dataclass as make_dc

@dc
class Record:
    value: int = dc_field(kw_only=False)

class TupleRecord(NT):
    value: int

FunctionalRecord = nt("FunctionalRecord", ["value"])
DynamicRecord = make_dc("DynamicRecord", [("value", int)])
"""
        )
        self.assertIn("keyword-only-dataclass", findings)
        self.assertIn("keyword-only-dataclass-field", findings)
        self.assertIn("keyword-only-generated-constructor", findings)

    def test_accepts_direct_keyword_only_dataclass_field(self) -> None:
        findings = self.findings_for_source(
            source="""
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class Record:
    value: int = field(kw_only=True)
"""
        )
        self.assertFalse(
            set(findings)
            & {
                "keyword-only-callable-alias",
                "keyword-only-dataclass",
                "keyword-only-dataclass-field",
            }
        )

    def test_rejects_all_positional_rule_suppression_routes(self) -> None:
        cases = {
            "ignore-all": 'ignore = ["ALL"]',
            "extend-ignore-parent": 'extend-ignore = ["PLR"]',
            "per-file-ignore": '[tool.ruff.lint.per-file-ignores]\n"*.py" = ["PL"]',
            "extend-per-file-ignore": (
                '[tool.ruff.lint.extend-per-file-ignores]\n"*.py" = ["PLR0917"]'
            ),
        }
        for name, suppression in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                pyproject = root / "pyproject.toml"
                pyproject.write_text(
                    f"""
[project]
requires-python = ">=3.13,<3.14"
dependencies = []

[dependency-groups]
dev = ["mypy", "pytest", "pytest-cov", "ruff"]

[tool.uv]
exclude-newer = "P7D"

[tool.ruff.lint]
preview = true
explicit-preview-rules = true
select = [
    "ANN", "ASYNC", "B", "C90", "E", "F", "FBT", "I", "PL", "PLR0917",
    "PT", "RUF", "S", "TRY", "UP", "W",
]
{suppression}

[tool.ruff.lint.pylint]
max-positional-args = 0

[tool.mypy]
strict = true
warn_unreachable = true

[tool.pytest.ini_options]
addopts = "--cov --cov-branch --cov-fail-under=100"

[tool.coverage.report]
fail_under = 100

[tool.coverage.run]
branch = true
""",
                    encoding="utf-8",
                )
                checker = Checker(root)
                checker._check_pyproject(pyproject)
                self.assertIn(
                    "ruff-positional-arguments-suppression",
                    {finding.code for finding in checker.findings},
                )

    def test_scans_source_build_package_but_skips_nested_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {
                "src/package/__init__.py": "",
                "src/package/build/module.py": "def checked(value):\n    return value\n",
                "examples/demo/.venv/bad.py": "def skipped(value):\n    return value\n",
                "tools/demo/build/bad.py": "def skipped(value):\n    return value\n",
            }
            for relative, source in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(source, encoding="utf-8")
            checker = Checker(root)
            checker._check_python_layout()
            keyword_paths = {
                finding.path
                for finding in checker.findings
                if finding.code == "keyword-only-definition"
            }
            self.assertEqual(keyword_paths, {"src/package/build/module.py:1"})

    def test_rejects_explicit_ruff_source_exclusions(self) -> None:
        for key, lint_exclude in (
            ("exclude", ""),
            ("extend-exclude", ""),
            ("", 'exclude = ["src/**"]'),
        ):
            with (
                self.subTest(key=key or "lint.exclude"),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                pyproject = root / "pyproject.toml"
                pyproject.write_text(
                    f"""
[project]
requires-python = ">=3.13,<3.14"
dependencies = []

[dependency-groups]
dev = ["mypy", "pytest", "pytest-cov", "ruff"]

[tool.uv]
exclude-newer = "P7D"

[tool.ruff]
{f'{key} = ["src/**"]' if key else ""}

[tool.ruff.lint]
{lint_exclude}
preview = true
explicit-preview-rules = true
select = [
    "ANN", "ASYNC", "B", "C90", "E", "F", "FBT", "I", "PL", "PLR0917",
    "PT", "RUF", "S", "TRY", "UP", "W",
]

[tool.ruff.lint.pylint]
max-positional-args = 0

[tool.mypy]
strict = true
warn_unreachable = true

[tool.pytest.ini_options]
addopts = "--cov --cov-branch --cov-fail-under=100"

[tool.coverage.report]
fail_under = 100

[tool.coverage.run]
branch = true
""",
                    encoding="utf-8",
                )
                checker = Checker(root)
                checker._check_pyproject(pyproject)
                self.assertIn(
                    "ruff-owned-source-exclusion",
                    {finding.code for finding in checker.findings},
                )

    def test_accepts_generated_agent_skill_exclusion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                """
[project]
requires-python = ">=3.13,<3.14"
dependencies = []

[dependency-groups]
dev = ["mypy", "pytest", "pytest-cov", "ruff"]

[tool.uv]
exclude-newer = "P7D"

[tool.ruff]
extend-exclude = [".agents/skills/**"]

[tool.ruff.lint]
preview = true
explicit-preview-rules = true
select = [
    "ANN", "ASYNC", "B", "C90", "E", "F", "FBT", "I", "PL", "PLR0917",
    "PT", "RUF", "S", "TRY", "UP", "W",
]

[tool.ruff.lint.pylint]
max-positional-args = 0

[tool.mypy]
strict = true
warn_unreachable = true

[tool.pytest.ini_options]
addopts = "--cov --cov-branch --cov-fail-under=100"

[tool.coverage.report]
fail_under = 100

[tool.coverage.run]
branch = true
""",
                encoding="utf-8",
            )
            checker = Checker(root)
            checker._check_pyproject(pyproject)
            self.assertNotIn(
                "ruff-owned-source-exclusion",
                {finding.code for finding in checker.findings},
            )


if __name__ == "__main__":
    unittest.main()
