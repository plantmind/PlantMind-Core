# CAP-001 — Runtime Capability

## Status

Draft

---

## Purpose

The Runtime Capability provides a unified view of the current PlantMind platform runtime.

It exposes runtime information required by both internal platform components and external APIs.

The Runtime Capability acts as the authoritative source for runtime state.

---

## Responsibilities

- Report platform version
- Report deployment mode
- Report environment
- Report runtime status
- Report platform readiness
- Report registered services

---

## Consumers

- Bootstrap Manager
- Service Registry
- Health API
- Monitoring
- Future Platform Dashboard

---

## Design Principles

- Single Source of Truth
- Read-only from consumers
- Platform-wide availability
- No business logic

---

## Future Extensions

- Build information
- Git commit identifier
- Startup timestamp
- Uptime
- Memory statistics
- CPU statistics

---

## Philosophy

Every platform decision begins with knowing the current runtime state.