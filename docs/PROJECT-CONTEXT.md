# PlantMind Project Context

## Document Control

| Property | Value |
|---|---|
| Project | PlantMind Core |
| Project ID | PM-001 |
| Status | Active Development |
| Deployment Model | On-Premise |
| Development Branch | `feature/engineering-platform` |
| Last Completed RFC | RFC-053 — Canonical Enterprise Knowledge Foundation Boundary |
| Test Baseline | 476 passing tests |
| Technical Baseline Commit | `ee18bc8` |
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
```

The first operational use cases include:

Equipment knowledge graph
PI System integration
Troubleshooting intelligence
Shift-handover intelligence
Operational reasoning
Risk assessment
Root-cause analysis
Recommendation generation
## 4. Enterprise Knowledge Sources

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
## 5. Core Architectural Direction

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
## 6. Current Core Platform Capabilities

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
Canonical Enterprise Knowledge Foundation
Canonical Database Runtime & Schema Lifecycle Foundation
Canonical Knowledge Relational Persistence Adapter
Canonical Knowledge Capture Application Boundary
## 7. Current PI Integration Foundation

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

## 8. Engineering Principles

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
## 9. Required RFC Completion Gate

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
## 10. Development Environment

The authoritative local Python environment is:

PlantMind-Core/.venv

The approved full test command is:

PYTHONPATH=backend ./.venv/bin/python -m pytest -q

The alternate environment below must not be used as the authoritative environment:

PlantMind-Core/backend/.venv

The last verified full regression baseline is:

476 passed

## 11. Git State at This Context Version
Branch:
feature/engineering-platform

Last completed technical RFC:
RFC-053 — Canonical Enterprise Knowledge Foundation Boundary

Technical baseline commit:
`ee18bc8`

Previous documentation closure commit:
`728559c`

Remote:
origin/feature/engineering-platform

Working tree after the verified RFC-053 technical push:
clean

## 12. Current Architectural Review

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
## 13. Deferred Architectural Work
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

## 14. Immediate Development Direction

RFC-049 — Mandatory Capability Composition Contract is technically complete.

RFC-049 established the canonical deployment-neutral composition boundary for:

- capability availability sources;
- mandatory-capability policy.

`CompositionRoot.build(...)` now supports explicit composition-time injection of:

- `Sequence[CapabilityAvailabilitySource]`;
- `MandatoryCapabilityPolicy`.

The existing fail-closed default remains unchanged.

When no capability availability sources are supplied:

- `CapabilityAvailabilityObserver` is composed with no sources.

When no mandatory-capability policy is supplied:

- composition creates an `UNCONFIGURED` policy;
- `required_capabilities` remains empty;
- default mandatory-capability coverage remains `UNSATISFIED`.

Explicitly supplied availability sources preserve:

- source ordering;
- source object identity.

CompositionRoot does not invoke, merge, deduplicate, prioritize or reinterpret availability sources.

Explicitly supplied mandatory-capability policy preserves exact object identity across:

- `PlatformComposition`;
- `ServiceContainer`;
- `MandatoryCapabilityCoverageEvaluator`.

Policy validation remains owned by `MandatoryCapabilityPolicy`.

Availability observation remains owned by `CapabilityAvailabilityObserver`.

Coverage evaluation remains owned by `MandatoryCapabilityCoverageEvaluator`.

Configured policy does not require matching availability sources at composition time.

Missing capability observations remain coverage diagnostics.

Duplicate capability sources remain preserved for existing ambiguous-capability evaluation semantics.

`ConfigurationProvider` does not own mandatory-capability policy.

Core composition remains capability-name agnostic.

RFC-049 introduced no deployment-specific capability names.

CompositionRoot does not:

- evaluate mandatory-capability coverage;
- construct `OperationalTransitionEvidence`;
- call `Runtime.request_operational(...)`;
- perform lifecycle-transition decisions.

Runtime remains the sole lifecycle-transition authority.

`build_platform_composition(...)` remains backward compatible and forwards RFC-049 composition inputs.

Existing no-argument and plugin-registration composition behavior remains supported.

RFC-049 verification:

- Contract commit: `ca5ccbf`
- Technical commit: `496fe42`
- Architecture decision: AD-035
- Focused TDD suite: 15 passed
- Impacted regression: 101 passed
- Full regression: 377 passed
- Compilation: passed
- Remote technical push: verified

RFC-050 — Operational Transition Coordination Contract is technically complete.

RFC-050 established the canonical explicit `OperationalTransitionCoordinator`.

The coordinator now:

- consumes approved `OperationalWorkloadEvidence` or `None`;
- obtains exactly one live capability-availability snapshot per request;
- delegates mandatory-capability coverage evaluation to the canonical evaluator;
- constructs one immutable `OperationalTransitionEvidence`;
- delegates the authoritative transition decision exactly once to `Runtime.request_operational(...)`.

The coordinator preserves exact identity of:

- Runtime;
- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityCoverageEvaluator`;
- supplied operational-workload evidence;
- evaluator-produced mandatory-capability coverage.

