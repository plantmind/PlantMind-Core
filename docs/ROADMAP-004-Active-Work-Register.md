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

## RFC-046 — Operational Workload Evidence Contract

### Status

Contract defined. Ready for contract verification and commit.

### Objective

Establish a trusted correlated operational-workload evidence boundary proving that one workload entered through the canonical `ApplicationFacade` and reached concrete execution start through `WorkflowExecutor`, without introducing operational-eligibility decisions or Runtime lifecycle-transition authority.

### Architectural Position

RFC-042 requires trustworthy evidence that:

- a workload entered through the canonical `ApplicationFacade`;
- the same workload reached concrete execution start through `WorkflowExecutor`.

RFC-045 separately established mandatory-capability coverage evidence.

RFC-046 SHALL establish the missing correlated workload-evidence boundary.

RFC-046 SHALL NOT combine workload evidence with mandatory-capability coverage or decide whether Runtime may become `OPERATIONAL`.

### Workload Identity

Each canonical `ApplicationFacade.analyze()` invocation SHALL create exactly one workload identity.

The workload identity SHALL:

- use `UUID`;
- be generated once at the canonical facade boundary;
- remain unchanged throughout that workload execution path;
- correlate facade-entry evidence with workflow-execution-start evidence;
- not be reused intentionally across separate facade invocations.

`IntegrationGateway`, `OrchestrationService` and `WorkflowExecutor` SHALL NOT replace or regenerate an existing workload identity.

### Application Facade Entry Evidence

RFC-046 SHALL introduce immutable:

`ApplicationFacadeEntryEvidence`

with:

`workload_id: UUID`

The evidence SHALL use `@dataclass(frozen=True, slots=True)`.

`ApplicationFacade` SHALL be the production owner responsible for originating canonical facade-entry evidence.

Creating facade-entry evidence SHALL NOT modify Runtime, request admission, availability, mandatory policy or capability coverage.

### Workflow Execution Start Evidence

RFC-046 SHALL introduce immutable:

`WorkflowExecutionStartEvidence`

with:

`workload_id: UUID`

The evidence SHALL use `@dataclass(frozen=True, slots=True)`.

`WorkflowExecutor` SHALL create workflow-execution-start evidence only when a canonical facade-entry evidence object has been propagated to it.

The execution-start evidence SHALL use the exact same workload identity as the propagated facade-entry evidence.

Execution-start evidence SHALL be established immediately before concrete workflow execution proceeds into the existing reasoning/presentation operation.

### Correlated Operational Workload Evidence

RFC-046 SHALL introduce immutable:

`OperationalWorkloadEvidence`

with:

- `facade_entry: ApplicationFacadeEntryEvidence`
- `execution_start: WorkflowExecutionStartEvidence`

The evidence SHALL use `@dataclass(frozen=True, slots=True)`.

Construction SHALL fail if the two evidence objects contain different workload identities.

Matching workload identity proves correlation between the two evidence categories.

The evidence SHALL contain no lifecycle state and no operational-eligibility decision.

### Evidence Propagation

The canonical evidence path SHALL be:

`ApplicationFacade`
→ `IntegrationGateway`
→ `OrchestrationService`
→ `WorkflowExecutor`

`ApplicationFacade` SHALL originate the facade-entry evidence.

`IntegrationGateway` SHALL forward supplied facade-entry evidence unchanged.

`OrchestrationService` SHALL forward supplied facade-entry evidence unchanged.

`WorkflowExecutor` SHALL consume the propagated facade-entry evidence and produce correlated execution-start evidence.

Intermediate layers SHALL NOT:

- originate canonical facade-entry evidence;
- replace the workload identity;
- regenerate workload identity;
- create lifecycle-transition decisions.

### Workflow Execution Exposure

`WorkflowExecution` SHALL expose:

`operational_workload_evidence: OperationalWorkloadEvidence | None = None`

The field SHALL remain optional to preserve existing construction and non-canonical internal execution paths.

Existing `WorkflowExecution.result`, `WorkflowExecution.stages` and `WorkflowExecution.is_complete` semantics SHALL remain unchanged.

A workflow reached through the canonical `ApplicationFacade` SHALL return correlated operational-workload evidence when execution completes successfully.

A workflow executed without propagated facade-entry evidence SHALL NOT fabricate canonical operational-workload evidence.

### Direct Internal Invocation Boundary

Direct calls to:

- `IntegrationGateway.execute()`;
- `OrchestrationService.run()`;
- `WorkflowExecutor.execute()`;

