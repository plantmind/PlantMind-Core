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

## RFC-049 — Mandatory Capability Composition Contract

### Status

Contract defined. Ready for contract verification and commit.

### Objective

Establish the explicit composition-time boundary for mandatory-capability availability sources and mandatory-capability policy so deployment-approved capability configuration can flow into the existing `CapabilityAvailabilityObserver` and `MandatoryCapabilityCoverageEvaluator`, while preserving fail-closed defaults, existing ownership boundaries and Runtime lifecycle authority.

### Architectural Position

RFC-043 established capability availability observation.

RFC-044 established immutable mandatory-capability policy.

RFC-045 established deterministic fail-closed mandatory-capability coverage evaluation.

RFC-048 established Runtime as the sole authoritative operational-transition authority.

The remaining composition gap is that production `CompositionRoot` currently always creates:

- `CapabilityAvailabilityObserver(sources=())`;
- `MandatoryCapabilityPolicy` in `UNCONFIGURED` state with no requirements.

Therefore the default production composition remains correctly fail-closed, but deployment-approved capability sources and policy cannot yet be injected through the canonical composition boundary.

RFC-049 SHALL close only that composition gap.

### Composition Inputs

`CompositionRoot.build(...)` SHALL support explicit composition-time inputs for:

- capability availability sources;
- mandatory-capability policy.

The canonical input types SHALL remain the existing architecture types:

- `Sequence[CapabilityAvailabilitySource]`;
- `MandatoryCapabilityPolicy`.

RFC-049 SHALL NOT introduce duplicate configuration models for these responsibilities.

### Fail-Closed Defaults

When no capability availability sources are supplied:

- `CapabilityAvailabilityObserver` SHALL be composed with no sources.

When no mandatory-capability policy is supplied:

- Composition SHALL use the existing canonical fail-closed policy:
  - state `MandatoryCapabilityPolicyState.UNCONFIGURED`;
  - empty `required_capabilities`.

The default composition SHALL therefore remain unable to produce satisfied mandatory-capability coverage.

RFC-049 SHALL NOT weaken existing default fail-closed behavior.

### Explicit Policy Injection

When an explicit `MandatoryCapabilityPolicy` is supplied:

- the exact supplied policy instance SHALL be used;
- the same policy instance SHALL be exposed through `PlatformComposition`;
- the same policy instance SHALL be registered in `ServiceContainer`;
- the same policy instance SHALL be supplied to `MandatoryCapabilityCoverageEvaluator`.

CompositionRoot SHALL NOT copy, reconstruct, normalize or reinterpret the supplied policy.

Policy validation remains owned by `MandatoryCapabilityPolicy`.

### Explicit Availability Source Injection

When capability availability sources are supplied:

- they SHALL be passed to the existing `CapabilityAvailabilityObserver`;
- source ordering SHALL be preserved;
- source object identity SHALL be preserved;
- CompositionRoot SHALL NOT invoke the sources during composition;
- CompositionRoot SHALL NOT merge, deduplicate, prioritize or reinterpret sources.

Availability observation remains owned by `CapabilityAvailabilityObserver`.

### Missing Capability Sources

Composition SHALL NOT require every mandatory capability to have a corresponding source at build time.

A configured policy whose required capability has no observation source SHALL remain a valid composition.

Missing coverage remains the responsibility of `MandatoryCapabilityCoverageEvaluator`.

RFC-049 SHALL NOT convert missing source coverage into a composition-time exception.

### Duplicate Capability Sources

Composition SHALL NOT deduplicate multiple sources that report the same capability.

Multiple observations for one required capability remain subject to existing coverage semantics, including `ambiguous_capabilities`.

CompositionRoot SHALL NOT introduce source-priority or source-selection policy.

### Source Failure Semantics

CompositionRoot SHALL NOT probe or execute capability sources.

Source execution and exception containment remain owned by `CapabilityAvailabilityObserver`.

Existing source-failure behavior that produces `UNKNOWN` observations remains unchanged.

### Configuration Ownership Boundary

`ConfigurationProvider` SHALL NOT become the owner of mandatory-capability policy.

RFC-049 SHALL NOT parse mandatory-capability names from application configuration.

RFC-049 SHALL NOT allow CompositionRoot to invent deployment-specific capability identifiers.

Deployment-approved policy and source construction SHALL occur outside the core composition decision logic and be supplied explicitly through the composition boundary.

### Coverage Ownership Boundary

`MandatoryCapabilityCoverageEvaluator` remains the sole owner of coverage evaluation.

CompositionRoot SHALL NOT:

- evaluate capability coverage;
- classify observations;
- decide whether coverage is satisfied;
- inspect capability availability;
- perform operational-transition eligibility decisions.

The evaluator SHALL continue to consume the exact policy supplied by composition.

### Runtime Boundary

RFC-049 SHALL NOT modify Runtime lifecycle behavior.

RFC-049 SHALL NOT call:

`Runtime.request_operational(...)`

Composition of capability sources or policy SHALL NOT automatically cause any lifecycle transition.

Runtime remains the sole lifecycle-transition authority.

### Operational Transition Evidence Boundary

