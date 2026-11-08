---
doc_id: LUD-PRC-003
title: Release Process
revision: "1.0"
status: baselined
owner: Project lead
---

# Release Process

## 1. Purpose

This process produces a release baseline: a tagged, verified and documented state of the
repository. It implements the baseline and release rules of the [SCMP](../plans/scmp.md),
sections 5, 7 and 11.

## 2. Roles

| Role | Responsibility |
|---|---|
| Release manager | A maintainer who prepares and tags the release |
| Quality assurance | Performs the release conformance audit ([SQAP](../plans/sqap.md), section 3) |

## 3. Procedure

1. **Freeze.** Announce the release candidate commit in a release tracking issue. Only fixes
   for problems found during the release are merged after the freeze.
2. **Problem reports.** Confirm that no PR-1 problem report is open. List open PR-2 and PR-3
   reports for the SAS ([LUD-PRC-001](problem-reporting.md), section 6).
3. **Version.** Choose the version under [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).
   Update all version files (SCMP, section 7). Move the `[Unreleased]` changelog entries to a
   new section `## [X.Y.Z] - YYYY-MM-DD` and leave an empty `[Unreleased]` section.
4. **Release records.** Create `docs/releases/vX.Y.Z/` with:
   - `sci.md`: Software Configuration Index, including the life cycle environment;
   - `sas.md`: Software Accomplishment Summary, including verification results, deviations,
     open items and open problem reports.
   Add both documents to the [register](../README.md).
5. **Matrix.** Regenerate the traceability matrix (`make matrix`) so that its revision is the
   new version.
6. **Verify.** Run `make check` locally and confirm that CI passes on the release pull
   request. Run `make commits RANGE=<previous tag>..HEAD` and record the result in the SAS.
7. **Audit.** Quality assurance completes the release conformance audit and records it in
   the SAS.
8. **Merge** the release pull request to `main`.
9. **Tag.** Create an annotated tag on the merge commit:

   ```sh
   git tag -a vX.Y.Z -m "Ludus X.Y.Z"
   git push origin vX.Y.Z
   ```

   Once signing is enabled (OI-003), the tag is signed with `git tag -s`.
10. **Publish.** Create the GitHub release from the tag, with the changelog section as
    release notes. When the release contains build artifacts, attach them with SHA-256
    checksums, a software bill of materials, and (once enabled) Sigstore signatures and SLSA
    provenance.
11. **Announce** the release and close the release tracking issue.

## 4. Security releases

A release that fixes a vulnerability follows the same procedure, coordinated with the
advisory under [LUD-SEC-001](../security/vulnerability-management.md): the fix is prepared in
the advisory's private fork, the release is made when the fix is merged, and the advisory is
published together with the release.

## 5. Faulty releases

A tag is never moved or deleted. A release found to be faulty is marked as such in its
GitHub release notes and superseded by a new patch release.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
