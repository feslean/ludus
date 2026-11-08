# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Requirements-based tests for the traceability checker (T-001)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ludus_tools import trace
from tests.tools.helpers import (
    INVALID_UTF8,
    hlr_requirement,
    sys_requirement,
    tag,
    toml_requirement,
    write,
    write_bytes,
)

CONFIG = """
[trace]
requirements_dirs = ["requirements"]
tag_dirs = ["src", "tests"]
tag_suffixes = [".py", ".c"]
matrix = "docs/matrix.md"
version_file = "VERSION"
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A minimal repository whose traceability is complete and correct."""
    write(tmp_path / "ludus-tools.toml", CONFIG)
    write(tmp_path / "VERSION", "9.9.9\n")
    write(tmp_path / "requirements" / "reqs.toml", sys_requirement() + hlr_requirement())
    write(tmp_path / "src" / "impl.py", tag("Implements", "HLR-ABC-001") + "x = 1\n")
    write(tmp_path / "tests" / "test_impl.py", tag("Verifies", "HLR-ABC-001") + "y = 2\n")
    return tmp_path


def run(repo: Path, *args: str) -> int:
    return trace.main(["--config", str(repo / "ludus-tools.toml"), *args])


def errors_for(repo: Path, requirements_text: str) -> list[str]:
    write(repo / "requirements" / "reqs.toml", requirements_text)
    config = trace.load_config(repo / "ludus-tools.toml")
    requirements, errors = trace.load_requirements(config.requirements_dirs, config.root)
    tags, tag_errors = trace.scan_tags(config.tag_dirs, config.tag_suffixes, config.root)
    return errors + tag_errors + trace.check(requirements, tags)


def joined(errors: list[str]) -> str:
    return "\n".join(errors)


# ----------------------------------------------------------------- exit status


# Verifies: HLR-TRC-015
def test_valid_repository_passes(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo, "check") == 0
    assert "trace: OK (2 requirements, 2 tags)" in capsys.readouterr().out


# Verifies: HLR-TRC-015
def test_errors_give_status_one(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(repo / "src" / "impl.py", "x = 1\n")
    assert run(repo, "check") == 1
    assert "no Implements tag references this requirement" in capsys.readouterr().err


# --------------------------------------------------------------- configuration


# Verifies: HLR-TRC-016
def test_missing_configuration_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert trace.main(["--config", str(tmp_path / "absent.toml"), "check"]) == 1
    assert "configuration file not found" in capsys.readouterr().err


# Verifies: HLR-TRC-016
def test_unreadable_configuration_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "dir.toml").mkdir()
    assert trace.main(["--config", str(tmp_path / "dir.toml"), "check"]) == 1
    assert "cannot read configuration file" in capsys.readouterr().err


# Verifies: HLR-TRC-016
def test_non_utf8_configuration_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write_bytes(tmp_path / "bad.toml", INVALID_UTF8)
    assert trace.main(["--config", str(tmp_path / "bad.toml"), "check"]) == 1
    assert "cannot read configuration file" in capsys.readouterr().err


# Verifies: HLR-TRC-016
def test_invalid_toml_configuration(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path / "bad.toml", "[trace\n")
    assert trace.main(["--config", str(tmp_path / "bad.toml"), "check"]) == 1
    assert "not valid TOML" in capsys.readouterr().err


# Verifies: HLR-TRC-016
def test_missing_section(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path / "cfg.toml", "[other]\nkey = 1\n")
    assert trace.main(["--config", str(tmp_path / "cfg.toml"), "check"]) == 1
    assert "missing [trace] section" in capsys.readouterr().err


