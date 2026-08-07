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

## RFC-031 — Plugin Identity Consistency Contract

### Status

Completed. Technical implementation and documentation verification are complete.

### Objective

Enforce one authoritative plugin identity by requiring every plugin instance created from a registered name to report the same `Plugin.name` as its registry identity.

### Current Technical Baseline

- Branch: `feature/engineering-platform`
- Current technical RFC: RFC-031 — Plugin Identity Consistency Contract
- Technical implementation commit: `defc1fe`
- Previous documentation baseline commit: `2c06b53`
- Full regression baseline: 184 passed

### Architectural Finding

The current `PluginRegistry` resolves a plugin factory by registration name but does not verify that the created plugin reports the same identity through `Plugin.name`.

`PluginLifecycleManager` later reports active plugin identities from `Plugin.name`.

Without an explicit consistency contract, registry identity and runtime plugin identity can diverge.

### Dependencies

- Existing `Plugin` contract
- Existing `PluginRegistry`
- Existing `PluginLifecycleManager`
- Existing Generic Registry behavior
- Controlled registration boundary established by RFC-030
- Composition ownership established by RFC-029

### RFC-031 Contract

- The registration name SHALL remain the authoritative registry identity.
- A plugin created for registration name `X` SHALL report `plugin.name == X`.
- Identity validation SHALL occur when the plugin instance is created, not during composition.
- Plugin creation SHALL remain lazy.
- Identity mismatch SHALL raise a dedicated plugin-specific error.
- Plugin identity errors SHALL NOT be added to the Generic Registry error hierarchy.
- A plugin with mismatched identity SHALL NOT be activated.
- Existing duplicate-registration and registration-not-found behavior SHALL remain unchanged.
- Existing registry ordering semantics SHALL remain unchanged.
- `PluginLifecycleManager` SHALL retain activation and deactivation responsibility.
- `BootstrapManager` SHALL retain startup and shutdown orchestration responsibility.
- RFC-031 SHALL NOT introduce plugin metadata, version compatibility, discovery, filesystem scanning, package loading, or security approval policy.

### TDD Scope

RFC-031 implementation SHALL be driven by focused tests proving:

1. A plugin whose runtime name matches its registration name is created normally.
2. A plugin whose runtime name differs from its registration name raises the dedicated identity mismatch error.
3. The mismatch error exposes the expected registration identity and actual plugin identity in a deterministic diagnostic message.
4. Identity validation occurs only when the factory is resolved and the plugin instance is created.
5. Composition remains lazy and does not instantiate plugins merely to validate identity.
6. A mismatched plugin supplied through the controlled composition boundary is rejected before activation.
7. A mismatched plugin is not added to the active plugin set.
8. Matching plugins continue to activate and deactivate through the existing lifecycle path.
9. Existing duplicate-registration behavior remains unchanged.
10. Existing registration-not-found behavior remains unchanged.

### Implementation Boundary

RFC-031 should modify only the minimum plugin error, registry and focused test surfaces required to establish plugin identity consistency.

Do not redesign the `Plugin` contract, Generic Registry, Composition Root, lifecycle architecture or Bootstrap orchestration.

### Verification

- Compilation: passed
- Focused RFC-031 tests: 10 passed
- Impacted plugin, composition and bootstrap tests: 34 passed
- Full regression: 184 passed
- `git diff --check`: passed
- Technical commit: `defc1fe`
- Push: verified
- Technical working tree: clean

### Next Exact Action

Commit and push the RFC-031 documentation closure if not already completed, then perform the architecture review required before selecting RFC-032.

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
