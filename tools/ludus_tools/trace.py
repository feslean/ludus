# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Requirements traceability checker (tool T-001, LUD-PRC-002).

Loads requirements from TOML files, scans source and test files for
traceability tags, checks the rules of the Requirements Standard
(LUD-STD-001) and generates the traceability matrix (LUD-VER-001).
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from ludus_tools._config import (
    ConfigError,
    display,
    get_str,
    get_str_list,
    load_section,
    read_text,
)

ID_PATTERN = re.compile(r"^(SYS|HLR|LLR)-[A-Z]{3}-[0-9]{3}$")
TAG_PATTERN = re.compile(r"^\s*(?:#|//|--|/\*|\*)\s*(Verifies|Implements):\s*(.*?)\s*(?:\*/)?\s*$")
SHALL_PATTERN = re.compile(r"\bshall\b", re.IGNORECASE)
VERIFICATION_METHODS = frozenset({"test", "analysis", "review", "inspection"})
ASSURANCE_LEVELS = frozenset({"LAL-1", "LAL-2", "LAL-3"})
STATUSES = frozenset({"draft", "approved", "implemented", "verified", "deleted"})
IMPLEMENTED_STATUSES = frozenset({"implemented", "verified"})
NEEDS_CHILD_STATUSES = frozenset({"approved", "implemented", "verified"})
PARENT_LEVEL = {"HLR": "SYS", "LLR": "HLR"}
LEVEL_ORDER = {"SYS": 0, "HLR": 1, "LLR": 2}
TEXT_ATTRIBUTES = ("id", "title", "statement", "rationale", "assurance", "status")


@dataclass(frozen=True)
class Requirement:
    """One requirement as read from a requirements file."""

    id: str
    title: str
    statement: str
    rationale: str
    verification: tuple[str, ...]
    assurance: str
    status: str
    parents: tuple[str, ...]
    derived: bool
    derived_rationale: str
    source: str

    @property
    def level(self) -> str:
        """Return the level prefix of the identifier (SYS, HLR or LLR)."""
        return self.id.split("-", 1)[0]


@dataclass(frozen=True)
class Tag:
    """One ``Verifies:`` or ``Implements:`` reference found in a file."""

    kind: str
    requirement_id: str
    location: str


@dataclass(frozen=True)
class TraceConfig:
    """Settings of the ``[trace]`` section."""

    root: Path
    requirements_dirs: tuple[Path, ...]
    tag_dirs: tuple[Path, ...]
    tag_suffixes: frozenset[str]
    matrix_path: Path
    version: str


def _is_str_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


# Implements: HLR-TRC-016
def load_config(path: Path) -> TraceConfig:
    """Read the ``[trace]`` section of the tool configuration file."""
    section = load_section(path, "trace")
    root = path.resolve().parent
    version_path = root / get_str(section, "version_file", path)
    version = read_text(version_path) if version_path.is_file() else None
    if version is None or not version.strip():
        raise ConfigError(f"{path}: version file '{version_path}' is missing or empty")
    return TraceConfig(
        root=root,
        requirements_dirs=tuple(root / d for d in get_str_list(section, "requirements_dirs", path)),
        tag_dirs=tuple(root / d for d in get_str_list(section, "tag_dirs", path)),
        tag_suffixes=frozenset(get_str_list(section, "tag_suffixes", path)),
        matrix_path=root / get_str(section, "matrix", path),
        version=version.strip(),
    )


