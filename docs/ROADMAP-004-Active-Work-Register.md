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

## RFC-034 — Bootstrap Startup Failure Atomicity Contract

### Status

Completed.

### Objective

Enforce fail-fast and atomic startup behavior at the Bootstrap orchestration boundary so that a failed startup cannot leave successfully started services or plugins intentionally running and Runtime cannot become READY.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Last completed RFC: RFC-033 — Plugin Version Format Contract
- RFC-033 technical commit: `569e4fb`
- Documentation baseline commit: `e3d3b3a`
- Full regression baseline: 204 passed

### Architectural Findings

- BOOT-002 requires Bootstrap to stop startup immediately when a critical dependency fails.
- BOOT-002 prohibits partial startup unless explicitly supported.
- BOOT-002 defines Service Validation before Service Initialization.
- RUNTIME-001 defines `FAILED` as the state for a critical failure preventing safe operation.
- Runtime currently exposes no public operation for transitioning to `FAILED`.
- `BootstrapManager.startup()` currently validates and initializes services one at a time rather than completing the validation phase before initialization.
- `BootstrapManager.startup()` currently performs no compensating cleanup when service initialization or plugin activation fails.
- `PluginLifecycleManager` already tracks successfully activated plugins and deactivates active plugins in reverse order.
- Startup recovery strategies remain a future enhancement and are not part of RFC-034.

### Dependencies

- BOOT-002 — Bootstrap Lifecycle Architecture
- BOOT-001 — Platform Bootstrap Lifecycle
- RUNTIME-001 — Platform Lifecycle Architecture
- `Runtime`
- `BootstrapManager`
- `ServiceRegistry`
- `BaseService`
- `PluginLifecycleManager`

### RFC-034 Contract

- Bootstrap startup SHALL remain deterministic and fail fast.
- All registered services SHALL complete validation before any registered service is initialized.
- A service validation failure SHALL stop startup before service initialization or plugin activation begins.
- A service initialization failure SHALL stop further initialization.
- Only services whose `initialize()` operation completed successfully during the current startup attempt SHALL be eligible for startup rollback.
- Successfully initialized services SHALL be shut down in reverse initialization order when a later startup stage fails.
- A plugin activation failure SHALL stop further activation.
- Successfully activated plugins SHALL be deactivated through the existing `PluginLifecycleManager` before initialized services are rolled back.
- Plugin rollback SHALL preserve the existing reverse activation order.
- Runtime SHALL expose a public failure transition operation owned by Runtime.
- A critical startup failure SHALL transition Runtime to `FAILED` through that public Runtime operation.
- Runtime readiness SHALL remain false after a failed startup.
- Runtime SHALL NOT transition to READY unless all mandatory startup stages complete successfully.
- The original startup exception SHALL remain the primary propagated failure when compensating cleanup completes successfully.
- Successful startup and shutdown behavior SHALL remain backward compatible.
- RFC-034 SHALL NOT introduce retry logic, automatic startup recovery, dependency graphs, parallel initialization, plugin discovery, service-state redesign, logging architecture redesign, or version compatibility policy.

### TDD Scope

RFC-034 implementation SHALL be driven by focused tests proving:

1. Runtime can transition to `FAILED` through its public API while remaining not ready.
2. A service validation failure prevents all service initialization.
3. A service validation failure prevents plugin activation.
4. A service initialization failure prevents subsequent service initialization.
5. Previously initialized services are shut down in reverse initialization order after initialization failure.
6. A plugin activation failure rolls back previously activated plugins in reverse activation order.
7. A plugin activation failure rolls back initialized services after plugin rollback.
8. Any critical startup failure leaves Runtime in `FAILED` and not ready.
9. The original startup exception remains the propagated failure when rollback completes successfully.
10. Existing successful startup and shutdown behavior remains unchanged.

### Implementation Boundary

RFC-034 should modify only the minimum Runtime, Bootstrap orchestration and focused test surfaces required to enforce the contract.

`Runtime` retains ownership of Runtime state transitions.

`BootstrapManager` retains startup and shutdown orchestration ownership.

`PluginLifecycleManager` retains plugin lifecycle ownership and its existing public deactivation path should be reused unless a failing focused test proves an architecture-reviewed change is required.

Do not redesign `ServiceRegistry`, `BaseService`, `ServiceState`, `PluginRegistry`, `PluginRegistration`, Composition Root, plugin metadata, plugin versioning or existing lifecycle ownership.

Secondary rollback-failure aggregation and startup recovery strategies require separate architecture review and are outside RFC-034.

### Verification

- Compilation: passed
- Focused RFC-034 tests: 10 passed
- Impacted runtime, bootstrap, plugin lifecycle and composition tests: 53 passed
- Full regression: 214 passed
- `git diff --check`: passed
- Technical commit: `a174009`
- Push: verified
- Technical working tree: clean

### Next Exact Action

Begin architecture review for RFC-035 from the RFC-034 technical and documentation baseline.


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

The previous RFC-021 and RFC-022 active-work entries were stale relative to the committed Git history and are no longer active items.

Any historical task suspected to remain incomplete must be reopened only after current-code, dependency and regression review.

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
