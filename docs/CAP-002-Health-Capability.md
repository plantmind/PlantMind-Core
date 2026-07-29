# CAP-002 — Health Capability

## Status

Draft

---

# Purpose

The Health Capability provides a unified view of the operational health of the PlantMind platform.

It is responsible for exposing the current health, readiness, and availability of the platform and its Core Services.

The Health Capability is the single authoritative source for platform health information.

---

# Responsibilities

- Report platform health
- Report runtime readiness
- Report Bootstrap status
- Report registered services
- Report active services
- Report failed services
- Report platform version
- Report deployment environment

---

# Consumers

- Health API
- Bootstrap Manager
- Runtime
- Monitoring
- Enterprise Dashboard
- Future Alerting Engine

---

# Design Principles

- Single Source of Truth
- Read-only from consumers
- Platform-wide visibility
- No business logic
- Deterministic health reporting

---

# Future Extensions

- Database health
- Neo4j health
- Vector Database health
- PI System connectivity
- OPC UA connectivity
- AI Model availability
- Memory usage
- CPU usage
- Startup duration
- Service latency

---

# Philosophy

Healthy systems are observable systems.