Runtime remains the sole lifecycle-transition authority.

RFC-050 introduces no automatic operational transition during:

- CompositionRoot construction;
- Bootstrap startup;
- workload execution;
- `ApplicationFacade.analyze(...)`;
- Health reporting.

The coordinator maintains no persistent evidence history, retry queue or independent lifecycle state.

RFC-050 verification:

- Contract commit: `0001bf0`
- Technical commit: `995a73b`
- Architecture decision: AD-036
- Focused TDD suite: 21 passed
- Impacted core regression: 261 passed
- Full regression: 398 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

RFC-051 — Explicit Operational Transition Application Boundary is technically complete.

RFC-051 established the canonical explicit `OperationalTransitionApplicationService`.

The application service now:

- accepts canonical `tuple[Observation, ...]`;
- executes workload exactly once through the composed `ApplicationFacade`;
- obtains trusted workload evidence only from the returned `WorkflowExecution`;
- forwards the exact workload-evidence value to `OperationalTransitionCoordinator`;
- delegates operational-transition coordination exactly once;
- returns immutable `OperationalTransitionApplicationResult`.

The service preserves exact identity of:

- the supplied observation tuple;
- the composed `ApplicationFacade`;
- the composed `OperationalTransitionCoordinator`;
- the returned `WorkflowExecution`;
- the workload evidence produced by that execution;
- the `OperationalTransitionEvidence` returned by the coordinator.

Runtime remains the sole lifecycle-transition authority.

RFC-051 introduces no:

- automatic transition from normal `ApplicationFacade.analyze(...)`;
- HTTP endpoint;
- FastAPI routing change;
- client-provided workload evidence;
- direct Runtime dependency;
- Bootstrap-triggered transition;
- Health-triggered transition;
- persistent transition state;
- independent lifecycle authority.

RFC-051 verification:

- Contract commit: `ccdd80d`
- Technical commit: `866f786`
- Architecture decision: AD-037
- Focused TDD suite: 18 passed
- Impacted services/core regression: 348 passed
- Full regression: 416 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

RFC-052 — Explicit Operational Transition API Boundary is technically complete.

RFC-052 introduced the canonical `POST /operational-transition` HTTP boundary backed by the exact composed `OperationalTransitionApplicationService`.

The API maps transport observations into existing immutable domain `Observation` objects, preserves observation order, rejects client-supplied workload or transition evidence, remains behind Runtime-owned request admission, and returns `204 No Content` on success.

Runtime remains the sole lifecycle-transition authority. Bootstrap and Health do not initiate operational transition.

RFC-052 verification: contract `f9b0816`; technical `62bb854`; architecture decision AD-038; focused suite 16 passed; API regression 25 passed; impacted API/services/core regression 373 passed; full regression 432 passed; compilation and `git diff --check` passed; remote technical push verified.

RFC-053 — Canonical Enterprise Knowledge Foundation Boundary is technically complete.

