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

## RFC-038 — Runtime Readiness Verification Contract

### Status

Architecture review complete; contract and TDD scope defined; implementation not started.

### Objective

Establish deterministic Runtime-owned readiness verification and align Bootstrap startup orchestration with the mandatory readiness requirements defined by BOOT-002 and RUNTIME-001.

### Architectural Findings

- RUNTIME-001 makes readiness a Runtime decision.
- Bootstrap may request readiness but SHALL NOT own Runtime state.
- ConfigurationProvider already owns mandatory configuration validation.
- Current Bootstrap startup does not invoke ConfigurationProvider validation.
- HealthCapability is read-only observation and reads Runtime readiness; it SHALL NOT become the readiness decision owner.
- Using HealthCapability as a pre-READY decision dependency would create a circular readiness dependency.
- ServiceRegistry owns service inventory and SHALL remain independent of lifecycle decisions.
- Current Bootstrap already owns deterministic service validation, initialization, plugin activation and rollback orchestration.
- Runtime metadata is already owned and available from Runtime.
- RFC-037 requires Request Admission to remain disabled until Runtime reaches READY.

### Dependencies

- BOOT-002 — Bootstrap Lifecycle Architecture
- RUNTIME-001 — Platform Lifecycle Architecture
- RFC-034 — Bootstrap Startup Failure Atomicity Contract
- RFC-035 — Bootstrap Shutdown Lifecycle Compliance Contract
- RFC-036 — Managed Shutdown Failure Containment Contract
- RFC-037 — Runtime Request Admission Control Contract
- ConfigurationProvider
- Runtime
- BootstrapManager
- ServiceRegistry
- HealthCapability

### RFC-038 Contract

- Runtime SHALL remain the exclusive owner of the READY lifecycle decision.
- Bootstrap SHALL request readiness only after all mandatory startup stages required by the current Core implementation have completed successfully.
- ConfigurationProvider SHALL remain the owner of configuration validation.
- Bootstrap SHALL invoke mandatory configuration validation before service validation or initialization.
- Runtime readiness verification SHALL consume immutable readiness evidence rather than infer readiness from HealthCapability.
- Readiness evidence SHALL represent completed mandatory startup conditions without transferring lifecycle ownership to Bootstrap.
- Runtime SHALL deterministically accept or reject the readiness request from the supplied evidence.
- Runtime SHALL NOT enter READY when any mandatory readiness evidence is unsatisfied.
- Bootstrap SHALL enable request admission only after Runtime has accepted the readiness request and entered READY.
- Failed readiness verification SHALL leave request admission disabled.
- Failed readiness verification SHALL participate in RFC-034 startup failure atomicity and rollback semantics.
- HealthCapability SHALL remain read-only observation and SHALL NOT become a readiness decision component.
- ServiceRegistry SHALL remain independent of lifecycle decisions.
- Existing RFC-035, RFC-036 and RFC-037 shutdown and request-admission behavior SHALL remain compatible.
- Existing Runtime mark_ready compatibility SHALL not be removed in RFC-038; production Bootstrap SHALL use the validated readiness path.
- RFC-038 SHALL NOT implement OPERATIONAL or DEGRADED transitions, API admission middleware, request rejection policy, traffic draining, retry, recovery, dependency-aware startup, parallel startup or health-report redesign.

### TDD Scope

RFC-038 implementation SHALL be driven by focused tests proving:

1. Readiness evidence is immutable.
2. Runtime accepts complete readiness evidence and enters READY.
3. Runtime rejects incomplete mandatory readiness evidence.
4. Rejected readiness leaves Runtime not ready.
5. Rejected readiness leaves request admission disabled.
6. Bootstrap invokes configuration validation before service validation.
7. Configuration validation failure prevents service validation, initialization and plugin activation.
8. Configuration validation failure transitions Runtime to FAILED.
9. Bootstrap constructs readiness evidence only after mandatory startup stages succeed.
10. Bootstrap requests validated readiness before enabling request admission.
11. Readiness rejection rolls back initialized plugins and services according to RFC-034 ordering.
12. HealthCapability remains read-only and is not used as the readiness decision owner.
13. Existing mark_ready compatibility remains available.
14. Existing RFC-034, RFC-035, RFC-036 and RFC-037 lifecycle behavior remains compatible.

### Implementation Boundary

- Introduce only the minimum immutable readiness-evidence contract and Runtime validation path.
- Inject ConfigurationProvider into Bootstrap through existing composition ownership.
- Preserve Composition Root as dependency-construction authority.
- Preserve Bootstrap as lifecycle orchestrator.
- Preserve Runtime as lifecycle-state and readiness-decision owner.
- Preserve HealthCapability as observation only.
- Do not introduce a second health subsystem or readiness manager.
- Do not implement OPERATIONAL, DEGRADED, API enforcement, retry, recovery or traffic draining.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Last completed RFC: RFC-037 — Runtime Request Admission Control Contract
- RFC-037 technical commit: `788b03b`
- Documentation baseline commit: `0d4d1f3`
- Full regression baseline: 236 passed

### Next Exact Action

Commit the RFC-038 contract, then write failing focused tests for immutable readiness evidence and Runtime readiness validation before implementation.



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

RFC-037 verification:

- Contract commit: `e6d2e51`
- Technical commit: `788b03b`
- Focused request-admission tests: 11 passed
- Runtime and Bootstrap lifecycle suite: 35 passed
- Impacted regression: 75 passed
- Full regression: 236 passed
- Remote push: verified

RFC-037 is closed.

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
