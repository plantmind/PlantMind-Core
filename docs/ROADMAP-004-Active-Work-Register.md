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

## RFC-030 — Controlled Plugin Registration Boundary

### Status

Completed. Technical implementation and documentation verification are complete.

### Objective

Introduce an explicit and deterministic boundary for registering approved plugins into the existing `PluginRegistry` without duplicating registry, lifecycle, bootstrap, or composition responsibilities.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Current technical RFC: RFC-030 — Controlled Plugin Registration Boundary
- Technical baseline commit: `72a8533`
- Full regression baseline: 174 passed

### Dependencies

- Existing `PluginRegistry`
- Existing `PluginLifecycleManager`
- Existing Composition Root ownership established by RFC-029
- Existing Bootstrap lifecycle integration
- Existing Generic Registry behavior and duplicate-registration protection

### Resume Condition

RFC-030 technical implementation is complete and verified.

RFC-030 implementation and documentation verification are complete.

### Verification

- Focused RFC-030 tests: 10 passed
- Impacted plugin, composition and bootstrap tests: 24 passed
- Full regression: 174 passed
- `git diff --check`: passed
- Technical commit: `72a8533`
- Push: verified
- Technical working tree: clean

### Next Exact Action

Commit and push the RFC-030 documentation closure if not already completed, then perform the architecture review required before selecting RFC-031.

The design must preserve existing registry, lifecycle, bootstrap and composition responsibilities and must not introduce automatic filesystem discovery or a parallel plugin registry.

### RFC-030 Contract

- Introduce an immutable `PluginRegistration` declaration containing a plugin name and factory.
- Extend the Composition Root with an optional sequence of plugin registrations.
- Preserve empty registration input as the backward-compatible default.
- Apply registrations to the existing composed `PluginRegistry`.
- Preserve existing `PluginRegistry` duplicate-registration semantics.
- Preserve existing `PluginRegistry.registered()` ordering semantics; RFC-030 SHALL NOT redefine registry ordering.
- Preserve the existing `PluginLifecycleManager` responsibility for plugin creation, activation and deactivation.
- Preserve lazy plugin creation; composition SHALL register factories without instantiating plugins.
- Keep `build_platform_composition` behavior aligned with `CompositionRoot.build` while preserving its no-argument compatibility.
- Preserve `BootstrapManager` responsibility for startup and shutdown orchestration.
- Do not introduce a second registrar, registry, lifecycle manager, or plugin object graph.
- Do not introduce filesystem discovery, dynamic module scanning, or automatic plugin loading in RFC-030.

### TDD Scope

RFC-030 implementation SHALL be driven by focused tests proving:

1. `PluginRegistration` is immutable.
2. Platform composition remains backward compatible when no plugin registrations are supplied.
3. Explicit plugin registrations are added to the composed `PluginRegistry`.
4. Registration ordering remains deterministic according to the existing `PluginRegistry` semantics.
5. Composition registers plugin factories without eagerly creating plugin instances.
6. The `PluginRegistry` resolved from `ServiceContainer` is the same registry containing the supplied registrations.
7. `BootstrapManager` creates and activates plugins supplied through the composition boundary.
8. Duplicate plugin registrations preserve the existing `DuplicateRegistrationError` behavior.
9. The backward-compatible `build_platform_composition` factory continues to work with no registrations.
10. `build_platform_composition` forwards explicit registrations through the same controlled boundary.

### Implementation Boundary

RFC-030 should modify only the minimum plugin-contract and composition surfaces required to establish this boundary.

Plugin discovery, security approval policy, plugin metadata, version compatibility, package loading and enterprise extension catalogs are explicitly outside RFC-030.

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
