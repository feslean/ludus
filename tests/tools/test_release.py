# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Requirements-based tests for the release consistency checker (T-004)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ludus_tools import release
from tests.tools.helpers import INVALID_UTF8, write, write_bytes

CONFIG = """
[release]
version_file = "VERSION"
pyproject = "pyproject.toml"
package_init = "pkg/__init__.py"
changelog = "CHANGELOG.md"
"""

CHANGELOG = "# Changelog\n\n## [Unreleased]\n\n## [1.2.3] - 2026-11-08\n\n- Added things.\n"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository whose version files are consistent."""
    write(tmp_path / "ludus-tools.toml", CONFIG)
    write(tmp_path / "VERSION", "1.2.3\n")
    write(tmp_path / "pyproject.toml", '[project]\nname = "x"\nversion = "1.2.3"\n')
    write(tmp_path / "pkg" / "__init__.py", '"""Doc."""\n\n__version__ = "1.2.3"\n')
    write(tmp_path / "CHANGELOG.md", CHANGELOG)
    return tmp_path


def errors(repo: Path) -> list[str]:
    return release.check_release(release.load_config(repo / "ludus-tools.toml"))


def run(repo: Path) -> int:
    return release.main(["--config", str(repo / "ludus-tools.toml")])


# Verifies: HLR-REL-004
def test_consistent_repository(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo) == 0
    assert "release: OK" in capsys.readouterr().out


# Verifies: HLR-REL-004
def test_inconsistent_repository_fails(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(repo / "VERSION", "1.2.4\n")
    assert run(repo) == 1
    assert "differs from VERSION '1.2.4'" in capsys.readouterr().err


# Verifies: HLR-REL-004
def test_configuration_errors(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path / "cfg.toml", "[release]\nversion_file = 'VERSION'\n")
    assert release.main(["--config", str(tmp_path / "cfg.toml")]) == 1
    assert "setting 'pyproject' must be a non-empty string" in capsys.readouterr().err


# Verifies: HLR-REL-004
@pytest.mark.parametrize("name", ["VERSION", "pyproject.toml", "pkg/__init__.py", "CHANGELOG.md"])
def test_missing_files(repo: Path, name: str) -> None:
    (repo / name).unlink()
    assert f"{name}: file is missing or not valid UTF-8" in errors(repo)


# Verifies: HLR-REL-004
def test_non_utf8_file(repo: Path) -> None:
    write_bytes(repo / "CHANGELOG.md", INVALID_UTF8)
    assert errors(repo) == ["CHANGELOG.md: file is missing or not valid UTF-8"]


# Verifies: HLR-REL-001
@pytest.mark.parametrize(
    ("content", "declared"),
    [
        ('[project]\nversion = "1.2.4"\n', "'1.2.4'"),
        ('[project]\nname = "x"\n', "None"),
        ("[project\n", "None"),
        ('project = "x"\n', "None"),
        ("[project]\nversion = 1\n", "None"),
    ],
)
def test_pyproject_version_mismatch(repo: Path, content: str, declared: str) -> None:
    write(repo / "pyproject.toml", content)
    assert errors(repo) == [
        f"pyproject.toml: project version {declared} differs from VERSION '1.2.3'"
    ]


# Verifies: HLR-REL-001
@pytest.mark.parametrize(
    ("content", "declared"),
    [('__version__ = "1.0.0"\n', "'1.0.0'"), ("VERSION = '1.2.3'\n", "None")],
)
def test_package_version_mismatch(repo: Path, content: str, declared: str) -> None:
    write(repo / "pkg" / "__init__.py", content)
    assert errors(repo) == [f"pkg/__init__.py: __version__ {declared} differs from VERSION '1.2.3'"]


# Verifies: HLR-REL-002
def test_changelog_without_unreleased_section(repo: Path) -> None:
    write(repo / "CHANGELOG.md", CHANGELOG.replace("## [Unreleased]\n", ""))
    assert errors(repo) == ["CHANGELOG.md: missing '## [Unreleased]' section"]


# Verifies: HLR-REL-002
@pytest.mark.parametrize(
    "heading",
    ["## [1.2.3]", "## [1.2.3] - 08/11/2026", "## 1.2.3 - 2026-11-08", "## [1.2.30] - 2026-11-08"],
)
def test_changelog_without_dated_version_section(repo: Path, heading: str) -> None:
    write(repo / "CHANGELOG.md", CHANGELOG.replace("## [1.2.3] - 2026-11-08", heading))
    assert errors(repo) == ["CHANGELOG.md: missing '## [1.2.3] - YYYY-MM-DD' section"]


# Verifies: HLR-REL-003
@pytest.mark.parametrize("version", ["1.2", "01.2.3", "1.2.3-", "v1.2.3", "1.2.3+", "1.2.3-01"])
def test_invalid_semantic_versions(repo: Path, version: str) -> None:
    write(repo / "VERSION", version + "\n")
    found = errors(repo)
    assert f"VERSION: '{version}' is not a SemVer 2.0.0 version" in found


# Verifies: HLR-REL-003
@pytest.mark.parametrize(
    "version", ["0.1.0", "1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-0.3.7", "1.0.0-rc.1+build.5"]
)
def test_valid_semantic_versions(repo: Path, version: str) -> None:
    write(repo / "VERSION", version + "\n")
    write(repo / "pyproject.toml", f'[project]\nversion = "{version}"\n')
    write(repo / "pkg" / "__init__.py", f'__version__ = "{version}"\n')
    write(repo / "CHANGELOG.md", CHANGELOG.replace("1.2.3", version))
    assert errors(repo) == []
