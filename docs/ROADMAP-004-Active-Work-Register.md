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

## RFC-042 — Runtime Operational Transition Evidence Contract

### Status

Contract defined. Evidence-source gap identified.

### Objective

Define the trusted evidence and ownership boundaries required before Runtime may support a future `READY` to `OPERATIONAL` lifecycle transition.

### Runtime-Owned Preconditions

Runtime SHALL evaluate its own lifecycle prerequisites directly.

The following SHALL NOT be duplicated as externally supplied operational evidence:

- current Runtime lifecycle state;
- current request-admission state.

A future operational transition SHALL require Runtime itself to verify:

- current lifecycle state is `READY`;
- request admission is enabled.

External components SHALL NOT attest Runtime-owned state on Runtime behalf.

### Operational Evidence

Operational-transition evidence SHALL represent independently observable facts that Runtime does not own directly.

The required evidence categories are:

#### Canonical Workload Boundary Entry

An approved operational workload has entered through the composed `ApplicationFacade` boundary established by RFC-041.

Only execution through the approved production workload path may satisfy this evidence category.

Direct invocation of internal orchestration, reasoning or engine components SHALL NOT satisfy the canonical workload-entry requirement.

#### Concrete Workflow Execution Start

The approved workload has progressed beyond application entry and concrete workflow execution has begun through the composed `WorkflowExecutor`.

Application entry alone SHALL NOT be interpreted as proof that operational execution started.

Workflow completion SHALL NOT be required merely to establish execution start.

#### Mandatory Capability Availability

Mandatory capabilities required for safe operational workload execution remain available at the time operational eligibility is evaluated.

Registration alone SHALL NOT prove availability.

Startup-time validation alone SHALL NOT prove continuing availability.

### Evidence Producers

Evidence production SHALL remain separate from lifecycle decision authority.

`ApplicationFacade` MAY provide evidence that the canonical application workload boundary was entered.

`WorkflowExecutor` MAY provide evidence that concrete workflow execution started.

Neither component SHALL modify Runtime lifecycle state.

Mandatory capability availability SHALL be supplied only by an approved read-only availability observation contract.

No trustworthy mandatory-capability availability producer currently exists in the committed platform.

`ServiceRegistry` registration, service count, startup readiness evidence and current `HealthCapability` reporting SHALL NOT be treated as substitutes for live mandatory-capability availability.

### Runtime Authority

Runtime remains the sole authoritative owner of lifecycle state.

Evidence SHALL inform a future Runtime decision but SHALL NOT itself cause a lifecycle transition.

A future Runtime operational-transition operation SHALL validate:

- Runtime-owned preconditions;
- trusted workload-boundary evidence;
- trusted workflow-execution evidence;
- trusted mandatory-capability availability evidence.

### Current Architecture Gap

The platform does not currently implement a trustworthy source for mandatory-capability availability.

RFC-042 SHALL record this as a blocking prerequisite for any future `READY` to `OPERATIONAL` implementation.

The platform SHALL NOT implement the operational transition by fabricating, assuming or hard-coding capability availability.

### Implementation Classification

RFC-042 is an architecture and evidence contract.

RFC-042 SHALL NOT introduce production transition behavior.

No production Python implementation is authorized solely to simulate unavailable evidence.

### Non-Goals

RFC-042 SHALL NOT:

- add `Runtime.mark_operational()`, `request_operational()` or equivalent;
- transition Runtime to `OPERATIONAL`;
- duplicate Runtime readiness or request-admission state inside externally supplied evidence;
- treat service registration as service availability;
- treat startup readiness as continuing operational availability;
- make HealthCapability a lifecycle authority;
- make ApplicationFacade or WorkflowExecutor lifecycle authorities;
- add `ServiceState.OPERATIONAL`;
- implement `DEGRADED`;
- implement traffic draining, retry or recovery;
- introduce authentication or authorization behavior.

### Future Dependency

Before a Runtime operational-transition implementation can be approved, PlantMind requires an architecture-controlled capability-availability observation contract.

That future capability SHALL remain read-only and SHALL provide trustworthy evidence without becoming a lifecycle decision owner.

### Next Exact Action

Validate and commit the RFC-042 evidence contract before selecting the architecture work required to provide trusted mandatory-capability availability evidence.

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
| RFC-041 | `1693a9b` | Operational workload entry boundary contract |

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

RFC-041 verification:

- Contract commit: `6a49e92`
- Technical commit: `1693a9b`
- Focused TDD suite: 7 passed
- Impacted regression: 41 passed
- Full regression: 263 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Runtime lifecycle transition behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-041 is technically complete.

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
