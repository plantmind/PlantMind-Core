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

## RFC-048 — Runtime Operational Transition Contract

### Status

Contract defined. Ready for contract verification and commit.

### Objective

Establish the authoritative fail-closed Runtime `READY` to `OPERATIONAL` transition boundary in which Runtime directly validates its own lifecycle state and request-admission state together with complete external `OperationalTransitionEvidence`, while preserving Runtime as the sole lifecycle-transition authority.

### Architectural Position

AD-028 established that Runtime alone owns final lifecycle-transition authority.

RFC-047 established immutable external `OperationalTransitionEvidence`.

Runtime-owned preconditions remain:

- lifecycle state is `READY`;
- request admission is enabled.

External evidence completeness remains represented by:

`OperationalTransitionEvidence.is_complete`

RFC-048 SHALL combine those conditions only inside Runtime.

No independent operational-eligibility service or lifecycle decision authority SHALL be introduced.

### Authoritative Transition Operation

RFC-048 SHALL introduce one guarded Runtime operation:

`request_operational(evidence: OperationalTransitionEvidence) -> None`

This SHALL be the only approved public operation for entering `RuntimeState.OPERATIONAL`.

RFC-048 SHALL NOT introduce a public:

`mark_operational()`

or another unguarded operational-state mutation method.

### Required Preconditions

`Runtime.request_operational()` SHALL transition Runtime to `OPERATIONAL` only when all of the following are true:

- current Runtime state is exactly `RuntimeState.READY`;
- request admission is enabled;
- supplied `OperationalTransitionEvidence.is_complete` is `True`.

All conditions are mandatory.

Runtime SHALL evaluate its own lifecycle state directly.

Runtime SHALL evaluate its own request-admission state directly.

Runtime SHALL consume external evidence completeness without accepting duplicated external attestations of Runtime-owned state.

### Successful Transition Semantics

When all required preconditions are satisfied:

- Runtime state SHALL become `RuntimeState.OPERATIONAL`;
- Runtime readiness SHALL remain `True`;
- request admission SHALL remain enabled;
- supplied evidence SHALL not be mutated;
- no additional lifecycle state SHALL be entered.

The transition SHALL represent:

`READY` → `OPERATIONAL`

only.

### Failure-Closed Transition Semantics

If any required precondition is not satisfied, `request_operational()` SHALL raise `RuntimeError`.

Failure SHALL be atomic.

On rejection:

- Runtime lifecycle state SHALL remain unchanged;
- Runtime readiness SHALL remain unchanged;
- request-admission state SHALL remain unchanged;
- supplied evidence SHALL remain unchanged.

RFC-048 SHALL NOT partially transition Runtime.

### Invalid Lifecycle State

Operational transition SHALL be rejected unless current Runtime state is exactly `READY`.

Requests from any other lifecycle state SHALL fail closed, including:

- `CREATED`;
- `BOOTSTRAPPING`;
- `INITIALIZING`;
- `OPERATIONAL`;
- `DEGRADED`;
- `STOPPING`;
- `STOPPED`;
- `FAILED`.

RFC-048 SHALL NOT interpret an already `OPERATIONAL` Runtime as another successful `READY` to `OPERATIONAL` transition.

Repeated operational-transition requests after successful transition therefore SHALL be rejected.

### Request Admission Boundary

Request admission is a Runtime-owned operational-transition precondition.

If request admission is disabled while Runtime is `READY`, operational transition SHALL be rejected.

RFC-048 SHALL NOT automatically enable request admission.

RFC-048 SHALL NOT automatically disable request admission when an operational-transition request is rejected.

Admission-control policy remains distinct from transition rejection.

### External Evidence Boundary

Runtime SHALL require supplied `OperationalTransitionEvidence`.

External evidence SHALL be accepted only through its existing derived:

`is_complete`

contract.

Runtime SHALL NOT:

- reconstruct operational-workload evidence;
- inspect workload UUID correlation independently;
- collect capability-availability observations;
- evaluate mandatory-capability policy;
- reevaluate mandatory-capability coverage;
- mutate external evidence.

