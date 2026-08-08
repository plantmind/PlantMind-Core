# PlantMind Project Context

## Document Control

| Property | Value |
|---|---|
| Project | PlantMind Core |
| Project ID | PM-001 |
| Status | Active Development |
| Deployment Model | On-Premise |
| Development Branch | `feature/engineering-platform` |
| Last Completed RFC        | RFC-036 — Managed Shutdown Failure Containment Contract                                |
| Test Baseline             | 225 passing tests                                                                      |
| Technical Baseline Commit | `438d7e4`                                                                              |
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

RFC-040 is complete at alignment commit `376970e`.

RFC-040 established authoritative platform operational semantics without modifying production Python code.

`READY`, request admission and `OPERATIONAL` are distinct platform concepts.

`READY` means mandatory startup and readiness requirements have completed successfully.

A Runtime in `READY` is eligible for request admission, but `READY` does not mean Runtime is `OPERATIONAL`.

Request admission remains an independent Runtime-owned control governing whether new operational requests may enter the API hosting boundary.

Enabling request admission does not transition Runtime to `OPERATIONAL`.

`OPERATIONAL` remains a distinct Runtime lifecycle state with no approved transition implementation yet.

A future `READY` to `OPERATIONAL` transition requires a dedicated architecture contract defining the operational workload execution boundary and authorized Runtime transition.

Runtime remains the sole authoritative owner of platform lifecycle state.

Bootstrap remains the startup and shutdown coordinator. Successful startup terminates at Runtime `READY`, followed by request-admission enablement.

HealthCapability remains read-only observation and reporting. It does not determine readiness, control request admission or authorize lifecycle transitions.

API request-admission enforcement remains read-only with respect to Runtime lifecycle state.

The `Operational` stage documented for Core Services represents target architectural lifecycle intent and is not currently implemented as `ServiceState.OPERATIONAL`.

Service lifecycle semantics remain separate from platform Runtime lifecycle semantics.

`DEGRADED` remains deferred and requires separate architecture review.

RFC-040 aligned:

- `BOOT-001 — Platform Bootstrap Lifecycle`
- `CAP-002 — Health Capability`
- `CORE-002 — Core Services Architecture`

RFC-040 architecture decision:

- AD-026 — Platform Operational Semantics Alignment

RFC-040 verification:

- Contract commit: `63d75ec`
- Alignment commit: `376970e`
- Production Python changes: none
- Full regression: 256 passed
- Documentation validation: passed
- Remote alignment push: verified

RFC-041 has not yet been selected.

Before selecting or implementing RFC-041:

Review the Active Work Register.
Review current committed code and tests.
Review accepted RFCs, ADRs, architecture documents and deferred work.
Preserve Runtime lifecycle-state ownership.
Preserve the distinction between `READY`, request admission and `OPERATIONAL`.
Preserve Bootstrap coordination ownership.
Preserve HealthCapability read-only observation.
Preserve API-hosting request-admission enforcement ownership.
Do not introduce an `OPERATIONAL` transition until its workload execution boundary and transition authority are explicitly approved.
Do not introduce `ServiceState.OPERATIONAL` without dedicated architecture review.
Keep `DEGRADED`, traffic draining, retry, recovery, authentication and authorization outside the next implementation unless explicitly selected through architecture review.
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