# Implements: HLR-TRC-002
def _parse_requirement(entry: object, source: str) -> tuple[Requirement | None, list[str]]:
    if not isinstance(entry, dict):
        return None, [f"{source}: requirement entry is not a table"]
    raw_id = entry.get("id")
    where = f"{source}: {raw_id if isinstance(raw_id, str) else '<missing id>'}"
    errors = [
        f"{where}: attribute '{name}' must be a non-empty string"
        for name in TEXT_ATTRIBUTES
        if not isinstance(entry.get(name), str) or not str(entry.get(name)).strip()
    ]
    verification = entry.get("verification")
    if not _is_str_list(verification) or not verification:
        errors.append(f"{where}: attribute 'verification' must be a non-empty list of strings")
    parents = entry.get("parents", [])
    if not _is_str_list(parents):
        errors.append(f"{where}: attribute 'parents' must be a list of strings")
    derived = entry.get("derived", False)
    if not isinstance(derived, bool):
        errors.append(f"{where}: attribute 'derived' must be a boolean")
    derived_rationale = entry.get("derived_rationale", "")
    if not isinstance(derived_rationale, str):
        errors.append(f"{where}: attribute 'derived_rationale' must be a string")
    if errors:
        return None, errors
    requirement = Requirement(
        id=str(entry["id"]),
        title=str(entry["title"]),
        statement=str(entry["statement"]),
        rationale=str(entry["rationale"]),
        verification=tuple(cast(list[str], verification)),
        assurance=str(entry["assurance"]),
        status=str(entry["status"]),
        parents=tuple(cast(list[str], parents)),
        derived=bool(derived),
        derived_rationale=str(derived_rationale),
        source=source,
    )
    return requirement, _check_values(requirement)


# Implements: HLR-TRC-003, HLR-TRC-005, HLR-TRC-006, HLR-TRC-007
def _check_values(req: Requirement) -> list[str]:
    where = f"{req.source}: {req.id}"
    errors: list[str] = []
    if not ID_PATTERN.match(req.id):
        errors.append(f"{where}: identifier does not match LEVEL-AREA-NNN")
    shall_count = len(SHALL_PATTERN.findall(req.statement))
    if shall_count != 1:
        errors.append(f"{where}: statement must contain 'shall' exactly once (found {shall_count})")
    errors.extend(
        f"{where}: unknown verification method '{method}'"
        for method in req.verification
        if method not in VERIFICATION_METHODS
    )
    if req.assurance not in ASSURANCE_LEVELS:
        errors.append(f"{where}: unknown assurance level '{req.assurance}'")
    if req.status not in STATUSES:
        errors.append(f"{where}: unknown status '{req.status}'")
    if ID_PATTERN.match(req.id):
        errors.extend(_check_hierarchy(req, where))
    return errors


# Implements: HLR-TRC-007
def _check_hierarchy(req: Requirement, where: str) -> list[str]:
    if req.level == "SYS":
        errors = [f"{where}: system requirements must not have parents"] if req.parents else []
        if req.derived:
            errors.append(f"{where}: system requirements cannot be derived")
        return errors
    errors = []
    if req.derived and not req.derived_rationale.strip():
        errors.append(f"{where}: derived requirements need a 'derived_rationale'")
    if not req.derived and not req.parents:
        errors.append(f"{where}: requirement has no parent and is not marked as derived")
    expected = PARENT_LEVEL[req.level]
    errors.extend(
        f"{where}: parent '{parent}' must be a {expected} requirement"
        for parent in req.parents
        if ID_PATTERN.match(parent) and parent.split("-", 1)[0] != expected
    )
    return errors


# Implements: HLR-TRC-001
def load_requirements(
    directories: Sequence[Path], root: Path
) -> tuple[list[Requirement], list[str]]:
    """Load every ``*.toml`` file found directly in ``directories``."""
    requirements: list[Requirement] = []
    errors: list[str] = []
    for directory in directories:
        if not directory.is_dir():
            errors.append(f"{display(directory, root)}: requirements directory does not exist")
            continue
        for path in sorted(directory.glob("*.toml")):
            source = display(path, root)
            text = read_text(path)
            if text is None:
                errors.append(f"{source}: file is not valid UTF-8")
                continue
            try:
                data = tomllib.loads(text)
            except tomllib.TOMLDecodeError as exc:
                errors.append(f"{source}: file is not valid TOML: {exc}")
                continue
            entries = data.get("requirement")
            if not isinstance(entries, list) or not entries:
                errors.append(f"{source}: no [[requirement]] tables found")
                continue
            for entry in entries:
                requirement, entry_errors = _parse_requirement(entry, source)
                errors.extend(entry_errors)
                if requirement is not None:
                    requirements.append(requirement)
    return requirements, errors


