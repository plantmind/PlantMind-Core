# CAP-002 — Health Capability

## Status

Draft

---

# Purpose

The Health Capability provides a unified read-only view of the health and observable lifecycle information of the PlantMind platform.

It is responsible for reporting current health, Runtime readiness, and observable service information without owning or modifying platform lifecycle state.

The Health Capability is the authoritative reporting interface for platform health information.

Runtime remains the sole authoritative owner of platform lifecycle state, readiness decisions, request-admission state, and future lifecycle transitions.

---

# Responsibilities

- Report platform health.
- Report observed Runtime readiness.
- Report observed Runtime lifecycle information when exposed by the approved health contract.
- Report registered service information.
- Report platform version.
- Report deployment environment.
- Remain read-only with respect to Runtime lifecycle and request admission.

Future reporting of active services, failed services, Bootstrap diagnostics, dependency health, and infrastructure health requires corresponding implemented observation contracts.

---

# Consumers

- Health API
- Bootstrap Manager for observation only
- Monitoring
- Enterprise Dashboard
- Future Alerting Engine

Runtime SHALL NOT depend on Health Capability to determine or authorize lifecycle transitions.

---

# Design Principles

- Authoritative health reporting interface
- Runtime remains authoritative for lifecycle state
- Read-only observation
- Platform-wide visibility
- No lifecycle decision authority
- No business logic
- Deterministic health reporting

---

# Lifecycle Boundary

`READY`, request admission, and `OPERATIONAL` are distinct platform concepts.

Health Capability MAY observe and report approved Runtime lifecycle information.

Health Capability SHALL NOT:

- decide whether Runtime is ready;
- enable or disable request admission;
- initiate or authorize an `OPERATIONAL` transition;
- create a second platform lifecycle state;
- interpret enabled request admission as proof that Runtime is `OPERATIONAL`.

A future `READY` to `OPERATIONAL` transition requires a separately approved Runtime lifecycle contract.

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
