# Contributing to Ludus

Thank you for your interest in Ludus. This guide explains how to contribute. Ludus runs
privileged code on players' machines, so it follows a stricter process than most
open-source projects. The process is defined in the controlled documents listed in the
[document register](docs/README.md); this guide summarizes it. Where this guide and a
controlled document differ, the controlled document applies.

## Before you start

- Read the [Code of Conduct](CODE_OF_CONDUCT.md).
- For anything larger than a small fix, open an issue first: a **change request** for new
  behavior, or a **problem report** for a defect. This avoids work on changes that cannot be
  accepted.
- **Security vulnerabilities are never reported in public.** See [SECURITY.md](SECURITY.md).

## Set up

```sh
git clone <repository URL>
cd ludus
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
make hooks        # checks commit messages when you commit
make check        # must pass before you open a pull request
```

## The workflow in eight steps

1. **Requirements first.** Behavior changes start with a requirement in
   [`requirements/`](requirements/), written to the
   [Requirements Standard](docs/standards/requirements-standard.md). One "shall" per
   statement, a rationale, a verification method and an assurance level.
2. **Branch.** Create a topic branch named `<type>/<short-description>`, for example
   `fix/recorder-crc-endianness`.
3. **Code to the standard.** Follow the [Coding Standard](docs/standards/coding-standard.md).
   Put an `Implements:` trace tag on the line above each function that implements a
   requirement.
4. **Test.** Write requirements-based tests for normal and robustness cases, with a
   `Verifies:` trace tag above each test. Coverage must stay at 100%. A fix for a problem
   report includes a regression test that fails without the fix
   ([SVP](docs/plans/svp.md), section 8).
5. **Document.** If you change a controlled document, increase its `revision` and add a row
   to its revision history ([Documentation Standard](docs/standards/documentation-standard.md)).
   Add an entry to the `[Unreleased]` section of [CHANGELOG.md](CHANGELOG.md) for changes
   users or contributors will notice.
6. **Regenerate the matrix** if you changed requirements or trace tags: `make matrix`.
7. **Commit** with messages that follow the [SCMP](docs/plans/scmp.md), section 6:

   ```text
   fix(recorder): use little-endian CRC field in block header

   Readers on big-endian hosts rejected valid session files.

   Refs: #42
   ```

   `feat`, `fix` and `perf` commits need a `Refs:` trailer. Headers are at most 72
   characters. History stays linear: rebase on `main`, never merge it into your branch.
8. **Open a pull request** and complete the template. Reviews depend on the assurance level
   of what you changed ([SVP](docs/plans/svp.md), section 2).

## Assurance levels in one paragraph

Every component has a Ludus Assurance Level ([PSAA](docs/plans/psaa.md), section 4).
**LAL-1** covers privileged code and the rollback path and needs 100% MC/DC coverage and
independent review. **LAL-2** covers unprivileged code that changes game behavior, and the
process tools, and needs 100% decision coverage. **LAL-3** needs 100% statement coverage. A
component that is not yet classified is treated as LAL-1.

## AI-assisted contributions

Contributions prepared with AI assistance are welcome under the same rules as any other
contribution: you must understand, review and be able to explain every line you submit.
Disclose the assistance in the pull request template and record it in the commit with a
`Co-Authored-By:` trailer or a note in the body.

## Licensing of contributions

By submitting a contribution, you agree that it is licensed under the license of the files
it changes, as declared by their SPDX headers or in [REUSE.toml](REUSE.toml) (inbound license
equals outbound license). New files carry SPDX headers; `make check` verifies this with
`reuse lint`. Do not submit code you do not have the right to license this way.

## Getting help

Open an issue. Maintainers are listed in [MAINTAINERS.md](MAINTAINERS.md).
