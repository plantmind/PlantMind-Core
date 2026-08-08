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

## RFC-043 — Mandatory Capability Availability Observation Contract

### Status

Contract defined. Ready for contract verification and commit.

### Objective

Establish a trustworthy read-only observation boundary for live PlantMind capability availability without introducing lifecycle decision authority or fabricated production probes.

### Availability State Contract

RFC-043 SHALL introduce:

`CapabilityAvailabilityState`

with exactly these states:

- `AVAILABLE`
- `UNAVAILABLE`
- `UNKNOWN`

`AVAILABLE` means the trusted source successfully established current capability availability.

`UNAVAILABLE` means the trusted source successfully established that the capability is not currently available.

`UNKNOWN` means current availability cannot be established with trustworthy evidence.

`UNKNOWN` SHALL include observation failure or inability to determine current availability.

`UNKNOWN` SHALL NOT be treated as `AVAILABLE`.

Availability SHALL NOT be represented by an ambiguous boolean-only contract.

### Immutable Observation Contract

RFC-043 SHALL introduce an immutable:

`CapabilityAvailabilityObservation`

with these fields:

- `capability_name: str`
- `state: CapabilityAvailabilityState`
- `observed_at: datetime`
- `source_name: str`

The observation SHALL use `@dataclass(frozen=True)`.

`capability_name` SHALL identify the observed capability.

`source_name` SHALL identify the trusted source responsible for the observation.

Both identifiers SHALL be non-empty.

`observed_at` SHALL require timezone-aware datetime information.

Accepted observation timestamps SHALL be normalized to UTC.

Naive datetimes SHALL be rejected.

An observation SHALL report evidence only and SHALL contain no lifecycle-transition authority.

### Trusted Source Contract

RFC-043 SHALL introduce an abstract:

`CapabilityAvailabilitySource`

The source contract SHALL expose:

- `capability_name`
- `source_name`
- `observe() -> CapabilityAvailabilityObservation`

Core availability-source contracts SHALL follow the existing PlantMind abstract-base-class pattern.

A source SHALL observe one explicitly identified capability.

A source SHALL NOT declare whether its capability is mandatory.

A source SHALL NOT modify Runtime lifecycle state.

A source SHALL NOT modify request-admission state.

A source SHALL NOT depend on `HealthCapability` for lifecycle decisions.

Production sources SHALL represent real approved observation mechanisms only.

RFC-043 SHALL NOT introduce fabricated production sources for capabilities that do not yet expose trustworthy probes.

### Observer Contract

RFC-043 SHALL introduce:

`CapabilityAvailabilityObserver`

The observer SHALL be a read-only coordinator over explicitly supplied trusted `CapabilityAvailabilitySource` instances.

The observer SHALL NOT introduce:

- automatic discovery;
- package scanning;
- a second service registry;
- inferred mandatory-capability membership.

Production source composition SHALL remain owned by `CompositionRoot`.

The observer SHALL produce immutable capability availability observations from its composed sources.

Observation ordering SHALL be deterministic.

A failure while obtaining current availability from one source SHALL NOT cause that capability to be interpreted as available.

Source observation failure SHALL result in `UNKNOWN` availability for the declared capability.

Failure of one source SHALL NOT prevent observation of other composed sources.

The observer SHALL NOT convert `UNKNOWN` to `AVAILABLE`.

### Source Identity Boundary

The observer SHALL preserve the explicitly declared capability and source identities of its composed trusted sources.

Availability evidence SHALL remain attributable to its observation source.

Source identity SHALL NOT be inferred from `ServiceRegistry` membership.

Capability identity SHALL NOT be inferred from service count, startup order or request traffic.

### Mandatory Capability Policy Boundary

RFC-043 SHALL NOT decide which capabilities are mandatory.

Mandatory-capability membership remains platform composition or configuration policy.

The observer SHALL observe explicitly composed sources without converting source membership into mandatory policy.

A future operational-transition contract SHALL separately verify that all capabilities required by the approved mandatory-capability policy are covered by trustworthy current observations.

### HealthCapability Boundary

`HealthCapability` remains the authoritative read-only platform health reporting interface.

`HealthCapability` MAY consume availability observations in a future approved reporting integration.

RFC-043 SHALL NOT require `HealthCapability` to become the availability producer.

`HealthCapability` SHALL NOT:

- probe capability-specific dependencies on behalf of Runtime;
- decide operational eligibility;
- initiate lifecycle transitions;
- fabricate missing availability observations;
- infer availability from service registration;
- interpret `UNKNOWN` as `AVAILABLE`.

### Runtime Boundary

Runtime remains the sole authoritative lifecycle-state owner.

Runtime SHALL NOT perform capability-specific availability probes.

RFC-043 SHALL NOT implement Runtime `READY` to `OPERATIONAL` transition behavior.

A future operational-transition RFC MAY consume trusted immutable availability evidence produced through this boundary.

### Composition Ownership

`CompositionRoot` SHALL own production construction and wiring of:

- the approved capability availability sources;
- the single composed `CapabilityAvailabilityObserver`;
- approved consumers of that observer.

Production code SHALL NOT independently construct competing availability observation graphs.

No production capability source SHALL be registered unless it has a real approved observation mechanism.

An observer with no composed production sources SHALL produce no false availability evidence.

### Implementation Scope

RFC-043 MAY implement:

- `CapabilityAvailabilityState`;
- immutable `CapabilityAvailabilityObservation`;
- abstract `CapabilityAvailabilitySource`;
- read-only `CapabilityAvailabilityObserver`;
- Composition Root ownership of the observer;
- focused contract and composition tests.

Test doubles MAY be used to verify observer semantics.

Test doubles SHALL NOT be treated as production availability sources.

### Non-Goals

RFC-043 SHALL NOT:

- implement `READY` to `OPERATIONAL`;
- add `Runtime.mark_operational()`, `request_operational()` or equivalent;
- introduce `DEGRADED`;
- add `ServiceState.OPERATIONAL`;
- make `ServiceState.READY` sufficient availability evidence;
- modify `BaseService` to fabricate availability;
- make `ServiceRegistry` an availability authority;
- create another service registry;
- make `HealthCapability` a lifecycle authority;
- define mandatory-capability policy;
- implement multi-source capability aggregation;
- implement caching or freshness policy;
- implement retry or recovery;
- implement traffic draining;
- introduce authentication or authorization.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- availability-state semantics;
- observation immutability;
- non-empty capability and source identities;
- timezone-aware timestamp requirement;
- UTC timestamp normalization;
- deterministic observer output;
- successful source observation;
- source failure mapped to `UNKNOWN`;
- failure isolation between sources;
- no fabricated evidence when no sources are composed;
- Composition Root ownership of the same observer instance;
- no Runtime lifecycle mutation during observation;
- no request-admission mutation during observation.

### Next Exact Action

Verify and commit the RFC-043 contract before writing focused TDD tests or production Python.

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