# Implements: HLR-TRC-009
def scan_tags(
    directories: Sequence[Path], suffixes: frozenset[str], root: Path
) -> tuple[list[Tag], list[str]]:
    """Collect traceability tags from comment lines of matching files."""
    tags: list[Tag] = []
    errors: list[str] = []
    for directory in directories:
        if not directory.is_dir():
            errors.append(f"{display(directory, root)}: tag directory does not exist")
            continue
        files = sorted(p for p in directory.rglob("*") if p.is_file() and p.suffix in suffixes)
        for path in files:
            text = read_text(path)
            if text is None:
                errors.append(f"{display(path, root)}: file is not valid UTF-8")
                continue
            for number, line in enumerate(text.splitlines(), start=1):
                match = TAG_PATTERN.match(line)
                if match is None:
                    continue
                kind, value = match.group(1), match.group(2)
                location = f"{display(path, root)}:{number}"
                tokens = [token for token in re.split(r"[,\s]+", value) if token]
                if not tokens:
                    errors.append(f"{location}: {kind} tag lists no requirement")
                for token in tokens:
                    if ID_PATTERN.match(token):
                        tags.append(Tag(kind, token, location))
                    else:
                        errors.append(f"{location}: malformed identifier '{token}' in {kind} tag")
    return tags, errors


def _children(requirements: Iterable[Requirement]) -> dict[str, list[str]]:
    children: dict[str, list[str]] = {}
    for req in requirements:
        if req.status != "deleted":
            for parent in req.parents:
                children.setdefault(parent, []).append(req.id)
    return {parent: sorted(ids) for parent, ids in children.items()}


