---
doc_id: LUD-PLN-005
title: Software Quality Assurance Plan (SQAP)
revision: "1.0"
status: baselined
owner: Project lead
---

# Software Quality Assurance Plan (SQAP)

## 1. Purpose

Quality assurance gives confidence that the life cycle processes defined in the plans are
followed and that the life cycle data is complete. This plan refines the [PSAA](psaa.md)
(LUD-PLN-001). Quality assurance does not verify the software; it checks that verification,
configuration management and development were done as planned.

## 2. Organization and authority

1. The **quality assurance role** is held by a maintainer other than the author of the item
   being assessed. While the project has one maintainer, the role is held by that maintainer,
   which is recorded under deviation D-002 (PSAA, section 7).
2. The quality assurance role may block a merge or a release by recording a finding. A
   finding is resolved before the merge or release, or the merge or release is deferred.
3. Quality assurance findings are tracked as problem reports with the label `qa-finding`.

## 3. Activities

| Activity | When | Method | Record |
|---|---|---|---|
| Automated process conformance | Every pull request | CI runs `make check` and the commit message check | CI run |
| Pull request conformance | Every pull request | Reviewer confirms the template checklist is complete and truthful | Pull request review |
| Transition criteria audit | Every gate (G0 to G3) | Checklist in section 4 | Gate record in `docs/releases/` |
| Release conformance audit | Every release | Checklist of the [Release Process](../process/release-process.md) | SAS of the release |
| Problem report audit | Every release | All problem reports closed or listed as open in the SAS | SAS of the release |
| Plan review | Every minor release | Plans and standards still describe the process actually used | Change requests for any update |

## 4. Gate audit checklist

At each gate the quality assurance role confirms:

1. The plans and standards that apply to the gate are `baselined` at the expected revision.
2. All requirements in the gate's scope have the expected status.
3. `make check` passes on the gate commit, and the traceability matrix shows no requirement
   in scope without implementation or verification.
4. The reviews required by the [SVP](svp.md) are recorded for every item in scope.
5. Deviations and open items are listed in the SAS with their status.
6. The gate record lists any finding and how it was resolved.

## 5. Conformity review

Before release 1.0 (gate G3), a conformity review checks that the life cycle data listed in
the PSAA, section 6, exists for every component, that it is under configuration control, and
that the SAS summarizes it accurately.

## 6. Records

Quality assurance records are pull request reviews, gate records and SAS entries. They are
retained under the [SCMP](scmp.md), section 12.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
