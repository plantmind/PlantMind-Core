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

## RFC-032 — Plugin Metadata Contract

### Status

Architecture review complete; contract and TDD scope defined; implementation not started.

### Objective

Introduce a minimal immutable metadata contract for registered plugins without changing the authoritative plugin identity, lifecycle architecture, controlled registration boundary, or existing backward-compatible plugin registration behavior.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Last completed RFC: RFC-031 — Plugin Identity Consistency Contract
- Technical implementation commit: `defc1fe`
- Documentation baseline commit: `8462b53`
- Full regression baseline: 184 passed

### Architectural Finding

The current Plugin Framework has an authoritative registration identity but no explicit plugin metadata or plugin-version contract.

`APP_VERSION` represents the PlantMind application version and SHALL NOT be reused as an implicit plugin version.

ARCH-003 requires contracts to expose explicit version information and preserve immutable contract semantics.

Plugin metadata must extend the existing controlled registration model without creating a second identity, registry, discovery mechanism, or compatibility engine.

### Dependencies

- Existing `Plugin` contract
- Existing `PluginRegistration`
- Existing `PluginRegistry`
- Plugin identity invariant established by RFC-031
- Controlled registration boundary established by RFC-030
- Composition ownership established by RFC-029
- ARCH-003 Contract Design Pattern

### RFC-032 Contract

- Introduce an immutable `PluginMetadata` contract.
- `PluginMetadata` SHALL declare an explicit `plugin_version`.
- `PluginMetadata` SHALL expose an explicit immutable metadata contract version.
- Plugin metadata SHALL NOT introduce another authoritative plugin name.
- `PluginRegistration.name` SHALL remain the authoritative plugin identity.
- Existing registrations without metadata SHALL remain backward compatible.
- `PluginRegistration` MAY carry `PluginMetadata`.
- Metadata supplied through controlled composition SHALL be associated with the same existing `PluginRegistry` registration.
- Metadata access SHALL NOT instantiate the plugin factory.
- Clearing the `PluginRegistry` SHALL also clear associated plugin metadata.
- Existing duplicate-registration, registration-not-found, ordering and identity semantics SHALL remain unchanged.
- Plugin metadata SHALL NOT alter lifecycle or Bootstrap behavior.
- `APP_VERSION` SHALL NOT be used as an implicit plugin version.
- RFC-032 SHALL NOT introduce semantic-version compatibility evaluation, plugin discovery, filesystem scanning, package loading, capability catalogs, or security approval policy.

### TDD Scope

RFC-032 implementation SHALL be driven by focused tests proving:

1. `PluginMetadata` is immutable.
2. Plugin version is explicitly represented independently from `APP_VERSION`.
3. The metadata contract exposes its own immutable contract version.
4. Existing `PluginRegistration(name, factory)` construction remains backward compatible.
5. A `PluginRegistration` can carry explicit plugin metadata.
6. Composition forwards supplied metadata into the same composed `PluginRegistry`.
7. Plugin metadata can be read without creating the plugin instance.
8. Clearing the Plugin Registry removes associated metadata.
9. Duplicate plugin registration preserves the existing `DuplicateRegistrationError` behavior without corrupting metadata.
10. Plugin metadata does not change RFC-031 identity validation or existing lifecycle behavior.

### Implementation Boundary

RFC-032 should modify only the minimum plugin metadata, registration, registry, composition and focused test surfaces required to establish the metadata contract.

Do not redesign the `Plugin` contract, Generic Registry, Plugin Lifecycle Manager, Bootstrap Manager or Composition Root ownership model.

### Next Exact Action

Write the RFC-032 failing focused tests before implementation.

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
