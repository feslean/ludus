---
doc_id: LUD-PLN-001
title: Plan for Software Aspects of Assurance (PSAA)
revision: "1.0"
status: baselined
owner: Project lead
---

# Plan for Software Aspects of Assurance (PSAA)

## 1. Purpose

This plan is the top-level assurance document of Ludus. It states which assurance
objectives the project commits to, how they are allocated to software components, which
life cycle data is produced, and where the project deliberately deviates from its
reference model. Every other plan and standard in this repository refines this document.

## 2. Applicability statement

Ludus is gaming software for personal computers. It is **not airborne software, it is not
certified, and no certification authority has reviewed this plan.**

The project uses RTCA DO-178C / EUROCAE ED-12C, *Software Considerations in Airborne
Systems and Equipment Certification* (2011), as a **process model**: the structure of plans,
standards, life cycle data, traceability, structural coverage and independence is taken from
it, and adapted where the context differs. Where this repository says a process is
"modeled on" DO-178C, it means the project's own interpretation. Decision record
[ADR-0007](../architecture/adr/0007-do-178c-as-process-model.md) explains why.

DO-178C is a copyrighted document. Its text and tables are not reproduced here; references
are to concepts and section topics only. Contributors who need the normative text must
obtain it from RTCA or EUROCAE.

## 3. System overview

Ludus is a Linux-based gaming operating system that records how each game runs, learns
per-game optimizations across sessions and applies only optimizations that pass automated
verification. It is described in the
[Architecture Overview](../architecture/overview.md) and the [Project Pitch](../pitch/pitch.md).

Baseline 0.1.0 is the **planning baseline**: it contains plans, standards, the first
requirements baseline and the process tools. It contains no product code by design, because
the plans must be in place before development starts (section 5).

## 4. Ludus Assurance Levels

DO-178C assigns a software level from the effect of anomalous behavior on the aircraft.
Ludus assigns a **Ludus Assurance Level (LAL)** from the worst credible effect of anomalous
behavior on the user's machine, data and security.

| LAL | Worst credible effect of a failure | Typical components | Reference DO-178C level | Structural coverage required (100%) | Independence |
|---|---|---|---|---|---|
| LAL-1 | Machine compromise, data loss or corruption, system crash, loss of the rollback path | Kernel and eBPF code, privileged daemons, rollback manager, update and profile installation paths | Level A objectives (with deviation D-001) | Statement, decision and MC/DC | Reviews and verification by someone other than the author |
| LAL-2 | Game crash, visible rendering corruption, wrong result from a verification tool | Unprivileged user-space components that change game behavior; process tools in `tools/` | Level B objectives | Statement and decision | Reviews by someone other than the author |
| LAL-3 | Inconvenience, cosmetic defects, wrong statistics in non-gating reports | User interface, documentation generators, analytics dashboards | Level C objectives | Statement | Review by any maintainer |

For reference, DO-178C defines 71, 69, 62 and 26 objectives for Levels A, B, C and D. Ludus
does not claim to satisfy those objective sets; it uses them as the yardstick for the rigor
expected at each LAL.

### 4.1 Allocation rules

1. A component that is not yet classified is treated as **LAL-1**. Lowering a level needs an
   approved change request with a written failure-effect analysis.
2. A component receives the highest LAL of any requirement allocated to it.
3. Every component that executes with elevated privileges is LAL-1 (requirement
   `SYS-SEC-001`).
4. A lower-LAL component must not be able to corrupt a higher-LAL component. Where it can,
   both are treated at the higher level until partitioning is demonstrated by analysis.

### 4.2 Current allocation

| Component | LAL | Status in 0.1.0 |
|---|---|---|
| Process tools (`tools/ludus_tools`) | LAL-2 | Implemented and verified |
| Flight recorder kernel probes | LAL-1 | Requirements drafted |
| Flight recorder user-space writer | LAL-2 | Requirements drafted |
| Rollback manager | LAL-1 | Planned |
| Learning engine, optimizers, verifier | To be classified (LAL-1 until then) | Planned |

## 5. Life cycle

The life cycle is described in the [Software Development Plan](sdp.md). Its processes are:

- **Planning**: this plan and the plans listed in section 6.
- **Development**: requirements, design, coding and integration.
- **Integral**: verification ([SVP](svp.md)), configuration management ([SCMP](scmp.md)),
  quality assurance ([SQAP](sqap.md)) and problem reporting
  ([LUD-PRC-001](../process/problem-reporting.md)).

Progress is controlled by four internal review gates, analogous to the four stages of
involvement used in certification practice. The gates are defined in the
[Roadmap](../project/roadmap.md):