# Verifies: HLR-TRC-016
@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ('matrix = "docs/matrix.md"', "matrix = 3", "'matrix' must be a non-empty string"),
        ('matrix = "docs/matrix.md"', 'matrix = "  "', "'matrix' must be a non-empty string"),
        (
            'requirements_dirs = ["requirements"]',
            "requirements_dirs = []",
            "'requirements_dirs' must be a non-empty list of strings",
        ),
        (
            'tag_suffixes = [".py", ".c"]',
            'tag_suffixes = [".py", 1]',
            "'tag_suffixes' must be a non-empty list of strings",
        ),
    ],
)
def test_invalid_settings(
    repo: Path, capsys: pytest.CaptureFixture[str], old: str, new: str, message: str
) -> None:
    write(repo / "ludus-tools.toml", CONFIG.replace(old, new))
    assert run(repo, "check") == 1
    assert message in capsys.readouterr().err


# Verifies: HLR-TRC-016
@pytest.mark.parametrize("content", [None, "  \n"])
def test_missing_or_empty_version_file(
    repo: Path, capsys: pytest.CaptureFixture[str], content: str | None
) -> None:
    if content is None:
        (repo / "VERSION").unlink()
    else:
        write(repo / "VERSION", content)
    assert run(repo, "check") == 1
    assert "is missing or empty" in capsys.readouterr().err


# Verifies: HLR-TRC-016
def test_non_utf8_version_file(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write_bytes(repo / "VERSION", INVALID_UTF8)
    assert run(repo, "check") == 1
    assert "is missing or empty" in capsys.readouterr().err


# ------------------------------------------------------------ file-level rules


# Verifies: HLR-TRC-001
def test_missing_requirements_directory(repo: Path) -> None:
    write(repo / "ludus-tools.toml", CONFIG.replace('["requirements"]', '["nowhere"]'))
    config = trace.load_config(repo / "ludus-tools.toml")
    _, errors = trace.load_requirements(config.requirements_dirs, config.root)
    assert errors == ["nowhere: requirements directory does not exist"]


# Verifies: HLR-TRC-001
def test_non_utf8_requirements_file(repo: Path) -> None:
    write_bytes(repo / "requirements" / "broken.toml", INVALID_UTF8)
    config = trace.load_config(repo / "ludus-tools.toml")
    _, errors = trace.load_requirements(config.requirements_dirs, config.root)
    assert errors == ["requirements/broken.toml: file is not valid UTF-8"]


# Verifies: HLR-TRC-001
def test_invalid_toml_requirements_file(repo: Path) -> None:
    write(repo / "requirements" / "broken.toml", "[[requirement]\n")
    config = trace.load_config(repo / "ludus-tools.toml")
    _, errors = trace.load_requirements(config.requirements_dirs, config.root)
    assert len(errors) == 1
    assert errors[0].startswith("requirements/broken.toml: file is not valid TOML")


# Verifies: HLR-TRC-001
@pytest.mark.parametrize("content", ["", 'requirement = "text"\n', "requirement = []\n"])
def test_file_without_requirement_tables(repo: Path, content: str) -> None:
    write(repo / "requirements" / "empty.toml", content)
    config = trace.load_config(repo / "ludus-tools.toml")
    _, errors = trace.load_requirements(config.requirements_dirs, config.root)
    assert errors == ["requirements/empty.toml: no [[requirement]] tables found"]


# ------------------------------------------------------- per-requirement rules


# Verifies: HLR-TRC-002
def test_entry_that_is_not_a_table(repo: Path) -> None:
    write(repo / "requirements" / "bad.toml", 'requirement = [1, "two"]\n')
    config = trace.load_config(repo / "ludus-tools.toml")
    requirements, errors = trace.load_requirements(config.requirements_dirs, config.root)
    assert errors == ["requirements/bad.toml: requirement entry is not a table"] * 2
    assert [req.id for req in requirements] == ["SYS-ABC-001", "HLR-ABC-001"]


# Verifies: HLR-TRC-002
@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"title": ""}, "attribute 'title' must be a non-empty string"),
        ({"status": 5}, "attribute 'status' must be a non-empty string"),
        ({"verification": "test"}, "attribute 'verification' must be a non-empty list"),
        ({"verification": []}, "attribute 'verification' must be a non-empty list"),
        ({"parents": "SYS-ABC-001"}, "attribute 'parents' must be a list of strings"),
        ({"derived": "yes"}, "attribute 'derived' must be a boolean"),
        ({"derived_rationale": 7}, "attribute 'derived_rationale' must be a string"),
    ],
)
def test_attribute_types(repo: Path, overrides: dict[str, object], message: str) -> None:
    errors = errors_for(repo, sys_requirement() + hlr_requirement(**overrides))
    assert any(message in error for error in errors), errors


