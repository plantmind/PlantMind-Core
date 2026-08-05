# ROADMAP-004 — Active Work Register

| Property | Value |
|----------|-------|
| Status | Active |
| Version | 1.0 |
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

---

# Active Work

## RFC-021 — Mock PI Tag Reader and Factory

### Status

Paused intentionally before completion.

### Completed

- `PITagReader` contract
- `PITagValue`
- `MockTagReader`
- `TagReaderFactory`
- Factory registration
- Factory resolution
- Duplicate registration protection
- Unknown reader protection
- Unit tests for the factory

### Remaining

- Unit tests dedicated to `MockTagReader`
- Public reset or isolated registry mechanism for tests
- Remove direct test access to `_registry`
- Export reader components through package `__init__.py`
- Integrate factory with the future Core Registry Framework
- Run full regression suite
- Commit and push RFC-021
- Verify clean working tree

### Dependency

RFC-022 — Core Registry Framework

### Resume Condition

Resume immediately after RFC-022 is implemented and tested.

### Next Exact Action

Refactor `TagReaderFactory` to use the Core Registry Framework, then complete RFC-021 tests and Git verification.

---

## RFC-022 — Core Registry Framework

### Status

Approved — Not Started

### Objective

Create a reusable registration and resolution framework for:

- PI readers
- Connectors
- Agents
- Engines
- Document parsers
- Knowledge sources
- Workflows
- Future plugins

### Planned Components

- Generic registry
- Registration validation
- Duplicate protection
- Resolution
- Enumeration
- Explicit reset or isolated registry support
- Typed tests
- Integration with `TagReaderFactory`

### Next Exact Action

Inspect all existing registry and factory implementations before writing code.

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
