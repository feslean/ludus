# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Release consistency checker (tool T-004, LUD-PRC-002).

Checks that the version identifier is a valid Semantic Versioning 2.0.0
version and is consistent across the files listed in the SCMP (LUD-PLN-004,
section 7) and that the changelog has a section for it.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from ludus_tools._config import ConfigError, display, get_str, load_section, read_text

# Regular expression published with the Semantic Versioning 2.0.0 specification.
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
INIT_VERSION_PATTERN = re.compile(r'^__version__ = "([^"]*)"$', re.MULTILINE)
UNRELEASED_HEADING = "## [Unreleased]"


@dataclass(frozen=True)
class ReleaseConfig:
    """Settings of the ``[release]`` section."""

    root: Path
    version_file: Path
    pyproject: Path
    package_init: Path
    changelog: Path


# Implements: HLR-REL-004
def load_config(path: Path) -> ReleaseConfig:
    """Read the ``[release]`` section of the tool configuration file."""
    section = load_section(path, "release")
    root = path.resolve().parent
    return ReleaseConfig(
        root=root,
        version_file=root / get_str(section, "version_file", path),
        pyproject=root / get_str(section, "pyproject", path),
        package_init=root / get_str(section, "package_init", path),
        changelog=root / get_str(section, "changelog", path),
    )


def _read(path: Path, root: Path, errors: list[str]) -> str | None:
    text = read_text(path) if path.is_file() else None
    if text is None:
        errors.append(f"{display(path, root)}: file is missing or not valid UTF-8")
    return text


# Implements: HLR-REL-001
def _pyproject_version(text: str) -> str | None:
    try:
        project = tomllib.loads(text).get("project")
    except tomllib.TOMLDecodeError:
        return None
    version = project.get("version") if isinstance(project, dict) else None
    return version if isinstance(version, str) else None


# Implements: HLR-REL-001, HLR-REL-002, HLR-REL-003
def check_release(config: ReleaseConfig) -> list[str]:
    """Return the version consistency errors of the repository."""
    errors: list[str] = []
    root = config.root
    version_text = _read(config.version_file, root, errors)
    if version_text is None:
        return errors
    version = version_text.strip()
    if not SEMVER_PATTERN.match(version):
        errors.append(
            f"{display(config.version_file, root)}: '{version}' is not a SemVer 2.0.0 version"
        )

    pyproject_text = _read(config.pyproject, root, errors)
    if pyproject_text is not None:
        declared = _pyproject_version(pyproject_text)
        if declared != version:
            errors.append(
                f"{display(config.pyproject, root)}: project version {declared!r} "
                f"differs from VERSION {version!r}"
            )

    init_text = _read(config.package_init, root, errors)
    if init_text is not None:
        match = INIT_VERSION_PATTERN.search(init_text)
        declared = match.group(1) if match else None
        if declared != version:
            errors.append(
                f"{display(config.package_init, root)}: __version__ {declared!r} "
                f"differs from VERSION {version!r}"
            )

    changelog_text = _read(config.changelog, root, errors)
    if changelog_text is not None:
        lines = changelog_text.splitlines()
        name = display(config.changelog, root)
        if UNRELEASED_HEADING not in lines:
            errors.append(f"{name}: missing '{UNRELEASED_HEADING}' section")
        section = re.compile(rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$")
        if not any(section.match(line) for line in lines):
            errors.append(f"{name}: missing '## [{version}] - YYYY-MM-DD' section")
    return errors


# Implements: HLR-REL-004
def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point. Returns the process exit status."""
    parser = argparse.ArgumentParser(
        prog="python -m ludus_tools.release",
        description="Check version identifier consistency and the changelog.",
    )
    parser.add_argument("--config", type=Path, default=Path("ludus-tools.toml"))
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    errors = check_release(config)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        return 1
    print("release: OK")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