# Implements: HLR-TRC-004, HLR-TRC-008, HLR-TRC-009, HLR-TRC-010, HLR-TRC-011, HLR-TRC-012
def check(requirements: Sequence[Requirement], tags: Sequence[Tag]) -> list[str]:
    """Apply the cross-requirement and tag coverage rules."""
    errors: list[str] = []
    by_id: dict[str, Requirement] = {}
    for req in requirements:
        if req.id in by_id:
            first = by_id[req.id].source
            errors.append(f"{req.source}: {req.id}: duplicate identifier (first in {first})")
        else:
            by_id[req.id] = req
    live = {rid for rid, req in by_id.items() if req.status != "deleted"}
    for req in by_id.values():
        if req.status == "deleted":
            continue
        errors.extend(
            f"{req.source}: {req.id}: parent '{parent}' is missing or deleted"
            for parent in req.parents
            if parent not in live
        )
    errors.extend(
        f"{tag.location}: {tag.kind} tag references missing or deleted '{tag.requirement_id}'"
        for tag in tags
        if tag.requirement_id not in live
    )
    verified = {tag.requirement_id for tag in tags if tag.kind == "Verifies"}
    implemented = {tag.requirement_id for tag in tags if tag.kind == "Implements"}
    children = _children(by_id.values())
    for req in by_id.values():
        where = f"{req.source}: {req.id}"
        is_implemented = req.status in IMPLEMENTED_STATUSES
        if is_implemented and "test" in req.verification and req.id not in verified:
            errors.append(f"{where}: no Verifies tag references this requirement")
        if is_implemented and req.level in PARENT_LEVEL and req.id not in implemented:
            errors.append(f"{where}: no Implements tag references this requirement")
        if req.level == "SYS" and req.status in NEEDS_CHILD_STATUSES and req.id not in children:
            errors.append(f"{where}: system requirement has no child requirement")
    return errors


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def _locations(tags: Sequence[Tag], kind: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for tag in tags:
        if tag.kind == kind:
            found.setdefault(tag.requirement_id, []).append(tag.location)
    return {rid: sorted(locations) for rid, locations in found.items()}


# Implements: HLR-TRC-013
def render_matrix(requirements: Sequence[Requirement], tags: Sequence[Tag], version: str) -> str:
    """Render the traceability matrix as a controlled Markdown document."""
    unique = {req.id: req for req in requirements}
    ordered = sorted(unique.values(), key=lambda r: (LEVEL_ORDER.get(r.level, 9), r.id))
    children = _children(ordered)
    verified = _locations(tags, "Verifies")
    implemented = _locations(tags, "Implements")
    counts = {status: 0 for status in sorted(STATUSES)}
    for req in ordered:
        counts[req.status] = counts.get(req.status, 0) + 1
    tested = [r for r in ordered if r.status in IMPLEMENTED_STATUSES and "test" in r.verification]
    covered = sum(1 for r in tested if r.id in verified)
    lines = [
        "---",
        "doc_id: LUD-VER-001",
        "title: Requirements Traceability Matrix",
        f'revision: "{version}"',
        "status: baselined",
        "owner: Project lead",
        "---",
        "",
        "# Requirements Traceability Matrix",
        "",
        "> Generated by `ludus_tools.trace`. Do not edit by hand. Regenerate with `make matrix`.",
        "",
        "## Summary",
        "",
        f"- Requirements: {len(ordered)}",
        *(f"- Status `{status}`: {count}" for status, count in counts.items()),
        f"- Implemented requirements with test verification that have a Verifies tag: "
        f"{covered} of {len(tested)}",
        "",
        "## Matrix",
        "",
        "| ID | Title | LAL | Status | Parents | Children | Implemented by | Verified by |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for req in ordered:
        row = [
            req.id,
            _cell(req.title),
            req.assurance,
            req.status,
            "<br>".join(req.parents) or "-",
            "<br>".join(children.get(req.id, [])) or "-",
            "<br>".join(implemented.get(req.id, [])) or "-",
            "<br>".join(verified.get(req.id, [])) or "-",
        ]
        lines.append("| " + " | ".join(row) + " |")
    lines += [
        "",
        "## Revision history",
        "",
        "| Revision | Description |",
        "|---|---|",
        f"| {version} | Generated for baseline {version}. |",
        "",
    ]
    return "\n".join(lines)


# Implements: HLR-TRC-014, HLR-TRC-015, HLR-TRC-016
def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point. Returns the process exit status."""
    parser = argparse.ArgumentParser(
        prog="python -m ludus_tools.trace",
        description="Check requirements traceability and generate the traceability matrix.",
    )
    parser.add_argument("--config", type=Path, default=Path("ludus-tools.toml"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="check the traceability rules")
    matrix = commands.add_parser("matrix", help="write or check the traceability matrix")
    mode = matrix.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write the matrix file")
    mode.add_argument("--check", action="store_true", help="fail if the matrix is out of date")
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    requirements, errors = load_requirements(config.requirements_dirs, config.root)
    tags, tag_errors = scan_tags(config.tag_dirs, config.tag_suffixes, config.root)
    errors += tag_errors + check(requirements, tags)

    if args.command == "matrix":
        text = render_matrix(requirements, tags, config.version)
        if args.write:
            config.matrix_path.parent.mkdir(parents=True, exist_ok=True)
            config.matrix_path.write_text(text, encoding="utf-8")
        else:
            current = read_text(config.matrix_path) if config.matrix_path.is_file() else None
            if current != text:
                matrix_name = display(config.matrix_path, config.root)
                errors.append(f"{matrix_name}: matrix is missing or out of date; run 'make matrix'")

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"trace: OK ({len(requirements)} requirements, {len(tags)} tags)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
