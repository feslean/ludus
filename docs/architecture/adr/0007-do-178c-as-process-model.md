---
doc_id: LUD-ADR-0007
title: "ADR-0007: Use DO-178C as a process model, without certification"
revision: "1.0"
status: baselined
owner: Project lead
---

# ADR-0007: Use DO-178C as a process model, without certification

## Status

Accepted

## Context

Ludus runs privileged code on players' machines and changes how their games run. Failures can
crash the system, corrupt data or open security holes. The project wants a development
process that is demanding, well understood and reviewable by outsiders.

RTCA DO-178C is the standard for software in airborne systems. It defines life cycle plans,
standards, bidirectional traceability, verification objectives scaled by software level,
structural coverage up to MC/DC, independence, configuration management and quality
assurance. Certification under it requires a certification authority and an aircraft or
equipment application, neither of which exists for Ludus.

## Decision

1. We will use DO-178C as a **process model**: the structure of plans, standards, life cycle
   data, traceability, coverage and independence follows it, adapted to Ludus through Ludus
   Assurance Levels ([PSAA](../../plans/psaa.md), section 4).
2. We will never claim that Ludus is certified, compliant with or approved under DO-178C.
   Documents say "modeled on DO-178C".
3. Differences from the model are recorded as deviations in the PSAA, section 7, and repeated
   in every release's SAS.
4. We will not reproduce the copyrighted text of DO-178C or related documents.

## Alternatives considered

- **IEC 61508 or ISO 26262.** Also suitable models, but DO-178C's objective tables and
  structural coverage criteria are the most precisely defined and the most widely recognized
  for software alone.
- **No formal process model.** Rejected: the project's value depends on players trusting
  privileged, self-modifying software.

## Consequences

- The process is heavier than usual for an open-source project; contributor documentation
  must make it easy to follow, and tools must automate as many checks as possible.
- Some objectives cannot be met by a volunteer project (deviations D-001 to D-004).

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
