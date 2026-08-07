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

## RFC-033 — Plugin Version Format Contract

### Status

Completed.

### Objective

Establish a deterministic validation contract for `PluginMetadata.plugin_version` without introducing version compatibility evaluation, discovery, package loading, or external version-parsing dependencies.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Current technical RFC: RFC-033 — Plugin Version Format Contract
- Technical implementation commit: `569e4fb`
- Previous documentation baseline commit: `04a5fc8`
- Full regression baseline: 204 passed

### Architectural Finding

RFC-032 introduced an explicit plugin version but currently accepts any string value.

The Plugin Framework requires a stable version-format invariant before future compatibility or catalog mechanisms can safely depend on plugin versions.

No version parsing utility or dedicated version dependency currently exists in the Core platform.

Validation belongs to the immutable `PluginMetadata` contract rather than Registry, Composition, Lifecycle or Bootstrap responsibilities.

### Dependencies

- `PluginMetadata` introduced by RFC-032
- Plugin-specific error hierarchy
- Plugin identity invariant established by RFC-031
- Controlled registration boundary established by RFC-030
- ARCH-003 Contract Design Pattern

### RFC-033 Contract

- `plugin_version` SHALL use canonical `MAJOR.MINOR.PATCH` format.
- `MAJOR`, `MINOR` and `PATCH` SHALL each be non-negative decimal integers.
- Numeric components SHALL NOT contain leading zeros except for the value `0`.
- Examples of valid versions include `0.1.0`, `1.0.0` and `12.4.27`.
- Prefixes such as `v`, surrounding whitespace, missing components and additional components SHALL be rejected.
- Pre-release and build metadata syntax SHALL NOT be introduced by RFC-033.
- Validation SHALL occur when `PluginMetadata` is constructed.
- Invalid versions SHALL raise a dedicated `InvalidPluginVersionError`.
- `InvalidPluginVersionError` SHALL remain within the plugin-specific error hierarchy and SHALL preserve `ValueError` semantics.
- Validation SHALL NOT be moved into `PluginRegistry`, `CompositionRoot`, `PluginLifecycleManager` or `BootstrapManager`.
- `PluginMetadata.contract_version` semantics SHALL remain unchanged.
- Existing valid RFC-032 metadata behavior SHALL remain unchanged.
- RFC-033 SHALL NOT introduce version comparison, semantic-version compatibility evaluation, plugin discovery, filesystem scanning, package loading, capability catalogs or security approval policy.
- RFC-033 SHALL NOT introduce an external version-parsing dependency.

### TDD Scope

RFC-033 implementation SHALL be driven by focused tests proving:

1. `0.1.0` is accepted.
2. `1.0.0` is accepted.
3. Multi-digit numeric components are accepted.
4. Missing version components are rejected.
5. Additional version components are rejected.
6. Leading-zero numeric components are rejected.
7. A `v` prefix is rejected.
8. Surrounding whitespace is rejected rather than silently normalized.
9. Pre-release or build suffixes are rejected.
10. Invalid versions raise `InvalidPluginVersionError` while valid metadata preserves RFC-032 behavior.

### Implementation Boundary

RFC-033 should modify only the minimum plugin metadata, plugin error, public API and focused test surfaces required to enforce the version-format contract.

Do not modify Generic Registry, `PluginRegistry`, `PluginRegistration`, Composition Root, Plugin Lifecycle Manager or Bootstrap Manager unless a failing regression proves a dependency that requires architecture review.

### Verification

- Compilation: passed
- Focused RFC-033 tests: 10 passed
- Impacted plugin, composition and bootstrap tests: 54 passed
- Full regression: 204 passed
- Invalid separator verification: passed
- `git diff --check`: passed
- Technical commit: `569e4fb`
- Push: verified
- Technical working tree: clean

### Next Exact Action

Begin architecture review for RFC-034 from the RFC-033 technical and documentation baseline.

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