RFC-053 established the immutable canonical `KnowledgeRecord` domain foundation together with open knowledge classification value objects, traceable `KnowledgeProvenance`, optional typed `KnowledgeSubject`, and the persistence-neutral `KnowledgeRecordRepository` port.

RFC-053 verification: contract `37112a2`; technical `ee18bc8`; architecture decision AD-039; focused verification 44 passed; full regression 476 passed; compilation and `git diff --check` passed; remote technical push verified.

RFC-053 introduced no production knowledge database adapter, no production knowledge composition or registration, no knowledge HTTP API, no RAG, no vector storage, no semantic search, no LLM integration and no change to Runtime lifecycle authority.

The required post-RFC-053 Source-of-Truth architecture review is complete.

The review established that the RFC-053 canonical knowledge foundation remains authoritative and must not be redesigned by the next workstream. Existing knowledge graph, RAG, semantic-search, memory and agent components remain prototype, placeholder or intentionally unimplemented.

`backend/app/database.py` is preliminary isolated SQLAlchemy infrastructure and is not the canonical PlantMind database runtime. The authoritative `.venv` does not currently provide SQLAlchemy, the declared backend dependencies do not establish SQLAlchemy, a PostgreSQL driver or Alembic, and no canonical ORM schema, schema metadata ownership, migration lifecycle or database test foundation currently exists.

No production code currently consumes `app.database`. Database readiness is not currently a mandatory Runtime capability, and Knowledge persistence must not be implemented before an approved database runtime and schema-lifecycle boundary exists.

The selected engineering direction is:

`Canonical Database Runtime & Schema Lifecycle Foundation`

This is an engineering direction only. No implementation is authorized until the corresponding architecture contract is drafted, reviewed and accepted.

The next exact action is to draft and review that architecture contract before introducing database dependencies, schema migrations, ORM models, production Knowledge persistence or database composition.

### RFC-054 — Canonical Database Runtime & Schema Lifecycle Foundation

RFC-054 is technically complete within the accepted AD-040 architecture boundary.

RFC-054 established the canonical infrastructure-owned synchronous SQLAlchemy database runtime, explicit PostgreSQL Psycopg URL validation, one canonical relational schema metadata authority, and Alembic as the sole relational schema-migration authority.

The legacy `backend/app/database.py` competing engine and session-factory owner was retired after repository and import dependency review confirmed that no production consumer required it.

Database configuration remains optional at general PlantMind Bootstrap. `DATABASE_URL` no longer contains a committed credential-bearing default and is validated only when database capability is explicitly constructed or invoked.

The initial Alembic revision `0001` establishes schema-neutral canonical migration lineage and is the single migration head.

RFC-054 introduced no production Knowledge persistence, Knowledge ORM model, Knowledge repository adapter, database-backed Knowledge application service, CompositionRoot database wiring, automatic migration at application startup, automatic database retry, production connectivity probe, or additional Runtime lifecycle authority.

RFC-054 verification:

- Architecture decision: AD-040
- Contract commit: `8659acd`
- Contract verification documentation commit: `c15ef48`
- Technical commit: `0e483d5`
- Focused RFC-054 verification: 32 passed
- Full PlantMind regression: 506 passed
- Python compilation: passed
- `git diff --check`: passed
- Alembic canonical head: `0001`
- Remote technical push: verified
- Local and remote technical commit identity: verified
- Working tree after technical push: clean

Production PostgreSQL connectivity, authentication policy, certificate policy, network segmentation, database hardening and Cybersecurity deployment approval remain intentionally unclaimed and require approved deployment-environment verification.

The next exact action is the required post-RFC-054 Source-of-Truth architecture review before defining or implementing the next architecture RFC.

### Post-RFC-054 Source-of-Truth Architecture Review

The required post-RFC-054 Source-of-Truth architecture review is complete.

The review confirmed that RFC-053 and RFC-054 remain authoritative and SHALL NOT be redesigned by the next workstream.

