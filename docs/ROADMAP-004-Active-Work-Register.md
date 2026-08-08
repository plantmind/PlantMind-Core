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

## RFC-037 — Runtime Request Admission Control Contract

### Status

Architecture review complete; contract and TDD scope defined; implementation not started.

### Objective

Establish Runtime-owned request-admission state and align Bootstrap startup and shutdown orchestration with the request-admission boundaries defined by BOOT-002 and RUNTIME-001.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Last completed RFC: RFC-036 — Managed Shutdown Failure Containment Contract
- RFC-036 technical commit: `438d7e4`
- Documentation baseline commit: `2f77dbf`
- Full regression baseline: 225 passed

### Architectural Findings

- BOOT-002 requires Request Admission Enabled only after Runtime reaches READY.
- BOOT-002 requires Request Admission Disabled before Runtime enters STOPPING.
- RUNTIME-001 assigns Request Admission State ownership to Runtime.
- RUNTIME-001 assigns request-admission enforcement to the API hosting layer.
- Runtime currently exposes lifecycle readiness but no explicit request-admission state.
- Bootstrap currently reaches READY without explicitly enabling request admission.
- Bootstrap currently enters STOPPING without explicitly disabling request admission.
- RUNTIME-001 defines OPERATIONAL only after operational workloads begin being served.
- No current API hosting integration exists in the Core lifecycle implementation.
- BOOT-002 makes health verification an optional Bootstrap interaction rather than a mandatory current lifecycle dependency.

### Dependencies

- BOOT-002 — Bootstrap Lifecycle Architecture
- RUNTIME-001 — Platform Lifecycle Architecture
- RFC-034 — Bootstrap Startup Failure Atomicity Contract
- RFC-035 — Bootstrap Shutdown Lifecycle Compliance Contract
- RFC-036 — Managed Shutdown Failure Containment Contract
- `Runtime`
- `BootstrapManager`

### RFC-037 Contract

- Runtime SHALL own request-admission state.
- Request admission SHALL be disabled when Runtime is created.
- Runtime SHALL expose a public read interface for request-admission state.
- Runtime SHALL expose public operations to enable and disable request admission.
- Bootstrap SHALL enable request admission only after all mandatory startup stages succeed and Runtime has reached READY.
- Failed startup SHALL never leave request admission enabled.
- Bootstrap SHALL disable request admission before requesting Runtime transition to STOPPING.
- Request admission SHALL remain disabled throughout managed shutdown.
- Failed managed shutdown SHALL leave request admission disabled while Runtime transitions to FAILED.
- Runtime transitions to FAILED SHALL disable request admission.
- Runtime transitions to STOPPING SHALL not permit request admission to remain enabled.
- Existing Runtime readiness semantics SHALL remain unchanged.
- Existing successful startup, shutdown and RFC-036 failure-containment behavior SHALL remain backward compatible.
- API hosting layers SHALL remain responsible for enforcing admission according to Runtime state.
- RFC-037 SHALL NOT implement an API server, middleware, authentication, authorization, health verification, OPERATIONAL transition, DEGRADED transition, workload execution, retry, recovery or traffic-draining policy.

### TDD Scope

RFC-037 implementation SHALL be driven by focused tests proving:

1. Request admission is disabled when Runtime is created.
2. Runtime exposes request-admission state through a public read interface.
3. Runtime can explicitly enable request admission.
4. Runtime can explicitly disable request admission.
5. Runtime failure transition disables request admission.
6. Runtime STOPPING transition disables request admission.
7. Successful Bootstrap startup enables request admission only after Runtime reaches READY.
8. Startup validation failure leaves request admission disabled.
9. Startup initialization failure leaves request admission disabled.
10. Startup plugin activation failure leaves request admission disabled.
11. Bootstrap disables request admission before managed shutdown begins.
12. Successful shutdown leaves request admission disabled.
13. Failed managed shutdown leaves request admission disabled.
14. Existing RFC-034, RFC-035 and RFC-036 lifecycle behavior remains compatible.

### Implementation Boundary

RFC-037 should modify only the minimum Runtime, Bootstrap orchestration and focused test surfaces required to establish request-admission state ownership and lifecycle coordination.

`Runtime` retains exclusive ownership of request-admission state.

`BootstrapManager` retains startup and shutdown orchestration ownership.

The future API hosting layer will enforce admission by reading Runtime state; RFC-037 SHALL NOT implement that hosting layer.

Do not introduce a second admission controller, middleware layer, traffic router, health subsystem or operational-workload manager.

Health verification, API enforcement, OPERATIONAL and DEGRADED transitions, traffic draining and request rejection response policy require separate architecture review.

### Next Exact Action

Commit the RFC-037 contract, then write failing focused Runtime request-admission tests before implementation.


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