| Gate | Purpose | Applies |
|---|---|---|
| G0 | Planning review: plans and standards are complete and consistent | Once, at baseline 0.1.0 |
| G1 | Development review: requirements and design of a phase are approved and follow the standards | At the start of every phase from phase 1, before implementation |
| G2 | Verification review: verification of a phase is complete and coverage objectives are met | At the end of every phase from phase 1 |
| G3 | Final review: life cycle data is complete for a 1.0 release | Once, before 1.0 |

## 6. Life cycle data

| DO-178C data item | Ludus artifact |
|---|---|
| Plan for Software Aspects of Certification | This document (LUD-PLN-001) |
| Software Development Plan | [LUD-PLN-002](sdp.md) |
| Software Verification Plan | [LUD-PLN-003](svp.md) |
| Software Configuration Management Plan | [LUD-PLN-004](scmp.md) |
| Software Quality Assurance Plan | [LUD-PLN-005](sqap.md) |
| Software Requirements Standards | [LUD-STD-001](../standards/requirements-standard.md) |
| Software Design Standards | [LUD-STD-002](../standards/design-standard.md) |
| Software Code Standards | [LUD-STD-003](../standards/coding-standard.md) |
| (none; project addition) | Documentation Standard [LUD-STD-004](../standards/documentation-standard.md) |
| Software Requirements Data | [`requirements/`](../../requirements/) (TOML) |
| Design Description | [Architecture Overview](../architecture/overview.md), decision records, low-level requirements (from phase 1) |
| Source Code | [`tools/`](../../tools/) and future component directories |
| Executable Object Code | Release artifacts ([LUD-PRC-003](../process/release-process.md)) |
| Software Verification Cases and Procedures | [`tests/`](../../tests/) and the [SVP](svp.md) |
| Software Verification Results | CI logs and coverage reports, summarized in the SAS of each release |
| Trace Data | [Traceability Matrix](../verification/traceability-matrix.md) (generated) |
| Software Life Cycle Environment Configuration Index | Environment section of each [SCI](../releases/v0.1.0/sci.md) |
| Software Configuration Index | [SCI v0.1.0](../releases/v0.1.0/sci.md) |
| Problem Reports | GitHub issues labelled `problem-report` ([LUD-PRC-001](../process/problem-reporting.md)) |
| Software Configuration Management Records | Git history, annotated release tags, pull request records |
| Software Quality Assurance Records | Pull request review records and gate checklists ([SQAP](sqap.md)) |
| Software Accomplishment Summary | [SAS v0.1.0](../releases/v0.1.0/sas.md) |

## 7. Deviations

A deviation is a known, accepted difference between this project's processes and its
reference model. Every deviation is listed here and repeated in the Software Accomplishment
Summary of each release while it is open.

| ID | Deviation | Justification | Mitigation | Status |
|---|---|---|---|---|
| D-001 | LAL-1 does not include verification of source code to object code correspondence | Commodity compilers and hardware; no practical tooling for a volunteer project | Optimized builds are tested; compiler warnings as errors; sanitizers in test builds; compiler versions pinned in the SCI | Open (permanent unless resourced) |
| D-002 | Independence objectives cannot be met while the project has one maintainer | Bootstrap phase | Self-review checklist recorded in every pull request; LAL-1 code is not merged without independent review | Open until a second maintainer joins |
| D-003 | Gates G0 to G3 are internal reviews, not reviews by a certification authority | No certification is sought | Gate records are public in the repository | Open (permanent) |
| D-004 | Tools are qualified under the project's own Tool Qualification Plan, not under DO-330 | No certification is sought | [LUD-PRC-002](../process/tool-qualification.md) applies requirements-based testing and full structural coverage to project tools | Open (permanent) |

## 8. Additional considerations

- **Tool qualification**: see [LUD-PRC-002](../process/tool-qualification.md).
- **Previously developed software**: Ludus builds on the Linux kernel, Mesa, Proton and
  vkd3d-proton ([ADR-0002](../architecture/adr/0002-build-on-linux.md)). Upstream code is not
  claimed to meet any LAL. Every Ludus modification of upstream code is developed under this
  plan, and integration tests verify Ludus requirements on the integrated system.
- **Security**: vulnerabilities are handled under
  [LUD-SEC-001](../security/vulnerability-management.md).
- **AI-assisted contributions**: contributions produced with AI assistance are accepted under
  the same requirements, review and verification rules as any other contribution. The pull
  request template asks contributors to disclose such assistance. This baseline was itself
  prepared with AI assistance; its review by the project lead and by an independent reviewer
  is tracked as open item OI-001 in the [SAS v0.1.0](../releases/v0.1.0/sas.md).

## 9. Schedule

The project does not commit to calendar dates in this plan. Phases and the evidence required
to pass each gate are defined in the [Roadmap](../project/roadmap.md).

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