Those responsibilities remain owned by RFC-043 through RFC-047 boundaries.

### Evidence Incompleteness

When `OperationalTransitionEvidence.is_complete` is `False`, transition SHALL be rejected.

Incomplete evidence SHALL NOT cause Runtime to:

- become `OPERATIONAL`;
- become `FAILED`;
- become `STOPPED`;
- become `DEGRADED`;
- disable request admission;
- modify readiness.

Evidence incompleteness means only that the requested operational transition is not currently permitted.

### Atomicity Boundary

Runtime SHALL validate all required transition conditions before mutating lifecycle state.

No successful-state mutation SHALL occur before all checks pass.

A rejected transition SHALL leave Runtime observably equivalent to its pre-request lifecycle, readiness and admission state.

### Runtime Readiness Semantics

`OPERATIONAL` SHALL remain a ready runtime condition.

After successful transition:

- `Runtime.state` SHALL be `RuntimeState.OPERATIONAL`;
- `Runtime.is_ready` SHALL remain `True`;
- the existing readiness boolean SHALL not be reset.

RFC-048 SHALL NOT redefine startup readiness semantics.

### Existing Lifecycle Operations

Existing Runtime operations SHALL retain their current responsibilities:

- `request_readiness()`;
- `mark_ready()`;
- `mark_not_ready()`;
- `mark_stopping()`;
- `mark_failed()`;
- request-admission enablement;
- request-admission disablement.

RFC-048 SHALL NOT redesign existing startup, stopping or failure behavior.

Existing `mark_stopping()` and `mark_failed()` admission-disabling behavior SHALL remain unchanged.

### Runtime Status

Existing Runtime status reporting SHALL naturally expose `operational` through the existing lifecycle-state value after successful transition.

RFC-048 SHALL NOT introduce a second operational-status flag.

`RuntimeState.OPERATIONAL` remains the authoritative operational lifecycle representation.

### Composition Boundary

RFC-048 requires no new lifecycle authority in `CompositionRoot`.

The existing composed Runtime instance remains the lifecycle authority.

`CompositionRoot` SHALL NOT construct or register:

- an operational-transition manager;
- an operational-eligibility decision service;
- a competing Runtime lifecycle controller.

### Bootstrap Boundary

Bootstrap remains responsible for startup through readiness and request-admission enablement.

RFC-048 SHALL NOT make Bootstrap automatically transition Runtime to `OPERATIONAL`.

Operational transition requires explicit Runtime invocation with approved external evidence after the required operational evidence exists.

### Application and Workflow Boundary

`ApplicationFacade`, `IntegrationGateway`, `OrchestrationService` and `WorkflowExecutor` SHALL NOT call Runtime lifecycle-transition operations as part of RFC-048.

They remain evidence-producing or workload-execution boundaries only.

RFC-048 SHALL NOT create hidden lifecycle side effects during workload execution.

### Health Boundary

`HealthCapability` remains read-only reporting.

RFC-048 SHALL NOT allow Health to request, authorize or execute Runtime lifecycle transitions.

### No Independent Eligibility State

RFC-048 SHALL NOT introduce:

- `OperationalEligibilityState`;
- an operational-eligibility evaluator;
- a second operational readiness boolean;
- duplicated lifecycle decision state.

The authoritative result of successful evaluation is the Runtime lifecycle transition itself.

### Implementation Scope

RFC-048 MAY implement:

- `Runtime.request_operational()`;
- guarded `READY` to `OPERATIONAL` transition;
- direct Runtime-owned lifecycle-state validation;
- direct Runtime-owned request-admission validation;
- external evidence completeness validation;
- atomic fail-closed rejection;
- preservation of readiness and admission semantics;
- focused Runtime transition tests;
- impacted regression tests.

### Non-Goals

RFC-048 SHALL NOT:

