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

## RFC-041 — Operational Workload Entry Boundary Contract

### Status

Architecture review complete. Contract definition active.

### Objective

Establish one canonical production entry boundary for PlantMind operational workloads and integrate that boundary into the platform dependency graph before any future `READY` to `OPERATIONAL` transition is implemented.

### Architecture Findings

- `ApplicationFacade` is the current stable application-level entry point.
- Current code explicitly directs external interfaces to use `ApplicationFacade` rather than internal orchestration or reasoning services.
- `IntegrationGateway` isolates external-facing integration concerns from internal application architecture.
- `OrchestrationService` coordinates the PlantMind workflow.
- `WorkflowExecutor` performs concrete workflow execution.
- Enterprise Engines SHALL NOT become workload orchestration owners.
- Production API hosting currently exposes observation endpoints only and is not the operational workload execution boundary.
- `ApplicationFacade`, `IntegrationGateway`, `OrchestrationService` and `WorkflowExecutor` are not currently composed by `CompositionRoot`.
- Current optional constructors allow these components to construct downstream dependencies independently.
- No approved Runtime `READY` to `OPERATIONAL` transition exists.

### Contract Direction

The canonical workload path SHALL be:

External Interface

↓

`ApplicationFacade`

↓

`IntegrationGateway`

↓

`OrchestrationService`

↓

`WorkflowExecutor`

↓

Approved reasoning and presentation capabilities

`ApplicationFacade` SHALL be the canonical application-level operational workload entry boundary.

`IntegrationGateway` SHALL remain an integration-isolation boundary and SHALL NOT compete with `ApplicationFacade` as the platform application entry authority.

`OrchestrationService` SHALL remain responsible for workflow coordination.

`WorkflowExecutor` SHALL remain responsible for concrete workflow execution.

Enterprise Engines SHALL NOT own orchestration.

Production composition SHALL use one explicitly constructed dependency chain owned by `CompositionRoot`.

External production interfaces SHALL consume the composed `ApplicationFacade` rather than independently constructing internal workload services.

### Lifecycle Boundary

RFC-041 SHALL establish the operational workload entry boundary but SHALL NOT transition Runtime to `OPERATIONAL`.

Admission of a request, invocation of `ApplicationFacade`, workflow execution, or workflow completion SHALL NOT automatically modify Runtime lifecycle state under RFC-041.

A future Runtime operational-transition RFC may use the RFC-041 workload boundary as lifecycle evidence only after transition conditions and authority are separately approved.

### Expected Technical Scope

RFC-041 MAY modify production composition code to:

- construct the workload dependency chain explicitly;
- expose the composed `ApplicationFacade`;
- preserve one dependency graph from facade through workflow execution;
- prevent production composition from relying on independent implicit construction.

Existing backward-compatible constructors MAY remain where required by current tests and compatibility contracts.

### Non-Goals

RFC-041 SHALL NOT:

- add `Runtime.mark_operational()` or equivalent;
- transition Runtime to `OPERATIONAL`;
- implement `DEGRADED`;
- add `ServiceState.OPERATIONAL`;
- add production business API routes solely for testing;
- redesign reasoning or Enterprise Engines;
- duplicate orchestration responsibilities;
- introduce authentication, authorization, retry, recovery or traffic draining.

### Next Exact Action

Define and commit the RFC-041 contract before TDD or production implementation begins.

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
| RFC-040 | `376970e` | Platform operational semantics alignment contract |

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

RFC-040 verification:

- Contract commit: `63d75ec`
- Alignment commit: `376970e`
- Architecture decision: AD-026 — Platform Operational Semantics Alignment
- BOOT-001 aligned
- CAP-002 aligned
- CORE-002 aligned
- Production Python changes: none
- Full regression: 256 passed
- `git diff --check`: passed after EOF normalization
- Remote alignment push: verified

RFC-040 is complete.

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