# Verifies: HLR-TRC-002
def test_missing_identifier_is_labelled(repo: Path) -> None:
    text = toml_requirement(
        title="T", statement="It shall work.", rationale="R", verification=["test"]
    )
    errors = errors_for(repo, sys_requirement() + text)
    assert "requirements/reqs.toml: <missing id>: attribute 'id' must be a non-empty string" in (
        errors
    )


# Verifies: HLR-TRC-003
@pytest.mark.parametrize("bad_id", ["HLR-AB-001", "hlr-ABC-001", "REQ-ABC-001", "HLR-ABC-01"])
def test_identifier_format(repo: Path, bad_id: str) -> None:
    errors = errors_for(repo, sys_requirement() + hlr_requirement(id=bad_id, parents=[]))
    assert f"requirements/reqs.toml: {bad_id}: identifier does not match LEVEL-AREA-NNN" in errors
    assert not any("no parent" in error for error in errors)


# Verifies: HLR-TRC-004
def test_duplicate_identifiers(repo: Path) -> None:
    errors = errors_for(repo, sys_requirement() + hlr_requirement() + hlr_requirement())
    assert (
        "requirements/reqs.toml: HLR-ABC-001: duplicate identifier "
        "(first in requirements/reqs.toml)"
    ) in errors


# Verifies: HLR-TRC-005
@pytest.mark.parametrize(
    ("statement", "count"),
    [("The software does the thing.", 0), ("It shall do this and shall do that.", 2)],
)
def test_statement_must_contain_one_shall(repo: Path, statement: str, count: int) -> None:
    errors = errors_for(repo, sys_requirement() + hlr_requirement(statement=statement))
    assert any(f"exactly once (found {count})" in error for error in errors), errors


# Verifies: HLR-TRC-006
@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"verification": ["test", "demo"]}, "unknown verification method 'demo'"),
        ({"assurance": "DAL-A"}, "unknown assurance level 'DAL-A'"),
        ({"status": "done"}, "unknown status 'done'"),
    ],
)
def test_enumerated_values(repo: Path, overrides: dict[str, object], message: str) -> None:
    errors = errors_for(repo, sys_requirement() + hlr_requirement(**overrides))
    assert any(message in error for error in errors), errors


# Verifies: HLR-TRC-007
@pytest.mark.parametrize(
    ("text", "message"),
    [
        (sys_requirement(parents=["SYS-ABC-002"]), "system requirements must not have parents"),
        (sys_requirement(derived=True), "system requirements cannot be derived"),
        (hlr_requirement(parents=[]), "has no parent and is not marked as derived"),
        (
            hlr_requirement(parents=[], derived=True),
            "derived requirements need a 'derived_rationale'",
        ),
        (
            hlr_requirement(id="HLR-ABC-002", parents=["HLR-ABC-001"]),
            "parent 'HLR-ABC-001' must be a SYS requirement",
        ),
        (
            hlr_requirement(id="LLR-ABC-001", parents=["SYS-ABC-001"]),
            "parent 'SYS-ABC-001' must be a HLR requirement",
        ),
    ],
)
def test_level_hierarchy(repo: Path, text: str, message: str) -> None:
    errors = errors_for(repo, sys_requirement() + hlr_requirement() + text)
    assert any(message in error for error in errors), errors


