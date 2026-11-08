---
doc_id: LUD-PRJ-004
title: Project Pitch
revision: "1.0"
status: baselined
owner: Project lead
---

# Ludus — a gaming system that learns every game you play

## The one-line version

Ludus records how each game really runs on your machine, learns between sessions what would
make it run better, proves every change safe before using it, and can undo everything with
one action — built with the discipline of avionics software, in the open.

## The problem

- **Stutter, not average FPS, is what players feel.** Frame-time spikes come from shader and
  pipeline compilation, poor scheduling of game threads, asset streaming and background
  work. Average frame rates hide them.
- **Tuning is manual and per game.** Players copy launch options, scheduler tweaks and driver
  variables from forums, one game at a time, with no way to tell whether a tweak helped or
  quietly broke something.
- **System software treats every game the same.** The kernel, the drivers and the
  compatibility layers use generic defaults, although each game repeats the same patterns
  session after session.

## The idea

Games are repetitive workloads. A system that watches them can learn them.

1. **Record.** A low-overhead flight recorder captures frame timing, thread scheduling, GPU
   pass timing and file access, budgeted at no more than 1.0% added frame time.
2. **Learn.** Between sessions, Ludus finds patterns: which shaders to compile ahead of time,
   which threads are on the critical path, which files to prefetch.
3. **Verify.** Every candidate change is tested automatically before use: lossless changes
   must produce identical output and not worse frame times; changes that affect image quality
   are opt-in and must pass a perceptual check.
4. **Apply and undo.** Only verified changes reach the next session, and a single action
   restores the original configuration.

## Why it can be trusted

Software that runs with privileges and changes how games behave must earn trust. Ludus uses
the structure of **DO-178C**, the standard for airborne software, as its process model:

- plans and standards baselined **before** any product code (this release);
- every requirement traced to code and tests, checked automatically on every change;
- assurance levels by risk: privileged code needs 100% MC/DC coverage, the most demanding
  structural coverage criterion in common use;
- a public vulnerability process with CVE assignment;
- every deviation from the model written down, not hidden.

Ludus is **not certified** and does not claim to be. The model is used because it is the
most precise public description of how to build software that must not fail.

## Why now

- **Linux gaming has a real user base.** Linux accounted for 3.95% of Steam users in Valve's
  October 2026 survey ([Phoronix](https://phoronix.com/news/Steam-Survey-October-2026)).
  Monthly survey figures swing considerably, so this is an indicator, not a precise count.
- **The kernel now allows game-aware scheduling without forking it.** The sched_ext scheduler
  class, which runs scheduling policies as BPF programs, was merged for Linux 6.12
  ([merge commit](https://gitlab.freedesktop.org/drm/misc/kernel/-/commit/88264981f2082248e892a706b2c5004650faac54)).
  Valve has worked with Igalia on a sched_ext scheduler for the Steam Deck
  ([LWN](https://lwn.net/Articles/978007)).
- **The whole graphics stack is open on AMD hardware**: the `amdgpu` kernel driver and Mesa's
  RADV Vulkan driver, with Proton translating Windows games to Vulkan. Every layer can be
  observed and improved.

## What exists today (release 0.1.0)

Release 0.1.0 is the planning baseline. It is complete as a foundation and contains no
product code, by design.

| Item | Status |
|---|---|
| Assurance plans (PSAA, SDP, SVP, SCMP, SQAP) | Baselined |
| Requirements, design, coding and documentation standards | Baselined |
| Requirements baseline | 57 requirements: process tooling implemented, flight recorder drafted |
| Process tools: traceability, document control, commit messages, release consistency | Implemented, 171 tests, 100% statement and branch coverage |
| CI enforcing all of the above on every pull request | In place |
| Vulnerability management, threat model, advisory template | In place (threat model in draft) |

## What we do not claim

- **No performance numbers yet.** Ludus will publish gains only after measuring them with its
  reference benchmark procedure, including the cases where it does not help.
- **No certification.** See above.
- **AMD first.** Early results will apply to AMD GPUs only.
- **Independent review is pending.** The project has one maintainer; the deviation is
  recorded and LAL-1 code will not be merged without an independent reviewer.

## Roadmap

| Phase | Delivers |
|---|---|
| 0 | Planning baseline (this release) |
| 1 | Flight recorder: measure where frame time goes, per game, with bounded overhead |
| 2 | Learning loop with lossless optimizations, verifier and one-action rollback |
| 3 | Session mode; opt-in perceptual optimizations and frame multipliers |
| 4 | Opt-in fleet learning from verified profiles of similar machines |

Each phase ends at a review gate, not a date ([Roadmap](../project/roadmap.md)).

## What we are looking for

1. **A second maintainer** with Linux kernel, eBPF or Mesa experience, to provide the
   independent reviews the plans require.
2. **Reviewers** for the plans and the flight recorder requirements before gate G1.
3. **Reference hardware** (AMD GPUs across generations) for the benchmark procedure.
4. **Sponsors** to fund reference machines, CI capacity and a security audit of the first
   privileged component.

## Learn more

- [README](../../README.md) — project overview and quick start
- [PSAA](../plans/psaa.md) — the assurance approach in one document
- [Architecture Overview](../architecture/overview.md) — components and optimization tiers
- [SAS v0.1.0](../releases/v0.1.0/sas.md) — what this release achieved, and what is open

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
