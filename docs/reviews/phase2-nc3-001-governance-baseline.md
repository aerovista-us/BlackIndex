# Phase 2 — NC3 001: Public Governance and Controlled-Access Baseline

## Status

`ACTIVE — first public governance/source-genealogy milestone complete`

This pass begins the NC3 source-genealogy lane above the platform/manual layer.

The corpus now verifies **54 checked / 0 failures**.

## Public governance artifacts preserved

- `DOD-2013-dod-instructions-001` — DoDI 3741.01, *National Leadership Command Capabilities (NLCC) Configuration Management (CM)*.
- `DOD-2014-dod-directives-001` — DoDD 3700.01, *DoD Command and Control Enabling Capabilities*.
- `JCS-2007-cjcs-instructions-001` — CJCSI 5119.01C, Nuclear C3 centralized direction/management/operation/technical-support charter.

These three records are Canon at the document/provenance level. Their public text does not erase or replace controlled parent directives they cite.
## Controlled-access artifacts preserved

BlackIndex also preserves the official one-page public placeholders for:

- `DOD-2015-dod-controlled-issuance-placeholders-001` — DoDI S-3730.01, NC3 System.
- `DOD-2015-dod-controlled-issuance-placeholders-002` — DoDD S-3710.01, NLCC.
- `DOD-2017-dod-controlled-issuance-placeholders-001` — DoDD S-5210.81, U.S. Nuclear Weapons Command and Control, Safety and Security.

These records are Canon **only as public access-boundary artifacts**. They establish title, issuing authority/date context, and the public restriction statement. They do not expose the controlled directive contents.

DoDI S-3730.01 and DoDD S-3710.01 placeholders direct authorized users toward controlled government access. DoDD S-5210.81 states that it has not been cleared for placement on the public website.

## Source genealogy established

Two explicit dependency edges are now encoded:

- DoDI 3741.01 → controlled DoDD S-3710.01 for the governing NLCC construct.
- DoDD 3700.01 → controlled DoDD S-3710.01 and DoDD S-5210.81 for NLCC / nuclear-command policy dependencies.

This prevents public implementation layers from being counted as independent reproductions of the controlled parent policy.

CJCSI 5119.01C is preserved as a public Joint Staff governance charter in its own right. Its references to higher-level national guidance are not treated as proof of those unavailable source contents.

## Unresolved governance nodes

- DoDD S-3730.02 — *The Nuclear Command, Control, and Communication Enterprise* is publicly indexed, but no public first-party artifact or placeholder was preserved in this pass.
- DoDI O-3710.02 and O-3710.03 remain controlled/certificate-gated source-address nodes.
- AFGSCMD 63-101 — *USAF Nuclear Command, Control, and Communications (NC3) Center* is publicly indexed, but the expected first-party PDF returned HTTP 404 during this pass.

`not publicly recovered` is not equivalent to `does not exist`.
## Guardrails

- Do not infer controlled directive contents from platform manuals, public implementation directives, or titles.
- Do not count repeated policy language across public DoD/Joint Staff layers as independent corroboration until source lineage is established.
- Preserve access restrictions as evidence about availability, not as evidence for or against the underlying policy content.
- Recover only authorized public, declassified, FOIA-released, or unrestricted first-party artifacts.

## Next gate

1. Preserve a current public Joint Staff directives index to establish currency/status for CJCSI 5119.01C.
2. Recover public DoD/Joint Staff C3/NC3 modernization and governance records that sit above or beside the current platform layers.
3. Continue first-party archive recovery for AFGSCMD 63-101 and any public placeholder for DoDD S-3730.02.
4. Build source genealogy from E-4B/E-6B public mission layers into the recovered governance stack without importing detailed operating procedures.
