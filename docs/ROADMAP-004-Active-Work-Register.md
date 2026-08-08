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

## RFC-045 — Mandatory Capability Coverage Evaluation Contract

### Status

Contract defined. Ready for contract verification and commit.

### Objective

Establish a deterministic fail-closed evaluation boundary that compares one approved `MandatoryCapabilityPolicy` with supplied trusted `CapabilityAvailabilityObservation` evidence without introducing Runtime lifecycle-transition authority.

### Coverage State

RFC-045 SHALL introduce:

`MandatoryCapabilityCoverageState`

with exactly:

- `SATISFIED`
- `UNSATISFIED`

`SATISFIED` means every required capability in a configured mandatory-capability policy is proven by exactly one matching trusted `AVAILABLE` observation.

`UNSATISFIED` means mandatory coverage cannot be proven.

Coverage state SHALL NOT represent Runtime lifecycle state.

### Immutable Coverage Result

RFC-045 SHALL introduce an immutable:

`MandatoryCapabilityCoverageResult`

with:

- `state: MandatoryCapabilityCoverageState`
- `required_capabilities: tuple[str, ...]`
- `satisfied_capabilities: tuple[str, ...]`
- `missing_capabilities: tuple[str, ...]`
- `unavailable_capabilities: tuple[str, ...]`
- `unknown_capabilities: tuple[str, ...]`
- `ambiguous_capabilities: tuple[str, ...]`

The result SHALL use `@dataclass(frozen=True)`.

All diagnostic capability collections SHALL preserve mandatory-policy requirement order.

Each required capability SHALL appear in exactly one diagnostic classification when policy state is `CONFIGURED`.

The result SHALL contain diagnostic evidence only.

The result SHALL NOT contain lifecycle-transition authority or a second operational-eligibility state.

### Evaluator Contract

RFC-045 SHALL introduce:

`MandatoryCapabilityCoverageEvaluator`

The evaluator SHALL be constructed with one explicit:

`MandatoryCapabilityPolicy`

The public evaluation operation SHALL be:

`evaluate(observations) -> MandatoryCapabilityCoverageResult`

The supplied observations SHALL be treated as one evaluation snapshot.

The evaluator SHALL be deterministic and read-only.

### Policy Ownership

The evaluator SHALL consume the same policy instance supplied during composition.

It SHALL NOT:

- construct an independent mandatory-capability policy;
- modify mandatory-policy membership;
- infer mandatory requirements from observations;
- convert observer membership into policy membership.

### Unconfigured Policy Semantics

When policy state is `UNCONFIGURED`:

- result state SHALL be `UNSATISFIED`;
- `required_capabilities` SHALL be empty;
- all diagnostic capability collections SHALL be empty;
- supplied observations SHALL NOT cause coverage to become satisfied.

An unconfigured empty policy SHALL therefore fail closed without fabricating requirements.

### Configured Policy Evaluation

For every capability in `required_capabilities`, matching SHALL use exact `capability_name` identity.

No matching observation:

- classify the capability as missing.

Exactly one matching observation with `AVAILABLE`:

- classify the capability as satisfied.

Exactly one matching observation with `UNAVAILABLE`:

- classify the capability as unavailable.

Exactly one matching observation with `UNKNOWN`:

- classify the capability as unknown.

More than one matching observation regardless of availability states:

- classify the capability as ambiguous.

Overall state SHALL be `SATISFIED` only when every required capability is classified as satisfied.

Any missing, unavailable, unknown or ambiguous required capability SHALL produce overall `UNSATISFIED`.

### Ambiguity Boundary

RFC-045 SHALL fail closed when multiple observations match one required capability.

The evaluator SHALL NOT:

- choose the newest observation;
- choose the oldest observation;
- prefer `AVAILABLE`;
- prefer `UNAVAILABLE`;
- prefer a particular source;
- combine or merge source states.

Multi-source aggregation remains outside RFC-045.

### Freshness Boundary

RFC-045 SHALL NOT evaluate timestamp freshness.

The evaluator SHALL NOT introduce:

- TTL;
- maximum observation age;
- staleness thresholds;
- current-time comparisons.

`observed_at` remains part of trusted evidence but its freshness semantics require a separately approved architecture contract.

### Non-Required Evidence

Observations whose `capability_name` is not present in the mandatory policy SHALL be ignored for mandatory coverage evaluation.

Non-required observations SHALL NOT:

- become mandatory;
- alter policy membership;
- affect overall coverage state.

### Availability Boundary

`CapabilityAvailabilityObserver` remains responsible for collecting availability observations.

`MandatoryCapabilityCoverageEvaluator` evaluates supplied observations against mandatory policy.

The evaluator SHALL NOT perform capability-specific probes.

It SHALL NOT modify `CapabilityAvailabilityObserver`.

### Runtime Boundary

Runtime remains the sole authoritative owner of platform lifecycle state.

Coverage evaluation SHALL NOT:

- modify Runtime lifecycle state;
- modify request-admission state;
- transition Runtime to `OPERATIONAL`.

A `SATISFIED` coverage result is evidence only.

It SHALL NOT itself authorize or execute a lifecycle transition.

### Composition Ownership

`CompositionRoot` SHALL construct one production `MandatoryCapabilityCoverageEvaluator`.

The evaluator SHALL receive the exact composed `MandatoryCapabilityPolicy` instance established by RFC-044.

The same evaluator instance SHALL be:

- registered in `ServiceContainer`;
- exposed through `PlatformComposition`.

Production code SHALL NOT construct competing coverage evaluators backed by independent mandatory policies.

### Implementation Scope

RFC-045 MAY implement:

- `MandatoryCapabilityCoverageState`;
- immutable `MandatoryCapabilityCoverageResult`;
- `MandatoryCapabilityCoverageEvaluator`;
- deterministic configured-policy evaluation;
- explicit unconfigured-policy fail-closed evaluation;
- Composition Root construction, registration and exposure;
- focused contract and composition tests.

### Non-Goals

RFC-045 SHALL NOT:

- implement Runtime `READY` to `OPERATIONAL`;
- add `Runtime.mark_operational()`, `request_operational()` or equivalent;
- introduce `DEGRADED`;
- add `ServiceState.OPERATIONAL`;
- perform capability probing;
- modify mandatory policy;
- implement multi-source aggregation;
- implement source priority;
- implement observation freshness or TTL;
- fabricate missing evidence;
- treat `UNKNOWN` as `AVAILABLE`;
- treat `UNAVAILABLE` as acceptable evidence;
- treat ambiguous evidence as satisfied;
- treat `UNCONFIGURED` policy as satisfied;
- introduce retry, recovery, traffic draining, authentication or authorization.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- exact coverage-state semantics;
- result immutability;
- unconfigured policy fails closed;
- configured policy with all required capabilities `AVAILABLE` is satisfied;
- missing required capability fails closed;
- `UNAVAILABLE` required capability fails closed;
- `UNKNOWN` required capability fails closed;
- multiple observations for one required capability are ambiguous and fail closed;
- non-required observations do not affect coverage;
- policy ordering is preserved in diagnostics;
- each configured required capability receives exactly one diagnostic classification;
- evaluator uses the exact composed policy instance;
- Composition Root exposes and registers the same evaluator instance;
- evaluation does not mutate Runtime lifecycle state;
- evaluation does not mutate request admission;
- evaluation does not mutate the availability observer or mandatory policy.

### Next Exact Action

Verify and commit the RFC-045 contract before writing focused TDD tests or production Python.

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
