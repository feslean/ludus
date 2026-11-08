# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
"""Requirements-based tests for the commit message checker (T-003)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from ludus_tools import commitcheck
from tests.tools.helpers import INVALID_UTF8, write, write_bytes

VALID = "feat(trace): add matrix generation\n\nLonger explanation.\n\nRefs: HLR-TRC-013, #12\n"


def git(repo: Path, *args: str) -> None:
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.org", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", "-b", "main")
    write(tmp_path / "a.txt", "a\n")
    git(tmp_path, "add", "a.txt")
    git(tmp_path, "commit", "-q", "-m", "chore: initial commit")
    return tmp_path


def commit(repo: Path, message: str) -> None:
    write(repo / "a.txt", (repo / "a.txt").read_text() + "x\n")
    git(repo, "commit", "-q", "-a", "-m", message)


# ---------------------------------------------------------------------- header


# Verifies: HLR-CMT-001
def test_valid_message_has_no_errors() -> None:
    assert commitcheck.check_message(VALID) == []


# Verifies: HLR-CMT-001
@pytest.mark.parametrize(
    "header",
    ["update the docs", "Docs: update", "docs(Trace): update", "docs:update", "docs: ", "fix()"],
)
def test_malformed_headers(header: str) -> None:
    assert commitcheck.check_message(header) == [
        "header must have the form '<type>(<scope>): <subject>'"
    ]


# Verifies: HLR-CMT-001
def test_unknown_type() -> None:
    assert commitcheck.check_message("feature: add thing") == ["unknown commit type 'feature'"]


# Verifies: HLR-CMT-001
@pytest.mark.parametrize(
    "header",
    ["docs: fix typo", "ci(workflows): pin actions", "chore(release-1): prepare", "test!: drop"],
)
def test_accepted_headers(header: str) -> None:
    message = header if "!" not in header else header + "\n\nBREAKING CHANGE: removed."
    assert commitcheck.check_message(message) == []


# Verifies: HLR-CMT-002
def test_header_too_long() -> None:
    header = "docs: " + "x" * 67
    assert commitcheck.check_message(header) == ["header is 73 characters long (maximum 72)"]
    assert commitcheck.check_message(header[:-1]) == []


# Verifies: HLR-CMT-002
def test_header_with_period() -> None:
    assert commitcheck.check_message("docs: update readme.") == [
        "header must not end with a period"
    ]


# ------------------------------------------------------------------------ body


# Verifies: HLR-CMT-003
def test_second_line_must_be_blank() -> None:
    assert commitcheck.check_message("docs: update\nbody right away") == [
        "the line after the header must be blank"
    ]


# Verifies: HLR-CMT-003
def test_long_body_lines() -> None:
    long_line = "word " * 21
    url_line = "See https://example.org/" + "a" * 120
    message = f"docs: update\n\n{long_line}\n{url_line}\n"
    assert commitcheck.check_message(message) == ["line 3 is longer than 100 characters"]


# Verifies: HLR-CMT-003, HLR-CMT-006
def test_trailing_blank_lines_are_ignored() -> None:
    assert commitcheck.check_message("docs: update\n\n\n\n") == []


# ------------------------------------------------------------------ references


# Verifies: HLR-CMT-004
@pytest.mark.parametrize("kind", ["feat", "fix", "perf"])
def test_functional_commits_need_refs(kind: str) -> None:
    assert commitcheck.check_message(f"{kind}: change behaviour") == [
        f"'{kind}' commits must include a 'Refs:' trailer"
    ]


# Verifies: HLR-CMT-004
def test_empty_and_invalid_refs() -> None:
    message = "fix: repair\n\nRefs:\nRefs: HLR-TRC-001, PROJ-12, #x\n"
    assert commitcheck.check_message(message) == [
        "'Refs:' trailer is empty",
        "invalid reference 'PROJ-12' in 'Refs:' trailer",
        "invalid reference '#x' in 'Refs:' trailer",
    ]


# Verifies: HLR-CMT-004
def test_refs_are_optional_for_other_types() -> None:
    assert commitcheck.check_message("docs: update\n\nRefs: #3\n") == []
    assert commitcheck.check_message("refactor: tidy") == []


# -------------------------------------------------------------- breaking change


# Verifies: HLR-CMT-005
def test_breaking_change_needs_footer() -> None:
    assert commitcheck.check_message("feat(api)!: change\n\nRefs: #1\n") == [
        "breaking changes must be explained in a 'BREAKING CHANGE: ' footer"
    ]
    explained = "feat(api)!: change\n\nRefs: #1\nBREAKING CHANGE: field renamed.\n"
    assert commitcheck.check_message(explained) == []


# ------------------------------------------------------------- empty and merges


# Verifies: HLR-CMT-006
@pytest.mark.parametrize("message", ["", "\n\n", "   \nbody"])
def test_empty_messages(message: str) -> None:
    assert commitcheck.check_message(message) == ["commit message is empty"]


# Verifies: HLR-CMT-006
def test_merge_commits_rejected() -> None:
    assert commitcheck.check_message("Merge branch 'topic' into main") == [
        "merge commits are not permitted; rebase onto the target branch instead"
    ]


# ----------------------------------------------------------------- input modes


# Verifies: HLR-CMT-007
def test_comment_lines_are_stripped_in_message_files() -> None:
    message = (
        "docs: update\n\n# Please enter the commit message\nBody.\n"
        "# ------------------------ >8 ------------------------\n"
        "diff --git a/x b/x with a very long line " + "x" * 120 + "\n"
    )
    assert commitcheck.check_message(message, strip_comments=True) == []
    assert commitcheck.check_message("# only a comment\n", strip_comments=True) == [
        "commit message is empty"
    ]


# Verifies: HLR-CMT-007, HLR-CMT-008
def test_message_file_mode(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    good = write(tmp_path / "good.txt", VALID)
    assert commitcheck.main(["--message-file", str(good)]) == 0
    assert "commitcheck: OK (1 commit message(s) checked)" in capsys.readouterr().out
    bad = write(tmp_path / "bad.txt", "bad message\n")
    assert commitcheck.main(["--message-file", str(bad)]) == 1
    assert "error: header must have the form" in capsys.readouterr().err


# Verifies: HLR-CMT-007, HLR-CMT-008
@pytest.mark.parametrize("make_file", [False, True])
def test_unreadable_message_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], make_file: bool
) -> None:
    path = tmp_path / "message.txt"
    if make_file:
        write_bytes(path, INVALID_UTF8)
    assert commitcheck.main(["--message-file", str(path)]) == 1
    assert f"error: cannot read {path}" in capsys.readouterr().err


# Verifies: HLR-CMT-007
def test_messages_in_range(git_repo: Path) -> None:
    commit(git_repo, "docs: first change")
    commit(git_repo, "docs: second change\n\nWith a body.")
    commits = commitcheck.messages_in_range("HEAD~2..HEAD", git_repo)
    assert [message.strip() for _, message in commits] == [
        "docs: second change\n\nWith a body.",
        "docs: first change",
    ]
    assert all(len(sha) == 40 for sha, _ in commits)


# Verifies: HLR-CMT-007, HLR-CMT-008
def test_range_mode(git_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    commit(git_repo, "docs: fine")
    assert commitcheck.main(["--range", "HEAD~1..HEAD", "--repo", str(git_repo)]) == 0
    assert "(1 commit message(s) checked)" in capsys.readouterr().out
    commit(git_repo, "Bad message.")
    assert commitcheck.main(["--range", "HEAD~2..HEAD", "--repo", str(git_repo)]) == 1
    err = capsys.readouterr().err
    assert ": header must have the form" in err
    assert ": header must not end with a period" in err


# Verifies: HLR-CMT-007
def test_empty_range(git_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert commitcheck.main(["--range", "HEAD..HEAD", "--repo", str(git_repo)]) == 0
    assert "(0 commit message(s) checked)" in capsys.readouterr().out


# Verifies: HLR-CMT-007, HLR-CMT-008
def test_git_failure(git_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert commitcheck.main(["--range", "nosuchref..HEAD", "--repo", str(git_repo)]) == 1
    assert "error:" in capsys.readouterr().err


# Verifies: HLR-CMT-007
def test_git_failure_without_stderr(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def fake_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args=["git"], returncode=128, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(commitcheck.GitError, match="git log exited with status 128"):
        commitcheck.messages_in_range("a..b", tmp_path)


# Verifies: HLR-CMT-008
def test_a_source_is_mandatory() -> None:
    with pytest.raises(SystemExit) as excinfo:
        commitcheck.main([])
    assert excinfo.value.code == 2
