# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Requirements-based tests for the controlled document checker (T-002)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ludus_tools import doccheck
from tests.tools.helpers import INVALID_UTF8, write, write_bytes

CONFIG = """
[doccheck]
controlled_dirs = ["docs"]
register = "docs/README.md"
exclude_dirs = [".git", "vendor"]
"""


def document(
    doc_id: str = "LUD-TST-001",
    revision: str = "1.0",
    status: str = "baselined",
    history: str = "| 1.0 | Initial release. |\n",
    body: str = "",
) -> str:
    return (
        "---\n"
        f"doc_id: {doc_id}\n"
        "title: Test document\n"
        f'revision: "{revision}"\n'
        f"status: {status}\n"
        "owner: Project lead\n"
        "---\n\n"
        "# Test document\n\n"
        f"{body}\n"
        "## Revision history\n\n"
        "| Revision | Description |\n"
        "|---|---|\n"
        f"{history}"
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository with one valid controlled document and a valid register."""
    write(tmp_path / "ludus-tools.toml", CONFIG)
    write(
        tmp_path / "docs" / "README.md",
        document(doc_id="LUD-PRJ-000", body="Register: LUD-PRJ-000, LUD-TST-001.\n"),
    )
    write(tmp_path / "docs" / "test.md", document(body="See [register](README.md).\n"))
    return tmp_path


def run(repo: Path) -> int:
    return doccheck.main(["--config", str(repo / "ludus-tools.toml")])


def document_errors(repo: Path) -> list[str]:
    return doccheck.check_documents(doccheck.load_config(repo / "ludus-tools.toml"))


def link_errors(repo: Path) -> list[str]:
    config = doccheck.load_config(repo / "ludus-tools.toml")
    return doccheck.check_links(config.root, config.exclude_dirs)


# ------------------------------------------------------- exit status, config


# Verifies: HLR-DOC-007
def test_valid_repository_passes(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo) == 0
    assert "doccheck: OK" in capsys.readouterr().out


# Verifies: HLR-DOC-007
def test_errors_give_status_one(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(repo / "docs" / "test.md", document(body="See [gone](missing.md).\n"))
    assert run(repo) == 1
    assert "broken link 'missing.md'" in capsys.readouterr().err


# Verifies: HLR-DOC-007
def test_configuration_errors(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path / "cfg.toml", "[doccheck]\ncontrolled_dirs = []\n")
    assert doccheck.main(["--config", str(tmp_path / "cfg.toml")]) == 1
    assert "'controlled_dirs' must be a non-empty list" in capsys.readouterr().err


# Verifies: HLR-DOC-007
def test_missing_configuration(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert doccheck.main(["--config", str(tmp_path / "none.toml")]) == 1
    assert "configuration file not found" in capsys.readouterr().err


# ----------------------------------------------------------------- front matter


# Verifies: HLR-DOC-001
@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("# No front matter\n", "does not start with front matter"),
        ("", "does not start with front matter"),
        ("---\ndoc_id LUD-TST-002\n---\n", "malformed front matter line 'doc_id LUD-TST-002'"),
        ("---\n: value\n---\n", "malformed front matter line ': value'"),
        ("---\ndoc_id: LUD-TST-002\n", "front matter is not terminated"),
    ],
)
def test_front_matter_problems(repo: Path, text: str, message: str) -> None:
    write(repo / "docs" / "other.md", text)
    errors = document_errors(repo)
    assert any(error.startswith("docs/other.md: ") and message in error for error in errors), errors


# Verifies: HLR-DOC-001
def test_missing_front_matter_keys(repo: Path) -> None:
    write(repo / "docs" / "other.md", "---\ndoc_id: LUD-TST-002\ntitle: x\nowner:\n---\n")
    assert document_errors(repo) == [
        "docs/other.md: missing front matter keys: revision, status, owner"
    ]


# Verifies: HLR-DOC-001
def test_controlled_document_not_utf8(repo: Path) -> None:
    write_bytes(repo / "docs" / "binary.md", INVALID_UTF8)
    assert "docs/binary.md: file is not valid UTF-8" in document_errors(repo)


# Verifies: HLR-DOC-001
def test_missing_controlled_directory(repo: Path) -> None:
    write(repo / "ludus-tools.toml", CONFIG.replace('["docs"]', '["docs", "absent"]'))
    assert document_errors(repo) == ["absent: controlled directory does not exist"]


# ------------------------------------------------------------------ identifiers


# Verifies: HLR-DOC-002
@pytest.mark.parametrize("bad_id", ["LUD-TS-001", "LUD-TST-01", "XYZ-TST-001", "lud-tst-001"])
def test_malformed_document_identifier(repo: Path, bad_id: str) -> None:
    write(repo / "docs" / "other.md", document(doc_id=bad_id))
    assert f"docs/other.md: document identifier '{bad_id}' is malformed" in document_errors(repo)


# Verifies: HLR-DOC-002
def test_four_digit_identifier_is_accepted(repo: Path) -> None:
    write(repo / "docs" / "adr.md", document(doc_id="LUD-ADR-0001"))
    write(
        repo / "docs" / "README.md", document(doc_id="LUD-PRJ-000", body="LUD-TST-001 LUD-ADR-0001")
    )
    assert document_errors(repo) == []


# Verifies: HLR-DOC-002
def test_duplicate_document_identifier(repo: Path) -> None:
    write(repo / "docs" / "zcopy.md", document())
    assert document_errors(repo) == [
        "docs/zcopy.md: document identifier 'LUD-TST-001' already used by docs/test.md"
    ]


# ----------------------------------------------------------------------- status


# Verifies: HLR-DOC-003
def test_unknown_status(repo: Path) -> None:
    write(repo / "docs" / "test.md", document(status="final"))
    assert document_errors(repo) == ["docs/test.md: unknown document status 'final'"]


# Verifies: HLR-DOC-003
@pytest.mark.parametrize("status", ["draft", "in-review", "baselined", "superseded"])
def test_known_statuses(repo: Path, status: str) -> None:
    write(repo / "docs" / "test.md", document(status=status))
    assert document_errors(repo) == []


# ------------------------------------------------------------- revision history


# Verifies: HLR-DOC-004
def test_missing_revision_history(repo: Path) -> None:
    text = document().split("## Revision history")[0]
    write(repo / "docs" / "test.md", text)
    assert document_errors(repo) == ["docs/test.md: missing '## Revision history' section"]


# Verifies: HLR-DOC-004
def test_empty_revision_history(repo: Path) -> None:
    write(repo / "docs" / "test.md", document(history=""))
    assert document_errors(repo) == ["docs/test.md: revision history table has no entries"]


# Verifies: HLR-DOC-004
def test_revision_mismatch(repo: Path) -> None:
    history = "| 0.9 | Draft. |\n| 1.0 | Release. |\n| 1.1 | Update. |\n"
    write(repo / "docs" / "test.md", document(revision="1.0", history=history))
    assert document_errors(repo) == [
        "docs/test.md: last revision history entry '1.1' does not match front matter revision '1.0'"
    ]


# Verifies: HLR-DOC-004
def test_history_stops_at_next_section(repo: Path) -> None:
    history = "| 1.0 | Release. |\n\n## Appendix\n\n| 2.0 | Not history. |\n"
    write(repo / "docs" / "test.md", document(history=history))
    assert document_errors(repo) == []


# --------------------------------------------------------------------- register


# Verifies: HLR-DOC-005
def test_document_missing_from_register(repo: Path) -> None:
    write(repo / "docs" / "README.md", document(doc_id="LUD-PRJ-000", body="LUD-PRJ-000 only"))
    assert document_errors(repo) == [
        "docs/test.md: LUD-TST-001 is not listed in the document register"
    ]


# Verifies: HLR-DOC-005
def test_register_identifier_must_match_exactly(repo: Path) -> None:
    write(
        repo / "docs" / "README.md", document(doc_id="LUD-PRJ-000", body="LUD-PRJ-000 LUD-TST-0011")
    )
    assert "docs/test.md: LUD-TST-001 is not listed in the document register" in (
        document_errors(repo)
    )


# Verifies: HLR-DOC-005
def test_register_missing(repo: Path) -> None:
    (repo / "docs" / "README.md").unlink()
    assert document_errors(repo) == ["docs/README.md: document register is unreadable"]


# Verifies: HLR-DOC-005
def test_register_not_utf8(repo: Path) -> None:
    write(repo / "ludus-tools.toml", CONFIG.replace("docs/README.md", "register.bin"))
    write_bytes(repo / "register.bin", INVALID_UTF8)
    errors = document_errors(repo)
    assert errors == ["register.bin: document register is unreadable"]


# ------------------------------------------------------------------------ links


# Verifies: HLR-DOC-006
def test_link_kinds(repo: Path) -> None:
    body = (
        "[ok](README.md) [anchor](README.md#section) [here](#local) [dir](.)\n"
        '[web](https://example.org/x.md) [mail](mailto:a@b.c) [titled](README.md "Title")\n'
        "[broken](nope.md) [absolute](/docs/README.md) [badanchor](gone.md#x)\n"
        "`[code](inline.md)` text\n"
        "```\n"
        "[fenced](fenced.md)\n"
        "```\n"
        "  ```text\n"
        "[fenced2](fenced2.md)\n"
        "  ```\n"
    )
    write(repo / "docs" / "test.md", document(body=body))
    assert link_errors(repo) == [
        "docs/test.md:13: broken link 'nope.md'",
        "docs/test.md:13: broken link '/docs/README.md'",
        "docs/test.md:13: broken link 'gone.md#x'",
    ]


# Verifies: HLR-DOC-006
def test_links_in_uncontrolled_and_excluded_files(repo: Path) -> None:
    write(repo / "README.md", "[docs](docs/README.md) [bad](missing.md)\n")
    write(repo / "vendor" / "x.md", "[bad](missing.md)\n")
    write(repo / ".git" / "y.md", "[bad](missing.md)\n")
    assert link_errors(repo) == ["README.md:1: broken link 'missing.md'"]


# Verifies: HLR-DOC-006
def test_markdown_file_not_utf8(repo: Path) -> None:
    write_bytes(repo / "notes.md", INVALID_UTF8)
    assert link_errors(repo) == ["notes.md: file is not valid UTF-8"]
