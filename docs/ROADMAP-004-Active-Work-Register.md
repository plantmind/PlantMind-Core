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

## RFC-035 — Bootstrap Shutdown Lifecycle Compliance Contract

### Status

Architecture review complete; contract and TDD scope defined; implementation not started.

### Objective

Align the implemented Bootstrap shutdown lifecycle with BOOT-002 and RUNTIME-001 while preserving existing Runtime, Service Registry and Plugin Lifecycle ownership boundaries.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Last completed RFC: RFC-034 — Bootstrap Startup Failure Atomicity Contract
- RFC-034 technical commit: `a174009`
- Documentation baseline commit: `6e34e7f`
- Full regression baseline: 214 passed

### Architectural Findings

- BOOT-002 requires Runtime transition to `STOPPING` before component shutdown begins.
- BOOT-002 requires Runtime transition to `STOPPED` only after shutdown completes.
- Runtime currently exposes no public transition operation for `STOPPING`.
- `Runtime.mark_not_ready()` currently transitions directly to `STOPPED`.
- `BootstrapManager.shutdown()` currently performs component shutdown without first requesting Runtime `STOPPING`.
- Runtime state ownership must remain inside Runtime.
- Bootstrap must continue to coordinate shutdown through public lifecycle interfaces.
- Shutdown-failure aggregation and recovery semantics are not defined by the current accepted architecture and remain outside RFC-035.

### Dependencies

- BOOT-002 — Bootstrap Lifecycle Architecture
- RUNTIME-001 — Platform Lifecycle Architecture
- RFC-034 — Bootstrap Startup Failure Atomicity Contract
- `Runtime`
- `BootstrapManager`
- `ServiceRegistry`
- `PluginLifecycleManager`

### RFC-035 Contract

- Runtime SHALL expose a public transition operation for `STOPPING`.
- The `STOPPING` transition SHALL set Runtime readiness to false.
- Bootstrap shutdown SHALL request Runtime transition to `STOPPING` before component shutdown begins.
- Runtime SHALL remain not ready throughout shutdown.
- Registered services SHALL be shut down in deterministic reverse registration order.
- Existing plugin deactivation SHALL remain owned by `PluginLifecycleManager`.
- Bootstrap SHALL request Runtime transition to `STOPPED` only after required shutdown operations complete successfully.
- `Runtime.mark_not_ready()` backward-compatible behavior SHALL remain unchanged unless a failing regression proves an architecture-reviewed change is required.
- Successful startup behavior established by RFC-034 SHALL remain unchanged.
- RFC-035 SHALL NOT introduce shutdown retry logic, cleanup-failure aggregation, automatic recovery, dependency graphs, parallel shutdown, ServiceState redesign, request-admission implementation, plugin discovery or logging architecture redesign.

### TDD Scope

RFC-035 implementation SHALL be driven by focused tests proving:

1. Runtime can transition to `STOPPING` through its public API.
2. Runtime is not ready while in `STOPPING`.
3. Bootstrap requests `STOPPING` before plugin or service shutdown work begins.
4. Registered services shut down in deterministic reverse registration order.
5. Plugin deactivation remains delegated to `PluginLifecycleManager`.
6. Runtime transitions to `STOPPED` only after shutdown operations complete.
7. Runtime remains not ready after successful shutdown.
8. Existing `mark_not_ready()` behavior remains backward compatible.
9. RFC-034 successful startup behavior remains unchanged.
10. Existing graceful shutdown behavior remains compatible except for the newly observable `STOPPING` transition.

### Implementation Boundary

RFC-035 should modify only the minimum Runtime, Bootstrap orchestration and focused test surfaces required to enforce the shutdown lifecycle contract.

`Runtime` retains exclusive ownership of Runtime state transitions.

`BootstrapManager` retains shutdown orchestration ownership.

`PluginLifecycleManager` retains plugin deactivation ownership.

Do not redesign `ServiceRegistry`, `BaseService`, `ServiceState`, `PluginRegistry`, Composition Root or the RFC-034 startup atomicity behavior.

Shutdown-failure aggregation, retry and recovery require separate architecture review and remain outside RFC-035.

### Next Exact Action

Write the RFC-035 failing focused tests before implementation.


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
