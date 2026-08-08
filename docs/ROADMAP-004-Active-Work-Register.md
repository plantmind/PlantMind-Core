# ROADMAP-004 — Active Work Register

| Property | Value |
|----------|-------|
| Status | Active |
| Version | 1.1 |
| Owner | Platform Architecture |
| Purpose | Prevent unfinished work from being lost |

---

# Rule

No RFC may be paused, redirected, or superseded without recording:

- Current status
- Completed work
- Remaining work
- Dependencies
- Resume condition
- Next exact action

No item may be marked complete until:

- Unit tests pass
- Full regression tests pass
- Git commit is verified
- Remote push is verified
- Working tree is clean
- Required engineering documentation is updated

---

# Active Work

## RFC-039 — API Request Admission Enforcement Contract

### Status

Architecture review complete; contract and TDD scope defined; implementation not started.

### Objective

Establish API-hosting enforcement of the Runtime-owned request-admission state without transferring admission ownership or lifecycle authority out of Runtime.

### Architectural Findings

- RFC-037 establishes Runtime as the exclusive owner of request-admission state.
- RUNTIME-001 requires the API hosting layer to enforce request admission according to Runtime.
- The current FastAPI hosting layer does not enforce Runtime request-admission state.
- The current application exposes platform status at `/` and platform health at `/health`.
- Platform status and health are observability interfaces and must remain available when operational request admission is disabled.
- `HealthCapability` remains read-only observation.
- Current production API hosting does not yet expose a real operational workload endpoint.
- Empty API modules SHALL NOT be populated merely to provide an RFC-039 test target.
- RFC-038 requires Runtime readiness before request admission can be enabled.
- OPERATIONAL state requires actual workload serving and therefore remains a separate lifecycle concern.

### Dependencies

- RUNTIME-001 — Platform Lifecycle Architecture
- BOOT-002 — Bootstrap Lifecycle Architecture
- RFC-037 — Runtime Request Admission Control Contract
- RFC-038 — Runtime Readiness Verification Contract
- Runtime
- FastAPI hosting layer
- HealthCapability
- Composition Root

### RFC-039 Contract

- Runtime SHALL remain the exclusive owner of request-admission state.
- The API hosting layer SHALL enforce the Runtime-owned request-admission state for operational requests.
- API admission enforcement SHALL observe Runtime through its public request-admission interface.
- API admission enforcement SHALL NOT modify Runtime lifecycle state or request-admission state.
- Operational requests received while request admission is disabled SHALL be rejected deterministically.
- Rejected operational requests SHALL return HTTP `503 Service Unavailable`.
- The rejection response SHALL use a stable platform-owned response contract.
- Platform observability endpoints SHALL remain available while operational request admission is disabled.
- `/` SHALL remain an approved platform-status observation endpoint.
- `/health` SHALL remain an approved platform-health observation endpoint.
- Observation exemptions SHALL be explicit and SHALL NOT use an unrestricted health-path wildcard.
- HealthCapability SHALL remain read-only and SHALL NOT participate in admission decisions.
- Bootstrap SHALL remain responsible only for enabling and disabling admission through Runtime lifecycle orchestration.
- API hosting SHALL consume the same composed Runtime instance used by the platform lifecycle.
- Request admission SHALL be evaluated when a new request enters the API hosting boundary.
- RFC-039 SHALL NOT define draining or cancellation semantics for already-running requests.
- Existing RFC-037 and RFC-038 lifecycle ordering SHALL remain compatible.
- RFC-039 SHALL NOT implement OPERATIONAL or DEGRADED transitions, authentication, authorization, rate limiting, retry, recovery, traffic draining, business workflows or new production workload endpoints.

### TDD Scope

RFC-039 implementation SHALL be driven by focused tests proving:

