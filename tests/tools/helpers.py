# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Shared helpers for the tool tests.

Traceability tags inside fixture content are always produced by ``tag()`` so that
no line of this test suite starts with a comment marker followed by a tag keyword
unless it is a real tag of the Ludus repository.
"""

from __future__ import annotations

import json
from pathlib import Path

INVALID_UTF8 = b"\xff\xfe\xfa not utf-8\n"


def write(path: Path, text: str) -> Path:
    """Write ``text`` to ``path``, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_bytes(path: Path, data: bytes) -> Path:
    """Write raw ``data`` to ``path``, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def tag(kind: str, ids: str, marker: str = "#") -> str:
    """Return one traceability tag line for fixture files."""
    return f"{marker} {kind}: {ids}\n"


def toml_requirement(**fields: object) -> str:
    """Return one ``[[requirement]]`` table with the given attributes."""
    body = "".join(f"{key} = {json.dumps(value)}\n" for key, value in fields.items())
    return "[[requirement]]\n" + body + "\n"


def sys_requirement(**overrides: object) -> str:
    """Return a valid system requirement, with optional overrides."""
    fields: dict[str, object] = {
        "id": "SYS-ABC-001",
        "title": "System thing",
        "statement": "The system shall do the thing.",
        "rationale": "Because.",
        "verification": ["inspection"],
        "assurance": "LAL-2",
        "status": "approved",
    }
    fields.update(overrides)
    return toml_requirement(**fields)


def hlr_requirement(**overrides: object) -> str:
    """Return a valid high-level requirement, with optional overrides."""
    fields: dict[str, object] = {
        "id": "HLR-ABC-001",
        "title": "Software thing",
        "statement": "The software shall do the thing.",
        "rationale": "Because.",
        "verification": ["test"],
        "assurance": "LAL-2",
        "status": "implemented",
        "parents": ["SYS-ABC-001"],
    }
    fields.update(overrides)
    return toml_requirement(**fields)
