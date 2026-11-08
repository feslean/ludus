# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Controlled document checker (tool T-002, LUD-PRC-002).

Checks the document-control rules of the Documentation Standard
(LUD-STD-004): front matter, identifiers, status values, revision history,
the document register and relative Markdown links.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from ludus_tools._config import (
    ConfigError,
    display,
    get_str,
    get_str_list,
    load_section,
    read_text,
)

DOC_ID_PATTERN = re.compile(r"^LUD-[A-Z]{3}-[0-9]{3,4}$")
DOC_STATUSES = frozenset({"draft", "in-review", "baselined", "superseded"})
REQUIRED_KEYS = ("doc_id", "title", "revision", "status", "owner")
HISTORY_HEADING = "## Revision history"
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^()\s]+)(?:\s+\"[^\"]*\")?\)")
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")
SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


@dataclass(frozen=True)
class DocConfig:
    """Settings of the ``[doccheck]`` section."""

    root: Path
    controlled_dirs: tuple[Path, ...]
    register: Path
    exclude_dirs: frozenset[str]


# Implements: HLR-DOC-007
def load_config(path: Path) -> DocConfig:
    """Read the ``[doccheck]`` section of the tool configuration file."""
    section = load_section(path, "doccheck")
    root = path.resolve().parent
    return DocConfig(
        root=root,
        controlled_dirs=tuple(root / d for d in get_str_list(section, "controlled_dirs", path)),
        register=root / get_str(section, "register", path),
        exclude_dirs=frozenset(get_str_list(section, "exclude_dirs", path)),
    )


# Implements: HLR-DOC-001
def parse_front_matter(text: str) -> tuple[dict[str, str] | None, str]:
    """Return the front matter mapping, or ``None`` and a reason."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, "document does not start with front matter ('---')"
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return metadata, ""
        key, separator, value = line.partition(":")
        if not separator or not key.strip():
            return None, f"malformed front matter line '{line}'"
        metadata[key.strip()] = value.strip().strip('"')
    return None, "front matter is not terminated by '---'"


# Implements: HLR-DOC-004
def last_history_revision(text: str) -> tuple[bool, str | None]:
    """Return whether a revision history exists and its last revision."""
    lines = text.splitlines()
    if HISTORY_HEADING not in lines:
        return False, None
    rows: list[str] = []
    for line in lines[lines.index(HISTORY_HEADING) + 1 :]:
        if line.startswith("## "):
            break
        if line.startswith("|"):
            rows.append(line)
    data_rows = rows[2:]
    if not data_rows:
        return True, None
    return True, data_rows[-1].strip().strip("|").split("|")[0].strip()


# Implements: HLR-DOC-001, HLR-DOC-002, HLR-DOC-003, HLR-DOC-004, HLR-DOC-005
def check_documents(config: DocConfig) -> list[str]:
    """Check every controlled document and the document register."""
    errors: list[str] = []
    seen: dict[str, str] = {}
    for directory in config.controlled_dirs:
        if not directory.is_dir():
            errors.append(f"{display(directory, config.root)}: controlled directory does not exist")
            continue
        for path in sorted(directory.rglob("*.md")):
            name = display(path, config.root)
            text = read_text(path)
            if text is None:
                errors.append(f"{name}: file is not valid UTF-8")
                continue
            metadata, problem = parse_front_matter(text)
            if metadata is None:
                errors.append(f"{name}: {problem}")
                continue
            missing = [key for key in REQUIRED_KEYS if not metadata.get(key)]
            if missing:
                errors.append(f"{name}: missing front matter keys: {', '.join(missing)}")
                continue
            doc_id = metadata["doc_id"]
            if not DOC_ID_PATTERN.match(doc_id):
                errors.append(f"{name}: document identifier '{doc_id}' is malformed")
            elif doc_id in seen:
                errors.append(
                    f"{name}: document identifier '{doc_id}' already used by {seen[doc_id]}"
                )
            else:
                seen[doc_id] = name
            if metadata["status"] not in DOC_STATUSES:
                errors.append(f"{name}: unknown document status '{metadata['status']}'")
            found, last = last_history_revision(text)
            if not found:
                errors.append(f"{name}: missing '{HISTORY_HEADING}' section")
            elif last is None:
                errors.append(f"{name}: revision history table has no entries")
            elif last != metadata["revision"]:
                errors.append(
                    f"{name}: last revision history entry '{last}' does not match "
                    f"front matter revision '{metadata['revision']}'"
                )
    register_text = read_text(config.register) if config.register.is_file() else None
    if register_text is None:
        errors.append(f"{display(config.register, config.root)}: document register is unreadable")
        return errors
    errors.extend(
        f"{name}: {doc_id} is not listed in the document register"
        for doc_id, name in sorted(seen.items())
        if not re.search(rf"\b{re.escape(doc_id)}\b", register_text)
    )
    return errors


# Implements: HLR-DOC-006
def check_links(root: Path, exclude_dirs: frozenset[str]) -> list[str]:
    """Check that relative links in every Markdown file resolve to a file."""
    errors: list[str] = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in exclude_dirs for part in relative.parts):
            continue
        text = read_text(path)
        if text is None:
            errors.append(f"{relative.as_posix()}: file is not valid UTF-8")
            continue
        in_fence = False
        for number, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in LINK_PATTERN.findall(INLINE_CODE_PATTERN.sub("", line)):
                if SCHEME_PATTERN.match(target) or target.startswith("#"):
                    continue
                file_part = target.split("#", 1)[0]
                if file_part.startswith("/") or not (path.parent / file_part).exists():
                    errors.append(f"{relative.as_posix()}:{number}: broken link '{target}'")
    return errors


# Implements: HLR-DOC-007
def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point. Returns the process exit status."""
    parser = argparse.ArgumentParser(
        prog="python -m ludus_tools.doccheck",
        description="Check controlled documents and Markdown links.",
    )
    parser.add_argument("--config", type=Path, default=Path("ludus-tools.toml"))
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    errors = check_documents(config) + check_links(config.root, config.exclude_dirs)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        return 1
    print("doccheck: OK")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