# Verifies: HLR-TRC-007
def test_derived_requirement_with_rationale_is_accepted(repo: Path) -> None:
    derived = hlr_requirement(
        id="HLR-ABC-002",
        parents=[],
        derived=True,
        derived_rationale="Needed by the design.",
        status="draft",
    )
    assert errors_for(repo, sys_requirement() + hlr_requirement() + derived) == []


# Verifies: HLR-TRC-008
def test_missing_and_deleted_parents(repo: Path) -> None:
    text = (
        sys_requirement()
        + sys_requirement(id="SYS-ABC-002", status="deleted")
        + hlr_requirement()
        + hlr_requirement(id="HLR-ABC-002", parents=["SYS-ABC-009"], status="draft")
        + hlr_requirement(id="HLR-ABC-003", parents=["SYS-ABC-002"], status="draft")
    )
    errors = errors_for(repo, text)
    assert "requirements/reqs.toml: HLR-ABC-002: parent 'SYS-ABC-009' is missing or deleted" in (
        errors
    )
    assert "requirements/reqs.toml: HLR-ABC-003: parent 'SYS-ABC-002' is missing or deleted" in (
        errors
    )


# Verifies: HLR-TRC-007, HLR-TRC-008
def test_malformed_parent_is_reported_as_missing(repo: Path) -> None:
    errors = errors_for(repo, sys_requirement() + hlr_requirement(parents=["bogus"]))
    assert "requirements/reqs.toml: HLR-ABC-001: parent 'bogus' is missing or deleted" in errors
    assert not any("must be a SYS requirement" in error for error in errors)


# Verifies: HLR-TRC-008
def test_deleted_requirement_parents_are_not_checked(repo: Path) -> None:
    deleted = hlr_requirement(id="HLR-ABC-002", parents=["SYS-ABC-009"], status="deleted")
    assert errors_for(repo, sys_requirement() + hlr_requirement() + deleted) == []


# ----------------------------------------------------------------------- tags


# Verifies: HLR-TRC-009
def test_tag_directory_missing(repo: Path) -> None:
    write(repo / "ludus-tools.toml", CONFIG.replace('["src", "tests"]', '["src", "gone"]'))
    config = trace.load_config(repo / "ludus-tools.toml")
    _, errors = trace.scan_tags(config.tag_dirs, config.tag_suffixes, config.root)
    assert errors == ["gone: tag directory does not exist"]


# Verifies: HLR-TRC-009
def test_tag_file_not_utf8(repo: Path) -> None:
    write_bytes(repo / "src" / "binary.py", INVALID_UTF8)
    config = trace.load_config(repo / "ludus-tools.toml")
    _, errors = trace.scan_tags(config.tag_dirs, config.tag_suffixes, config.root)
    assert errors == ["src/binary.py: file is not valid UTF-8"]


# Verifies: HLR-TRC-009
def test_tag_parsing_variants(repo: Path) -> None:
    content = (
        tag("Implements", "HLR-ABC-001, SYS-ABC-001", marker="//")
        + "/* Verifies: HLR-ABC-001 */\n"
        + tag("Verifies", "HLR-ABC-001 SYS-ABC-001", marker=" *")
        + "int verifies_not_a_tag = 0; /* Verifies: HLR-ABC-001 */\n"
    )
    write(repo / "src" / "impl.c", content)
    write(repo / "src" / "ignored.txt", tag("Verifies", "HLR-ZZZ-999"))
    config = trace.load_config(repo / "ludus-tools.toml")
    tags, errors = trace.scan_tags(config.tag_dirs, config.tag_suffixes, config.root)
    assert errors == []
    found = {(t.kind, t.requirement_id, t.location) for t in tags}
    assert ("Implements", "SYS-ABC-001", "src/impl.c:1") in found
    assert ("Verifies", "HLR-ABC-001", "src/impl.c:2") in found
    assert ("Verifies", "SYS-ABC-001", "src/impl.c:3") in found
    assert not any(t.location == "src/impl.c:4" for t in tags)
    assert not any(t.requirement_id == "HLR-ZZZ-999" for t in tags)


