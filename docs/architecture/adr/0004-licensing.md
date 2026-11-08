---
doc_id: LUD-ADR-0004
title: "ADR-0004: Licensing of Ludus code"
revision: "1.0"
status: baselined
owner: Project lead
---

# ADR-0004: Licensing of Ludus code

## Status

Proposed. The project lead must confirm this decision before the first product code is merged
(open item OI-007).

## Context

Ludus code falls into three groups with different constraints:

1. Code written only for Ludus, such as the process tools and the learning engine.
2. Code that becomes part of, or is loaded into, an upstream project: kernel patches and eBPF
   programs, patches to Mesa, vkd3d-proton or DXVK.
3. Documentation and requirements.

Upstream licenses include GPL-2.0 for the Linux kernel, LGPL-2.1 for vkd3d-proton, the zlib
license for DXVK and mostly MIT for Mesa. eBPF programs that use GPL-only kernel helpers must
declare a GPL-compatible license.

## Decision

1. Code written only for Ludus is licensed under **MIT**.
2. Code that is contributed to, linked into or loaded by an upstream project uses a license
   compatible with that project, normally the upstream project's own license. eBPF programs
   are dual-licensed `GPL-2.0-only OR MIT` unless they need GPL-only helpers, in which case they
   are `GPL-2.0-only`.
3. Documentation and requirements are licensed under MIT together with the code, so that
   text can move between documents and code comments without a license change.
4. Every file declares its license with SPDX identifiers, checked by `reuse lint`
   ([SCMP](../../plans/scmp.md), section 10).

## Alternatives considered

- **Apache-2.0 for new code.** Gives an explicit patent grant, which matters for a project
  with possible commercial contributors. It is incompatible with GPL-2.0-only code, which
  would complicate moving code between Ludus components and kernel patches. This is the main
  open question for confirmation.
- **GPL-3.0 for everything.** Would prevent use of Ludus components in GPL-2.0-only kernel code
  and discourage commercial distribution.
- **CC-BY-4.0 for documentation.** Common for documents, but prevents copying text into
  MIT-licensed code comments without a second license.

## Consequences

- Contributors must check the license of the directory they contribute to.
- A change to this decision before the first product code costs little; afterwards, it
  requires the agreement of all contributors to the affected code.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