RFC-049 SHALL NOT construct `OperationalTransitionEvidence`.

RFC-049 SHALL NOT combine workload evidence with mandatory-capability coverage.

Operational-transition coordination remains a future architecture concern.

### Bootstrap Boundary

Bootstrap SHALL NOT observe mandatory capabilities as part of RFC-049.

Bootstrap SHALL NOT transition Runtime to `OPERATIONAL`.

Startup readiness semantics remain unchanged.

### Application and Workflow Boundary

`ApplicationFacade`, `IntegrationGateway`, `OrchestrationService` and `WorkflowExecutor` SHALL remain unchanged by RFC-049.

Capability composition SHALL NOT introduce hidden workload or lifecycle side effects.

### Health Boundary

`HealthCapability` remains read-only reporting.

RFC-049 SHALL NOT make Health the owner of capability observation, coverage policy or operational transition.

### Composition Identity Contract

For explicitly supplied dependencies, the canonical composition SHALL preserve one dependency graph.

The policy instance exposed by:

- `PlatformComposition.mandatory_capability_policy`;
- `ServiceContainer`;
- `MandatoryCapabilityCoverageEvaluator`;

SHALL be the same object identity.

The availability sources stored by the composed observer SHALL be the same supplied source objects in the same order.

RFC-049 SHALL NOT introduce duplicate policy or observer instances.

### Compatibility Factory

`build_platform_composition(...)` SHALL preserve its backward-compatible factory role.

Any new RFC-049 composition inputs supported by `CompositionRoot.build(...)` SHALL also be supported and forwarded by `build_platform_composition(...)`.

Existing callers that provide only plugin registrations or no arguments SHALL continue to work unchanged.

### No Deployment-Specific Capability Names

RFC-049 SHALL NOT add hard-coded capability names such as:

- PI System;
- DCS;
- CMMS;
- database;
- document repository;
- model runtime.

Core composition remains capability-name agnostic.

Deployment-specific capability selection belongs outside this RFC.

### Implementation Scope

RFC-049 MAY implement:

- optional capability-source input on `CompositionRoot.build(...)`;
- optional mandatory-capability-policy input on `CompositionRoot.build(...)`;
- preservation of existing fail-closed defaults;
- explicit dependency forwarding into `CapabilityAvailabilityObserver`;
- explicit policy forwarding into `MandatoryCapabilityCoverageEvaluator`;
- matching forwarding through `build_platform_composition(...)`;
- focused composition tests;
- impacted regression tests.

### Non-Goals

RFC-049 SHALL NOT:

- create concrete production capability sources;
- define deployment-specific mandatory capability names;
- parse capability policy from environment or configuration files;
- modify `ConfigurationProvider`;
- modify capability observation semantics;
- modify capability coverage semantics;
- introduce source priority;
- deduplicate availability sources;
- require complete source coverage at composition time;
- construct operational-transition evidence;
- create an operational-transition coordinator;
- call `Runtime.request_operational(...)`;
- automatically transition Runtime to `OPERATIONAL`;
- introduce evidence freshness or TTL;
- introduce `DEGRADED` behavior;
- introduce operational recovery.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- default composition still exposes an observer with no availability sources;
- default composition still exposes an `UNCONFIGURED` empty mandatory-capability policy;
- default mandatory-capability coverage remains `UNSATISFIED`;
- explicit availability sources are accepted by `CompositionRoot.build(...)`;
- explicit source ordering is preserved;
- explicit source object identity is preserved;
- sources are not invoked during composition;
- explicit mandatory-capability policy is accepted;
- exact supplied policy identity is exposed by `PlatformComposition`;
- exact supplied policy identity is registered in `ServiceContainer`;
- evaluator owns the exact supplied policy instance;
- configured policy with no matching source remains valid composition;
- duplicate capability sources remain preserved for evaluator ambiguity handling;
- source failures remain handled by `CapabilityAvailabilityObserver`;
- CompositionRoot does not evaluate coverage during build;
- composition does not call `Runtime.request_operational(...)`;
- composition does not construct `OperationalTransitionEvidence`;
- no deployment-specific capability identifiers are hard-coded;
- existing no-argument composition remains backward compatible;
- existing plugin-registration composition remains backward compatible;
- `build_platform_composition(...)` forwards RFC-049 inputs;
- no duplicate policy, observer or lifecycle authority is introduced.

### Next Exact Action

Verify and commit the RFC-049 contract before writing focused TDD tests or production Python.

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
| RFC-048 | `b714ceb` | Runtime operational transition contract |

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

RFC-048 verification:

- Contract commit: `ac1c625`
- Technical commit: `b714ceb`
- Architecture decision: AD-034
- Focused TDD suite: 18 passed
- Impacted regression: 93 passed
- Full regression: 362 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Guarded Runtime operational transition: introduced
- Public `mark_operational()` bypass: not introduced
- Runtime readiness after success: preserved
- Request admission after success: preserved
- Rejected transition mutation: none
- Bootstrap automatic operational transition: not introduced
- Workload-triggered lifecycle transition: not introduced
- Independent operational-eligibility authority: not introduced

RFC-048 is technically complete.

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