# Verifies: HLR-TRC-009
def test_malformed_and_empty_tags(repo: Path) -> None:
    write(repo / "src" / "bad.py", tag("Verifies", "HLR-ABC-1") + tag("Implements", ""))
    config = trace.load_config(repo / "ludus-tools.toml")
    _, errors = trace.scan_tags(config.tag_dirs, config.tag_suffixes, config.root)
    assert errors == [
        "src/bad.py:1: malformed identifier 'HLR-ABC-1' in Verifies tag",
        "src/bad.py:2: Implements tag lists no requirement",
    ]


# Verifies: HLR-TRC-009
def test_tags_referencing_missing_or_deleted_requirements(repo: Path) -> None:
    write(repo / "src" / "extra.py", tag("Implements", "HLR-ABC-009, HLR-ABC-002"))
    deleted = hlr_requirement(id="HLR-ABC-002", status="deleted")
    errors = errors_for(repo, sys_requirement() + hlr_requirement() + deleted)
    assert "src/extra.py:1: Implements tag references missing or deleted 'HLR-ABC-009'" in errors
    assert "src/extra.py:1: Implements tag references missing or deleted 'HLR-ABC-002'" in errors


# ------------------------------------------------------------- coverage rules


# Verifies: HLR-TRC-010
def test_implemented_requirement_without_test(repo: Path) -> None:
    write(repo / "tests" / "test_impl.py", "y = 2\n")
    errors = errors_for(repo, sys_requirement() + hlr_requirement(status="verified"))
    assert "requirements/reqs.toml: HLR-ABC-001: no Verifies tag references this requirement" in (
        errors
    )


# Verifies: HLR-TRC-010
@pytest.mark.parametrize(
    "overrides", [{"verification": ["review"]}, {"status": "draft"}, {"status": "approved"}]
)
def test_test_coverage_not_required(repo: Path, overrides: dict[str, object]) -> None:
    write(repo / "tests" / "test_impl.py", "y = 2\n")
    errors = errors_for(repo, sys_requirement() + hlr_requirement(**overrides))
    assert not any("no Verifies tag" in error for error in errors), errors


# Verifies: HLR-TRC-011
def test_implemented_hlr_without_implementation(repo: Path) -> None:
    write(repo / "src" / "impl.py", "x = 1\n")
    errors = errors_for(repo, sys_requirement() + hlr_requirement())
    assert errors == [
        "requirements/reqs.toml: HLR-ABC-001: no Implements tag references this requirement"
    ]


# Verifies: HLR-TRC-011
def test_system_requirement_needs_no_implements_tag(repo: Path) -> None:
    text = sys_requirement(status="implemented", verification=["review"]) + hlr_requirement()
    assert errors_for(repo, text) == []


# Verifies: HLR-TRC-012
def test_approved_system_requirement_without_children(repo: Path) -> None:
    text = sys_requirement() + sys_requirement(id="SYS-ABC-002") + hlr_requirement()
    errors = errors_for(repo, text)
    assert errors == [
        "requirements/reqs.toml: SYS-ABC-002: system requirement has no child requirement"
    ]


# Verifies: HLR-TRC-012
def test_children_rule_ignores_drafts_and_deleted_children(repo: Path) -> None:
    text = (
        sys_requirement()
        + sys_requirement(id="SYS-ABC-002", status="draft")
        + sys_requirement(id="SYS-ABC-003")
        + hlr_requirement()
        + hlr_requirement(id="HLR-ABC-002", parents=["SYS-ABC-003"], status="deleted")
    )
    errors = errors_for(repo, text)
    assert errors == [
        "requirements/reqs.toml: SYS-ABC-003: system requirement has no child requirement"
    ]