without facade-entry evidence SHALL remain supported for existing internal and focused-test use.

Such calls SHALL produce no `OperationalWorkloadEvidence`.

Absence of canonical facade-entry evidence SHALL fail closed.

Internal execution alone SHALL NOT be interpreted as proof that the workload entered through `ApplicationFacade`.

### Failure Boundary

RFC-046 SHALL NOT introduce a persistent or global evidence recorder.

If workflow execution raises before a `WorkflowExecution` result is returned, RFC-046 SHALL NOT expose fabricated completed correlated evidence to the caller.

Partial in-flight evidence persistence, failure-event recording and historical workload tracing remain outside RFC-046.

### Trust Boundary

RFC-046 defines trusted in-process architectural provenance.

Production trust derives from the canonical composed call path and ownership boundaries.

RFC-046 SHALL NOT introduce:

- cryptographic attestation;
- cross-process evidence signing;
- distributed trace authentication;
- external identity verification.

Those concerns require separate architecture contracts if needed.

### Capability Coverage Boundary

RFC-046 SHALL NOT modify or duplicate:

- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityPolicy`;
- `MandatoryCapabilityCoverageEvaluator`;
- `MandatoryCapabilityCoverageResult`.

Operational workload evidence and mandatory-capability coverage remain independent evidence categories.

RFC-046 SHALL NOT combine them into an operational-eligibility result.

### Runtime Boundary

Runtime remains the sole authoritative owner of platform lifecycle state.

RFC-046 SHALL NOT:

- modify Runtime lifecycle state;
- modify request-admission state;
- add `Runtime.mark_operational()`;
- add `Runtime.request_operational()`;
- transition Runtime from `READY` to `OPERATIONAL`;
- introduce `DEGRADED` behavior.

Operational workload evidence SHALL be evidence only.

It SHALL NOT authorize or execute a lifecycle transition.

### Composition Boundary

RFC-046 SHALL preserve the canonical production chain owned by `CompositionRoot`:

`ApplicationFacade`
→ `IntegrationGateway`
→ `OrchestrationService`
→ `WorkflowExecutor`

RFC-046 SHALL NOT introduce a second application facade, gateway, orchestration service or workflow executor.

No global mutable workload-evidence registry SHALL be added to `CompositionRoot`.

### Implementation Scope

RFC-046 MAY implement:

- immutable workload evidence types;
- UUID workload correlation;
- facade-entry evidence creation;
- transparent evidence propagation through the existing canonical workload path;
- workflow-execution-start evidence creation;
- correlated evidence validation;
- optional evidence exposure through `WorkflowExecution`;
- focused contract and regression tests.

### Non-Goals

RFC-046 SHALL NOT:

- implement operational eligibility evaluation;
- combine workload evidence with mandatory-capability coverage;
- implement Runtime `READY` to `OPERATIONAL`;
- add lifecycle-transition authority outside Runtime;
- modify request admission;
- introduce workload evidence timestamps or freshness semantics;
- introduce a global or persistent evidence recorder;
- introduce multi-process or cryptographic attestation;
- change workflow completion semantics;
- require direct internal execution paths to fabricate facade-entry evidence;
- implement retry, recovery, traffic draining, authentication or authorization.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- evidence models are immutable;
- workload identity uses `UUID`;
- mismatched facade-entry and execution-start identities are rejected;
- one canonical facade invocation produces correlated workload evidence;
- facade-entry and execution-start evidence share exactly one workload identity;
- separate canonical facade invocations receive distinct workload identities;
- `IntegrationGateway` forwards supplied facade-entry evidence unchanged;
- `OrchestrationService` forwards supplied facade-entry evidence unchanged;
- `WorkflowExecutor` creates execution-start evidence from the propagated workload identity;
- direct gateway execution without facade-entry evidence does not fabricate operational-workload evidence;
- direct orchestration execution without facade-entry evidence does not fabricate operational-workload evidence;
- direct workflow execution without facade-entry evidence does not fabricate operational-workload evidence;
- existing `WorkflowExecution` construction without operational evidence remains valid;
- existing workflow completion semantics remain unchanged;
- operational-workload evidence does not modify Runtime lifecycle state;
- operational-workload evidence does not modify request admission;
- workload evidence does not modify availability observation, mandatory policy or mandatory-capability coverage;
- no Runtime operational transition is introduced.

### Next Exact Action

Verify and commit the RFC-046 contract before writing focused TDD tests or production Python.

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
