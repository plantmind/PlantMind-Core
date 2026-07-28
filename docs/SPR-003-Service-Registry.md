# SPR-003 — Service Registry

## Status

Approved

---

## Purpose

The Service Registry is responsible for managing the lifecycle of all PlantMind Core Services.

It acts as the central registry where platform services are registered, initialized, validated, monitored, and gracefully shut down.

The Bootstrap Manager interacts only with the Service Registry rather than individual services.

---

## Responsibilities

- Register services
- Retrieve services
- Initialize all services
- Validate all services
- Shutdown all services
- Report service status

---

## Design Principles

- Single Source of Truth for registered services.
- Bootstrap never directly manages individual services.
- Services remain independent.
- Platform services are lifecycle-managed.
- Supports future Dependency Injection.

---

## Future Extensions

- Automatic service discovery
- Dependency graph
- Startup ordering
- Event publishing
- Metrics collection
- Service health aggregation

---

## Philosophy

A platform grows through managed services, not unmanaged objects.