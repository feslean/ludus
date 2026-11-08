---
doc_id: LUD-PRJ-001
title: Roadmap and Review Gates
revision: "1.0"
status: baselined
owner: Project lead
---

# Roadmap and Review Gates

## 1. Principles

1. Phases end when their exit gate is passed, not on a date. This roadmap deliberately has no
   calendar dates.
2. Each phase delivers something a player or contributor can measure.
3. A phase does not start implementation before its requirements and design have passed G1.

## 2. Phases

| Phase | Scope | Version range | Entry | Exit |
|---|---|---|---|---|
| 0 | **Planning baseline**: plans, standards, requirements baseline, process tools, CI | 0.1.x | — | G0 |
| 1 | **Flight recorder**: kernel and eBPF probes, translation-layer GPU timing, session writer and file format, overhead measurement | 0.2.x | G1 | G2 |
| 2 | **Learning loop, tier 1**: learning engine, verifier, profile store, rollback manager, lossless optimizations (shader cache warming, scheduling hints, I/O prefetch) | 0.3.x – 0.4.x | G1 | G2 |
| 3 | **Session mode and tiers 2–3**: suspension of non-essential services during play; opt-in perceptual and multiplier optimizations | 0.5.x – 0.6.x | G1 | G2 |
| 4 | **Fleet learning**: opt-in sharing of verified profiles between similar machines | 0.7.x – 0.9.x | G1 | G2 |
| 1.0 | **Release 1.0**: conformity review of all life cycle data | 1.0.0 | — | G3 |

## 3. Gates

### G0 — Planning review

Passed when:

1. the PSAA, SDP, SVP, SCMP and SQAP are baselined;
2. the requirements, design, coding and documentation standards are baselined;
3. the process tools meet their requirements with 100% statement and branch coverage;
4. CI runs every automated check on every pull request;
5. the SAS lists all deviations and open items.

### G1 — Development review (each phase)

Passed when:

1. the phase's system and high-level requirements are `approved`;
2. the design of each component is reviewed (SVP, section 5.2), including interface
   descriptions and LAL allocation;
3. the threat model is updated for the phase's components;
4. the verification approach, including test environments and reference machines, is
   defined.

### G2 — Verification review (each phase)

Passed when:

1. every requirement in scope is `verified`;
2. the coverage objectives of each component's LAL are met;
3. performance requirements are verified with the reference benchmark procedure;
4. no PR-1 problem report is open;
5. the phase release's SAS records the results.

### G3 — Final review

Passed when the conformity review of the [SQAP](../plans/sqap.md), section 5, is complete
and every open deviation is accepted in the SAS of 1.0.

## 4. Status

| Phase | Status |
|---|---|
| 0 | G0 evidence assembled in release 0.1.0; independent review pending (OI-001) |
| 1 | High-level requirements drafted (`HLR-FRC-001` to `HLR-FRC-012`) |
| 2 – 4 | Not started |

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