The review established that no production implementation of `KnowledgeRecordRepository`, Knowledge relational mapping, Knowledge relational table or Unit of Work currently exists.

`DatabaseRuntime` owns database engine and session-factory lifecycle but does not own repository transaction policy.

Alembic revision `0001` remains intentionally schema-neutral and SHALL NOT be rewritten. Future canonical Knowledge persistence requires a new append-only migration revision.

Default `CompositionRoot` does not register or expose `KnowledgeRecordRepository`, and application startup does not require database configuration.

The selected engineering direction is:

`Canonical Knowledge Relational Persistence Adapter Boundary`

This is an engineering direction only. It is not yet an accepted architecture contract and implementation is not yet authorized.

The future contract is expected to define infrastructure-owned relational representation and mapping for canonical `KnowledgeRecord`, a production relational `KnowledgeRecordRepository` adapter, explicit repository-operation transaction ownership, deterministic session lifetime and a new append-only Alembic migration.

The next workstream SHALL NOT automatically introduce a Unit of Work, default CompositionRoot database wiring, mandatory PostgreSQL startup, Knowledge HTTP APIs, document ingestion, semantic search, vector persistence, Knowledge Graph persistence, RAG, LLM invocation or production PI connectivity.

The next exact action is to draft and review the architecture contract for the Canonical Knowledge Relational Persistence Adapter Boundary before any implementation.


### RFC-055 — Canonical Knowledge Relational Persistence Adapter Boundary

RFC-055 is technically complete within the accepted AD-041 architecture boundary.

RFC-055 established the first canonical relational persistence adapter for RFC-053 Knowledge while preserving the persistence-neutral domain boundary.

The implementation established:

- infrastructure-owned `KnowledgeRecordRow` mapping under `app.infrastructure.knowledge`;
- explicit Domain-to-Relational and Relational-to-Domain mapping;
- canonical SQLAlchemy implementation of `KnowledgeRecordRepository`;
- explicit independent repository-operation session lifetime;
- explicit `add()` transaction commit and rollback semantics;
- read-only `get()` behavior without application-data commit;
- structured canonical duplicate-identity classification using PostgreSQL SQLSTATE and the stable `pk_knowledge_records` constraint identity;
- canonical `knowledge_records` relational schema registration with `DatabaseBase.metadata`;
- append-only Alembic revision `0002` following `0001`;
- one canonical Alembic migration head at `0002`;
- preservation of default CompositionRoot, Bootstrap and Runtime database independence.

RFC-055 verification:

- Architecture decision: AD-041
- Contract commit: `ea046bd`
- Technical commit: `9fc34c7`
- Focused RFC-055 verification: 137 passed
- Full PlantMind regression: 543 passed
- Python compilation: passed
- `git diff --check`: passed
- Alembic canonical head: `0002`
- Remote technical push: verified
- Local and remote technical commit identity: verified
- Working tree after technical push: clean

RFC-055 does not claim production PostgreSQL deployment, production schema application, deployment configuration or Cybersecurity approval.

Those remain subject to separately approved PostgreSQL integration, deployment and Cybersecurity verification.

### Post-RFC-055 Source-of-Truth Architecture Review

The required post-RFC-055 Source-of-Truth architecture review is complete.

The review confirmed that RFC-053, RFC-054 and RFC-055 remain authoritative and SHALL NOT be redesigned by the next workstream.

The review established that:

- canonical Knowledge remains persistence-neutral at the domain and repository-port boundaries;
- RFC-055 provides the canonical relational adapter but does not make Knowledge persistence part of default platform composition;
- no production Knowledge application service currently owns Knowledge write or read use-case coordination;
- `ApplicationFacade` remains the canonical entry boundary for the existing analysis/orchestration workload and SHALL NOT automatically absorb Knowledge persistence operations;
- PlantMind already uses specialized application services for distinct application use cases;
- specialized application services receive dependencies explicitly and do not own Runtime lifecycle authority;
- the existing Knowledge repository contract currently exposes only `add()` and `get()`;
- existing document parser, semantic search, RAG and Knowledge Graph files remain empty, prototype or intentionally unimplemented capability seams and SHALL NOT be promoted by the next workstream;
- default `CompositionRoot` remains free of Knowledge repository registration and PostgreSQL dependency.

