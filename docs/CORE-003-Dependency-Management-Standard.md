# CORE-003 — Dependency Management Standard

| Property | Value |
|----------|-------|
| Status | Approved |
| Version | 2.0 |
| Owner | Enterprise Architecture |
| Applies To | Entire PlantMind Platform |
| Last Updated | 2026-07 |

---

# Authority

This document is normative.

Every component within the scope of this standard SHALL comply with the requirements defined in this document unless explicitly superseded by an approved Architecture Decision Record (ADR).

---

# Purpose

This standard defines the dependency management rules governing every software component within the PlantMind platform.

Its objective is to maintain a clean, predictable, and scalable architecture by enforcing explicit dependency boundaries.

---

# Scope

This standard applies to:

- Core Services
- Business Services
- Intelligence Engines
- AI Agents
- Infrastructure Components
- Shared Libraries
- Domain Models
- Contracts

---

# Dependency Philosophy

Dependencies SHALL always move toward lower architectural layers.

Higher-level components may depend on lower-level components.

Lower-level components SHALL NEVER depend on higher-level components.

Circular dependencies are strictly prohibited.

---

# Dependency Hierarchy

External Systems

↓

Infrastructure

↓

Core Services

↓

Business Services

↓

Intelligence Engines

↓

AI Agents

---

# Allowed Dependencies

Components MAY depend on:

- Shared Models
- Contracts
- Value Objects
- Interfaces
- Standard Libraries
- Approved Infrastructure Components

Dependencies SHALL remain explicit.

---

# Forbidden Dependencies

Components SHALL NOT depend on:

- Circular References
- UI Implementations
- Runtime State
- Internal Implementation Details
- Private Modules
- Temporary Components
- Experimental Features

---

# Dependency Injection

Dependencies SHALL be injected through explicit constructors or approved dependency injection mechanisms.

Hidden dependencies are prohibited.

---

# Interface Principle

Components SHALL communicate through stable interfaces whenever practical.

Implementation details SHALL remain isolated.

---

# Layer Isolation

Each architectural layer SHALL remain independently maintainable.

No layer may expose internal implementation details to higher layers.

---

# Change Management

Breaking dependency changes SHALL undergo architectural review.

Major dependency modifications SHALL require ADR approval.

---

# Compliance Checklist

A component is compliant when:

- Dependency direction verified
- Circular dependencies absent
- Interfaces defined
- Hidden dependencies eliminated
- Layer boundaries respected
- Architecture review completed

---

# Definition of Done

Dependency management is complete when:

- All dependency rules are satisfied.
- Architecture validation has passed.
- Dependency graph remains acyclic.
- Documentation has been completed.
- Engineering approval has been granted.

---