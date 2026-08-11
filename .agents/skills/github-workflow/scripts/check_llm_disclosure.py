#!/usr/bin/env python3
"""Validate required LLM disclosure and pull-request body preservation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DISCLOSURES = {
    "pull-request": (
        "> [!WARNING]\n"
        "> This pull request was created with assistance from LLMs."
    ),
    "comment": (
        "> [!WARNING]\n"
        "> This comment was created with assistance from LLMs."
    ),
}


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def read_body(args: argparse.Namespace) -> str:
    if args.body_file is not None:
        return read_text(args.body_file)

    with args.body_json_file.open("r", encoding="utf-8", newline="") as stream:
        document = json.load(stream)
    if not isinstance(document, dict) or not isinstance(document.get("body"), str):
        raise ValueError("JSON must contain one string-valued 'body' property")
    return document["body"]


def disclosure_prefixes(disclosure: str) -> tuple[str, str]:
    lf_prefix = disclosure + "\n\n"
    crlf_prefix = disclosure.replace("\n", "\r\n") + "\r\n\r\n"
    return lf_prefix, crlf_prefix


def matches_candidate(body: str, candidate: str) -> bool:
    """Compare bodies, permitting only one terminal newline representation."""
    if body == candidate:
        return True

    def without_terminal_newline(value: str) -> str:
        if value.endswith("\r\n"):
            return value[:-2]
        if value.endswith(("\n", "\r")):
            return value[:-1]
        return value

    return without_terminal_newline(body) == without_terminal_newline(candidate)


def validate(args: argparse.Namespace) -> list[str]:
    body = read_body(args)
    disclosure = DISCLOSURES[args.kind]
    normalized = body.replace("\r\n", "\n").replace("\r", "\n")
    required_prefix = disclosure + "\n\n"
    errors: list[str] = []

    if not normalized.startswith(required_prefix):
        errors.append("required LLM disclosure is not the absolute first block")
    if normalized.count(disclosure) != 1:
        errors.append("required LLM disclosure must appear exactly once")

    if args.prior_body_file is not None:
        prior = read_text(args.prior_body_file)
        raw_prefix = next(
            (
                prefix
                for prefix in disclosure_prefixes(disclosure)
                if body.startswith(prefix)
            ),
            None,
        )
        if raw_prefix is None or body[len(raw_prefix) :] != prior:
            errors.append(
                "candidate is not exactly the disclosure prefix plus the prior body"
            )

    if args.expected_body_file is not None:
        expected = read_text(args.expected_body_file)
        if not matches_candidate(body, expected):
            errors.append(
                "stored body does not match the approved candidate, allowing only "
                "terminal-newline normalization"
            )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--kind",
        choices=tuple(DISCLOSURES),
        required=True,
        help="Disclosure text to require.",
    )
    body = parser.add_mutually_exclusive_group(required=True)
    body.add_argument("--body-file", type=Path)
    body.add_argument(
        "--body-json-file",
        type=Path,
        help="Complete JSON response containing a string-valued body property.",
    )
    parser.add_argument(
        "--prior-body-file",
        type=Path,
        help="Require a disclosure-only prefix edit that preserves this body exactly.",
    )
    parser.add_argument(
        "--expected-body-file",
        type=Path,
        help=(
            "Require the body to match this approved candidate, allowing only "
            "terminal-newline normalization."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        errors = validate(args)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("LLM disclosure and body preservation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
