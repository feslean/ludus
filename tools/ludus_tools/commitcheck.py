# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Commit message checker (tool T-003, LUD-PRC-002).

Enforces the commit message rules of the Software Configuration
Management Plan (LUD-PLN-004, section 6).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

COMMIT_TYPES = frozenset(
    {"feat", "fix", "perf", "refactor", "docs", "test", "build", "ci", "chore", "revert"}
)
REFS_REQUIRED_TYPES = frozenset({"feat", "fix", "perf"})
HEADER_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[a-z0-9][a-z0-9-]*)\))?(?P<breaking>!)?: (?P<subject>\S.*)$"
)
REFERENCE_PATTERN = re.compile(r"^(?:(?:SYS|HLR|LLR)-[A-Z]{3}-[0-9]{3}|#[0-9]+)$")
MAX_HEADER_LENGTH = 72
MAX_BODY_LENGTH = 100


class GitError(Exception):
    """Raised when git cannot list the requested commits."""


# Implements: HLR-CMT-001, HLR-CMT-002, HLR-CMT-003, HLR-CMT-004, HLR-CMT-005, HLR-CMT-006
def check_message(message: str, strip_comments: bool = False) -> list[str]:
    """Return the rule violations found in one commit message."""
    lines = message.splitlines()
    if strip_comments:
        kept: list[str] = []
        for line in lines:
            if line.startswith("# ") and ">8" in line:
                break
            if not line.startswith("#"):
                kept.append(line)
        lines = kept
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines or not lines[0].strip():
        return ["commit message is empty"]
    header = lines[0]
    if header.startswith("Merge "):
        return ["merge commits are not permitted; rebase onto the target branch instead"]
    errors: list[str] = []
    match = HEADER_PATTERN.match(header)
    if match is None:
        errors.append("header must have the form '<type>(<scope>): <subject>'")
    elif match["type"] not in COMMIT_TYPES:
        errors.append(f"unknown commit type '{match['type']}'")
    if len(header) > MAX_HEADER_LENGTH:
        errors.append(f"header is {len(header)} characters long (maximum {MAX_HEADER_LENGTH})")
    if header.endswith("."):
        errors.append("header must not end with a period")
    if len(lines) > 1 and lines[1].strip():
        errors.append("the line after the header must be blank")
    errors.extend(
        f"line {number} is longer than {MAX_BODY_LENGTH} characters"
        for number, line in enumerate(lines[2:], start=3)
        if len(line) > MAX_BODY_LENGTH and "://" not in line
    )
    if match is None:
        return errors
    references = [line[len("Refs:") :].strip() for line in lines[1:] if line.startswith("Refs:")]
    if match["type"] in REFS_REQUIRED_TYPES and not references:
        errors.append(f"'{match['type']}' commits must include a 'Refs:' trailer")
    for value in references:
        tokens = [token.strip() for token in value.split(",") if token.strip()]
        if not tokens:
            errors.append("'Refs:' trailer is empty")
        errors.extend(
            f"invalid reference '{token}' in 'Refs:' trailer"
            for token in tokens
            if not REFERENCE_PATTERN.match(token)
        )
    if match["breaking"] and not any(line.startswith("BREAKING CHANGE: ") for line in lines[1:]):
        errors.append("breaking changes must be explained in a 'BREAKING CHANGE: ' footer")
    return errors


# Implements: HLR-CMT-007
def messages_in_range(revision_range: str, cwd: Path) -> list[tuple[str, str]]:
    """Return ``(sha, message)`` for each commit in ``revision_range``."""
    result = subprocess.run(  # noqa: S603 - fixed argument vector, no shell
        ["git", "log", "--format=%H%x00%B%x1e", revision_range],  # noqa: S607 - git from PATH
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise GitError(result.stderr.strip() or f"git log exited with status {result.returncode}")
    commits: list[tuple[str, str]] = []
    for raw_record in result.stdout.split("\x1e"):
        record = raw_record.strip("\n")
        if record:
            sha, _, body = record.partition("\x00")
            commits.append((sha, body))
    return commits


# Implements: HLR-CMT-007, HLR-CMT-008
def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point. Returns the process exit status."""
    parser = argparse.ArgumentParser(
        prog="python -m ludus_tools.commitcheck",
        description="Check commit messages against the SCMP commit rules.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--range", dest="revision_range", help="git revision range to check")
    source.add_argument("--message-file", type=Path, help="commit message file (commit-msg hook)")
    parser.add_argument("--repo", type=Path, default=Path(), help="repository directory")
    args = parser.parse_args(argv)

    errors: list[str] = []
    checked = 0
    if args.message_file is not None:
        try:
            message = args.message_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"error: cannot read {args.message_file}: {exc}", file=sys.stderr)
            return 1
        errors = check_message(message, strip_comments=True)
        checked = 1
    else:
        try:
            commits = messages_in_range(args.revision_range, args.repo)
        except GitError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        for sha, message in commits:
            errors.extend(f"{sha[:12]}: {problem}" for problem in check_message(message))
        checked = len(commits)

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"commitcheck: OK ({checked} commit message(s) checked)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