- introduce a public `mark_operational()`;
- introduce an independent operational-eligibility service;
- modify `OperationalTransitionEvidence`;
- modify workload-evidence generation;
- modify mandatory-capability coverage evaluation;
- collect availability observations;
- automatically transition during Bootstrap;
- automatically transition during workload execution;
- introduce `DEGRADED` behavior;
- introduce `ServiceState.OPERATIONAL`;
- implement operational recovery;
- implement transition retry;
- implement evidence freshness or TTL;
- implement traffic draining;
- implement authentication or authorization.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- Runtime initially has no operational state transition;
- complete external evidence alone cannot transition a non-`READY` Runtime;
- `READY` alone cannot transition when request admission is disabled;
- `READY` plus request admission cannot transition with incomplete external evidence;
- `READY` plus enabled request admission plus complete external evidence transitions to `OPERATIONAL`;
- successful transition preserves `is_ready == True`;
- successful transition preserves enabled request admission;
- supplied external evidence is not mutated;
- rejected transition raises `RuntimeError`;
- rejected transition preserves lifecycle state;
- rejected transition preserves readiness;
- rejected transition preserves request admission;
- transition from `CREATED` is rejected;
- transition from `OPERATIONAL` is rejected;
- transition from `STOPPING` is rejected;
- transition from `STOPPED` is rejected;
- transition from `FAILED` is rejected;
- repeated operational-transition request is rejected;
- no public `mark_operational()` bypass is introduced;
- Runtime status reports `operational` after successful transition;
- Bootstrap does not automatically transition Runtime to `OPERATIONAL`;
- canonical workload execution does not automatically transition Runtime to `OPERATIONAL`;
- Health does not become lifecycle-transition authority;
- no independent operational-eligibility service is introduced through `CompositionRoot`.

### Next Exact Action

Verify and commit the RFC-048 contract before writing focused TDD tests or production Python.

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
| RFC-042 | `3168014` | Runtime operational transition evidence contract |
| RFC-043 | `ed807f0` | Mandatory capability availability observation contract |
| RFC-044 | `a709c0d` | Mandatory capability policy contract |
| RFC-045 | `0b410ce` | Mandatory capability coverage evaluation contract |
| RFC-046 | `6aca0a1` | Operational workload evidence contract |
| RFC-047 | `ebc4769` | Operational transition evidence aggregation contract |

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

RFC-042 verification:

- Contract commit: `3168014`
- Architecture decision: AD-028
- Production Python changes: none
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced
- Full regression baseline remains: 263 passed
- Blocking dependency identified: trusted mandatory-capability availability observation

RFC-042 is complete.

RFC-043 verification:

- Contract commit: `0d30cfb`
- Technical commit: `ed807f0`
- Architecture decision: AD-029
- Focused TDD suite: 15 passed
- Impacted regression: 40 passed
- Full regression: 278 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Production capability sources: none
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-043 is technically complete.

RFC-044 verification:

- Contract commit: `91c6090`
- Technical commit: `a709c0d`
- Architecture decision: AD-030
- Focused TDD suite: 15 passed
- Impacted regression: 55 passed
- Full regression: 293 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Production mandatory-capability policy: `UNCONFIGURED`
- Fabricated mandatory capabilities: none
- Policy-to-availability coverage evaluator: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-044 is technically complete.

RFC-045 verification:

- Contract commit: `9abde19`
- Technical commit: `0b410ce`
- Architecture decision: AD-031
- Focused TDD suite: 16 passed
- Impacted regression: 71 passed
- Full regression: 309 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Multi-source aggregation: not introduced
- Freshness policy: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-045 is technically complete.

RFC-046 verification:

- Contract commit: `2365b68`
- Technical commit: `6aca0a1`
- Architecture decision: AD-032
- Focused TDD suite: 18 passed
- Impacted regression: 32 passed
- Full regression: 327 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Workload correlation: UUID
- Canonical facade-entry evidence: introduced
- Workflow-execution-start evidence: introduced
- Persistent/global evidence recorder: not introduced
- Operational eligibility: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-046 is technically complete.

RFC-047 verification:

- Contract commit: `35004dc`
- Technical commit: `ebc4769`
- Architecture decision: AD-033
- Focused TDD suite: 17 passed
- Impacted regression: 56 passed
- Full regression: 344 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- External evidence aggregation: introduced
- Runtime-owned preconditions: excluded from aggregate
- Operational eligibility: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-047 is technically complete.

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
