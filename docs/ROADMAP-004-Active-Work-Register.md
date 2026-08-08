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

## RFC-036 — Managed Shutdown Failure Containment Contract

### Status

Completed.

### Objective

Ensure managed platform shutdown continues deterministically after individual component failures, exposes unresolved shutdown state safely, and reports all shutdown failures without introducing automatic recovery or retry behavior.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Current technical RFC: RFC-036 — Managed Shutdown Failure Containment Contract
- Technical implementation commit: `438d7e4`
- Previous documentation baseline commit: `864af34`
- Full regression baseline: 225 passed

### Architectural Findings

- `PluginLifecycleManager.deactivate_all()` currently stops at the first plugin deactivation exception.
- A plugin deactivation exception currently prevents remaining plugins from being attempted.
- A plugin deactivation exception currently prevents registered services from being shut down by Bootstrap.
- A service shutdown exception currently prevents remaining services from being attempted.
- A shutdown exception currently leaves Runtime in `STOPPING`.
- RUNTIME-001 defines `FAILED` as the state for a critical failure preventing safe operation.
- RFC-035 requires Runtime to reach `STOPPED` only after required shutdown operations complete successfully.
- No existing shutdown failure aggregation policy exists.
- Python 3.11 provides native `ExceptionGroup` support for deterministic multi-error propagation.

### Dependencies

- BOOT-002 — Bootstrap Lifecycle Architecture
- RUNTIME-001 — Platform Lifecycle Architecture
- RFC-034 — Bootstrap Startup Failure Atomicity Contract
- RFC-035 — Bootstrap Shutdown Lifecycle Compliance Contract
- `Runtime`
- `BootstrapManager`
- `PluginLifecycleManager`
- `ServiceRegistry`

### RFC-036 Contract

- Managed shutdown SHALL remain best-effort after an individual component shutdown failure.
- Runtime SHALL enter `STOPPING` before managed shutdown attempts begin.
- `PluginLifecycleManager` SHALL attempt all active plugin deactivations in reverse activation order even when one or more plugin deactivations fail.
- Successfully deactivated plugins SHALL no longer be tracked as active.
- Plugins whose deactivation fails SHALL remain tracked as active because their final lifecycle state is unresolved.
- Plugin deactivation ownership SHALL remain exclusively in `PluginLifecycleManager`.
- Bootstrap SHALL continue to registered-service shutdown even when plugin deactivation reports failure.
- Bootstrap SHALL attempt all registered service shutdown operations in deterministic reverse registry enumeration order even when one or more service shutdown operations fail.
- Runtime SHALL transition to `STOPPED` only when all required managed shutdown operations complete successfully.
- If any managed shutdown operation fails, Runtime SHALL transition to `FAILED` and readiness SHALL remain false.
- A single shutdown failure SHALL remain the directly propagated original exception after all required shutdown attempts complete.
- Multiple shutdown failures SHALL be propagated as an `ExceptionGroup`.
- Failure aggregation SHALL preserve deterministic shutdown encounter order.
- Successful RFC-035 shutdown behavior SHALL remain backward compatible.
- RFC-034 startup atomicity behavior SHALL remain unchanged.
- RFC-036 SHALL NOT introduce automatic retry, automatic recovery, dependency graphs, parallel shutdown, ServiceState redesign, request-admission implementation, logging architecture redesign or process termination policy.

### TDD Scope

RFC-036 implementation SHALL be driven by focused tests proving:

1. Plugin deactivation continues after an individual plugin failure.
2. Plugin deactivation preserves reverse activation order during failure handling.
3. Successfully deactivated plugins are removed from the active set.
4. Plugins whose deactivation fails remain tracked as active.
5. A single plugin deactivation failure is propagated as the original exception.
6. Multiple plugin deactivation failures are propagated as an `ExceptionGroup`.
7. Plugin shutdown failure does not prevent registered-service shutdown.
8. Service shutdown failure does not prevent remaining service shutdown operations.
9. Any managed shutdown failure transitions Runtime to `FAILED` and keeps readiness false.
10. Runtime does not transition to `STOPPED` after failed managed shutdown.
11. A single Bootstrap-managed shutdown failure remains the original propagated exception.
12. Multiple Bootstrap-managed shutdown failures are propagated as an `ExceptionGroup` in deterministic encounter order.
13. Existing successful shutdown behavior remains unchanged.
14. RFC-034 successful startup and startup failure atomicity behavior remain unchanged.

### Implementation Boundary

RFC-036 should modify only the minimum Plugin Lifecycle, Bootstrap orchestration and focused test surfaces required for shutdown failure containment.

`Runtime` retains exclusive ownership of Runtime state transitions.

`BootstrapManager` retains shutdown orchestration ownership.

`PluginLifecycleManager` retains plugin deactivation ownership.

`ServiceRegistry` ordering semantics remain unchanged.

Do not introduce a second lifecycle manager, shutdown coordinator, retry engine or recovery subsystem.

Automatic retry, recovery strategy, process termination policy, dependency-aware shutdown and structured shutdown telemetry require separate architecture review.

### Verification

- Compilation: passed
- Focused RFC-036 lifecycle and shutdown containment tests: 31 passed
- Impacted runtime, bootstrap, plugin lifecycle and composition tests: 64 passed
- Full regression: 225 passed
- `git diff --check`: passed after EOF cleanup
- Technical commit: `438d7e4`
- Push: verified

### Next Exact Action

Synchronize the engineering-memory documents with the RFC-036 technical baseline before selecting RFC-037.


---

# Recently Completed Work

| RFC-036 | `438d7e4` | Managed shutdown failure containment contract |

| RFC-035 | `3e613df` | Bootstrap shutdown lifecycle compliance contract |

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
