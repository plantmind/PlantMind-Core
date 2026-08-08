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

## RFC-044 — Mandatory Capability Policy Contract

### Status

Contract defined. Ready for contract verification and commit.

### Objective

Establish an explicit immutable mandatory-capability policy that distinguishes unconfigured policy from approved configured requirements and remains separate from configuration access, availability observation and Runtime lifecycle authority.

### Policy State

RFC-044 SHALL introduce:

`MandatoryCapabilityPolicyState`

with exactly:

- `UNCONFIGURED`
- `CONFIGURED`

`UNCONFIGURED` means no approved mandatory-capability requirements have been established for the current platform composition or deployment.

`CONFIGURED` means an explicit approved set of mandatory-capability requirements has been established.

Policy state SHALL NOT be inferred solely from collection length by downstream consumers.

### Immutable Policy Contract

RFC-044 SHALL introduce an immutable:

`MandatoryCapabilityPolicy`

with:

- `state: MandatoryCapabilityPolicyState`
- `required_capabilities: tuple[str, ...]`

The policy SHALL use `@dataclass(frozen=True)`.

Explicit capability ordering SHALL be preserved.

Capability identifiers SHALL:

- be non-empty;
- not contain leading or trailing whitespace;
- be unique within the policy.

Duplicate identifiers SHALL be rejected rather than silently collapsed.

### State Invariants

The policy SHALL enforce:

`UNCONFIGURED`

- requires `required_capabilities` to be empty;
- represents absence of approved mandatory-capability requirements;
- SHALL NOT be interpreted as successful operational eligibility.

`CONFIGURED`

- requires at least one mandatory capability;
- SHALL NOT permit an empty `required_capabilities` collection.

A `CONFIGURED` empty policy SHALL be invalid.

This prevents vacuous policy satisfaction during future availability-coverage evaluation.

### Explicit Configuration Semantics

RFC-044 SHALL NOT fabricate production mandatory capabilities.

The current production composition MAY use:

`MandatoryCapabilityPolicyState.UNCONFIGURED`

with an empty capability collection until real mandatory-capability requirements are architecture-approved.

No default capability names SHALL be invented solely to make the policy configured.

### Policy Ownership

`MandatoryCapabilityPolicy` owns:

- mandatory-capability membership representation;
- policy-state invariants;
- identifier validation;
- deterministic requirement ordering.

`ConfigurationProvider` remains responsible for configuration access and mandatory configuration validation.

`ConfigurationProvider` SHALL NOT become the semantic policy owner.

A future configuration-backed integration MAY provide raw configured capability identifiers to policy construction.

Policy invariants SHALL remain owned by `MandatoryCapabilityPolicy`.

### Availability Boundary

`MandatoryCapabilityPolicy` defines what capabilities are required.

`CapabilityAvailabilityObserver` observes what capability availability evidence currently exists.

Neither component SHALL own the responsibility of the other.

Observer source membership SHALL NOT imply mandatory-policy membership.

Availability state SHALL NOT modify policy membership.

Policy membership SHALL NOT fabricate availability evidence.

### Future Coverage Evaluation

RFC-044 SHALL NOT implement mandatory-capability availability coverage evaluation.

A future architecture-controlled evaluator MAY compare:

- a `CONFIGURED` mandatory-capability policy;
- trusted immutable observations from `CapabilityAvailabilityObserver`.

Future eligibility evaluation SHALL fail closed when:

- policy state is `UNCONFIGURED`;
- required capability evidence is missing;
- required capability state is `UNKNOWN`;
- required capability state is `UNAVAILABLE`.

Those evaluation semantics require a separate approved RFC.

### Runtime Boundary

Runtime remains the sole authoritative owner of platform lifecycle state.

Runtime SHALL NOT define mandatory-capability membership.

Runtime SHALL NOT infer mandatory requirements from observer sources.

RFC-044 SHALL NOT implement `READY` to `OPERATIONAL`.

### HealthCapability Boundary

`HealthCapability` remains read-only health reporting.

It SHALL NOT:

- define mandatory-capability policy;
- decide policy satisfaction;
- decide operational eligibility;
- modify Runtime lifecycle state.

### Composition Ownership

`CompositionRoot` SHALL construct one explicit `MandatoryCapabilityPolicy`.

The same composed policy SHALL be:

- registered in `ServiceContainer`;
- exposed through `PlatformComposition`.

Production code SHALL NOT independently construct competing mandatory-capability policies.

Until real mandatory requirements are approved, production composition SHALL use one explicit `UNCONFIGURED` policy rather than fabricated capability names.

### Implementation Scope

RFC-044 MAY implement:

- `MandatoryCapabilityPolicyState`;
- immutable `MandatoryCapabilityPolicy`;
- policy invariant validation;
- explicit unconfigured production composition;
- Composition Root registration and exposure;
- focused contract and composition tests.

### Non-Goals

RFC-044 SHALL NOT:

- define unapproved real plant mandatory capabilities;
- permit a configured empty policy;
- infer policy state from observer membership;
- make `ConfigurationProvider` the policy owner;
- modify `CapabilityAvailabilityObserver` responsibility;
- implement policy-to-availability coverage evaluation;
- implement operational eligibility;
- implement `READY` to `OPERATIONAL`;
- add `Runtime.mark_operational()`, `request_operational()` or equivalent;
- introduce `DEGRADED`;
- add `ServiceState.OPERATIONAL`;
- implement retry, recovery or traffic draining;
- introduce authentication or authorization.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- exact policy-state semantics;
- policy immutability;
- `UNCONFIGURED` requires empty requirements;
- `CONFIGURED` requires at least one requirement;
- non-empty capability identifiers;
- rejection of leading or trailing identifier whitespace;
- duplicate capability rejection;
- deterministic requirement ordering;
- explicit unconfigured production composition;
- Composition Root ownership of the same policy instance;
- no Runtime lifecycle mutation;
- no request-admission mutation;
- no availability-observer mutation.

### Next Exact Action

Verify and commit the RFC-044 contract before writing focused TDD tests or production Python.

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
