---
doc_id: LUD-PLN-004
title: Software Configuration Management Plan (SCMP)
revision: "1.0"
status: baselined
owner: Project lead
---

# Software Configuration Management Plan (SCMP)

## 1. Purpose

This plan defines how every Ludus configuration item is identified, changed, baselined,
released and retrieved. It refines the [PSAA](psaa.md) (LUD-PLN-001). Where a rule in this
plan is checked by a tool, the tool and the requirement it implements are named.

## 2. Configuration items

Everything in the Git repository is a configuration item, identified by its path and the
commit that contains it. The repository includes:

| Category | Examples | Control category |
|---|---|---|
| Plans, standards, processes | `docs/plans/`, `docs/standards/`, `docs/process/` | CC1 |
| Requirements | `requirements/*.toml` | CC1 |
| Source code and build files | `tools/`, `Makefile`, `pyproject.toml` | CC1 |
| Verification cases | `tests/` | CC1 |
| Release records | `docs/releases/`, `CHANGELOG.md`, `VERSION` | CC1 |
| Generated trace data | `docs/verification/traceability-matrix.md` | CC1 (regenerated, never hand-edited) |
| Community and template files | `README.md`, `CONTRIBUTING.md`, `.github/` | CC2 |
| Problem reports and change requests | GitHub issues | CC2 |
| CI logs and coverage reports | GitHub Actions run records | CC2 |

**CC1** items are changed only through the full change control of section 4 and are part of
every baseline. **CC2** items are kept under version control or in the issue tracker with
their history, but a change does not need a change request.

Items outside the repository that affect the result (the CI runner images, the Python
interpreter, external tools) are life cycle environment items, controlled by section 9.

## 3. Repository, branches and history

1. The authoritative repository is the public GitHub repository of the project. The branch
   `main` is the integration branch and is always releasable.
2. All changes reach `main` through pull requests from short-lived topic branches. Direct
   pushes to `main` are disabled by branch protection.
3. History on `main` is linear. Pull requests are rebased or squashed; merge commits are not
   permitted (the commit message checker rejects them, `HLR-CMT-006`, and branch protection
   requires linear history).
4. History on `main` is never rewritten. Force pushes and branch deletion are disabled for
   `main` and for release tags.
5. Branch names follow `<type>/<short-description>`, for example
   `feat/recorder-ring-buffer`, using the commit types of section 6.
6. Maintenance branches for released minor versions are named `release/X.Y` and created only
   when a fix must be released for an older minor version.

## 4. Change control

### 4.1 Problem reports and change requests

- A **problem report** records a deviation of the software or its documentation from its
  requirements, standards or plans. It is handled under
  [LUD-PRC-001](../process/problem-reporting.md).
- A **change request** proposes new or changed behavior or a change to a CC1 document. It is
  opened with the change request issue template.

### 4.2 Pull requests

Every pull request:

1. references the problem report, change request or requirement it addresses;
2. completes the pull request template, including the review checklist of the
   [SVP](svp.md), section 5, and the disclosure of AI assistance;
3. passes all CI checks (SVP, section 11);
4. receives the reviews required for the highest LAL of the changed items (SVP, section 2),
   with approval from the code owners listed in `.github/CODEOWNERS`;
5. updates the `[Unreleased]` section of `CHANGELOG.md` when the change is visible to users
   or affects a CC1 document;
6. updates the revision and revision history of every controlled document it changes
   (LUD-STD-004);
7. regenerates the traceability matrix when requirements or trace tags change
   (`make matrix`).

### 4.3 Impact analysis

A change to a requirement, a design element or a CC1 document needs an impact analysis in
the pull request description: which requirements, code, tests and documents are affected,
and which verification must be repeated. The traceability matrix is the starting point.

## 5. Baselines

| Baseline | Content | Identified by |
|---|---|---|
| Planning baseline | Plans, standards and process documents approved at gate G0 | Release 0.1.0 |
| Requirements baseline | Requirements approved for a phase | The release that closes the phase gate |
| Release baseline | Everything in the repository at a release commit | Annotated tag `vX.Y.Z` |

A baseline is created by the release process ([LUD-PRC-003](../process/release-process.md)).
A baselined item changes only through a new commit on `main`; the baseline itself remains
retrievable from its tag.

## 6. Commit message rules

Commit messages are part of the modification history. They follow
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) with the
project rules below. The commit message checker (tool T-003, requirements `HLR-CMT-001` to
`HLR-CMT-008`) enforces rules 1 to 7 in CI for every commit of a pull request and every
commit pushed to `main`, and locally through the optional `commit-msg` hook (`make hooks`).

1. **Header form.** `<type>(<scope>)!: <subject>`. The scope and the `!` breaking-change
   marker are optional. The scope is lower case letters, digits and hyphens.
2. **Types.** One of:

   | Type | Use |
   |---|---|
   | `feat` | New behavior |
   | `fix` | Correction of a problem report |
   | `perf` | Performance change without behavior change |
   | `refactor` | Code change without behavior change |
   | `docs` | Documentation only |
   | `test` | Verification cases only |
   | `build` | Build system, dependencies, packaging |
   | `ci` | CI configuration |
   | `chore` | Repository maintenance that fits no other type |
   | `revert` | Reverts an earlier commit |