The evidence-based post-RFC-055 direction was formalized as:

`RFC-056 — Canonical Knowledge Capture Application Boundary`

under accepted architecture decision AD-042.

RFC-056 is technically complete.

The implementation established:

- immutable `KnowledgeCaptureRequest`;
- immutable optional `KnowledgeCaptureSubject`;
- specialized `KnowledgeCaptureApplicationService`;
- application-owned canonical `EntityId` creation;
- application-owned provenance capture-time sourcing;
- construction of canonical Knowledge domain objects through accepted domain constructors;
- persistence through the persistence-neutral `KnowledgeRecordRepository`;
- exactly one repository `add()` call for a capture reaching persistence;
- no repository pre-read, retry, overwrite or duplicate-identity regeneration;
- explicit propagation of canonical duplicate conflicts and unexpected repository failures;
- no SQLAlchemy, Session, engine, `DatabaseRuntime`, migration or transaction ownership in the Capture application boundary;
- no default CompositionRoot, ServiceContainer or PlatformComposition registration or exposure.

RFC-056 verification:

- Architecture decision: AD-042
- Contract commit: `6998f32`
- Technical commit: `66c24f0`
- Focused RFC-056 and architecture verification: 19 passed
- Broader Knowledge verification: 96 passed
- Full PlantMind regression: 558 passed
- Python compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Local and remote technical commit identity: verified
- Working tree after technical push: clean

RFC-056 does not claim production Knowledge Capture composition, production HTTP or other transport exposure, PostgreSQL deployment verification, authentication or authorization readiness, actor-audit semantics, Cybersecurity approval or production deployment readiness.

Those capabilities remain separately governed.

## Post-RFC-056 Source-of-Truth Architecture Review

The required post-RFC-056 Source-of-Truth architecture review is complete.

The review confirmed that RFC-053 / AD-039 through RFC-056 / AD-042 remain authoritative and SHALL NOT be redesigned by the next workstream.

The review established that:

- PM-001 requires company-Knowledge capture, a Document Library and an AI Knowledge Engine;
- PM-002 places Engineering Documents and Procedures among enterprise knowledge sources and defines a Knowledge Center containing procedures, manuals, P&ID, Cause & Effect, Operating Philosophy and Lessons Learned;
- the canonical Knowledge domain, repository port, relational adapter and Capture application boundary now provide the accepted downstream foundation for document-derived Knowledge;
- `backend/app/knowledge/document_parser.py`, semantic-search, RAG, graph, Knowledge-memory and vector-memory seams remain empty or intentionally unimplemented;
- the existing `KnowledgeGraphService` remains an isolated in-memory prototype and SHALL NOT be promoted by the next workstream;
- default Knowledge persistence and Capture composition remain intentionally absent;
- `backend/app/core/security.py` is only a minimal boolean-gate prototype and does not establish accepted authentication, authorization, RBAC, principal, actor-audit, Active Directory, LDAP or MFA semantics;
- absence of a production security boundary prohibits external or production Knowledge-ingestion exposure, but does not require an isolated application-level ingestion contract to be deferred;
- future document ingestion SHALL consume the accepted `KnowledgeCaptureApplicationService` boundary rather than bypassing it and writing directly through `KnowledgeRecordRepository`.

The initial post-RFC-056 working direction was a Canonical Document Knowledge Ingestion Application Boundary.

Deeper repository and contract review established that PlantMind did not yet possess a canonical enterprise Document identity or Document domain contract.

Introducing ingestion before that foundation would either have forced document identity/lifecycle responsibility into an application service or created a thin translation wrapper over `KnowledgeCaptureApplicationService`.

The direction was therefore refined before contract acceptance to:

`RFC-057 — Canonical Enterprise Document Foundation Boundary`

under accepted:

