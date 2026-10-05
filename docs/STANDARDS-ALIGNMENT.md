# Standards Alignment — Signalproof Intelligence

**Revision:** V1/RD1  
**Status:** Candidate until governed merge to `main`

Signalproof Intelligence applies a repository-specific standards crosswalk to selected concepts from the NIST AI Risk Management Framework (AI RMF), NIST AI 600-1 Generative AI Profile, and the NIST AI 200-2 Initial Public Draft / TEVV-Athlon Framework.

This document describes only controls visible in this public repository. It does **not** claim NIST certification, NIST endorsement, or universal NIST compliance.

## Current Community CLI mapping

| Control / concept | NIST relationship | State | Public evidence |
|---|---|---:|---|
| Explicit model-route selection | GOVERN / MAP / MEASURE | IMPLEMENTED | `community-cli/README.md`, source and tests |
| No silent fallback | GOVERN / MEASURE | IMPLEMENTED | `community-cli/README.md`, source and tests |
| Loopback-only transport | MAP / MANAGE | IMPLEMENTED | `community-cli/README.md`, `PUBLIC-BOUNDARY.md` |
| No private connector inheritance | GOVERN / MANAGE | IMPLEMENTED | `PUBLIC-BOUNDARY.md` |
| No model tool authority | GOVERN / MANAGE | IMPLEMENTED | `community-cli/README.md` |
| Human approval before optional model download | GOVERN / MANAGE | IMPLEMENTED | `community-cli/README.md` |
| Exact model digest surfaced | MEASURE / VERIFY | IMPLEMENTED | `community-cli/README.md`, runtime/source behavior |
| Public sanitization gate | GOVERN / MEASURE / MANAGE | IMPLEMENTED | `tools/check_public_sanitization.py` and CI |
| Full model/agent TEVV acceptance suite | TEST / EVALUATION / VERIFICATION / VALIDATION | PLANNED / EXTERNAL | Not implemented by the Community CLI itself |
| Production deployment validation | VALIDATION / MANAGE | N/A | Community CLI is advisory/local-only |

## Interpretation

The Community CLI demonstrates a small set of governance controls around upstream local models. It is **not** presented as a complete AI risk-management implementation.

The canonical Signalproof standards methodology is maintained in the public Signalproof Skills repository under `standards/`, including the Signalproof AI Acceptance Protocol and NIST crosswalk documents.

## Claim rule

Preferred wording:

> The Signalproof Community CLI implements selected controls that map to NIST AI RMF and TEVV concepts.

Avoid:

> The Signalproof Community CLI is NIST compliant.

## Revalidation triggers

Revisit this mapping after any material change to:

- supported model routes;
- fallback behavior;
- transport boundaries;
- connector/tool authority;
- authentication/authorization;
- download/install behavior;
- public sanitization controls;
- deployment intent;
- relevant NIST framework revisions.