# ---------------------------------------------------------------------- matrix


# Verifies: HLR-TRC-013
def test_matrix_content_and_order(repo: Path) -> None:
    text = (
        hlr_requirement(id="LLR-ABC-001", parents=["HLR-ABC-001"], status="draft", title="A|B")
        + hlr_requirement()
        + sys_requirement()
        + hlr_requirement()
    )
    write(repo / "requirements" / "reqs.toml", text)
    config = trace.load_config(repo / "ludus-tools.toml")
    requirements, _ = trace.load_requirements(config.requirements_dirs, config.root)
    tags, _ = trace.scan_tags(config.tag_dirs, config.tag_suffixes, config.root)
    matrix = trace.render_matrix(requirements, tags, "1.2.3")
    rows = [line for line in matrix.splitlines() if line.startswith("| ") and "-ABC-" in line]
    assert [row.split(" | ")[0] for row in rows] == [
        "| SYS-ABC-001",
        "| HLR-ABC-001",
        "| LLR-ABC-001",
    ]
    assert "| HLR-ABC-001 | Software thing | LAL-2 | implemented | SYS-ABC-001 | LLR-ABC-001 |" in (
        matrix
    )
    assert "src/impl.py:1" in matrix
    assert "tests/test_impl.py:1" in matrix
    assert "A\\|B" in matrix
    assert 'revision: "1.2.3"' in matrix
    assert "| 1.2.3 | Generated for baseline 1.2.3. |" in matrix
    assert "- Implemented requirements with test verification that have a Verifies tag: 1 of 1" in (
        matrix
    )
    assert matrix == trace.render_matrix(
        list(reversed(requirements)), list(reversed(tags)), "1.2.3"
    )


# Verifies: HLR-TRC-013
def test_matrix_placeholders_and_unknown_levels(repo: Path) -> None:
    text = sys_requirement() + hlr_requirement(id="XYZ-ABC-001", status="other", parents=[])
    write(repo / "requirements" / "reqs.toml", text)
    config = trace.load_config(repo / "ludus-tools.toml")
    requirements, _ = trace.load_requirements(config.requirements_dirs, config.root)
    matrix = trace.render_matrix(requirements, [], "1.0")
    assert "| SYS-ABC-001 | System thing | LAL-2 | approved | - | - | - | - |" in matrix
    assert matrix.index("SYS-ABC-001 |") < matrix.index("XYZ-ABC-001 |")
    assert "- Status `other`: 1" in matrix


# Verifies: HLR-TRC-013, HLR-TRC-014
def test_matrix_write_then_check(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo, "matrix", "--write") == 0
    assert (repo / "docs" / "matrix.md").is_file()
    assert run(repo, "matrix", "--check") == 0
    assert "trace: OK" in capsys.readouterr().out


# Verifies: HLR-TRC-014
def test_matrix_check_missing(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo, "matrix", "--check") == 1
    assert "docs/matrix.md: matrix is missing or out of date" in capsys.readouterr().err


# Verifies: HLR-TRC-014
def test_matrix_check_out_of_date(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo, "matrix", "--write") == 0
    write(repo / "VERSION", "10.0.0\n")
    assert run(repo, "matrix", "--check") == 1
    assert "matrix is missing or out of date" in capsys.readouterr().err


# Verifies: HLR-TRC-014
def test_matrix_check_not_utf8(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    write_bytes(repo / "docs" / "matrix.md", INVALID_UTF8)
    assert run(repo, "matrix", "--check") == 1
    assert "matrix is missing or out of date" in capsys.readouterr().err


# Verifies: HLR-TRC-015
def test_command_is_mandatory(repo: Path) -> None:
    with pytest.raises(SystemExit) as excinfo:
        trace.main(["--config", str(repo / "ludus-tools.toml")])
    assert excinfo.value.code == 2
