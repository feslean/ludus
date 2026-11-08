---
doc_id: LUD-REL-001
title: Software Configuration Index, release 0.1.0
revision: "0.1.0"
status: baselined
owner: Release manager
---

# Software Configuration Index, release 0.1.0

## 1. Identification

| Item | Value |
|---|---|
| Product | Ludus |
| Release | 0.1.0 (planning baseline) |
| Release date | 2026-11-08 |
| Git tag | `v0.1.0` (annotated) |
| Content | Every file in the Git tree of the tagged commit |

The tag identifies the commit, and the commit's tree object identifies the exact content of
every file by hash. Retrieve the configuration with `git checkout v0.1.0` and check the
integrity of the repository with `git fsck`.

This release contains no executable product code and no build artifacts. Its configuration
items are documents, requirements, process tools and their tests.

## 2. Controlled documents

| ID | Title | Revision | Status |
|---|---|---|---|
| LUD-PRJ-000 | Document Register | 1.0 | baselined |
| LUD-PRJ-001 | Roadmap and Review Gates | 1.0 | baselined |
| LUD-PRJ-002 | Risk Register | 1.0 | baselined |
| LUD-PRJ-003 | Glossary | 1.0 | baselined |
| LUD-PRJ-004 | Project Pitch | 1.0 | baselined |
| LUD-PLN-001 | Plan for Software Aspects of Assurance (PSAA) | 1.0 | baselined |
| LUD-PLN-002 | Software Development Plan (SDP) | 1.0 | baselined |
| LUD-PLN-003 | Software Verification Plan (SVP) | 1.0 | baselined |
| LUD-PLN-004 | Software Configuration Management Plan (SCMP) | 1.0 | baselined |
| LUD-PLN-005 | Software Quality Assurance Plan (SQAP) | 1.0 | baselined |
| LUD-STD-001 | Requirements Standard | 1.0 | baselined |
| LUD-STD-002 | Design Standard | 1.0 | baselined |
| LUD-STD-003 | Coding Standard | 1.0 | baselined |
| LUD-STD-004 | Documentation Standard | 1.0 | baselined |
| LUD-PRC-001 | Problem Reporting and Corrective Action Process | 1.0 | baselined |
| LUD-PRC-002 | Tool Qualification Plan | 1.0 | baselined |
| LUD-PRC-003 | Release Process | 1.0 | baselined |
| LUD-SEC-001 | Vulnerability Management Process | 1.0 | baselined |
| LUD-SEC-002 | Threat Model | 0.1 | draft |
| LUD-SEC-003 | Security Advisory Index | 1.0 | baselined |
| LUD-SEC-004 | Security Advisory Template | 1.0 | baselined |
| LUD-ARC-001 | Architecture Overview | 0.1 | draft |
| LUD-ADR-0000 | ADR-0000: Decision record template | 1.0 | baselined |
| LUD-ADR-0001 | ADR-0001: Record architecture decisions | 1.0 | baselined |
| LUD-ADR-0002 | ADR-0002: Build on Linux instead of a new kernel | 1.0 | baselined |
| LUD-ADR-0003 | ADR-0003: Target AMD graphics hardware first | 1.0 | baselined |
| LUD-ADR-0004 | ADR-0004: Licensing of Ludus code | 1.0 | baselined |
| LUD-ADR-0005 | ADR-0005: Programming languages by assurance level | 1.0 | baselined |
| LUD-ADR-0006 | ADR-0006: Perceptual optimizations are opt-in | 1.0 | baselined |
| LUD-ADR-0007 | ADR-0007: Use DO-178C as a process model, without certification | 1.0 | baselined |
| LUD-VER-001 | Requirements Traceability Matrix | 0.1.0 | baselined (generated) |
| LUD-REL-001 | Software Configuration Index, release 0.1.0 | 0.1.0 | baselined |
| LUD-REL-002 | Software Accomplishment Summary, release 0.1.0 | 0.1.0 | baselined |

## 3. Requirements

| File | Content | Requirements |
|---|---|---|
| `requirements/system.toml` | System requirements | 10 |
| `requirements/hlr-process-tooling.toml` | High-level requirements of tools T-001 to T-004 | 35 |
| `requirements/hlr-flight-recorder.toml` | High-level requirements of the flight recorder (draft) | 12 |

## 4. Process tools

| ID | Tool | Source | Version |
|---|---|---|---|
| T-001 | Traceability checker | `tools/ludus_tools/trace.py` | 0.1.0 |
| T-002 | Document checker | `tools/ludus_tools/doccheck.py` | 0.1.0 |
| T-003 | Commit message checker | `tools/ludus_tools/commitcheck.py` | 0.1.0 |
| T-004 | Release checker | `tools/ludus_tools/release.py` | 0.1.0 |
| — | Shared configuration helpers | `tools/ludus_tools/_config.py` | 0.1.0 |

Verification cases: `tests/tools/`.

## 5. Life cycle environment

The environment in which the verification results of the SAS were produced:

| Item | Version |
|---|---|
| Operating system | Ubuntu 24.04.5 LTS, Linux 6.18 x86_64 |
| Python | 3.13.18 |
| pytest | 9.1.1 |
| pytest-cov | 7.1.0 |
| coverage.py | 7.17.2 |
| ruff | 0.17.4 |
| mypy | 2.3.1 |
| reuse | 6.3.0 |
| Git | 2.43.0 |
| GNU Make | 4.3 |

CI uses the runner image and actions named in `.github/workflows/ci.yml`, with the Python
packages pinned in `requirements-dev.txt`.

## 6. Build and retrieval instructions

```sh
git clone <repository URL>
cd ludus
git checkout v0.1.0
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
make check
```

## Revision history

| Revision | Date | Description |
|---|---|---|
| 0.1.0 | 2026-11-08 | Configuration index for release 0.1.0. |