`AD-043 — Canonical Enterprise Document Foundation Boundary`

RFC-057 is technically complete.

The implementation established:

- canonical `app.domain.document`;
- immutable open `DocumentType`;
- immutable open `DocumentSourceType`;
- immutable `DocumentSource`;
- immutable canonical `EnterpriseDocument`;
- shared canonical `EntityId` as Document identity;
- explicit separation between canonical PlantMind identity and opaque source-system reference;
- lowercase normalized open classifications;
- trimmed, case-preserving source references;
- revision-neutral canonical Document-record semantics;
- canonical Document validation through existing `DomainException`.

RFC-057 verification:

- Architecture decision: AD-043
- Contract commit: `63d9119`
- Technical commit: `a134c7a`
- Focused RFC-057 plus Knowledge architecture verification: 70 passed
- Full PlantMind regression: 586 passed
- Python compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Exact local/remote technical commit identity: verified
- Working tree after technical push: clean

RFC-057 does not introduce or claim:

- Document repository or persistence;
- Document Library production behavior;
- document revision/version lifecycle;
- document ingestion;
- parsing, OCR or chunking;
- document-to-Knowledge transformation;
- search, embeddings, vector or graph persistence;
- RAG or LLM behavior;
- default production composition;
- production authentication/authorization;
- Cybersecurity approval;
- production deployment readiness.

Those capabilities remain separately governed.

## Post-RFC-057 Source-of-Truth Architecture Review

The required post-RFC-057 Source-of-Truth architecture review is complete.

The review confirmed that RFC-057 / AD-043 established the canonical enterprise Document domain but intentionally introduced no Document repository, persistence adapter, relational schema, Document Library, revision lifecycle, ingestion or search capability.

Repository evidence confirmed that the next missing prerequisite is a persistence-neutral Document repository contract rather than Document ingestion or a production Document Library.

The review established the following preliminary repository direction:

- repository port: `EnterpriseDocumentRepository`;
- duplicate conflict: `EnterpriseDocumentAlreadyExistsError`;
- canonical operations: `add(document) -> None` and `get(document_id) -> EnterpriseDocument | None`;
- duplicate semantics apply only to canonical `EntityId`;
- absent identity lookup returns `None`;
- `DocumentSource.source_reference` remains traceability only and SHALL NOT become canonical identity or globally unique repository key;
- no `find_by_source_reference`, list, search, update, delete or upsert operation is authorized;
- no document revision semantics are introduced;
- no SQLAlchemy adapter, database schema, migration or production composition is authorized.

The persistence-neutral repository namespace direction is:

`app.document.repository`

This mirrors the accepted separation between `app.domain.knowledge` and `app.knowledge.repository` without placing repository responsibility inside the canonical domain or infrastructure layers.

The evidence-based next architecture direction is:

`RFC-058 — Canonical Enterprise Document Repository Foundation Boundary`

RFC-058 is a selected engineering direction only.

Its architecture contract has not yet been accepted.

AD-044 has not been created.

RFC-058 technical implementation is not authorized.

The next exact action is to draft and review the RFC-058 architecture contract before any implementation.

## 15. Session Continuation Instruction

When continuing PlantMind in a new engineering session:

Continue PlantMind PM-001 as Chief Software Architect.

Read and follow:
- docs/PROJECT-CONTEXT.md
- docs/SESSION-HANDOFF.md
- docs/ENGINEERING-JOURNAL.md
- docs/ARCHITECTURE-DECISIONS.md
- docs/ROADMAP-004-Active-Work-Register.md

Continue from the latest committed Git state.
Do not redesign completed components without dependency review.
Use the authoritative root .venv environment.
Follow the RFC Completion Gate.
Provide concise executable steps unless explanation is requested.

## 16. Source of Truth Order

When information conflicts, use this priority:

Current committed code and tests
Accepted ADR, ARCH, CORE and RFC documents
Active Work Register
Project Context
Session Handoff
Engineering Journal
Conversation history

The conversation is supporting context, not the authoritative engineering record.
