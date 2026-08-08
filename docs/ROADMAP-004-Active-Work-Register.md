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

## RFC-047 — Operational Transition Evidence Aggregation Contract

### Status

Contract defined. Ready for contract verification and commit.

### Objective

Establish an immutable fail-closed external operational-transition evidence aggregate that combines trusted correlated `OperationalWorkloadEvidence` with `MandatoryCapabilityCoverageResult` while excluding Runtime-owned lifecycle state and request-admission state and without introducing lifecycle-transition authority.

### Architectural Position

AD-028 requires operational-transition evaluation to distinguish:

- Runtime-owned preconditions;
- externally supplied operational evidence.

Runtime-owned preconditions are:

- Runtime lifecycle state is `READY`;
- request admission is enabled.

These SHALL remain directly owned and evaluated by Runtime.

RFC-045 established trusted mandatory-capability coverage evidence.

RFC-046 established trusted correlated operational-workload evidence.

RFC-047 SHALL aggregate those external evidence categories only.

RFC-047 SHALL NOT evaluate Runtime-owned preconditions and SHALL NOT decide whether Runtime may transition to `OPERATIONAL`.

### Operational Transition Evidence

RFC-047 SHALL introduce immutable:

`OperationalTransitionEvidence`

with:

- `operational_workload: OperationalWorkloadEvidence | None`
- `mandatory_capability_coverage: MandatoryCapabilityCoverageResult | None`

The model SHALL use `@dataclass(frozen=True, slots=True)`.

Both fields SHALL remain optional so incomplete external evidence can be represented explicitly and evaluated fail closed.

### External Evidence Completeness

`OperationalTransitionEvidence` SHALL expose:

`is_complete: bool`

as a derived read-only property.

`is_complete` SHALL be `True` only when:

- `operational_workload` is present;
- `mandatory_capability_coverage` is present;
- `mandatory_capability_coverage.state` is `MandatoryCapabilityCoverageState.SATISFIED`.

Otherwise `is_complete` SHALL be `False`.

The property SHALL NOT inspect Runtime state.

The property SHALL NOT inspect request admission.

The property SHALL NOT represent final operational eligibility.

It represents completeness of externally supplied operational-transition evidence only.

### Workload Evidence Boundary

When `operational_workload` is present, RFC-047 SHALL consume the existing validated `OperationalWorkloadEvidence`.

RFC-047 SHALL NOT:

- reconstruct facade-entry evidence;
- reconstruct workflow-execution-start evidence;
- generate workload identity;
- replace workload identity;
- perform additional workload correlation;
- fabricate canonical workload provenance.

Correlation validation remains owned by `OperationalWorkloadEvidence`.

Absence of operational-workload evidence SHALL cause external evidence completeness to fail closed.

### Mandatory Capability Coverage Boundary

When `mandatory_capability_coverage` is present, RFC-047 SHALL consume the existing `MandatoryCapabilityCoverageResult`.

RFC-047 SHALL NOT:

- observe capability availability;
- construct mandatory policy;
- evaluate capability observations;
- reclassify missing capabilities;
- reclassify unavailable capabilities;
- reclassify unknown capabilities;
- resolve ambiguous capability observations.

Those responsibilities remain owned by RFC-043, RFC-044 and RFC-045 boundaries.

Only a coverage result whose state is `SATISFIED` SHALL satisfy the mandatory-capability portion of external transition evidence.

`UNSATISFIED` coverage SHALL fail closed.

Absence of capability-coverage evidence SHALL fail closed.

### Runtime-Owned Preconditions Exclusion

`OperationalTransitionEvidence` SHALL NOT contain:

- Runtime lifecycle state;
- Runtime readiness state;
- request-admission state;
- duplicated booleans representing Runtime-owned preconditions;
- external attestations that Runtime is ready;
- external attestations that request admission is enabled.

Runtime SHALL continue to evaluate its own state directly.

External evidence SHALL NOT attest Runtime-owned state on Runtime behalf.

### Lifecycle Authority Boundary

RFC-047 SHALL NOT introduce lifecycle-transition authority.

`OperationalTransitionEvidence.is_complete` SHALL NOT:

