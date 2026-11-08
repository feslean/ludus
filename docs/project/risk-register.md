---
doc_id: LUD-PRJ-002
title: Risk Register
revision: "1.0"
status: baselined
owner: Project lead
---

# Risk Register

Likelihood and impact are rated 1 (low) to 3 (high). The register is reviewed at every gate
and every minor release.

| ID | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | Measured gains from tier 1 optimizations are too small to attract players | 2 | 3 | Phase 1 measures where time is lost before any optimization is built; publish results honestly whatever they show | Project lead | Open |
| R-02 | The flight recorder's overhead exceeds its 1.0% budget | 2 | 2 | eBPF ring buffers, sampling options, early overhead measurement with the SVP procedure | Architecture lead | Open |
| R-03 | Anti-cheat software flags Ludus behavior | 2 | 3 | No injection into game processes; perceptual tiers off for competitive titles (ADR-0006); contact anti-cheat vendors before phase 3 | Project lead | Open |
| R-04 | The assurance process is too heavy for volunteer contributors | 3 | 2 | Automate checks; clear contributor guide; templates; mentoring | Project lead | Open |
| R-05 | Only one maintainer: independence objectives cannot be met and the bus factor is one | 3 | 3 | Recruit a second maintainer before phase 1 implementation; LAL-1 code is not merged without independent review (D-002) | Project lead | Open |
| R-06 | Upstream changes (kernel, Mesa, Proton) break Ludus components | 2 | 2 | Use stable interfaces (eBPF, sched_ext, Vulkan layers); upstream patches; CI against upstream releases | Architecture lead | Open |
| R-07 | Privileged components introduce vulnerabilities | 2 | 3 | LAL-1 process, MISRA C, fuzzing, threat model, vulnerability process | Security lead | Open |
| R-08 | The project name "Ludus" conflicts with an existing trademark | 2 | 2 | Trademark search before public launch (OI-005) | Project lead | Open |
| R-09 | Readers mistake the DO-178C process model for a certification claim | 2 | 2 | Explicit statements in README, PSAA and ADR-0007; Documentation Standard rule 9.4 | Project lead | Open |
| R-10 | Telemetry raises privacy concerns or legal obligations | 2 | 3 | Local-only by default, redaction, opt-in sharing, data inventory before phase 4 | Security lead | Open |

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
