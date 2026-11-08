---
doc_id: LUD-PRC-002
title: Tool Qualification Plan
revision: "1.0"
status: baselined
owner: Project lead
---

# Tool Qualification Plan

## 1. Purpose

A tool needs qualification when the project relies on it in place of a process that would
otherwise be carried out and checked by people. This plan identifies the tools Ludus relies
on, classifies them and defines the activities that give confidence in them.

The classification follows the three criteria of RTCA DO-330, *Software Tool Qualification
Considerations*, and the tool qualification levels (TQL) DO-178C associates with them. Ludus
does not perform DO-330 qualification (deviation D-004, [PSAA](../plans/psaa.md),
section 7); it applies the activities in section 4, which are modeled on TQL-5.

## 2. Classification criteria

| Criterion | Meaning |
|---|---|
| 1 | The tool's output is part of the product and the tool could insert an error |
| 2 | The tool automates verification and could fail to detect an error, and its output is used to eliminate or reduce other verification or development processes |
| 3 | Within its intended use, the tool could fail to detect an error |

For criterion 3, DO-178C assigns TQL-5 at every software level. Criterion 2 would require
TQL-4 at Levels A and B.

## 3. Tool inventory

### 3.1 Project tools

| ID | Tool | Module | Function | Criterion | Requirements |
|---|---|---|---|---|---|
| T-001 | Traceability checker | `ludus_tools.trace` | Checks requirements and trace tags; generates the traceability matrix | 3 | `HLR-TRC-001` to `HLR-TRC-016` |
| T-002 | Document checker | `ludus_tools.doccheck` | Checks controlled documents and links | 3 | `HLR-DOC-001` to `HLR-DOC-007` |
| T-003 | Commit message checker | `ludus_tools.commitcheck` | Checks commit messages against SCMP section 6 | 3 | `HLR-CMT-001` to `HLR-CMT-008` |
| T-004 | Release checker | `ludus_tools.release` | Checks version consistency and changelog | 3 | `HLR-REL-001` to `HLR-REL-004` |

The project tools are classified under criterion 3 because reviewers still examine
traceability, documents and commit history during reviews; the tools find errors earlier but
do not replace the reviews. If the project ever removes a review because a tool performs the
check, that tool is reclassified under criterion 2 and this plan is updated first.

### 3.2 External tools

| Tool | Version | Function | Criterion | Basis for confidence |
|---|---|---|---|---|
| pytest | Pinned in `requirements-dev.txt` | Runs verification cases | 3 | Widely used; failing results are investigated; seeded-failure check (section 5) |
| coverage.py (with pytest-cov) | Pinned | Measures statement and branch coverage | 3 | Widely used; limitations recorded in SVP section 7.2; seeded-gap check (section 5) |
| ruff | Pinned | Lint and format check | 3 | Supplementary to code review |
| mypy | Pinned | Static type check | 3 | Supplementary to code review |
| reuse | Pinned | Licensing metadata check | 3 | Supplementary to review |
| Git | Recorded in the SCI | Configuration management | Not classified | Integrity by content hashing; history verified at each release |
| GCC (from phase 1) | Recorded in the SCI | Compiles C code; measures MC/DC | 1 (compiler), 3 (coverage) | Compiler output is verified by testing the compiled code (D-001 applies); coverage results are cross-checked on seeded gaps |
| Clang/LLVM (from phase 1) | Recorded in the SCI | Compiles eBPF programs | 1 | Output is checked by the kernel eBPF verifier and by tests |

## 4. Activities for project tools

1. **Tool operational requirements.** Each tool's behavior is specified by HLRs in
   [`requirements/hlr-process-tooling.toml`](../../requirements/hlr-process-tooling.toml),
   traced to the system requirements `SYS-PRC-001` to `SYS-PRC-004`.
2. **Development.** The tools are developed at LAL-2 under the [SDP](../plans/sdp.md) and
   the [Coding Standard](../standards/coding-standard.md).
3. **Verification.** Requirements-based tests in [`tests/tools/`](../../tests/tools/), normal
   range and robustness, with 100% statement and branch coverage enforced in CI.
4. **Configuration management.** The tools are CC1 items. Their version is the project
   version.
5. **Records.** Test and coverage results of each release are summarized in its SAS.

## 5. Activities for external tools

1. **Version control.** Versions are pinned. An upgrade is a `build` change reviewed by a
   code owner, and the release notes of the new version are checked for defects affecting
   the project's use.
2. **Seeded checks on upgrade.** Before an upgrade of pytest or coverage.py is merged, the
   reviewer confirms in the pull request that the tool still detects a seeded failure (a
   failing assertion) and a seeded coverage gap (an untested branch). The seeded change is
   not committed.
3. **Known limitations** are recorded in the SVP, section 7.2.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
