---
doc_id: LUD-REL-002
title: Software Accomplishment Summary, release 0.1.0
revision: "0.1.0"
status: baselined
owner: Release manager
---

# Software Accomplishment Summary, release 0.1.0

## 1. Summary

Release 0.1.0 is the **planning baseline** of Ludus and the evidence for gate G0
([Roadmap](../../project/roadmap.md)). It establishes the plans, standards and processes
under which all later Ludus software is developed, the first requirements baseline, and the
process tools that enforce traceability, document control, commit rules and release
consistency. It contains no product code.

Ludus is not certified under DO-178C or any other standard. DO-178C is used as a process
model ([ADR-0007](../../architecture/adr/0007-do-178c-as-process-model.md)).

## 2. Software identification

The configuration is identified in the [SCI v0.1.0](sci.md) (LUD-REL-001).

## 3. Software characteristics

| Item | Value |
|---|---|
| Product code | None in this release |
| Process tools | 4 tools and 1 shared module, Python 3.13, assurance level LAL-2 |
| Requirements | 57 (10 system, 47 high-level) |
| Verification cases | 171 test cases in `tests/tools/` |

## 4. Life cycle data produced

All life cycle data listed in the [PSAA](../../plans/psaa.md), section 6, exists for this
release in the form described there, except:

- design description: only the [Architecture Overview](../../architecture/overview.md)
  (draft) and decision records exist, as no product component has been designed yet;
- executable object code: none, as there is no product code.

## 5. Verification results

Results were produced in the environment recorded in the SCI, section 5, on the release
commit.

| Check | Command | Result |
|---|---|---|
| Lint and formatting | `ruff check .`, `ruff format --check .` | No findings |
| Static type check | `mypy` (strict) | No findings |
| Requirements-based tests | `pytest` | 171 passed, 0 failed, 0 skipped |
| Structural coverage, process tools | `pytest --cov` (statement and branch) | 100% statement, 100% branch |
| Traceability | `python -m ludus_tools.trace check` | No errors; 57 requirements, 165 trace tags |
| Traceability matrix current | `python -m ludus_tools.trace matrix --check` | Current |
| Document control and links | `python -m ludus_tools.doccheck` | No errors |
| Licensing metadata | `reuse lint` | Compliant with REUSE |
| Release consistency | `python -m ludus_tools.release` | No errors |
| Commit messages | `python -m ludus_tools.commitcheck --range HEAD` (every commit, including the root) | All commits conform |

Coverage exclusions used: four of category E-1 ([SVP](../../plans/svp.md), section 7.3),
one per tool module entry point.

### 5.1 Requirement status

| Status | Count | Requirements |
|---|---|---|
| implemented | 35 | `HLR-TRC-001` to `HLR-TRC-016`, `HLR-DOC-001` to `HLR-DOC-007`, `HLR-CMT-001` to `HLR-CMT-008`, `HLR-REL-001` to `HLR-REL-004` |
| approved | 7 | `SYS-PRC-001` to `SYS-PRC-004`, `SYS-FRC-001` to `SYS-FRC-003` |
| draft | 15 | `SYS-SAF-001`, `SYS-SAF-002`, `SYS-SEC-001`, `HLR-FRC-001` to `HLR-FRC-012` |
| verified | 0 | — |

The tool requirements are `implemented` rather than `verified` because the independent
review of the verification cases required by the SVP has not been performed (OI-001).

### 5.2 Limits of the verification

- The history leading to this release was created as a single bootstrap series before any
  hosted CI existed. All checks above were run on the release commit; intermediate commits
  were not each verified.
- Reviews were self-reviews by the project lead (deviation D-002).

## 6. Deviations

Deviations from the DO-178C process model, from the [PSAA](../../plans/psaa.md), section 7:

| ID | Deviation | Status |
|---|---|---|
| D-001 | No verification of source code to object code correspondence at LAL-1 | Open (permanent unless resourced) |
| D-002 | Independence objectives not met while the project has one maintainer | Open |
| D-003 | Gates are internal reviews, not reviews by a certification authority | Open (permanent) |
| D-004 | Tools qualified under the project's own plan, not under DO-330 | Open (permanent) |

## 7. Open items

| ID | Open item | Needed before |
|---|---|---|
| OI-001 | Review of this baseline by the project lead and by an independent reviewer; then set tool requirements to `verified` | Gate G1 of phase 1 |
| OI-002 | Hosting repository settings: branch protection on `main` (required reviews and status checks, linear history, no force push or deletion), code owner reviews, private vulnerability reporting | Public announcement |
| OI-003 | Signed commits and signed release tags are not yet enforced; tag `v0.1.0` is annotated but not signed | Release 0.2.0 |
| OI-004 | GitHub Actions are pinned to major version tags, not to full commit SHAs | Release 0.2.0 |
| OI-005 | Trademark clearance of the name "Ludus" | Public announcement |
| OI-006 | Off-site mirror of the repository, including tags | Release 0.2.0 |
| OI-007 | Confirmation of the licensing decision ([ADR-0004](../../architecture/adr/0004-licensing.md), status Proposed) | First product code |
| OI-008 | A dedicated private contact address for security and conduct reports | Public announcement |

## 8. Problem reports

No problem reports are open. No problem reports were raised against this release before
publication.

## 9. Gate G0 record

| Criterion ([Roadmap](../../project/roadmap.md), section 3) | Result |
|---|---|
| Plans baselined | Met: LUD-PLN-001 to LUD-PLN-005 at revision 1.0 |
| Standards baselined | Met: LUD-STD-001 to LUD-STD-004 at revision 1.0 |
| Process tools meet their requirements with full coverage | Met: section 5 |
| CI runs every automated check on every pull request | Met in configuration (`.github/workflows/ci.yml`); first hosted run pending OI-002 |
| Deviations and open items listed | Met: sections 6 and 7 |

**Gate status:** self-assessed by the project lead; confirmation by an independent reviewer is
pending (OI-001). Phase 1 implementation does not start before OI-001 is closed.

## 10. Statement

The software life cycle processes of this release followed the plans listed in the SCI, with
the deviations in section 6 and the open items in section 7. This baseline was prepared with
AI assistance (recorded with `Co-Authored-By` trailers in the commit history).

## Revision history

| Revision | Date | Description |
|---|---|---|
| 0.1.0 | 2026-11-08 | Accomplishment summary for release 0.1.0. |
