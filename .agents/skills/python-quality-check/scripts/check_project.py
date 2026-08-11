# /// script
# requires-python = ">=3.11,<3.15"
# dependencies = []
# [tool.uv]
# exclude-newer = "P7D"
# ///
"""Check the mechanical floor of a uv-managed Python repository without modifying it."""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import sys
import tokenize
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import tomllib

REQUIRED_FILES = (
    "pyproject.toml",
    ".python-version",
    "uv.lock",
    "README.md",
)
REQUIRED_DEV_DEPENDENCIES = {"mypy", "pytest", "pytest-cov", "ruff"}
REQUIRED_RUFF_FAMILIES = {
    "ANN",
    "ASYNC",
    "B",
    "C90",
    "E",
    "F",
    "FBT",
    "I",
    "PL",
    "PLR0917",
    "PT",
    "RUF",
    "S",
    "TRY",
    "UP",
    "W",
}
REQUIRED_CI_COMMANDS = (
    "uv lock --check",
    "uv sync --locked --all-groups",
    "uv run --locked ruff check",
    "uv run --locked ruff format --check",
    "uv run --locked mypy",
    "uv run --locked pytest",
)
TOP_LEVEL_EXCLUDED_PYTHON_PARTS = {
    ".agents",
    ".git",
    "apm_modules",
}
NESTED_EXCLUDED_PYTHON_PARTS = {
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "site-packages",
}
ALLOWED_RUFF_EXCLUDE_PATHS = {
    ".agents/skills",
    ".agents/worktrees",
    "apm_modules",
}
RECEIVER_PRESERVING_DECORATOR_PATHS = {
    "abc.abstractmethod",
    "builtins.property",
    "functools.cache",
    "functools.cached_property",
    "functools.lru_cache",
    "property",
    "typing.override",
    "typing_extensions.override",
}
IMPLICIT_CLASS_RECEIVER_METHODS = {
    "__class_getitem__",
    "__init_subclass__",
    "__new__",
}
PROTECTED_POSITIONAL_POLICY_PATHS = RECEIVER_PRESERVING_DECORATOR_PATHS | {
    "builtins.classmethod",
    "builtins.staticmethod",
    "classmethod",
    "collections.namedtuple",
    "dataclasses.dataclass",
    "dataclasses.field",
    "dataclasses.make_dataclass",
    "staticmethod",
    "typing.NamedTuple",
}
USES_PATTERN = re.compile(r"""\buses:\s*["']?([^\s#"']+)""")
KEYWORD_ONLY_EXCEPTION_PATTERN = re.compile(
    r"^#\s*(?:noqa:\s*PLR0917\s*--\s*)?keyword-only-exception:\s*"
    r"(?P<reason>\S(?:.*\S)?)\s*$"
)


@dataclass(frozen=True, slots=True)
class Finding:
    """One mechanical baseline violation."""

    code: str
    path: str
    message: str


