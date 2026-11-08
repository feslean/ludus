# Ludus

**A gaming system that learns every game you play — and proves each change safe before
using it.**

Ludus records how each game really runs on your machine, learns between sessions which
scheduling, shader, memory and I/O changes would make it run better, verifies every change
automatically, and can undo everything with a single action. It builds on Linux, Mesa and
Proton, and targets AMD graphics hardware first.

> **Status: planning baseline (0.1.0).** This release contains the plans, standards,
> requirements baseline and process tools under which Ludus will be built. It contains no
> product code yet. See the [roadmap](docs/project/roadmap.md).

> **Not certified.** Ludus uses DO-178C, the standard for airborne software, as a
> *process model*. Ludus is not certified under DO-178C or any other standard, and no
> certification authority has reviewed it. See
> [ADR-0007](docs/architecture/adr/0007-do-178c-as-process-model.md).

## Why Ludus is different

| Property | How Ludus will achieve it |
|---|---|
| Every change is verified before use | Tiered verification; image-changing optimizations are opt-in ([ADR-0006](docs/architecture/adr/0006-perceptual-tiers-opt-in.md)) |
| Everything is reversible | Single-action rollback to the unmodified configuration |
| Your data stays local | Telemetry is kept on your machine unless you opt in |
| Privileged code is held to the highest rigor | Assurance level LAL-1: 100% MC/DC structural coverage, independent review |
| Every function traces to a requirement | Bidirectional traceability between requirements, code and tests, checked on every pull request (in place today) |

Read the [project pitch](docs/pitch/pitch.md) for the full story.

## How the project is run

Ludus is developed under a set of controlled documents modeled on DO-178C. The
[document register](docs/README.md) lists all of them. The most important are:

| Document | What it tells you |
|---|---|
| [PSAA](docs/plans/psaa.md) | Assurance levels, life cycle data, deviations from the model |
| [SDP](docs/plans/sdp.md) | How requirements, design and code are produced |
| [SVP](docs/plans/svp.md) | Reviews, tests, structural coverage, regression policy, benchmarks |
| [SCMP](docs/plans/scmp.md) | Branches, commit rules, versioning, baselines |
| [SQAP](docs/plans/sqap.md) | Quality assurance and gate audits |
| [Vulnerability management](docs/security/vulnerability-management.md) | How vulnerabilities are handled and CVEs assigned |

## Repository layout

```text
requirements/      System and high-level requirements (TOML)
docs/              Controlled documents (plans, standards, processes, security, releases)
tools/ludus_tools/ Process tools: traceability, document, commit and release checkers
tests/             Verification cases
.github/           CI workflows, issue and pull request templates
```

## Quick start

Requirements: Python 3.13, Git, GNU Make.

```sh
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
make check        # lint, type check, tests with coverage, traceability, documents, licensing
make hooks        # optional: check commit messages locally
```

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first: Ludus has a
stricter process than most open-source projects, and the guide explains it step by step.
All participants follow the [Code of Conduct](CODE_OF_CONDUCT.md). Project roles and
decision making are described in [GOVERNANCE.md](GOVERNANCE.md).

## Security

Do not report vulnerabilities in public issues. See [SECURITY.md](SECURITY.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

Ludus code and documentation are licensed under the MIT License; see [LICENSE](LICENSE).
Components that are contributed to upstream projects use licenses compatible with those
projects, as described in [ADR-0004](docs/architecture/adr/0004-licensing.md). Every file
declares its license with [SPDX](https://spdx.dev/) identifiers, checked with
[REUSE](https://reuse.software/).
