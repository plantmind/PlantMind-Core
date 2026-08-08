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

## RFC-040 — Platform Operational Semantics Alignment Contract

### Status

Contract defined. Documentation alignment active.

### Objective

Establish one authoritative meaning for `READY`, request admission and `OPERATIONAL` before any future implementation of the `READY` to `OPERATIONAL` lifecycle transition.

### Architecture Problem

Current architecture contains terminology that can be interpreted inconsistently:

- Runtime defines `READY` and `OPERATIONAL` as distinct platform lifecycle states.
- Bootstrap currently completes successful startup at `READY` and then enables request admission.
- Request admission currently permits new operational API requests but does not transition Runtime to `OPERATIONAL`.
- HealthCapability is read-only observation and must not become a lifecycle decision authority.
- BOOT-001 uses the word operational for successful startup criteria while ending at `READY`.
- CORE-002 describes a conceptual service lifecycle containing `Operational`, while the implemented `ServiceState` does not contain `OPERATIONAL`.
- No approved Runtime operation currently performs the `READY` to `OPERATIONAL` transition.

### Contract

#### READY

`READY` means all mandatory startup and readiness requirements have completed successfully.

A Runtime in `READY` is eligible for request admission.

`READY` does not mean the platform has entered the `OPERATIONAL` lifecycle state.

#### Request Admission

Request admission is an independent Runtime-owned control indicating whether new operational requests may enter the API hosting boundary.

Request admission may be enabled after Runtime reaches `READY`.

Enabling request admission SHALL NOT itself transition Runtime to `OPERATIONAL`.

#### OPERATIONAL

`OPERATIONAL` remains a distinct Runtime lifecycle state.

The platform SHALL NOT enter `OPERATIONAL` merely because:

- Bootstrap completed;
- Runtime entered `READY`;
- request admission was enabled;
- an API middleware allowed a request.

A future `READY` to `OPERATIONAL` transition SHALL require a dedicated architecture contract defining the approved operational workload execution boundary and transition authority.

#### Runtime

Runtime remains the sole authoritative owner of platform lifecycle state.

Only an approved Runtime public operation may perform a future `OPERATIONAL` transition.

RFC-040 SHALL NOT add such an operation.

#### Bootstrap

Bootstrap remains the startup and shutdown coordinator.

Successful Bootstrap startup SHALL terminate at Runtime `READY`, followed by request-admission enablement.

Bootstrap SHALL NOT transition Runtime to `OPERATIONAL` under RFC-040.

#### HealthCapability

HealthCapability remains read-only observation.

HealthCapability MAY report observed Runtime lifecycle and health information.

HealthCapability SHALL NOT decide, initiate or authorize the `OPERATIONAL` transition.

HealthCapability SHALL NOT become a second lifecycle authority.

#### API Hosting

API request-admission enforcement remains read-only with respect to Runtime lifecycle ownership.

Allowing an operational request through the admission boundary SHALL NOT itself cause a lifecycle transition.

#### Core Service Lifecycle

The `Operational` stage described by CORE-002 SHALL be treated as architectural lifecycle intent and not as currently implemented `ServiceState` behavior.

RFC-040 SHALL NOT add `ServiceState.OPERATIONAL`.

Any future expansion of Core Service lifecycle states requires dedicated architecture review.

#### DEGRADED

`DEGRADED` remains deferred.

RFC-040 SHALL NOT define or implement degraded-state detection, transition or recovery.

### Documentation Alignment Required

RFC-040 SHALL align conflicting terminology in:

- `docs/BOOT-001-Platform-Bootstrap-Lifecycle.md`
- `docs/CAP-002-Health-Capability.md`
- `docs/CORE-002-Core-Services-Architecture.md`

Alignment SHALL preserve accepted ADR decisions and current committed behavior.

`RUNTIME-001` remains authoritative for the distinction between `READY` and `OPERATIONAL`.

### Non-Goals

RFC-040 SHALL NOT:

- modify production Python code;
- add a Runtime operational transition method;
- modify Bootstrap execution behavior;
- modify request-admission behavior;
- modify API middleware behavior;
- add `ServiceState.OPERATIONAL`;
- implement operational workload detection;
- implement `DEGRADED`;
- implement traffic draining;
- implement retry or recovery;
- introduce authentication or authorization behavior.

### Verification

RFC-040 completion requires:

- conflicting lifecycle terminology aligned;
- Runtime lifecycle ownership preserved;
- Bootstrap ownership preserved;
- HealthCapability read-only boundary preserved;
- API admission ownership preserved;
- no production code changes;
- documentation diff validation passed;
- full regression remains unchanged from the RFC-039 technical baseline unless unrelated repository state requires otherwise.

### Next Exact Action

Align BOOT-001, CAP-002 and CORE-002 with this contract without changing production code.

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
| RFC-039 | `bc26371` | API request admission enforcement contract |

RFC-039 verification:

- Contract commit: `4b738df`
- Technical commit: `bc26371`
- Focused API and lifecycle suite: 39 passed
- Impacted regression: 88 passed
- Full regression: 256 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

RFC-039 is technically complete.

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
