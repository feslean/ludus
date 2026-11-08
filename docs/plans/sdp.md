---
doc_id: LUD-PLN-002
title: Software Development Plan (SDP)
revision: "1.0"
status: baselined
owner: Project lead
---

# Software Development Plan (SDP)

## 1. Purpose

This plan defines how Ludus software is specified, designed, coded and integrated. It
refines the [PSAA](psaa.md) (LUD-PLN-001). Verification is defined in the [SVP](svp.md),
configuration management in the [SCMP](scmp.md) and quality assurance in the
[SQAP](sqap.md).

## 2. Development standards

| Standard | Document | Applies to |
|---|---|---|
| Requirements Standard | [LUD-STD-001](../standards/requirements-standard.md) | All requirements in `requirements/` |
| Design Standard | [LUD-STD-002](../standards/design-standard.md) | Architecture, decision records, low-level requirements, interfaces |
| Coding Standard | [LUD-STD-003](../standards/coding-standard.md) | All source code |
| Documentation Standard | [LUD-STD-004](../standards/documentation-standard.md) | All controlled documents in `docs/` |

## 3. Life cycle model

Ludus uses an incremental life cycle. Each roadmap phase
([LUD-PRJ-001](../project/roadmap.md)) runs the development processes below for the
components in its scope and ends at a review gate. Work inside a phase is iterative, but no
code is merged before the requirements it implements are at least `approved`.

```text
 System requirements (SYS)
        |
        v
 High-level requirements (HLR) ----> verification cases (tests, analyses, reviews)
        |                                      ^
        v                                      |
 Design: architecture, ADRs, LLR  -------------+
        |                                      |
        v                                      |
 Source code ------------------------> coverage analysis (SVP)
        |
        v
 Integration, release (LUD-PRC-003)
```

## 4. Development processes

### 4.1 System requirements

System requirements (`SYS-*`) state what Ludus must do as a whole. They are written by the
project lead or a maintainer, reviewed in a pull request and set to `approved` when merged.

**Transition criteria.** Entry: a roadmap phase or an accepted change request needs the
requirement. Exit: the requirement conforms to LUD-STD-001, has a rationale and a verification
method, and the traceability checker reports no error.

### 4.2 Software high-level requirements

High-level requirements (`HLR-*`) refine system requirements for one component. Every HLR
names its parent system requirements or is marked `derived` with a rationale. Derived
requirements are also reported to the safety and security review of the next gate, because
they add behavior that the system requirements did not ask for.

**Transition criteria.** Entry: parent system requirements are `approved`. Exit: the HLR set
of the component is reviewed against the review checklist in the [SVP](svp.md), section 5.1,
and set to `approved`.

### 4.3 Software design

Design consists of:

- the [Architecture Overview](../architecture/overview.md) (component structure, data and
  control flow, privilege boundaries);
- Architecture Decision Records in [`docs/architecture/adr/`](../architecture/adr/);
- low-level requirements (`LLR-*`) for LAL-1 and LAL-2 components, precise enough that code
  can be written and reviewed against them without further information;
- interface descriptions for every interface that crosses a privilege or process boundary.

For LAL-3 components, the HLR together with the code documentation may serve as the design,
in which case no LLRs are written.

**Transition criteria.** Entry: the HLRs of the component are `approved`. Exit: the design
conforms to LUD-STD-002 and the design review of the [SVP](svp.md), section 5.2, has been
recorded.

### 4.4 Coding

Source code is written to the [Coding Standard](../standards/coding-standard.md). Every
function or module that implements a requirement carries an `Implements:` tag naming the
requirement identifiers (LUD-STD-001, section 9). Code without a requirement is not merged;
if a needed function has no requirement, a derived requirement is written first.

**Transition criteria.** Entry: the design is `approved` for the code being written. Exit:
the code passes all automated checks (`make check`) and the code review of the
[SVP](svp.md), section 5.3.

### 4.5 Integration

Integration combines components into a release candidate. The integration procedure,
including builds, package assembly and release records, is the
[Release Process](../process/release-process.md) (LUD-PRC-003).

## 5. Language policy

The language policy is recorded in
[ADR-0005](../architecture/adr/0005-language-policy.md) and summarized here.

| Use | Language | Condition |
|---|---|---|
| LAL-1 kernel, eBPF and privileged code | C11 (GNU extensions allowed where the kernel requires them) | Compiled with GCC 14 or later so that MC/DC can be measured with `-fcondition-coverage` |
| LAL-2 user-space components | C11 or Rust | Rust only after decision coverage measurement for Rust has been demonstrated to the SVP's satisfaction and recorded in a decision record |
| LAL-3 components | C11, Rust or Python 3.13 | Statement coverage measurable |
| Process tools | Python 3.13 | Treated as LAL-2 (PSAA, section 4.2) |

Introducing another language at any level needs an approved decision record that shows how
the coverage objectives of the target level are met.

## 6. Development environment

| Item | Version or rule | Purpose |
|---|---|---|
| Git | 2.40 or later | Configuration management |
| Python | 3.13 | Process tools and their tests |
| Python development packages | Pinned in [`requirements-dev.txt`](../../requirements-dev.txt) | Test, lint, type check, license check |
| GCC | 14 or later (from phase 1) | C compilation and MC/DC measurement |
| Clang/LLVM | Version pinned in the SCI of the phase-1 release | eBPF compilation |
| GNU Make | 4.3 or later | Entry point for all checks |
| CI | GitHub Actions, workflows in [`.github/workflows/`](../../.github/workflows/) | Automated verification of every pull request |

The exact versions used to produce a release are recorded in the environment section of its
Software Configuration Index (for example [SCI v0.1.0](../releases/v0.1.0/sci.md)). Tools
that can insert errors into the product or fail to detect errors are handled under the
[Tool Qualification Plan](../process/tool-qualification.md).

## 7. Repository layout

| Path | Content | Controlled under |
|---|---|---|
| `requirements/` | Requirements in TOML | LUD-STD-001 |
| `docs/` | Controlled documents, listed in the [register](../README.md) | LUD-STD-004 |
| `tools/` | Process tools | LUD-STD-003, LUD-PRC-002 |
| `tests/` | Verification cases and procedures | LUD-PLN-003 |
| `tests/regression/` | Regression tests for fixed problem reports | LUD-PLN-003, section 8 |
| `.github/` | CI workflows, templates, code owners | LUD-PLN-004 |
| `.githooks/` | Optional local hooks | LUD-PLN-004 |
| `LICENSES/`, `REUSE.toml` | License texts and licensing metadata | LUD-PLN-004, section 10 |

Product component directories (for example `recorder/`) are added when their phase starts,
together with an update of this table.

## 8. Upstream components

Ludus modifies upstream projects (Linux, Mesa, Proton, vkd3d-proton) only where its
requirements make that necessary, and prefers upstreaming changes over carrying patches.
Every carried patch:

1. is stored in the Ludus repository as a patch file with an SPDX header that preserves the
   upstream license;
2. carries `Implements:` tags in its description (the traceability configuration in
   `ludus-tools.toml` is extended to scan patch files when the first patch is added);
3. is listed in the SCI of every release that contains it, with the upstream base revision.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