3. **Header length.** At most 72 characters, no trailing period. The subject is written in the
   imperative mood ("add", not "added").
4. **Body.** The line after the header is blank. Body lines are at most 100 characters,
   except lines that contain a URL. The body explains why the change is made.
5. **References.** `feat`, `fix` and `perf` commits have at least one `Refs:` trailer naming
   requirement identifiers (for example `Refs: HLR-FRC-001, HLR-FRC-002`) or issue numbers
   (for example `Refs: #42`). Other types may have one. Every value must be a well-formed
   identifier or issue number.
6. **Breaking changes.** A commit with `!` in its header has a `BREAKING CHANGE: ` footer that
   describes the incompatibility and the migration.
7. **No merge commits** (section 3).
8. **Attribution.** When a contribution was prepared with the help of another person or an AI
   tool, the commit records it with a `Co-Authored-By:` trailer or in the body. Contributors
   do not add a `Signed-off-by:` trailer on behalf of anyone else.
9. **Signing.** Commits on `main` should be signed (section 8). This rule is not yet enforced
   (open item OI-003 in the [SAS v0.1.0](../releases/v0.1.0/sas.md)).
10. **Automated dependency updates.** Dependabot writes commit bodies that may not meet
    rule 4. Its pull requests are therefore not checked commit by commit; they are
    squash-merged with a message that meets this section, and CI checks the resulting
    commit after the push to `main`.

Example:

```text
feat(recorder): add CRC-32C protection of session blocks

Each block written to the session file now carries a CRC-32C checksum so that
truncated or corrupted files are detected by readers.

Refs: HLR-FRC-009
```

## 7. Versioning and version files

1. **Scheme.** Releases use [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).
   While the major version is 0, any minor release may contain breaking changes, which are
   always listed in the changelog.
2. **Version files.** The release version is declared in exactly these files, which must
   agree (tool T-004, requirements `HLR-REL-001` to `HLR-REL-004`):

   | File | Declaration |
   |---|---|
   | `VERSION` | The version alone on one line; the authoritative source |
   | `pyproject.toml` | `version` in the `[project]` table |
   | `tools/ludus_tools/__init__.py` | `__version__` |
   | `CHANGELOG.md` | A section `## [X.Y.Z] - YYYY-MM-DD` |

   The traceability matrix and the release documents also carry the version, through their
   revision (LUD-STD-004).
3. **Changelog.** `CHANGELOG.md` follows
   [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). It always has an
   `## [Unreleased]` section at the top. Entries are grouped under `Added`, `Changed`,
   `Deprecated`, `Removed`, `Fixed` and `Security`. Security entries name the advisory and
   CVE identifiers.
4. **Tags.** Each release is an annotated tag `vX.Y.Z` on a commit of `main` (or of a
   `release/X.Y` branch). Tags are never moved or deleted. A faulty release is superseded by
   a new version, not replaced.
5. **Pre-releases** use SemVer pre-release identifiers, for example `0.2.0-rc.1`.

## 8. Integrity and signing

| Control | Status in 0.1.0 |
|---|---|
| Branch protection on `main` (reviews, status checks, linear history, no force push) | To be enabled on the hosting repository (OI-002) |
| Signed commits on `main` | Not yet enforced (OI-003) |
| Signed annotated release tags | Planned; tag 0.1.0 is annotated but not signed (OI-003) |
| Release artifacts signed with Sigstore and accompanied by SLSA provenance | Planned from the first release with build artifacts |
| GitHub Actions pinned to full commit SHAs | Not yet done; actions are pinned to major version tags (OI-004) |
| Dependency updates proposed automatically | Dependabot configuration in `.github/dependabot.yml` |

## 9. Life cycle environment control

1. Python development tools are pinned to exact versions in `requirements-dev.txt`.
2. CI uses the runner image and actions named in `.github/workflows/`. A change to a workflow
   is a CC2 change but needs review by a code owner.
3. Upgrading a pinned tool is a `build` change. If the tool is listed in the
   [Tool Qualification Plan](../process/tool-qualification.md), the qualification activities
   for that tool are repeated in the same pull request.
4. The SCI of every release records the environment actually used.

## 10. Licensing and provenance

1. Every file carries SPDX copyright and license information, either in a header or in
   `REUSE.toml`. Compliance with the [REUSE specification](https://reuse.software/spec/) is
   checked by `reuse lint` in CI.
2. License texts are stored in `LICENSES/`. New Ludus code is licensed under MIT unless a
   decision record says otherwise ([ADR-0004](../architecture/adr/0004-licensing.md)).
3. Third-party code keeps its original license and copyright notices.
4. Contributions are accepted under the inbound license terms described in `CONTRIBUTING.md`.

## 11. Archive, retrieval and release

1. Every baseline can be retrieved by checking out its tag.
2. Release archives and their checksums are attached to the GitHub release of the tag.
3. The project keeps at least one off-site mirror of the repository, including tags. Setting
   up the mirror is open item OI-006.
4. Release procedure: [LUD-PRC-003](../process/release-process.md).

## 12. Records

| Record | Kept in |
|---|---|
| Change history | Git history of `main` |
| Change requests, problem reports | GitHub issues |
| Reviews | GitHub pull request reviews |
| Verification results | CI runs; summarized in the SAS |
| Release records | `docs/releases/vX.Y.Z/` and the GitHub release |

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