class Checker:
    """Collect deterministic repository findings."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.findings: list[Finding] = []

    def add(self, code: str, path: str, message: str) -> None:
        """Record a finding."""
        self.findings.append(Finding(code, path, message))

    def require(self, condition: bool, code: str, path: str, message: str) -> None:
        """Record a finding unless a condition holds."""
        if not condition:
            self.add(code, path, message)

    def run(self) -> list[Finding]:
        """Run all mechanical checks."""
        for relative in REQUIRED_FILES:
            self.require(
                (self.root / relative).is_file(),
                "required-file",
                relative,
                "required baseline file is missing",
            )

        pyproject_path = self.root / "pyproject.toml"
        if pyproject_path.is_file():
            self._check_pyproject(pyproject_path)
        self._check_python_layout()
        self._check_workflows()
        return sorted(
            self.findings, key=lambda item: (item.path, item.code, item.message)
        )

    def _check_pyproject(self, path: Path) -> None:
        try:
            document = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            self.add("invalid-pyproject", "pyproject.toml", f"cannot parse TOML: {exc}")
            return

        project = _table(document, "project")
        self.require(
            bool(project.get("name")),
            "project-name",
            "pyproject.toml",
            "project.name is required",
        )
        self.require(
            bool(project.get("description"))
            and project.get("description") != "Add your description here",
            "project-description",
            "pyproject.toml",
            "project.description must be intentional, not a generated placeholder",
        )
        self.require(
            bool(project.get("requires-python")),
            "requires-python",
            "pyproject.toml",
            "project.requires-python must define the supported range",
        )

        dev_groups = _table(document, "dependency-groups")
        dev = {_dependency_name(value) for value in _string_list(dev_groups.get("dev"))}
        missing_dev = sorted(REQUIRED_DEV_DEPENDENCIES - dev)
        self.require(
            not missing_dev,
            "dev-dependencies",
            "pyproject.toml",
            f"dependency-groups.dev is missing: {', '.join(missing_dev)}",
        )

        tool = _table(document, "tool")
        uv = _table(tool, "uv")
        self.require(
            uv.get("exclude-newer") == "P7D",
            "uv-cooldown",
            "pyproject.toml",
            'tool.uv.exclude-newer must equal "P7D"',
        )

        ruff = _table(tool, "ruff")
        self.require(
            bool(ruff.get("target-version")),
            "ruff-target",
            "pyproject.toml",
            "tool.ruff.target-version is required",
        )
        ruff_lint = _table(ruff, "lint")
        selected = set(_string_list(ruff_lint.get("select")))
        missing_families = sorted(REQUIRED_RUFF_FAMILIES - selected)
        self.require(
            not missing_families,
            "ruff-families",
            "pyproject.toml",
            f"Ruff minimum families are missing: {', '.join(missing_families)}",
        )
        self.require(
            ruff_lint.get("preview") is True,
            "ruff-preview",
            "pyproject.toml",
            "tool.ruff.lint.preview must be true for PLR0917",
        )
        self.require(
            ruff_lint.get("explicit-preview-rules") is True,
            "ruff-explicit-preview",
            "pyproject.toml",
            "tool.ruff.lint.explicit-preview-rules must be true",
        )
        ruff_pylint = _table(ruff_lint, "pylint")
        max_positional_args = ruff_pylint.get("max-positional-args")
        self.require(
            type(max_positional_args) is int and max_positional_args == 0,
            "ruff-positional-arguments",
            "pyproject.toml",
            "tool.ruff.lint.pylint.max-positional-args must equal 0",
        )
        ignored_selectors = {
            selector.upper()
            for key in ("ignore", "extend-ignore")
            for selector in _string_list(ruff_lint.get(key))
        }
        for key in ("per-file-ignores", "extend-per-file-ignores"):
            per_file_ignores = _table(ruff_lint, key)
            ignored_selectors.update(
                selector.upper()
                for selectors in per_file_ignores.values()
                for selector in _string_list(selectors)
            )
        self.require(
            not any(
                selector == "ALL" or "PLR0917".startswith(selector)
                for selector in ignored_selectors
            ),
            "ruff-positional-arguments-suppression",
            "pyproject.toml",
            "PLR0917 must not be suppressed globally or through per-file ignores",
        )
        ruff_excludes = {
            _normalize_ruff_exclude(pattern)
            for value in (
                ruff.get("exclude"),
                ruff.get("extend-exclude"),
                ruff_lint.get("exclude"),
            )
            for pattern in _string_list(value)
        }
        self.require(
            ruff_excludes <= ALLOWED_RUFF_EXCLUDE_PATHS,
            "ruff-owned-source-exclusion",
            "pyproject.toml",
            "Ruff exclusions may contain only generated APM or agent-worktree paths",
        )

        mypy = _table(tool, "mypy")
        self.require(
            mypy.get("strict") is True,
            "mypy-strict",
            "pyproject.toml",
            "tool.mypy.strict must be true",
        )
        self.require(
            mypy.get("warn_unreachable") is True,
            "mypy-unreachable",
            "pyproject.toml",
            "tool.mypy.warn_unreachable must be true",
        )
        mypy_files = set(_string_list(mypy.get("files")))
        self.require(
            {"src", "tests"}.issubset(mypy_files),
            "mypy-scope",
            "pyproject.toml",
            'tool.mypy.files must include "src" and "tests"',
        )

        pytest = _table(tool, "pytest")
        pytest_options = _table(pytest, "ini_options")
        addopts = " ".join(_string_list(pytest_options.get("addopts")))
        for token in (
            "--strict-config",
            "--strict-markers",
            "--cov-branch",
            "--cov-fail-under=100",
        ):
            self.require(
                token in addopts,
                "pytest-option",
                "pyproject.toml",
                f"pytest addopts must contain {token}",
            )
        self.require(
            re.search(r"(?:^|\s)--cov=[^\s]+", addopts) is not None,
            "coverage-source",
            "pyproject.toml",
            "pytest addopts must name the owned package with --cov=<package>",
        )

        coverage = _table(tool, "coverage")
        coverage_run = _table(coverage, "run")
        self.require(
            coverage_run.get("branch") is True,
            "coverage-branch",
            "pyproject.toml",
            "tool.coverage.run.branch must be true",
        )
        source_scope = _string_list(coverage_run.get("source")) + _string_list(
            coverage_run.get("source_pkgs")
        )
        self.require(
            bool(source_scope),
            "coverage-scope",
            "pyproject.toml",
            "coverage must name owned source/package scope",
        )
        coverage_report = _table(coverage, "report")
        self.require(
            coverage_report.get("fail_under") == 100,
            "coverage-threshold",
            "pyproject.toml",
            "tool.coverage.report.fail_under must equal 100",
        )
        self.require(
            coverage_report.get("show_missing") is True,
            "coverage-missing",
            "pyproject.toml",
            "tool.coverage.report.show_missing must be true",
        )

    def _check_python_layout(self) -> None:
        src = self.root / "src"
        tests = self.root / "tests"
        self.require(
            any(src.rglob("*.py")) if src.is_dir() else False,
            "src-layout",
            "src",
            "src must contain Python source",
        )
        self.require(
            any(tests.rglob("test_*.py")) if tests.is_dir() else False,
            "test-layout",
            "tests",
            "tests must contain pytest modules",
        )

        for file in self.root.rglob("*.py"):
            relative_parts = file.relative_to(self.root).parts
            if not _python_file_is_excluded(relative_parts):
                self._check_keyword_only_definitions(file)

    def _check_keyword_only_definitions(self, file: Path) -> None:
        relative = file.relative_to(self.root).as_posix()
        try:
            text = file.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=relative)
        except SyntaxError as exc:
            self.add(
                "invalid-python",
                f"{relative}:{exc.lineno or 1}",
                f"cannot parse Python while checking API policy: {exc.msg}",
            )
            return
        except (OSError, UnicodeError) as exc:
            self.add(
                "unreadable-python",
                relative,
                f"cannot read Python while checking API policy: {exc}",
            )
            return
        parents = {
            child: parent
            for parent in ast.walk(tree)
            for child in ast.iter_child_nodes(parent)
        }
        comments = _comments_by_line(text)
        import_aliases = _import_aliases(tree)
        for node in ast.walk(tree):
            alias_value = _assignment_value(node)
            if (
                alias_value is not None
                and _resolved_path(
                    alias_value,
                    import_aliases=import_aliases,
                )
                in PROTECTED_POSITIONAL_POLICY_PATHS
            ):
                self.add(
                    "keyword-only-callable-alias",
                    f"{relative}:{node.lineno}",
                    "use the standard decorator or constructor directly instead of an "
                    "assignment alias",
                )
                continue
            if isinstance(node, ast.Lambda):
                if (
                    node.args.posonlyargs
                    or node.args.args
                    or node.args.vararg is not None
                ):
                    self.add(
                        "keyword-only-lambda",
                        f"{relative}:{node.lineno}",
                        "make lambda parameters keyword-only with 'lambda *, ...' or use a "
                        "named definition for an external-signature exception",
                    )
                continue
            if isinstance(node, ast.ClassDef):
                dataclass_decorator = _dataclass_decorator(
                    node=node,
                    import_aliases=import_aliases,
                )
                if dataclass_decorator is not None and not _dataclass_is_keyword_only(
                    dataclass_decorator
                ):
                    self.add(
                        "keyword-only-dataclass",
                        f"{relative}:{node.lineno}",
                        "define project-owned dataclasses with dataclass(kw_only=True)",
                    )
                if dataclass_decorator is not None and _dataclass_has_positional_field(
                    node=node,
                    import_aliases=import_aliases,
                ):
                    self.add(
                        "keyword-only-dataclass-field",
                        f"{relative}:{node.lineno}",
                        "remove field(kw_only=False) from keyword-only dataclasses",
                    )
                if any(
                    _resolved_path(base, import_aliases=import_aliases)
                    == "typing.NamedTuple"
                    for base in node.bases
                ):
                    self.add(
                        "keyword-only-generated-constructor",
                        f"{relative}:{node.lineno}",
                        "replace project-owned NamedTuple positional construction with a "
                        "keyword-only value type",
                    )
                continue
            if isinstance(node, ast.Call) and _resolved_path(
                node.func,
                import_aliases=import_aliases,
            ) in {
                "collections.namedtuple",
                "dataclasses.make_dataclass",
                "typing.NamedTuple",
            }:
                self.add(
                    "keyword-only-generated-constructor",
                    f"{relative}:{node.lineno}",
                    "replace generated project-owned positional construction with a "
                    "keyword-only value type",
                )
                continue
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            positional = [*node.args.posonlyargs, *node.args.args]
            if positional and _is_implicit_receiver(
                node=node,
                parent=parents.get(node),
                parameter=positional[0],
                import_aliases=import_aliases,
            ):
                positional = positional[1:]
            if not positional and node.args.vararg is None:
                continue
            exception = KEYWORD_ONLY_EXCEPTION_PATTERN.fullmatch(
                comments.get(node.lineno, "")
            )
            if exception is not None and len(exception.group("reason")) >= 8:
                continue
            self.add(
                "keyword-only-definition",
                f"{relative}:{node.lineno}",
                "make the first project-owned parameter keyword-only with '*' or document a "
                "narrow external-signature exception",
            )

    def _check_workflows(self) -> None:
        workflow_root = self.root / ".github" / "workflows"
        workflows = (
            sorted((*workflow_root.glob("*.yml"), *workflow_root.glob("*.yaml")))
            if workflow_root.is_dir()
            else []
        )
        self.require(
            bool(workflows),
            "ci-workflow",
            ".github/workflows",
            "at least one GitHub Actions workflow is required",
        )
        if not workflows:
            return
        workflow_text = "\n".join(
            path.read_text(encoding="utf-8") for path in workflows
        )
        ci_files = self._collect_ci_files(workflows)
        combined = "\n".join(path.read_text(encoding="utf-8") for path in ci_files)
        for command in REQUIRED_CI_COMMANDS:
            self.require(
                command in combined,
                "ci-command",
                ".github/workflows",
                f"workflow must run: {command}",
            )
        self.require(
            re.search(r"(?m)^permissions:\s*\n\s+contents:\s*read\s*$", workflow_text)
            is not None,
            "ci-permissions",
            ".github/workflows",
            "workflow permissions must include contents: read",
        )
        self.require(
            "persist-credentials: false" in workflow_text,
            "checkout-credentials",
            ".github/workflows",
            "checkout must disable persisted credentials",
        )
        self.require(
            "timeout-minutes:" in workflow_text,
            "ci-timeout",
            ".github/workflows",
            "jobs must have an explicit timeout",
        )
        for path in ci_files:
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                match = USES_PATTERN.search(line)
                if match is None or match.group(1).startswith("./"):
                    continue
                value = match.group(1)
                if re.fullmatch(r"[^@]+@[0-9a-fA-F]{40}", value) is None:
                    self.add(
                        "action-pin",
                        f"{path.relative_to(self.root).as_posix()}:{line_number}",
                        "external action/reusable workflow must use a full commit SHA",
                    )

    def _collect_ci_files(self, workflows: list[Path]) -> list[Path]:
        """Follow repository-local actions and reusable workflows from CI roots."""
        repository_root = self.root.resolve()
        pending = list(reversed(workflows))
        collected: list[Path] = []
        seen: set[Path] = set()
        while pending:
            path = pending.pop().resolve()
            if path in seen:
                continue
            seen.add(path)
            collected.append(path)
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                match = USES_PATTERN.search(line)
                if match is None or not match.group(1).startswith("./"):
                    continue
                referenced = (repository_root / match.group(1)[2:]).resolve()
                relative_source = path.relative_to(repository_root).as_posix()
                if not referenced.is_relative_to(repository_root):
                    self.add(
                        "local-action-path",
                        f"{relative_source}:{line_number}",
                        "repository-local action/workflow reference escapes the repository",
                    )
                    continue
                target = _resolve_local_ci_file(referenced)
                if target is None:
                    self.add(
                        "local-action-missing",
                        f"{relative_source}:{line_number}",
                        f"repository-local action/workflow does not resolve: {match.group(1)}",
                    )
                    continue
                target = target.resolve()
                if not target.is_relative_to(repository_root):
                    self.add(
                        "local-action-path",
                        f"{relative_source}:{line_number}",
                        "repository-local action/workflow resolves outside the repository",
                    )
                    continue
                if target not in seen:
                    pending.append(target)
        return collected


def _table(value: dict[str, Any], key: str) -> dict[str, Any]:
    child = value.get(key)
    return child if isinstance(child, dict) else {}


def _resolve_local_ci_file(path: Path) -> Path | None:
    if path.is_file() and path.suffix in {".yaml", ".yml"}:
        return path
    if not path.is_dir():
        return None
    for name in ("action.yml", "action.yaml"):
        candidate = path / name
        if candidate.is_file():
            return candidate
    return None


def _string_list(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _dependency_name(requirement: str) -> str:
    match = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", requirement.strip())
    return match.group(0).lower().replace("_", "-") if match else ""


def _comments_by_line(text: str) -> dict[int, str]:
    return {
        token.start[0]: token.string
        for token in tokenize.generate_tokens(io.StringIO(text).readline)
        if token.type == tokenize.COMMENT
    }


def _is_implicit_receiver(
    *,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    parent: ast.AST | None,
    parameter: ast.arg,
    import_aliases: dict[str, str],
) -> bool:
    if not isinstance(parent, ast.ClassDef):
        return False
    decorator_paths = {
        _resolved_path(decorator, import_aliases=import_aliases)
        for decorator in node.decorator_list
    }
    staticmethod_paths = {"staticmethod", "builtins.staticmethod"}
    classmethod_paths = {"classmethod", "builtins.classmethod"}
    property_decorators = {
        f"{node.name}.deleter",
        f"{node.name}.getter",
        f"{node.name}.setter",
    }
    class_bound_names = {
        name
        for statement in parent.body
        if statement is not node
        for name in _bound_names(statement)
    }
    if any(
        path not in property_decorators and path.partition(".")[0] in class_bound_names
        for path in decorator_paths
    ):
        return False
    known_decorators = (
        RECEIVER_PRESERVING_DECORATOR_PATHS
        | property_decorators
        | staticmethod_paths
        | classmethod_paths
    )
    if not decorator_paths <= known_decorators:
        return False
    if decorator_paths & staticmethod_paths:
        return False
    if node.name in IMPLICIT_CLASS_RECEIVER_METHODS:
        return parameter.arg == "cls"
    if decorator_paths & classmethod_paths:
        return parameter.arg == "cls"
    if parameter.arg != "self":
        return False
    return decorator_paths <= RECEIVER_PRESERVING_DECORATOR_PATHS | property_decorators


def _decorator_path(decorator: ast.expr) -> str:
    if isinstance(decorator, ast.Call):
        return _decorator_path(decorator.func)
    if isinstance(decorator, ast.Name):
        return decorator.id
    if isinstance(decorator, ast.Attribute):
        prefix = _decorator_path(decorator.value)
        return f"{prefix}.{decorator.attr}" if prefix else decorator.attr
    return ""


def _dataclass_decorator(
    *,
    node: ast.ClassDef,
    import_aliases: dict[str, str],
) -> ast.expr | None:
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if (
            _resolved_path(target, import_aliases=import_aliases)
            == "dataclasses.dataclass"
        ):
            return decorator
    return None


def _dataclass_is_keyword_only(decorator: ast.expr) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    return any(
        keyword.arg == "kw_only"
        and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is True
        for keyword in decorator.keywords
    )


def _dataclass_has_positional_field(
    *,
    node: ast.ClassDef,
    import_aliases: dict[str, str],
) -> bool:
    for statement in node.body:
        if not isinstance(statement, ast.AnnAssign) or not isinstance(
            statement.value, ast.Call
        ):
            continue
        if (
            _resolved_path(statement.value.func, import_aliases=import_aliases)
            != "dataclasses.field"
        ):
            continue
        if any(
            keyword.arg == "kw_only"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is False
            for keyword in statement.value.keywords
        ):
            return True
    return False


def _import_aliases(tree: ast.Module) -> dict[str, str]:
    candidates: dict[str, set[str]] = {}
    for statement in _module_scope_statements(tree):
        if isinstance(statement, ast.ImportFrom) and statement.module is not None:
            for imported in statement.names:
                candidates.setdefault(imported.asname or imported.name, set()).add(
                    f"{statement.module}.{imported.name}"
                )
        elif isinstance(statement, ast.Import):
            for imported in statement.names:
                candidates.setdefault(imported.asname or imported.name, set()).add(
                    imported.name
                )
        else:
            for name in _bound_names(statement):
                candidates.setdefault(name, set()).add("<shadowed>")
    return {
        name: next(iter(paths)) if len(paths) == 1 else "<shadowed>"
        for name, paths in candidates.items()
    }


def _module_scope_statements(tree: ast.Module) -> list[ast.stmt]:
    statements: list[ast.stmt] = []
    pending = list(reversed(tree.body))
    while pending:
        statement = pending.pop()
        statements.append(statement)
        if isinstance(statement, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        children = [
            child
            for child in ast.iter_child_nodes(statement)
            if isinstance(child, ast.stmt)
        ]
        pending.extend(reversed(children))
    return statements


def _bound_names(statement: ast.stmt) -> set[str]:
    if isinstance(statement, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        return {statement.name}
    if isinstance(statement, ast.ImportFrom):
        return {imported.asname or imported.name for imported in statement.names}
    if isinstance(statement, ast.Import):
        return {
            imported.asname or imported.name.partition(".")[0]
            for imported in statement.names
        }
    targets: list[ast.expr] = []
    if isinstance(statement, ast.Assign):
        targets.extend(statement.targets)
    elif isinstance(statement, (ast.AnnAssign, ast.AugAssign)):
        targets.append(statement.target)
    elif isinstance(statement, (ast.For, ast.AsyncFor)):
        targets.append(statement.target)
    elif isinstance(statement, (ast.With, ast.AsyncWith)):
        targets.extend(
            item.optional_vars for item in statement.items if item.optional_vars
        )
    return {
        node.id
        for target in targets
        for node in ast.walk(target)
        if isinstance(node, ast.Name)
    }


def _resolved_path(expression: ast.expr, *, import_aliases: dict[str, str]) -> str:
    path = _decorator_path(expression)
    first, separator, remainder = path.partition(".")
    resolved_first = import_aliases.get(first, first)
    return f"{resolved_first}.{remainder}" if separator else resolved_first


def _python_file_is_excluded(relative_parts: tuple[str, ...]) -> bool:
    if relative_parts[0] in TOP_LEVEL_EXCLUDED_PYTHON_PARTS:
        return True
    if not NESTED_EXCLUDED_PYTHON_PARTS.isdisjoint(relative_parts):
        return True
    return relative_parts[0] != "src" and any(
        part in {"build", "dist"} for part in relative_parts[:-1]
    )


def _normalize_ruff_exclude(pattern: str) -> str:
    normalized = pattern.replace("\\", "/").strip("/")
    return normalized.removesuffix("/**").rstrip("/")


def _assignment_value(node: ast.AST) -> ast.expr | None:
    if (
        isinstance(node, ast.Assign)
        and all(isinstance(target, ast.Name) for target in node.targets)
        and isinstance(node.value, (ast.Name, ast.Attribute))
    ):
        return node.value
    if (
        isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and isinstance(node.value, (ast.Name, ast.Attribute))
    ):
        return node.value
    return None


def main() -> int:
    """Run the command-line checker."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="uv-managed Python repository root")
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON"
    )
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    findings = Checker(root).run()
    if args.json:
        print(
            json.dumps(
                {
                    "status": "PASS" if not findings else "FAIL",
                    "findings": [asdict(item) for item in findings],
                },
                indent=2,
            )
        )
    elif findings:
        for finding in findings:
            print(f"{finding.path}: [{finding.code}] {finding.message}")
        print(f"FAIL: {len(findings)} finding(s)")
    else:
        print("PASS: mechanical Python project baseline satisfied")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
