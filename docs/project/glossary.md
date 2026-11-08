---
doc_id: LUD-PRJ-003
title: Glossary
revision: "1.0"
status: baselined
owner: Project lead
---

# Glossary

| Term | Definition |
|---|---|
| ADR | Architecture Decision Record ([Design Standard](../standards/design-standard.md), section 3) |
| Baseline | An approved, tagged state of configuration items that changes only through change control |
| CC1, CC2 | Configuration control categories ([SCMP](../plans/scmp.md), section 2) |
| CNA | CVE Numbering Authority: an organization authorized to assign CVE identifiers |
| CVE | Common Vulnerabilities and Exposures identifier |
| CVSS | Common Vulnerability Scoring System; Ludus uses version 4.0 |
| Decision coverage | Every entry and exit point invoked and every decision has taken every possible outcome at least once |
| Deactivated code | Code intentionally not executed in some configurations, documented and verified in the configurations where it is active |
| Dead code | Code that cannot be executed or whose results are never used; removed when found |
| Derived requirement | A requirement not directly traceable to a parent, introduced by a design decision |
| Deviation | A recorded, accepted difference between Ludus processes and the DO-178C process model ([PSAA](../plans/psaa.md), section 7) |
| DO-178C | RTCA standard *Software Considerations in Airborne Systems and Equipment Certification*, used by Ludus as a process model only |
| DO-330 | RTCA standard *Software Tool Qualification Considerations* |
| eBPF | Extended Berkeley Packet Filter: verified programs loaded into the Linux kernel |
| Flight recorder | The Ludus component that records per-session performance telemetry |
| Gate | A review point (G0 to G3) that a phase must pass ([Roadmap](roadmap.md)) |
| GHSA | GitHub Security Advisory identifier |
| HLR | High-level requirement |
| Independence | Verification or review by a person other than the author of the item |
| LAL | Ludus Assurance Level, LAL-1 (highest) to LAL-3 ([PSAA](../plans/psaa.md), section 4) |
| LLR | Low-level requirement |
| MC/DC | Modified condition/decision coverage: decision coverage plus a demonstration that each condition in a decision independently affects its outcome |
| Optimization tier | The class of an optimization by its effect on what the player sees ([Architecture Overview](../architecture/overview.md), section 3) |
| Problem report | A recorded deviation from requirements, standards or plans ([LUD-PRC-001](../process/problem-reporting.md)) |
| Profile | A verified set of optimizations for one game on one class of machine |
| Proton | Valve's compatibility layer that runs Windows games on Linux |
| PSAA | Plan for Software Aspects of Assurance |
| Reference benchmark | A workload of the reference benchmark set ([SVP](../plans/svp.md), section 9) |
| Regression test | A test that reproduces a fixed problem so that it cannot return unnoticed |
| SAS | Software Accomplishment Summary |
| sched_ext | Linux scheduler class that runs scheduling policies written as BPF programs |
| SCI | Software Configuration Index |
| SCMP | Software Configuration Management Plan |
| SDP | Software Development Plan |
| SQAP | Software Quality Assurance Plan |
| Statement coverage | Every statement executed at least once |
| SVP | Software Verification Plan |
| SYS | System requirement |
| TQL | Tool Qualification Level |
| Trace tag | A comment line `Implements:` or `Verifies:` that links code or a test to requirements |

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