- transition Runtime;
- authorize Runtime transition by itself;
- call Runtime;
- modify Runtime;
- modify request admission.

A complete external evidence aggregate remains evidence only.

Final transition authority remains exclusively with Runtime.

### Evidence Ownership

RFC-047 SHALL NOT introduce a global mutable evidence collector or recorder.

The aggregate SHALL be constructed explicitly from already produced evidence objects.

RFC-047 SHALL NOT discover, fetch or generate its dependencies implicitly.

This preserves explicit dependency flow and prevents hidden evidence sources.

### Immutability and Identity

RFC-047 SHALL preserve the exact evidence objects supplied to the aggregate.

It SHALL NOT copy, normalize, replace or mutate:

- `OperationalWorkloadEvidence`;
- `MandatoryCapabilityCoverageResult`.

The aggregate SHALL therefore preserve evidence identity and provenance.

### Determinism

For the same supplied evidence objects, `is_complete` SHALL always produce the same result.

RFC-047 SHALL NOT introduce:

- current-time checks;
- evidence freshness;
- TTL;
- retry;
- source priority;
- external I/O;
- probing;
- mutable internal state.

### Failure-Closed Semantics

The following SHALL produce `is_complete == False`:

- both evidence categories absent;
- workload evidence absent;
- mandatory-capability coverage absent;
- mandatory-capability coverage state `UNSATISFIED`.

The aggregate SHALL never infer missing evidence from unrelated platform state.

### Composition Boundary

RFC-047 does not require `CompositionRoot` to own or register a persistent aggregate instance.

`OperationalTransitionEvidence` represents per-evaluation evidence and SHALL be created explicitly when evidence needs to cross into a future Runtime operational-transition evaluation boundary.

`CompositionRoot` SHALL NOT maintain a mutable global operational-transition evidence object.

### Relationship to Future Runtime Transition

A future separately approved RFC MAY allow Runtime to consume:

- `OperationalTransitionEvidence`;
- Runtime-owned lifecycle state;
- Runtime-owned request-admission state.

That future Runtime contract SHALL independently validate its own preconditions.

RFC-047 SHALL NOT implement that future operation.

No `mark_operational()`, `request_operational()` or equivalent method is introduced by RFC-047.

### Implementation Scope

RFC-047 MAY implement:

- immutable `OperationalTransitionEvidence`;
- optional external evidence fields;
- deterministic derived `is_complete`;
- fail-closed completeness semantics;
- focused contract tests.

### Non-Goals

RFC-047 SHALL NOT:

- implement operational lifecycle transition;
- implement final operational eligibility;
- add `Runtime.mark_operational()`;
- add `Runtime.request_operational()`;
- inspect Runtime state;
- inspect request-admission state;
- duplicate Runtime-owned preconditions;
- modify Runtime;
- modify request admission;
- collect availability observations;
- evaluate mandatory-capability coverage;
- create operational-workload evidence;
- introduce evidence freshness or TTL;
- introduce persistent evidence storage;
- introduce global mutable evidence state;
- introduce `DEGRADED`;
- introduce `ServiceState.OPERATIONAL`;
- implement retry, recovery, traffic draining, authentication or authorization.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- `OperationalTransitionEvidence` is immutable;
- existing evidence objects are preserved by identity;
- both evidence categories absent fails closed;
- missing operational-workload evidence fails closed;
- missing mandatory-capability coverage fails closed;
- `UNSATISFIED` mandatory-capability coverage fails closed;
- present correlated operational-workload evidence plus `SATISFIED` mandatory-capability coverage produces complete external evidence;
- completeness is deterministic;
- completeness does not inspect or depend on Runtime lifecycle state;
- completeness does not inspect or depend on request-admission state;
- aggregate construction does not mutate operational-workload evidence;
- aggregate construction does not mutate mandatory-capability coverage;
- no availability observation occurs;
- no capability-coverage evaluation occurs;
- no Runtime lifecycle transition occurs;
- no Runtime operational-transition API is introduced;
- no global or persistent evidence aggregate is introduced through `CompositionRoot`.

### Next Exact Action

Verify and commit the RFC-047 contract before writing focused TDD tests or production Python.

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
