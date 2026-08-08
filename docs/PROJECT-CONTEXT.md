# PlantMind Project Context

## Document Control

| Property | Value |
|---|---|
| Project | PlantMind Core |
| Project ID | PM-001 |
| Status | Active Development |
| Deployment Model | On-Premise |
| Development Branch | `feature/engineering-platform` |
| Last Completed RFC        | RFC-035 — Bootstrap Shutdown Lifecycle Compliance Contract                             |
| Test Baseline             | 217 passing tests                                                                      |
| Technical Baseline Commit | `3e613df`                                                                              |
| Purpose | Authoritative context for continuing PlantMind development across engineering sessions |

---

## 1. Project Vision

PlantMind is an Enterprise Operational Intelligence Platform for industrial and petrochemical environments.

The platform transforms plant operations from reactive decision-making into contextual, explainable, knowledge-driven and eventually predictive operations.

PlantMind is not merely a chatbot, PI System interface, document search tool, or standalone AI agent.

It is designed to understand the plant by combining:

- Live operational data
- Engineering design knowledge
- Operating procedures
- Maintenance and reliability history
- Incident and RCA records
- Shift-handover knowledge
- Expert operational experience
- Enterprise workflows and governance

---

## 2. Deployment and Security Position

PlantMind production deployment SHALL be:

- Inside the company environment
- On the internal network
- On-premise by default
- Subject to company Cybersecurity approval
- Integrated with Active Directory where applicable
- Protected by RBAC and data-permission controls
- Designed to prevent unauthorized data disclosure
- Independent of public cloud services for production operation
- Capable of using locally hosted AI models

GitHub is used as the development repository only.

The final enterprise product is not delivered as a public GitHub repository.

---

## 3. Initial Industrial Scope

Phase 1 is anchored around:

```text
COMP-H-001 — Ethane Booster Compressor

The first operational use cases include:

Equipment knowledge graph
PI System integration
Troubleshooting intelligence
Shift-handover intelligence
Operational reasoning
Risk assessment
Root-cause analysis
Recommendation generation
4. Enterprise Knowledge Sources

PlantMind is intended to integrate and reason across multiple source classes.

Live Operational Data
PI System
Historians
DCS / Emerson DeltaV
OPC UA
SCADA
SQL databases
Engineering Knowledge
P&ID
PFD
Cause and Effect
Control narratives
Equipment datasheets
Instrument datasheets
Loop diagrams
Vendor manuals
Engineering drawings
Operational Knowledge
Operating procedures
SOPs
Startup procedures
Shutdown procedures
Emergency procedures
Work instructions
Checklists
Historical Knowledge
Incident reports
RCA reports
Shift handovers
Operator notes
CMMS history
SAP PM
Work orders
Maintenance records
Lessons learned
5. Core Architectural Direction

The authoritative architectural layers are:

Industrial Data Layer
Knowledge Intelligence Layer
AI Orchestration Layer
PlantMind AI Experience Layer
Enterprise Intelligence Layer

The Enterprise Intelligence Layer includes:

Operational Intelligence Engine
Knowledge Graph Engine
Decision Engine
Risk Engine
RCA Engine
Recommendation Engine
Compliance Engine
Workflow Intelligence
Learning Engine
6. Current Core Platform Capabilities

The following foundations have been implemented and tested:

Runtime
Runtime State
Bootstrap
Bootstrap Manager
Composition Root
Service Registry
Service Container
Configuration Provider
Logging Provider
Health Capability
Event Bus
Industrial Connector Framework
PI Connector lifecycle foundation
PI Session Manager
PI Client foundation
PI Tag Reader contract
Mock PI Tag Reader
PI Tag Reader Factory
Generic Registry Framework
Registry Public API
Core Plugin Framework
Plugin Lifecycle Manager
Plugin Infrastructure Composition
7. Current PI Integration Foundation

The PI integration structure currently includes:

backend/app/connectors/
├── base_connector.py
├── connector_state.py
├── pi_connector.py
└── pi/
    ├── __init__.py
    ├── client.py
    ├── models.py
    ├── session.py
    └── readers/
        ├── __init__.py
        ├── factory.py
        ├── tag_reader.py
        └── mock/
            ├── __init__.py
            └── mock_tag_reader.py

Real PI Web API network integration has not yet been implemented.

Mock implementations are intentionally used to develop and verify the internal platform architecture before introducing network, authentication, certificates and production-system dependencies.

8. Engineering Principles

All future work SHALL follow these principles.

Architecture Before Features

No feature is implemented before reviewing its architectural responsibility, dependencies and impact.

Nothing Gets Forgotten

Paused, deferred or superseded work must be documented with:

Current status
Completed work
Remaining work
Dependencies
Resume condition
Next exact action
Enterprise First

Every decision must be evaluated as part of a long-lived enterprise industrial platform.

No Duplicate Responsibility

Two components must not own the same responsibility without a documented architectural reason.

Reuse Before Rebuild

Existing components must be reviewed before creating replacements.

Preserve Before Delete

The preferred decision order is:

Keep
Rename
Move
Merge
Add compatibility wrapper
Deprecate
Delete only after dependency and impact verification
Refactor by Design

Refactoring must be planned, tested and documented. It must not be performed impulsively.

Replaceable Components

External systems, AI models, databases, connectors and services should be replaceable without breaking unrelated platform layers.

The Platform Must Understand Itself

PlantMind should eventually understand:

What has been built
What remains incomplete
Component dependencies
Technical debt
Release readiness
Engineering governance state
9. Required RFC Completion Gate

No RFC is complete until all relevant checks pass:

Existing-code review
Architecture review
Dependency and impact analysis
Implementation
Python compilation checks
Focused unit tests
Full regression tests
Git status review
Commit verification
Remote push verification
Clean working tree
Active Work Register update when required
10. Development Environment

The authoritative local Python environment is:

PlantMind-Core/.venv

The approved full test command is:

PYTHONPATH=backend ./.venv/bin/python -m pytest -q

The alternate environment below must not be used as the authoritative environment:

PlantMind-Core/backend/.venv

The last verified baseline is:

184 passed
11. Git State at This Context Version
Branch:
feature/engineering-platform

Last completed technical RFC commit:
defc1fe RFC-031: enforce plugin identity consistency

Remote:
origin/feature/engineering-platform

Technical working tree after RFC-031:
clean
12. Current Architectural Review

An existing service lifecycle framework already exists:

backend/app/core/services/
├── base_service.py
├── service_registry.py
└── service_state.py

It is already used by:

Bootstrap Manager
Composition Root
Health Capability
Core public API

It must not be replaced by another Service Registry without a documented dependency review.

The Generic Registry, Plugin Registry, Plugin Lifecycle Manager, Service Registry, Bootstrap Manager and Composition Root have distinct responsibilities:

Component               Responsibility
Registry[T]             Generic factory registration and resolution
PluginRegistry          Plugin creation and registration
PluginLifecycleManager  Plugin activation and deactivation
ServiceRegistry         Runtime service instances and service lifecycle
BootstrapManager        Platform startup and shutdown orchestration
CompositionRoot         Platform dependency construction and wiring
ServiceContainer        Resolution of composed platform dependencies
13. Deferred Architectural Work
PI Connector Package Migration

Current compatibility structure:

backend/app/connectors/pi_connector.py
backend/app/connectors/pi/

Future direction:

backend/app/connectors/pi/connector.py

The legacy module should remain as a compatibility wrapper until dependency review confirms safe migration.

Logging Consolidation

Current structure:

backend/app/core/logger.py
backend/app/core/logging/logging_provider.py

Consumers should eventually migrate to the logging package before legacy removal.

Session Memory Review

Current file:

backend/app/memory/session_memory.py

Its responsibility must be defined before deciding whether to implement, rename, merge or remove it.

Enterprise Extension Framework

A future extension layer may build on the Plugin Framework to support:

Connectors
AI Agents
Engines
Knowledge Providers
Reasoning extensions
Enterprise modules

It must extend, not discard, the accepted Plugin Framework.

14. Immediate Development Direction

RFC-035 is complete at the technical baseline.

The Bootstrap Shutdown Lifecycle Compliance Contract aligns implemented shutdown behavior with BOOT-002 and RUNTIME-001.

Runtime now exposes a public `mark_stopping()` transition.

The `STOPPING` transition makes Runtime not ready before component shutdown begins.

Bootstrap requests Runtime transition to `STOPPING` before plugin or service shutdown work begins.

Plugin deactivation remains owned by `PluginLifecycleManager`.

Registered services continue to shut down in deterministic reverse registry enumeration order.

Runtime transitions to `STOPPED` only after required shutdown operations complete successfully.

Existing `Runtime.mark_not_ready()` behavior remains backward compatible.

RFC-034 startup atomicity behavior remains unchanged.

RFC-035 introduces no shutdown retry logic, cleanup-failure aggregation, automatic recovery, dependency graphs, parallel shutdown, ServiceState redesign, request-admission implementation, plugin discovery or logging architecture redesign.

Technical verification completed with 11 focused Runtime and Bootstrap tests, 56 impacted runtime/bootstrap/plugin/composition tests and a full regression baseline of 217 passing tests.

RFC-036 has not yet been selected.

Before selecting or implementing RFC-036:

Review the Active Work Register.
Review current committed code and tests.
Review accepted RFCs, ADRs, architecture documents and deferred work.
Preserve established Runtime ownership, Bootstrap orchestration, Service Registry, Plugin Lifecycle, Registry, Metadata, Version Format and Composition responsibilities.
Do not introduce shutdown recovery, cleanup-failure aggregation, dependency graphs, parallel shutdown, ServiceState redesign or request-admission implementation without dedicated architecture review.
Record the selected RFC objective and next exact action before implementation begins.

15. Session Continuation Instruction

When continuing PlantMind in a new engineering session:

Continue PlantMind PM-001 as Chief Software Architect.

Read and follow:
- docs/PROJECT-CONTEXT.md
- docs/ENGINEERING-JOURNAL.md
- docs/ARCHITECTURE-DECISIONS.md
- docs/ROADMAP-004-Active-Work-Register.md

Continue from the latest committed Git state.
Do not redesign completed components without dependency review.
Use the authoritative root .venv environment.
Follow the RFC Completion Gate.
Provide concise executable steps unless explanation is requested.
16. Source of Truth Order

When information conflicts, use this priority:

Current committed code and tests
Accepted ADR, ARCH, CORE and RFC documents
Active Work Register
Project Context
Engineering Journal
Conversation history

The conversation is supporting context, not the authoritative engineering record.


```bash
python -m py_compile backend/app/core/plugins/__init__.py
wc -l docs/PROJECT-CONTEXT.md
git status --short
