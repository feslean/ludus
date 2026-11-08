---
doc_id: LUD-ADR-0002
title: "ADR-0002: Build on Linux instead of a new kernel"
revision: "1.0"
status: baselined
owner: Architecture lead
---

# ADR-0002: Build on Linux instead of a new kernel

## Status

Accepted

## Context

The project began from the idea of a new operating system written for games, possibly with
its own instruction encoding and a kernel running on the GPU. Analysis of where frame time is
actually lost on a modern PC pointed elsewhere:

- Frame-time spikes come mostly from shader and pipeline compilation, CPU scheduling of game
  threads, asset streaming and background work, not from system call overhead.
- A new kernel would need new GPU, storage, network, audio and input drivers before running a
  single game. GPU drivers alone are years of work per vendor.
- Commercial games are built for Windows. On Linux they run through Proton, Wine,
  vkd3d-proton and DXVK, which already translate Direct3D to Vulkan.
- Linux offers the extension points Ludus needs without forking the kernel: eBPF for
  observation and sched_ext, merged in Linux 6.12, for scheduling policies written as BPF
  programs. The `scx_lavd` scheduler, developed by Igalia for Valve's Steam Deck, shows that
  game-aware scheduling can be delivered this way.

## Decision

We will build Ludus as a set of components on an unmodified or minimally patched Linux
kernel, with Mesa and Proton, and focus Ludus's own work on recording, learning, verifying and
applying per-game optimizations. Ludus will use eBPF and sched_ext in preference to kernel
patches, and will propose changes upstream rather than carry them.

## Alternatives considered

- **A new kernel and operating system.** Rejected: driver and compatibility cost far exceeds
  the possible gain, and it would delay any measurable result by years.
- **A kernel running on the GPU.** Rejected: GPUs lack the interrupt handling, memory
  protection and I/O control a kernel needs; the CPU would still have to drive devices.
- **A virtual machine that suspends the host during play.** Deferred: a lighter "session
  mode" that stops non-essential services gives most of the benefit with less risk
  (Architecture Overview, phase 3).

## Consequences

- Ludus can show measured results on real games within the first phases.
- Ludus depends on upstream release cycles and on Proton compatibility.
- Previously developed software (Linux, Mesa, Proton) is not developed under the Ludus plans;
  the PSAA, section 8, states how it is handled.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
