# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Shared configuration loading for the Ludus process tools."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path


class ConfigError(Exception):
    """Raised when a tool configuration file cannot be used."""


# Implements: HLR-TRC-016, HLR-DOC-007
def load_section(path: Path, name: str) -> dict[str, object]:
    """Return the table called ``name`` from the TOML file at ``path``."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ConfigError(f"{path}: configuration file not found") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise ConfigError(f"{path}: cannot read configuration file: {exc}") from None
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path}: configuration file is not valid TOML: {exc}") from None
    section = data.get(name)
    if not isinstance(section, dict):
        raise ConfigError(f"{path}: missing [{name}] section")
    return section


# Implements: HLR-TRC-016, HLR-DOC-007
def get_str(section: dict[str, object], key: str, path: Path) -> str:
    """Return a mandatory non-empty string setting."""
    value = section.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{path}: setting '{key}' must be a non-empty string")
    return value


# Implements: HLR-TRC-016, HLR-DOC-007
def get_str_list(section: dict[str, object], key: str, path: Path) -> list[str]:
    """Return a mandatory non-empty list of non-empty strings."""
    value = section.get(key)
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) and item.strip() for item in value)
    ):
        raise ConfigError(f"{path}: setting '{key}' must be a non-empty list of strings")
    return [str(item) for item in value]


# Implements: HLR-TRC-013
def display(path: Path, root: Path) -> str:
    """Return ``path`` relative to ``root`` using forward slashes."""
    return Path(os.path.relpath(path, root)).as_posix()


# Implements: HLR-TRC-001, HLR-TRC-009, HLR-DOC-001, HLR-DOC-006
def read_text(path: Path) -> str | None:
    """Return the UTF-8 content of ``path`` or ``None`` if it is not valid UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
