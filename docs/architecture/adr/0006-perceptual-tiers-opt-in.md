---
doc_id: LUD-ADR-0006
title: "ADR-0006: Perceptual optimizations are opt-in"
revision: "1.0"
status: baselined
owner: Architecture lead
---

# ADR-0006: Perceptual optimizations are opt-in

## Status

Accepted

## Context

Optimization tiers 2 (perceptual: variable-rate shading, shader simplification) and 3
(multipliers: upscaling, frame generation, learned latency control) change what the player
sees or when they see it. Even when a perceptual metric says the change is invisible:

- some players notice artifacts that metrics miss;
- frame generation adds latency, which matters in competitive play;
- changing a game's rendering may be seen as an unfair advantage or may trigger anti-cheat
  software;
- a developer's artistic intent may be altered.

## Decision

1. Tier 1 (lossless) optimizations are enabled by default once verified.
2. Tier 2 and tier 3 optimizations are **off by default** and are enabled only by an explicit
   user choice for each game.
3. For titles with competitive online play, tiers 2 and 3 are not offered unless the title is
   on an allow-list maintained by the project, with the reason for each entry.
4. The user interface always shows which tiers are active for the running game.

## Alternatives considered

- **Enable every verified optimization automatically.** Rejected: the perceptual threshold is
  a statistical judgement, and players must be able to decide for themselves.
- **Never offer perceptual tiers.** Rejected: on low-end hardware these tiers can make a game
  playable that otherwise is not.

## Consequences

- The verifier must classify every optimization by tier; the classification is part of its
  requirements.
- Benchmarks and the pitch must state results for tier 1 separately from tiers 2 and 3.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