1. An operational request is allowed when Runtime request admission is enabled.
2. An operational request is rejected when Runtime request admission is disabled.
3. Rejected operational requests return HTTP 503.
4. Rejection uses a deterministic response contract.
5. API enforcement does not enable or disable Runtime admission.
6. API enforcement does not change Runtime lifecycle state.
7. `/` remains available when request admission is disabled.
8. `/health` remains available when request admission is disabled.
9. Observation exemptions are explicit rather than wildcard-based.
10. API enforcement reads the same composed Runtime instance used by the platform.
11. Normal successful application startup preserves existing API behavior.
12. RFC-037 request-admission lifecycle tests remain compatible.
13. RFC-038 readiness verification behavior remains compatible.
14. Existing API tests remain compatible.
15. No production business endpoint is introduced solely for admission testing.

### Implementation Boundary

- Introduce the minimum API-hosting admission enforcement component.
- Preserve Runtime as admission-state owner.
- Preserve Bootstrap as lifecycle orchestrator.
- Preserve HealthCapability as read-only observation.
- Preserve Composition Root dependency ownership.
- Keep approved observation routes explicit.
- Use test-only operational routes where necessary to verify enforcement.
- Do not populate empty business API modules as part of RFC-039.
- Do not implement OPERATIONAL, DEGRADED, authentication, authorization, rate limiting, retry, recovery or traffic draining.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Last completed RFC: RFC-038 — Runtime Readiness Verification Contract
- RFC-038 technical commit: `b65cceb`
- Documentation baseline commit: `4dfd886`
- Full regression baseline: 248 passed

### Next Exact Action

Commit the RFC-039 contract, then write failing focused API request-admission enforcement tests before implementation.

---

# Recently Completed Work

| RFC | Commit | Result |
|---|---|---|
| RFC-021 | `132baca` | Extensible PI tag reader architecture |
| RFC-022 | `0f35b3e` | Generic registry framework |
| RFC-023 | `dbb0a3d` | PI tag reader factory migration to generic registry |
| RFC-024 | `ed9dd63` | Registry public API |
| RFC-025 | `fab2740` | Core plugin framework |
| RFC-026 | `e91a5a7` | Bootstrap public API consolidation |
| RFC-027 | `463e13f` | Plugin lifecycle integration into Bootstrap |
| RFC-028 | `128f129` | Plugin lifecycle manager |
| RFC-029 | `10d6171` | Plugin infrastructure composition |
| RFC-030 | `72a8533` | Controlled plugin registration boundary |
| RFC-031 | `defc1fe` | Plugin identity consistency contract |
| RFC-032 | `6b4d80f` | Plugin metadata contract |
| RFC-033 | `569e4fb` | Plugin version format contract |
| RFC-034 | `a174009` | Bootstrap startup failure atomicity contract |
| RFC-035 | `3e613df` | Bootstrap shutdown lifecycle compliance contract |
| RFC-036 | `438d7e4` | Managed shutdown failure containment contract |
| RFC-037 | `788b03b` | Runtime request admission control contract |
| RFC-038 | `b65cceb` | Runtime readiness verification contract |

RFC-038 verification:

- Contract commit: `cc683fc`
- Technical commit: `b65cceb`
- Focused RFC-038 suite: 52 passed
- Impacted regression: 91 passed
- Full regression: 248 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

RFC-038 is technically complete.

---

# Deferred Architecture Work

## PI Connector Package Migration

### Status

Deferred intentionally.

### Current State

- `backend/app/connectors/pi_connector.py`
- `backend/app/connectors/pi/`

### Future Action

Move the implementation to:

`backend/app/connectors/pi/connector.py`

Retain a backward-compatible wrapper temporarily before removal.

---

## Logging Consolidation

### Status

Deferred intentionally.

### Current State

- `backend/app/core/logger.py`
- `backend/app/core/logging/logging_provider.py`

### Future Action

Migrate all logging consumers to the logging package, then deprecate the legacy wrapper.

---

## Session Memory Naming Review

### Status

Deferred intentionally.

### Current State

`backend/app/memory/session_memory.py` is empty.

### Future Action

Define its intended responsibility before deciding whether to rename, merge, implement, or remove it.

---

# Completion Discipline

At the end of every work session, this register SHALL be updated before starting unrelated work.

The active item at the top of this document SHALL always contain the next exact executable action.
