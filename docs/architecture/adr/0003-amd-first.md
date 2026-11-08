---
doc_id: LUD-ADR-0003
title: "ADR-0003: Target AMD graphics hardware first"
revision: "1.0"
status: baselined
owner: Architecture lead
---

# ADR-0003: Target AMD graphics hardware first

## Status

Accepted

## Context

Ludus needs to observe and, later, adjust work at every level of the graphics stack: the
kernel driver, the Vulkan driver and its shader compiler. On AMD hardware the whole stack is
open source and maintained upstream: the `amdgpu` kernel driver and Mesa's RADV Vulkan driver
with its ACO shader compiler. AMD hardware is also common among Linux players on Steam, partly
because Valve's own devices use AMD processors.

## Decision

We will develop and verify Ludus first on AMD GPUs with the `amdgpu` kernel driver and Mesa
RADV. Reference machines for the benchmark procedure ([SVP](../../plans/svp.md), section 9)
will use AMD GPUs. Other vendors will be considered after phase 2, in a new decision record.

## Alternatives considered

- **Vendor-neutral from the start.** Rejected for now: the lowest common denominator would
  exclude the driver-level instrumentation that the learning loop needs.
- **NVIDIA first.** Rejected for now: it has the largest share of gaming GPUs, but its
  production Vulkan driver is proprietary, which limits what Ludus can observe and verify.

## Consequences

- Early results apply only to AMD hardware; the pitch and release notes must say so.
- Components must keep vendor-specific code behind interfaces so that other vendors can be
  added without redesign.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
