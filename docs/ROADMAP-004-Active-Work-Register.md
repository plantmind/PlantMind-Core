# ROADMAP-004 — Active Work Register

| Property | Value |
|----------|-------|
| Status | Active |
| Version | 1.2 |
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

## RFC-053 — Canonical Enterprise Knowledge Foundation Boundary

### Status

Accepted.

The RFC-053 architecture contract is accepted.

Production implementation has not started.

### Objective

Establish the canonical enterprise knowledge foundation for PlantMind by defining an immutable, traceable and persistence-neutral domain representation of enterprise knowledge together with the repository port required to store and retrieve that representation by canonical identity.

RFC-053 SHALL create the minimum foundation required for later Document Library, Asset Library, Search Engine, Knowledge Graph, semantic retrieval and RAG capabilities without coupling the PlantMind domain to any specific database, graph engine, vector database, LLM or external industrial system.

### Architectural Position

RFC-052 completed the canonical operational-transition path through the HTTP boundary.

The post-RFC-052 Source-of-Truth architecture review established that PM-001 Phase 1 still requires production-grade enterprise knowledge capabilities.

The review also established that:

- `app.domain.equipment.Equipment` is the established canonical equipment domain entity;
- `EquipmentSnapshot` is the established immutable point-in-time equipment operational view;
- `app.models.equipment.Equipment` belongs to a separate prototype or legacy seam and SHALL NOT become a second canonical equipment domain;
- the existing `EquipmentService` is an in-memory prototype;
- the existing `KnowledgeGraphService` is an in-memory prototype;
- the existing `KnowledgeGraphEngine` is a placeholder;
- the current document parser, equipment graph, plant graph, RAG engine, relationship builder, semantic search, knowledge memory, vector memory and knowledge agent files contain no production implementation;
- `backend/app/database.py` provides concrete SQLAlchemy session infrastructure and is not a domain repository abstraction;
- the existing reasoning engine and reasoning pipeline consume `Observation` and expose no accepted enterprise-knowledge input boundary;
- no production knowledge repository abstraction currently exists.

RFC-053 SHALL establish the knowledge foundation without promoting prototype components into production or changing accepted operational, reasoning or lifecycle responsibilities.

### Canonical Knowledge Responsibility

PlantMind SHALL introduce a canonical:

`KnowledgeRecord`

as the immutable domain representation of one addressable enterprise knowledge item.

A `KnowledgeRecord` SHALL represent domain knowledge.

It SHALL NOT represent:

- a database row;
- a Neo4j node;
- a Qdrant point;
- an embedding;
- an LLM prompt;
- an LLM response;
- a document chunk transport object;
- a PI tag value;
- an operational observation;
- a search result;
- a reasoning result.

Storage, indexing, graph and AI technologies SHALL remain representations or consumers of knowledge rather than owners of the canonical knowledge model.

### Knowledge Domain Boundary

RFC-053 SHALL introduce immutable domain contracts for:

- `KnowledgeRecord`;
- `KnowledgeKind`;
- `KnowledgeProvenance`;
- `KnowledgeSourceType`;
- `KnowledgeSubject`;
- `KnowledgeSubjectType`.

These contracts SHALL use existing PlantMind domain primitives.

`KnowledgeKind`, `KnowledgeSourceType` and `KnowledgeSubjectType` SHALL be open immutable value objects rather than closed enums, allowing future approved knowledge categories and source or subject types without replacing the canonical contracts.

Each value object SHALL contain one `str` value.

Each value SHALL be normalized by:

- removing leading and trailing whitespace;
- converting alphabetic characters to lowercase.

Internal whitespace and characters SHALL otherwise be preserved.

The normalized value SHALL be non-empty.

RFC-053 SHALL NOT establish a closed vocabulary, enum membership rule or global type registry.

`KnowledgeRecord` SHALL inherit the canonical PlantMind domain identity model through:

`DomainEntity[EntityId]`

RFC-053 SHALL NOT introduce another entity identifier framework.

### Knowledge Record Contract

`KnowledgeRecord` SHALL contain:

- canonical `EntityId` identity;
- `kind: KnowledgeKind`;
- `title: str`;
- `content: str`;
- `provenance: KnowledgeProvenance`;
- `subject: KnowledgeSubject | None`.

`kind` SHALL be a canonical `KnowledgeKind`.

`KnowledgeKind` SHALL contain one normalized non-empty string value.

`title` SHALL be normalized by removing leading and trailing whitespace only.

`content` SHALL be normalized by removing leading and trailing whitespace only.

Internal title and content characters, whitespace and line breaks SHALL otherwise be preserved.

`title` SHALL be non-empty after normalization.

`content` SHALL be non-empty after normalization.

RFC-053 SHALL NOT introduce arbitrary untyped metadata dictionaries into the canonical knowledge record.

Additional typed knowledge attributes require an explicit future contract.

### Domain Validation Boundary

RFC-053 domain invariants SHALL be enforced by the canonical domain types themselves.

Validation failures produced by:

- `KnowledgeRecord`;
- `KnowledgeKind`;
- `KnowledgeProvenance`;
- `KnowledgeSourceType`;
- `KnowledgeSubject`;
- `KnowledgeSubjectType`;

SHALL raise the existing PlantMind `DomainException` or a domain-specific subtype of `DomainException`.

Domain validation SHALL NOT require:

- repository access;
- database access;
- graph traversal;
- vector lookup;
- API access;
- application-service execution.

Repository conflicts are not domain-validation failures.

`KnowledgeRecordAlreadyExistsError` SHALL remain owned by the repository boundary and SHALL NOT become an alternate domain-invariant authority.

### Knowledge Identity Boundary

`KnowledgeRecord.id`

SHALL be the canonical PlantMind identity of the knowledge record.

External identifiers SHALL NOT replace the canonical `EntityId`.

The following SHALL NOT become canonical knowledge identity:

- database primary keys owned by an adapter;
- Neo4j internal identifiers;
- vector-store identifiers;
- document file paths;
- PI tag names;
- equipment tags;
- source-system row identifiers.

External identifiers MAY be preserved through provenance or later adapter-specific mappings.

### Knowledge Provenance Boundary

`KnowledgeProvenance`

SHALL preserve the traceable origin of a knowledge record.

It SHALL contain:

- `source_type: KnowledgeSourceType`;
- `source_reference: str`;
- `captured_at: datetime`.

`source_type` SHALL be a canonical `KnowledgeSourceType`.

`KnowledgeSourceType` SHALL contain one normalized non-empty string value.

`source_reference` SHALL be normalized by removing leading and trailing whitespace and SHALL be non-empty after normalization.

`captured_at` SHALL be timezone-aware.

The domain SHALL normalize `captured_at` to UTC while preserving the represented instant.

Each `KnowledgeRecord` SHALL contain exactly one `KnowledgeProvenance`.

RFC-053 SHALL NOT merge or infer multiple independent provenance sources into one knowledge record.

Cross-record corroboration, derivation and provenance relationships require a future explicit contract.

Provenance records where knowledge came from.

Provenance SHALL NOT by itself establish:

- correctness;
- authorization;
- operational trust;
- reasoning eligibility;
- safety approval;
- lifecycle readiness.

RFC-053 SHALL NOT introduce a client-controlled or source-controlled trusted flag.

### Knowledge Subject Boundary

`KnowledgeSubject`

SHALL provide an optional typed primary contextual reference from a knowledge record to an existing PlantMind domain entity.

It SHALL contain:

- `subject_type: KnowledgeSubjectType`;
- `subject_id: EntityId`.

`subject_type` SHALL be a canonical `KnowledgeSubjectType`.

`KnowledgeSubjectType` SHALL contain one normalized non-empty string value.

`subject_id` SHALL be a canonical `EntityId`.

The subject reference SHALL NOT embed or duplicate the complete referenced domain entity.

The optional subject SHALL identify only the primary contextual subject of the record.

It SHALL NOT be interpreted as an exhaustive relationship model.

Additional knowledge-to-entity relationships require a future explicit relationship or Knowledge Graph contract.

When enterprise knowledge refers to canonical equipment, `subject_id` SHALL use the canonical equipment `EntityId`.

Equipment tag SHALL remain an equipment attribute and SHALL NOT replace domain entity identity.

RFC-053 SHALL NOT create a third equipment model.

### Subject Resolution Boundary

Construction of `KnowledgeSubject` SHALL NOT resolve or load the referenced domain entity.

RFC-053 SHALL NOT require `KnowledgeSubject` construction to call:

- an equipment service;
- a knowledge repository;
- a database;
- a Knowledge Graph;
- an API;
- another domain repository.

RFC-053 SHALL NOT establish referential-integrity verification between `subject_type` and `subject_id`.

The subject contract records a typed canonical reference only.

Verification that a referenced entity exists, is accessible or corresponds to the declared subject type requires a future explicit application or integration contract.

### Equipment Domain Relationship

RFC-053 SHALL preserve:

`app.domain.equipment.Equipment`

as the canonical equipment entity.

RFC-053 SHALL preserve:

`EquipmentSnapshot`

as the immutable point-in-time equipment operational view.

Knowledge records MAY reference equipment through `KnowledgeSubject`.

RFC-053 SHALL NOT:

- move equipment ownership into the knowledge subsystem;
- duplicate equipment lifecycle state;
- duplicate equipment criticality;
- duplicate equipment alarms;
- treat `KnowledgeRecord` as an equipment entity;
- migrate `app.models.equipment.Equipment`;
- promote the existing in-memory `EquipmentService` into production.

Any migration or retirement of the prototype equipment path requires a separate reviewed change.

### Knowledge Repository Port Boundary

RFC-053 SHALL introduce a persistence-neutral:

`KnowledgeRecordRepository`

port.

The repository SHALL own persistence operations for canonical `KnowledgeRecord` instances.

The minimum approved operations SHALL be:

`add(record: KnowledgeRecord) -> None`

and:

`get(record_id: EntityId) -> KnowledgeRecord | None`

`add(...)` SHALL NOT silently overwrite an existing record with the same canonical identity.

A duplicate canonical identity SHALL raise:

`KnowledgeRecordAlreadyExistsError`

`get(...)` SHALL return `None` when the requested canonical identity is not present.

The repository SHALL NOT mutate a supplied immutable `KnowledgeRecord`.

Repository implementations MAY reconstruct an immutable record when reading from persistence.

Python object identity SHALL NOT be required across repository operations.

A successfully retrieved record SHALL preserve the complete canonical domain value of the stored `KnowledgeRecord`.

### Repository Failure Boundary

RFC-053 MAY introduce repository-specific exception contracts required to provide deterministic repository semantics.

At minimum, duplicate canonical identity SHALL be distinguishable from successful storage.

RFC-053 SHALL NOT introduce a platform-wide exception taxonomy.

Unexpected adapter or persistence failures SHALL NOT be converted into synthetic success.

RFC-053 SHALL NOT introduce automatic repository retries.

### Dependency Direction Boundary

The canonical knowledge domain SHALL NOT depend on `KnowledgeRecordRepository`.

`KnowledgeRecordRepository` MAY depend on the canonical knowledge domain types required by its contract.

Future application services MAY depend on `KnowledgeRecordRepository`.

Future infrastructure adapters MAY implement `KnowledgeRecordRepository` and depend on approved persistence technology.

Dependency direction SHALL NOT point from the canonical knowledge domain toward:

- SQLAlchemy;
- PostgreSQL;
- Neo4j;
- Qdrant;
- API transport;
- application orchestration;
- CompositionRoot;
- ServiceContainer.

### Persistence Technology Boundary

`KnowledgeRecordRepository`

SHALL be independent of persistence technology.

RFC-053 SHALL NOT bind the domain or repository port to:

- SQLAlchemy;
- PostgreSQL;
- Neo4j;
- Qdrant;
- Redis;
- filesystem storage;
- cloud object storage;
- a remote API.

`backend/app/database.py`

remains concrete SQLAlchemy infrastructure and SHALL NOT become the enterprise knowledge repository contract.

A future persistence adapter MAY depend on approved infrastructure while implementing the canonical repository port.

RFC-053 SHALL NOT introduce a production persistence adapter.

A test-only in-memory repository implementation MAY be used to verify repository semantics.

Any such in-memory implementation SHALL remain test infrastructure and SHALL NOT be composed, registered or represented as a production knowledge repository.

### Document Knowledge Boundary

RFC-053 SHALL NOT implement document ingestion.

It SHALL NOT implement:

- file upload;
- PDF parsing;
- OCR;
- chunking;
- document versioning;
- document storage;
- document-to-knowledge transformation.

A future document-ingestion boundary MAY construct canonical knowledge records according to the accepted knowledge contract.

The existing empty `document_parser.py` SHALL NOT be treated as a completed Document Library capability.

### Asset Knowledge Boundary

RFC-053 establishes the ability for knowledge to reference an existing domain entity through `KnowledgeSubject`.

It SHALL NOT introduce an Asset Library service or API.

Equipment remains owned by the equipment domain.

Future Asset Library behavior SHALL build on canonical domain identity rather than recreate equipment state inside the knowledge layer.

### Search and Retrieval Boundary

Repository retrieval by canonical `EntityId` is identity lookup.

It is not the PlantMind Search Engine.

RFC-053 SHALL NOT introduce:

- keyword search;
- full-text search;
- filtering language;
- ranking;
- semantic search;
- similarity search;
- hybrid retrieval;
- search-result scoring.

Search requires a future contract.

### Knowledge Graph Boundary

RFC-053 SHALL NOT introduce graph persistence or graph traversal.

A future Knowledge Graph MAY project or relate canonical knowledge records and domain entities.

The Knowledge Graph SHALL NOT automatically become the authoritative owner of knowledge or equipment identity.

The existing in-memory `KnowledgeGraphService` and placeholder `KnowledgeGraphEngine` SHALL NOT be composed into production by RFC-053.

### Vector and Semantic Retrieval Boundary

RFC-053 SHALL NOT introduce:

- embeddings;
- embedding models;
- vector identifiers;
- vector indexing;
- vector similarity;
- Qdrant integration;
- semantic retrieval.

A future vector representation SHALL reference canonical knowledge identity and SHALL NOT replace it.

The existing empty vector-memory and semantic-search files SHALL NOT be treated as implemented capabilities.

### RAG Boundary

RFC-053 SHALL NOT introduce RAG behavior.

It SHALL NOT:

- construct prompts;
- invoke an LLM;
- perform retrieval-augmented generation;
- treat generated output as authoritative stored knowledge;
- create an AI answer endpoint.

A future RAG boundary SHALL consume approved retrieval output without becoming the canonical knowledge repository.

The existing empty `rag_engine.py` SHALL NOT be treated as an implemented AI Knowledge Engine.

### Reasoning Integration Boundary

RFC-053 SHALL NOT modify:

- `ReasoningEngine`;
- `ReasoningPipeline`;
- reasoning builders;
- `Observation`;
- `ReasoningResult`;
- operational workload execution.

The current reasoning path remains observation-based.

RFC-053 SHALL NOT inject knowledge directly into reasoning without a separate accepted integration contract.

Reasoning SHALL remain a consumer of approved inputs and SHALL NOT become the owner of enterprise knowledge persistence.

### Application Service Boundary

RFC-053 SHALL NOT introduce a production knowledge application service.

The domain and repository port SHALL be established before application use cases are approved.

A future knowledge application service SHALL depend on the canonical repository port rather than SQLAlchemy, Neo4j, Qdrant or prototype in-memory services directly.

### Composition Boundary

RFC-053 SHALL NOT modify production `CompositionRoot`.

No production repository adapter exists yet.

RFC-053 SHALL NOT create hidden global knowledge infrastructure.

A future composition contract SHALL explicitly provide the canonical repository implementation and preserve dependency identity.

### ServiceContainer Boundary

RFC-053 SHALL NOT register a production knowledge repository or application service in `ServiceContainer`.

Future registration SHALL occur only after the corresponding production composition contract is accepted.

### API Boundary

RFC-053 introduces no HTTP endpoint and no transport schema.

The API layer SHALL NOT directly create persistence infrastructure or become the owner of knowledge-domain rules.

Future knowledge APIs SHALL delegate through approved application boundaries.

### Security and Trust Boundary

Stored knowledge SHALL NOT automatically become trusted operational evidence.

Knowledge provenance and operational evidence are separate concepts.

RFC-053 SHALL NOT:

- create authorization bypasses;
- create a trusted knowledge flag controlled by clients;
- grant knowledge records lifecycle authority;
- treat stored knowledge as mandatory-capability evidence;
- expose unrestricted enterprise knowledge through a new API.

RBAC, data-permission filtering and source-specific authorization remain future integration responsibilities unless already governed by accepted platform architecture.

### State and Persistence Semantics

`KnowledgeRecord` SHALL remain immutable after construction.

RFC-053 SHALL provide additive repository semantics only.

RFC-053 SHALL NOT introduce:

- record update;
- record deletion;
- knowledge supersession;
- knowledge version chains;
- retention policy;
- archival policy;
- persistent search indexes;
- persistent graph state;
- persistent vector state.

Those capabilities require explicit future contracts.

### Failure Semantics

Domain validation failures SHALL remain domain failures.

A domain validation failure SHALL prevent repository storage.

Duplicate canonical identity SHALL fail rather than silently overwrite an existing record.

Unexpected repository failures SHALL propagate to the caller.

RFC-053 SHALL NOT:

- retry storage automatically;
- fabricate a stored record;
- silently discard a failure;
- fall back to a prototype knowledge service;
- write the same record through multiple persistence paths.

### Prototype and Legacy Containment

The following existing components SHALL NOT be interpreted as canonical production knowledge infrastructure merely because they exist in the repository:

- `app.models.equipment.Equipment`;
- `EquipmentService`;
- `KnowledgeGraphService`;
- `KnowledgeGraphEngine`;
- empty knowledge parser modules;
- empty graph modules;
- empty RAG modules;
- empty semantic-search modules;
- empty knowledge-memory modules;
- empty vector-memory modules;
- empty knowledge-agent modules.

RFC-053 SHALL NOT delete, rename or migrate these components unless required by the accepted RFC-053 implementation and separately verified against existing dependencies.

Preserve-before-delete remains authoritative.

### Migration Boundary

RFC-053 establishes the canonical future direction without performing broad legacy migration.

Future migration work SHALL identify:

- the legacy responsibility;
- the canonical replacement responsibility;
- dependency impact;
- compatibility requirements;
- removal conditions.

No prototype component SHALL be silently redirected to the new knowledge domain.

### PI and Operational Data Boundary

RFC-053 SHALL NOT introduce:

- PI Web API communication;
- PI authentication;
- PI certificate handling;
- PI connectivity probes;
- production PI availability sources;
- automatic conversion of PI values into enterprise knowledge;
- automatic conversion of `Observation` into `KnowledgeRecord`.

PI operational data and enterprise knowledge remain separate architectural concepts.

Any future transformation between them requires an explicit accepted boundary.

### Lifecycle Boundary

RFC-053 SHALL NOT modify:

- Runtime states;
- Runtime readiness;
- request admission;
- mandatory-capability policy;
- mandatory-capability availability;
- operational-transition evidence;
- Bootstrap behavior;
- Health behavior.

The knowledge foundation SHALL NOT become a mandatory operational capability merely because the domain contracts exist.

Runtime remains the sole lifecycle-transition authority.

### Non-Goals

RFC-053 SHALL NOT:

- implement Document Library;
- implement Asset Library;
- implement Search Engine;
- implement Knowledge Graph persistence;
- implement semantic search;
- implement vector storage;
- implement RAG;
- invoke an LLM;
- implement PI production connectivity;
- implement a production knowledge database adapter;
- modify `database.py`;
- redesign the equipment domain;
- redesign the reasoning subsystem;
- add a knowledge HTTP API;
- add knowledge application orchestration;
- modify CompositionRoot production wiring;
- modify ServiceContainer production registration;
- introduce record update or deletion;
- introduce automatic retry;
- introduce another source of operational lifecycle authority.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- `KnowledgeRecord` uses canonical `EntityId`;
- `KnowledgeRecord` is immutable;
- `KnowledgeKind` rejects empty or whitespace-only values;
- `KnowledgeKind` trims leading and trailing whitespace and normalizes alphabetic characters to lowercase;
- `KnowledgeKind` preserves internal whitespace and characters;
- title validation rejects empty or whitespace-only values;
- content validation rejects empty or whitespace-only values;
- title and content normalization removes only leading and trailing whitespace;
- internal content whitespace and line breaks are preserved;
- `KnowledgeSourceType` rejects empty or whitespace-only values;
- `KnowledgeSourceType` trims leading and trailing whitespace and normalizes alphabetic characters to lowercase;
- `KnowledgeSourceType` preserves internal whitespace and characters;
- `KnowledgeProvenance` rejects empty source reference;
- provenance timestamps require timezone information;
- provenance timestamps normalize to UTC;
- `KnowledgeSubjectType` rejects empty or whitespace-only values;
- `KnowledgeSubjectType` trims leading and trailing whitespace and normalizes alphabetic characters to lowercase;
- `KnowledgeSubjectType` preserves internal whitespace and characters;
- `KnowledgeSubject.subject_id` references canonical `EntityId`;
- `KnowledgeSubject` construction performs no entity lookup or external resolution;
- knowledge records may exist without a subject;
- an optional knowledge subject is a primary contextual reference and not an exhaustive relationship model;
- subject construction does not establish referential integrity or prove referenced-entity existence;
- knowledge records may reference canonical equipment identity without embedding the equipment object;
- no third equipment model is introduced;
- `KnowledgeRecordRepository` exposes the approved identity-based add and get operations;
- repository add does not mutate the supplied immutable record;
- successful add and get preserve complete domain-value equivalence without requiring Python object identity;
- duplicate canonical identity raises `KnowledgeRecordAlreadyExistsError`;
- missing identity lookup returns `None`;
- repository semantics do not silently overwrite;
- RFC-053 domain validation failures use `DomainException` or a domain-specific subtype;
- `KnowledgeRecordAlreadyExistsError` remains a repository-boundary failure rather than a domain-validation failure;
- the canonical knowledge domain does not depend on the repository port;
- the canonical knowledge domain does not depend on SQLAlchemy;
- the canonical repository port does not depend on SQLAlchemy;
- the canonical knowledge domain does not depend on Neo4j;
- the canonical knowledge domain does not depend on Qdrant;
- the canonical knowledge domain does not depend on an LLM;
- no production knowledge repository is composed by `CompositionRoot`;
- no production knowledge service is registered in `ServiceContainer`;
- existing Runtime and operational-transition behavior remains unchanged;
- existing reasoning behavior remains unchanged;
- existing equipment-domain behavior remains unchanged.

### Verification

- Contract Acceptance Review: passed.
- Architecture decision: AD-039.
- Production implementation: not started.
- TDD: not started.
- Pre-RFC-053 full regression baseline: 432 passed.
- `git diff --check`: passed before acceptance update.

### Next Exact Action

Commit and remote-verify the accepted RFC-053 contract together with AD-039.

After contract commit verification and a clean working tree, begin RFC-053 TDD before any production implementation.

---

## RFC-052 — Explicit Operational Transition API Boundary

### Status

Complete.

### Objective

Establish the canonical HTTP transport boundary for an explicit operational-transition request by accepting transport-level observation input, mapping that input into existing immutable domain `Observation` objects, and delegating exactly once to the canonical `OperationalTransitionApplicationService`, without moving workload orchestration, workload-evidence trust, capability evaluation, or Runtime lifecycle authority into the API layer.

### Architectural Position

RFC-041 established `ApplicationFacade` as the canonical operational workload entry boundary.

RFC-046 established trusted correlated `OperationalWorkloadEvidence` produced by the approved workload execution path.

RFC-048 established Runtime as the sole authoritative `READY` to `OPERATIONAL` lifecycle-transition authority.

RFC-050 established `OperationalTransitionCoordinator` as the canonical transition-evidence coordination boundary.

RFC-051 established `OperationalTransitionApplicationService` as the canonical explicit application use-case boundary joining workload execution and operational-transition coordination.

RFC-051 intentionally did not introduce an HTTP endpoint and reserved transport-specific request schemas for a future external-interface RFC.

RFC-052 SHALL provide that transport boundary without duplicating or bypassing any established application or lifecycle responsibility.

### HTTP Operation

RFC-052 SHALL introduce:

`POST /operational-transition`

The endpoint SHALL represent one explicit request to execute the approved operational workload and request the resulting operational transition.

A successful request SHALL return:

`204 No Content`

The HTTP response SHALL NOT expose internal `WorkflowExecution`, `OperationalWorkloadEvidence`, `OperationalTransitionEvidence`, mandatory-capability observations, or Runtime-internal evidence structures.

### Request Schema

RFC-052 SHALL introduce a transport-only request schema containing:

`observations`

The observations collection SHALL preserve client-supplied ordering.

Each transport observation SHALL contain the information required to construct the existing domain `Observation`:

- `source`;
- `observation_type`;
- `value`;
- `observed_at`.

The transport schema SHALL NOT replace the domain `Observation`.

The transport schema SHALL NOT become an alternate domain model.

### Observation Mapping Boundary

The API boundary SHALL map each accepted transport observation into exactly one existing immutable domain `Observation`.

Observation ordering SHALL be preserved.

The resulting tuple of domain observations SHALL be supplied unchanged to:

`OperationalTransitionApplicationService.request_operational(...)`

exactly once.

Domain `Observation` remains authoritative for domain validation and normalization.

The API layer SHALL NOT:

- reinterpret observation meaning;
- normalize observation values independently;
- fabricate observations;
- enrich observations from external systems;
- infer missing observations;
- create workload evidence.

Transport deserialization and transport-to-domain mapping are the only observation responsibilities introduced by RFC-052.

### Application Service Boundary

The endpoint SHALL depend on the exact canonical:

`OperationalTransitionApplicationService`

composed by `CompositionRoot`.

The API layer SHALL NOT construct a second application service.

It SHALL NOT independently construct or resolve alternate instances of:

- `ApplicationFacade`;
- `OperationalTransitionCoordinator`;
- `Runtime`;
- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityCoverageEvaluator`.

The endpoint SHALL invoke:

`OperationalTransitionApplicationService.request_operational(...)`

exactly once per accepted request.

### Workload Evidence Trust Boundary

The API SHALL NOT accept:

- workload identifiers;
- `ApplicationFacadeEntryEvidence`;
- `WorkflowExecutionStartEvidence`;
- `OperationalWorkloadEvidence`;
- `OperationalTransitionEvidence`;
- capability-coverage evidence.

The client SHALL have no authority to construct or supply trusted internal operational-transition evidence.

All workload evidence SHALL continue to originate from the canonical workload execution path established by RFC-046 and consumed through RFC-051.

### Runtime Authority Boundary

RFC-052 SHALL NOT call:

`Runtime.request_operational(...)`

directly.

The API SHALL NOT:

- inspect Runtime readiness to decide transition eligibility;
- inspect Runtime lifecycle state to reproduce transition rules;
- enable request admission;
- disable request admission;
- mark Runtime operational;
- construct transition evidence;
- evaluate mandatory capabilities;
- establish independent lifecycle authority.

Runtime remains the sole authoritative lifecycle-transition owner.

### Request Admission Boundary

`POST /operational-transition`

SHALL remain subject to the existing `RequestAdmissionMiddleware`.

The endpoint SHALL NOT be added to:

`DEFAULT_ADMISSION_EXEMPT_PATHS`

RFC-052 SHALL NOT alter existing Runtime-owned request-admission semantics.

If operational request admission is disabled, the existing middleware SHALL reject the request before the operational-transition endpoint executes.

### Success Semantics

A successful endpoint request SHALL mean that:

- transport input was accepted;
- domain observations were constructed;
- the canonical application service completed successfully;
- the authoritative transition path completed successfully.

The endpoint SHALL then return:

`204 No Content`

The endpoint SHALL NOT independently mutate Runtime after the application service returns.

### Validation Semantics

FastAPI and the approved transport schema SHALL remain responsible for transport deserialization and structural request validation.

Domain `Observation` SHALL remain responsible for its existing domain invariants.

The API layer MAY translate a domain observation-construction validation failure into an appropriate client validation response.

RFC-052 SHALL NOT duplicate domain validation rules inside a second business-validation model.

### Failure Semantics

If observation mapping fails:

- the application service SHALL NOT be invoked;
- no operational-transition request SHALL occur.

If `OperationalTransitionApplicationService.request_operational(...)` raises:

- the exception SHALL NOT cause an automatic retry;
- the application service SHALL NOT be invoked a second time;
- the API SHALL NOT independently repeat workload execution;
- the API SHALL NOT independently request a Runtime transition;
- no synthetic success response SHALL be returned.

RFC-052 SHALL NOT introduce a new platform-wide exception taxonomy.

Existing lower-layer failure atomicity and fail-closed semantics remain authoritative.

### Router Composition Boundary

The operational-transition HTTP boundary SHALL be explicitly composed into the FastAPI application using the exact canonical application-service instance supplied by `PlatformComposition`.

Router composition SHALL preserve dependency identity.

The API module SHALL NOT import or build an independent `CompositionRoot`.

The API module SHALL NOT create hidden global platform infrastructure.

### Bootstrap Boundary

Bootstrap SHALL NOT invoke the operational-transition endpoint or its application service automatically.

RFC-052 SHALL NOT introduce startup-triggered transition behavior.

### Health Boundary

Health endpoints SHALL remain observational.

Health SHALL NOT invoke the operational-transition application service.

Health SHALL NOT initiate an operational transition.

### PI and External Connectivity Boundary

RFC-052 SHALL NOT introduce:

- PI Web API network communication;
- PI authentication;
- PI certificate handling;
- PI connectivity probes;
- connector lifecycle changes;
- capability availability sources;
- mandatory-capability deployment policy.

Existing mock-before-production integration architecture remains unchanged.

### State and Persistence Boundary

The API boundary SHALL remain stateless between requests.

It SHALL NOT persist:

- observations;
- workflow executions;
- workload evidence;
- transition evidence;
- transition eligibility;
- Runtime lifecycle state;
- retry state.

### Non-Goals

RFC-052 SHALL NOT:

- redesign `ApplicationFacade`;
- redesign `OperationalTransitionApplicationService`;
- redesign `OperationalTransitionCoordinator`;
- modify Runtime transition semantics;
- modify request-admission semantics;
- modify mandatory-capability observation semantics;
- modify mandatory-capability policy semantics;
- modify mandatory-capability coverage semantics;
- introduce trusted PI connectivity;
- introduce production capability availability sources;
- introduce automatic operational transition;
- expose internal transition evidence over HTTP;
- introduce retries;
- introduce recovery;
- introduce traffic draining;
- introduce `DEGRADED` behavior;
- introduce persistent transition history;
- introduce another lifecycle authority.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- the endpoint is exposed as `POST /operational-transition`;
- the endpoint remains behind Runtime request admission;
- the endpoint is not admission-exempt;
- closed admission prevents application-service invocation;
- accepted transport observations map into domain `Observation` objects;
- observation order is preserved;
- timezone-aware observation timestamps reach the domain boundary correctly;
- domain observation validation failures do not invoke the application service;
- the canonical `OperationalTransitionApplicationService` is invoked exactly once;
- the service receives the exact mapped observation tuple;
- no workload evidence is accepted from client input;
- no transition evidence is accepted from client input;
- successful application execution returns `204 No Content`;
- internal workflow and transition evidence are not serialized into the response;
- application-service failure is not retried;
- application-service failure does not produce synthetic success;
- the API does not call Runtime directly;
- the API does not evaluate mandatory capabilities directly;
- the API does not create a second application-service instance;
- FastAPI composition uses the exact canonical application-service instance;
- Bootstrap does not invoke the endpoint use case;
- Health does not invoke the endpoint use case;
- existing root and health behavior remains unchanged;
- existing request-admission behavior remains unchanged.

### Verification

- Contract commit: `f9b0816`
- Technical commit: `62bb854`
- Architecture decision: AD-038
- Focused RFC-052 suite: 16 passed
- API regression: 25 passed
- Impacted API/services/core regression: 373 passed
- Full regression: 432 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Canonical operational-transition HTTP boundary: introduced
- `POST /operational-transition`: introduced
- Successful response: `204 No Content`
- Client-supplied workload and transition evidence: rejected
- Runtime-owned request admission: preserved
- Bootstrap-triggered transition: not introduced
- Health-triggered transition: not introduced
- Runtime remains sole operational-transition authority

### Next Exact Action

RFC-052 is complete.

The required post-RFC-052 Source-of-Truth architecture review is complete. Subsequent active architecture work proceeds through RFC-053 contract definition.

---

## RFC-051 — Explicit Operational Transition Application Boundary

### Status

Complete.

### Objective

Establish a canonical application-level boundary for an explicit operational-transition use case that executes an approved operational workload through `ApplicationFacade`, obtains the trusted `OperationalWorkloadEvidence` produced by that execution, and delegates the explicit transition request to `OperationalTransitionCoordinator`, without moving workload-evidence trust, lifecycle authority, or orchestration responsibility into the API transport layer.

### Architectural Position

RFC-041 established `ApplicationFacade` as the canonical application-level operational workload entry boundary.

RFC-046 established correlated `OperationalWorkloadEvidence` produced by the approved workload execution path.

RFC-048 established Runtime as the sole authoritative `READY` to `OPERATIONAL` lifecycle-transition authority.

RFC-050 established `OperationalTransitionCoordinator` as the canonical evidence coordination boundary.

The remaining application-level gap is an explicit use-case boundary that connects:

`ApplicationFacade`

to:

`OperationalTransitionCoordinator`

without making FastAPI, another external interface, or the client responsible for workload evidence construction or application orchestration.

### Application Service

RFC-051 SHALL introduce:

`OperationalTransitionApplicationService`

The service SHALL depend on the exact canonical instances of:

- `ApplicationFacade`;
- `OperationalTransitionCoordinator`.

The service SHALL coordinate one explicit application use case.

It SHALL NOT replace `ApplicationFacade` as the canonical workload-entry boundary.

### Public Operation

The approved application operation SHALL be:

`request_operational(observations: tuple[Observation, ...]) -> OperationalTransitionApplicationResult`

The operation SHALL be explicit.

It SHALL execute the workload through:

`ApplicationFacade.analyze(...)`

exactly once.

It SHALL then obtain:

`WorkflowExecution.operational_workload_evidence`

from the returned canonical `WorkflowExecution`.

It SHALL delegate that exact workload-evidence object, including `None`, to:

`OperationalTransitionCoordinator.request_operational(...)`

exactly once.

### Observation Input Boundary

RFC-051 SHALL consume existing immutable `Observation` domain objects.

RFC-051 SHALL NOT introduce a duplicate observation model.

Observation validation remains owned by `Observation`.

The application service SHALL NOT:

- reinterpret observations;
- normalize observation values;
- change observation timestamps;
- fabricate observations;
- perform transport-layer deserialization.

Transport-specific request schemas remain a separate future interface concern.

### Workload Execution Boundary

`ApplicationFacade` remains the canonical operational workload entry boundary.

`OperationalTransitionApplicationService` SHALL call the composed `ApplicationFacade`.

It SHALL NOT directly call:

- `IntegrationGateway`;
- `OrchestrationService`;
- `WorkflowExecutor`;
- reasoning services;
- presentation services.

The service SHALL NOT construct an alternate workload execution path.

### Workload Evidence Trust Boundary

The application service SHALL obtain workload evidence only from the `WorkflowExecution` returned by the canonical `ApplicationFacade` path.

It SHALL NOT:

- create workload identifiers;
- create `ApplicationFacadeEntryEvidence`;
- create `WorkflowExecutionStartEvidence`;
- create `OperationalWorkloadEvidence`;
- reconstruct workload evidence;
- accept workload evidence from an external client;
- accept workload evidence as an independent public input;
- validate UUID correlation independently;
- infer evidence from workflow stages.

Workload evidence remains owned by RFC-046.

### Evidence Handoff

The exact value of:

`WorkflowExecution.operational_workload_evidence`

SHALL be supplied unchanged to:

`OperationalTransitionCoordinator.request_operational(...)`.

The application service SHALL NOT copy, normalize, reconstruct, replace, or reinterpret the workload evidence.

If the workflow execution contains `None` workload evidence, `None` SHALL be delegated unchanged.

Fail-closed evaluation remains owned by the coordinator and Runtime chain.

### Transition Coordination Boundary

The application service SHALL NOT construct `OperationalTransitionEvidence`.

It SHALL NOT:

- observe mandatory capabilities directly;
- evaluate mandatory-capability coverage;
- inspect mandatory-capability policy;
- inspect Runtime state;
- inspect Runtime readiness;
- inspect request admission;
- call `Runtime.request_operational(...)` directly.

Those responsibilities remain owned by RFC-043 through RFC-050.

### Application Result

RFC-051 SHALL introduce an immutable:

`OperationalTransitionApplicationResult`

The result SHALL contain:

- the exact `WorkflowExecution` returned by `ApplicationFacade`;
- the exact `OperationalTransitionEvidence` returned by `OperationalTransitionCoordinator`.

The result SHALL preserve object identity.

It SHALL NOT become:

- lifecycle state;
- transition authority;
- persistent transition history;
- eligibility state.

### Successful Request

When workload execution and operational-transition coordination both succeed:

- the exact `WorkflowExecution` returned by `ApplicationFacade` SHALL be preserved;
- the exact transition evidence returned by the coordinator SHALL be preserved;
- the application service SHALL return one immutable application result;
- no additional Runtime mutation SHALL occur.

Runtime remains responsible for the actual lifecycle transition.

### Workload Failure Semantics

If `ApplicationFacade.analyze(...)` raises:

- the exception SHALL propagate;
- `OperationalTransitionCoordinator` SHALL NOT be called;
- the application service SHALL NOT retry;
- no synthetic workload evidence SHALL be created;
- no operational-transition request SHALL be attempted.

### Transition Failure Semantics

If `OperationalTransitionCoordinator.request_operational(...)` raises:

- the exception SHALL propagate;
- the application service SHALL NOT retry;
- workload execution SHALL NOT be repeated;
- workload evidence SHALL NOT be replaced;
- Runtime state SHALL NOT be modified independently;
- request admission SHALL NOT be modified independently.

Existing RFC-048 and RFC-050 failure semantics remain authoritative.

### No Automatic Lifecycle Side Effects

RFC-051 SHALL NOT modify `ApplicationFacade.analyze(...)` to automatically request an operational transition.

Normal calls to:

`ApplicationFacade.analyze(...)`

remain workload-only operations.

The new application service SHALL be invoked only when the caller explicitly requests the combined operational-transition use case.

### Composition Boundary

`CompositionRoot` SHALL compose exactly one `OperationalTransitionApplicationService` using the existing canonical:

- `ApplicationFacade`;
- `OperationalTransitionCoordinator`.

The exact service instance SHALL be:

- exposed through `PlatformComposition`;
- registered in `ServiceContainer`.

The service SHALL preserve exact dependency identity.

CompositionRoot SHALL NOT execute the service during build.

### API Boundary

RFC-051 SHALL NOT introduce an HTTP endpoint.

RFC-051 SHALL NOT modify FastAPI routing.

RFC-051 SHALL NOT make the API hosting layer responsible for:

- constructing workload evidence;
- extracting internal transition evidence;
- calling Runtime directly;
- coordinating internal workflow components.

A future external-interface RFC MAY expose the approved application service through HTTP or another transport.

That future interface SHALL remain behind Runtime-owned request-admission enforcement unless separately architecture-approved.

### Bootstrap and Health Boundaries

Bootstrap SHALL NOT invoke `OperationalTransitionApplicationService`.

Health SHALL NOT invoke `OperationalTransitionApplicationService`.

RFC-051 introduces no startup-triggered or health-triggered operational transition.

### State and Persistence Boundary

`OperationalTransitionApplicationService` SHALL remain stateless between calls.

It SHALL NOT maintain:

- last workflow execution;
- last workload evidence;
- last transition evidence;
- transition history;
- retry queues;
- lifecycle state;
- operational eligibility state.

### Dependency Identity

The application service `ApplicationFacade` dependency SHALL be the same object as:

`PlatformComposition.application_facade`

The application service coordinator dependency SHALL be the same object as:

`PlatformComposition.operational_transition_coordinator`

No duplicate workload or transition dependency graph SHALL be introduced.

### Non-Goals

RFC-051 SHALL NOT:

- introduce an HTTP endpoint;
- introduce API request schemas;
- modify Runtime transition semantics;
- modify request-admission semantics;
- modify `OperationalTransitionCoordinator` evidence semantics;
- modify workload evidence semantics;
- modify capability observation semantics;
- modify mandatory-capability policy semantics;
- modify mandatory-capability coverage semantics;
- create workload evidence from client input;
- automatically transition after every workload execution;
- introduce retries;
- introduce recovery;
- introduce `DEGRADED` behavior;
- introduce traffic draining;
- persist transition evidence;
- introduce another lifecycle authority.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- the application service accepts canonical `Observation` tuples;
- `ApplicationFacade.analyze(...)` is called exactly once;
- the exact observation tuple is passed unchanged to `ApplicationFacade`;
- the exact `WorkflowExecution` returned by `ApplicationFacade` is preserved;
- the exact `operational_workload_evidence` from that execution is supplied to the coordinator;
- `None` workload evidence is supplied unchanged;
- workload evidence is not reconstructed;
- coordinator invocation occurs exactly once;
- the exact transition evidence returned by the coordinator is preserved;
- successful execution returns an immutable application result;
- workload failure prevents coordinator invocation;
- workload failure is propagated without retry;
- coordinator failure is propagated without retry;
- coordinator failure does not repeat workload execution;
- the service does not inspect Runtime lifecycle state;
- the service does not inspect request admission;
- the service does not call Runtime directly;
- normal `ApplicationFacade.analyze(...)` remains free of automatic transition side effects;
- CompositionRoot exposes exactly one application service;
- ServiceContainer resolves that same application service;
- the service uses the exact composed `ApplicationFacade`;
- the service uses the exact composed `OperationalTransitionCoordinator`;
- CompositionRoot does not execute the service during build;
- Bootstrap does not execute the service;
- Health does not execute the service;
- no persistent application-transition state is introduced;
- no independent lifecycle authority is introduced.

### Next Exact Action

RFC-051 is complete. Subsequent architecture work proceeded through RFC-052.

---

## RFC-050 — Operational Transition Coordination Contract

### Status

Complete.

### Objective

Establish the explicit operational-transition coordination boundary that consumes approved operational-workload evidence, obtains live mandatory-capability availability observations, evaluates mandatory-capability coverage, constructs `OperationalTransitionEvidence`, and delegates the authoritative lifecycle-transition decision to `Runtime.request_operational(...)`, while preserving Runtime as the sole lifecycle-transition authority and avoiding hidden workload-triggered lifecycle side effects.

### Architectural Position

RFC-046 established correlated `OperationalWorkloadEvidence`.

RFC-043 through RFC-045 established:

- capability availability observation;
- mandatory-capability policy;
- mandatory-capability coverage evaluation.

RFC-047 established immutable `OperationalTransitionEvidence`.

RFC-048 established guarded Runtime `READY` to `OPERATIONAL` transition authority.

RFC-049 established explicit deployment-neutral composition of capability sources and mandatory-capability policy.

All required transition components now exist.

The remaining gap is an explicit coordinator that composes these existing responsibilities without becoming a competing lifecycle authority.

### Coordinator

RFC-050 SHALL introduce:

`OperationalTransitionCoordinator`

The coordinator SHALL depend on the existing canonical instances of:

- `Runtime`;
- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityCoverageEvaluator`.

The coordinator SHALL NOT own:

- Runtime lifecycle state;
- request admission;
- mandatory-capability policy;
- capability source definitions;
- workload execution;
- workload evidence generation.

### Public Operation

The approved coordination operation SHALL be:

`request_operational(workload_evidence: OperationalWorkloadEvidence | None) -> OperationalTransitionEvidence`

The operation SHALL be explicit.

It SHALL NOT be invoked automatically by workload execution, Bootstrap, Health or CompositionRoot construction.

### Workload Evidence Input Boundary

The coordinator SHALL consume `OperationalWorkloadEvidence` directly.

RFC-050 SHALL NOT require or accept `WorkflowExecution` as the authoritative coordination input.

The caller remains responsible for obtaining workload evidence from the approved workload execution path.

The coordinator SHALL NOT:

- create workload identities;
- recreate workload evidence;
- validate UUID correlation independently;
- execute workflows;
- inspect workflow stages;
- reinterpret workload provenance.

Those responsibilities remain owned by RFC-046.

A `None` workload evidence input SHALL remain representable as incomplete external transition evidence.

### Observation Snapshot

Each explicit coordination request SHALL obtain one availability observation snapshot by calling:

`CapabilityAvailabilityObserver.observe_all()`

exactly once.

The returned observation tuple SHALL be supplied unchanged to the canonical `MandatoryCapabilityCoverageEvaluator`.

RFC-050 SHALL NOT:

- invoke individual capability sources directly;
- obtain multiple snapshots for one request;
- merge snapshots;
- retry observations;
- cache observations;
- reorder observations;
- apply freshness or TTL rules.

### Capability Coverage

The coordinator SHALL call the existing:

`MandatoryCapabilityCoverageEvaluator.evaluate(...)`

exactly once per coordination request.

The evaluator SHALL receive the exact observation snapshot returned by the observer.

The coordinator SHALL NOT:

- inspect mandatory-capability policy directly;
- classify observations itself;
- alter coverage diagnostics;
- convert `UNSATISFIED` into another state;
- fabricate satisfied coverage.

Coverage semantics remain owned by RFC-045.

### Transition Evidence Construction

After coverage evaluation, the coordinator SHALL construct one immutable:

`OperationalTransitionEvidence`

using:

- the exact supplied `OperationalWorkloadEvidence` object, including `None`;
- the exact `MandatoryCapabilityCoverageResult` returned by the evaluator.

The coordinator SHALL preserve object identity.

It SHALL NOT reconstruct, copy, normalize or reinterpret either evidence category.

### Runtime Delegation

The coordinator SHALL delegate the constructed evidence to:

`Runtime.request_operational(...)`

exactly once.

The exact `OperationalTransitionEvidence` instance constructed by the coordinator SHALL be supplied to Runtime.

Runtime remains the sole lifecycle-transition authority.

The coordinator SHALL NOT inspect or duplicate Runtime-owned preconditions before delegation, including:

- lifecycle state;
- readiness;
- request admission.

Runtime remains responsible for evaluating those conditions directly.

### Successful Coordination

When Runtime accepts the transition:

- Runtime SHALL enter `RuntimeState.OPERATIONAL` according to RFC-048;
- the coordinator SHALL return the exact `OperationalTransitionEvidence` instance supplied to Runtime;
- the coordinator SHALL retain no mutable transition state;
- no additional lifecycle mutation SHALL occur.

The returned evidence is a coordination result and SHALL NOT become a second lifecycle authority.

### Rejected Coordination

If Runtime rejects the transition:

- Runtime SHALL remain governed by RFC-048 atomic rejection semantics;
- the coordinator SHALL propagate the Runtime failure;
- the coordinator SHALL NOT retry;
- the coordinator SHALL NOT alter Runtime state;
- the coordinator SHALL NOT enable or disable request admission;
- the coordinator SHALL NOT mutate evidence;
- the coordinator SHALL NOT convert the rejection into `FAILED`, `STOPPED` or `DEGRADED`.

### Observer Failure Boundary

Capability-source exceptions remain contained by `CapabilityAvailabilityObserver` according to RFC-043.

The coordinator SHALL consume the observer output normally, including `UNKNOWN` observations.

RFC-050 SHALL NOT bypass observer exception containment.

### Unexpected Coordination Failures

If availability observation or coverage evaluation cannot return normally because of an unexpected coordinator dependency failure:

- Runtime SHALL NOT be called;
- no lifecycle transition SHALL be attempted;
- the exception SHALL propagate;
- RFC-050 SHALL NOT retry automatically.

No partial lifecycle side effect SHALL occur before Runtime delegation.

### No Automatic Lifecycle Side Effects

RFC-050 SHALL NOT modify:

- `ApplicationFacade.analyze(...)`;
- `IntegrationGateway.execute(...)`;
- `OrchestrationService.run(...)`;
- `WorkflowExecutor.execute(...)`.

A successful operational workload SHALL NOT automatically request an operational lifecycle transition.

The explicit coordinator operation remains required.

### Bootstrap Boundary

Bootstrap SHALL NOT invoke `OperationalTransitionCoordinator`.

Startup remains responsible only for the existing readiness and request-admission sequence.

Bootstrap SHALL NOT automatically enter `OPERATIONAL`.

### Health Boundary

`HealthCapability` remains read-only reporting.

Health SHALL NOT invoke the coordinator or Runtime operational transition.

### Composition Boundary

`CompositionRoot` SHALL compose exactly one `OperationalTransitionCoordinator` using the existing canonical instances of:

- Runtime;
- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityCoverageEvaluator`.

The exact coordinator instance SHALL be:

- exposed through `PlatformComposition`;
- registered in `ServiceContainer`.

CompositionRoot SHALL NOT execute the coordinator during build.

Composition SHALL NOT create duplicate observer, evaluator or Runtime instances for the coordinator.

### Dependency Identity

The coordinator SHALL retain the exact composed dependency instances.

The coordinator Runtime SHALL be the same object as:

`PlatformComposition.runtime`

The coordinator observer SHALL be the same object as:

`PlatformComposition.availability_observer`

The coordinator coverage evaluator SHALL be the same object as:

`PlatformComposition.mandatory_capability_coverage_evaluator`

RFC-050 SHALL preserve one canonical dependency graph.

### No Persistent Evidence Store

RFC-050 SHALL NOT introduce:

- global transition evidence;
- persistent transition evidence;
- mutable last-transition state;
- evidence history;
- evidence recorder;
- transition retry queue.

Each coordination request SHALL operate only on its explicit workload evidence and one current capability observation snapshot.

### No Independent Eligibility Authority

RFC-050 SHALL NOT introduce:

- `OperationalEligibilityEvaluator`;
- operational eligibility state;
- another operational readiness boolean;
- another lifecycle controller.

The coordinator coordinates evidence and delegates.

Runtime decides.

### Implementation Scope

RFC-050 MAY implement:

- `OperationalTransitionCoordinator`;
- explicit `request_operational(...)`;
- one observation snapshot per request;
- one mandatory-capability coverage evaluation per request;
- one `OperationalTransitionEvidence` construction per request;
- one Runtime transition delegation per request;
- canonical CompositionRoot wiring;
- focused coordination tests;
- impacted regression tests.

### Non-Goals

RFC-050 SHALL NOT:

- modify `Runtime.request_operational(...)`;
- modify operational workload evidence semantics;
- modify capability availability semantics;
- modify mandatory-capability policy semantics;
- modify mandatory-capability coverage semantics;
- introduce concrete deployment capability sources;
- hard-code deployment-specific capability names;
- automatically execute workflows;
- automatically transition after workload execution;
- transition during Bootstrap;
- transition during CompositionRoot construction;
- introduce evidence freshness or TTL;
- introduce retry behavior;
- introduce operational recovery;
- introduce `DEGRADED` behavior;
- introduce traffic draining;
- persist operational-transition evidence.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- coordinator accepts `OperationalWorkloadEvidence` directly;
- coordinator does not require `WorkflowExecution`;
- one availability snapshot is obtained per coordination request;
- observer output identity/order is passed unchanged to coverage evaluation;
- one coverage evaluation occurs per request;
- exact supplied workload evidence identity is preserved;
- exact produced coverage-result identity is preserved;
- constructed `OperationalTransitionEvidence` contains those exact objects;
- exact constructed transition-evidence instance is supplied to Runtime;
- Runtime transition delegation occurs exactly once;
- coordinator does not inspect Runtime lifecycle state before delegation;
- coordinator does not inspect request admission before delegation;
- successful coordination returns the exact transition-evidence instance;
- incomplete workload evidence remains fail-closed through Runtime;
- unsatisfied coverage remains fail-closed through Runtime;
- Runtime rejection is propagated without retry;
- rejected coordination does not alter admission independently;
- observer source failure continues to become `UNKNOWN`;
- unexpected observation failure prevents Runtime delegation;
- unexpected coverage-evaluation failure prevents Runtime delegation;
- no automatic transition occurs during CompositionRoot build;
- no automatic transition occurs during Bootstrap startup;
- no automatic transition occurs during `ApplicationFacade.analyze(...)`;
- CompositionRoot exposes one coordinator instance;
- ServiceContainer resolves that same coordinator instance;
- coordinator uses the exact composed Runtime instance;
- coordinator uses the exact composed availability observer;
- coordinator uses the exact composed coverage evaluator;
- no persistent/global transition evidence state is introduced;
- no independent lifecycle or eligibility authority is introduced.

### Next Exact Action

RFC-050 is complete. Subsequent architecture work proceeded through RFC-051.

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
| RFC-032 | `6b4d80f` | Plugin metadata contract |
| RFC-033 | `569e4fb` | Plugin version format contract |
| RFC-034 | `a174009` | Bootstrap startup failure atomicity contract |
| RFC-035 | `3e613df` | Bootstrap shutdown lifecycle compliance contract |
| RFC-036 | `438d7e4` | Managed shutdown failure containment contract |
| RFC-037 | `788b03b` | Runtime request admission control contract |
| RFC-038 | `b65cceb` | Runtime readiness verification contract |
| RFC-039 | `bc26371` | API request admission enforcement contract |
| RFC-040 | `376970e` | Platform operational semantics alignment contract |
| RFC-041 | `1693a9b` | Operational workload entry boundary contract |
| RFC-042 | `3168014` | Runtime operational transition evidence contract |
| RFC-043 | `ed807f0` | Mandatory capability availability observation contract |
| RFC-044 | `a709c0d` | Mandatory capability policy contract |
| RFC-045 | `0b410ce` | Mandatory capability coverage evaluation contract |
| RFC-046 | `6aca0a1` | Operational workload evidence contract |
| RFC-047 | `ebc4769` | Operational transition evidence aggregation contract |
| RFC-048 | `b714ceb` | Runtime operational transition contract |
| RFC-049 | `496fe42` | Mandatory capability composition contract |
| RFC-050 | `995a73b` | Operational transition coordination contract |
| RFC-051 | `866f786` | Explicit operational transition application boundary |
| RFC-052 | `62bb854` | Explicit operational transition API boundary |

RFC-039 verification:

- Contract commit: `4b738df`
- Technical commit: `bc26371`
- Focused API and lifecycle suite: 39 passed
- Impacted regression: 88 passed
- Full regression: 256 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

RFC-039 is technically complete.

RFC-040 verification:

- Contract commit: `63d75ec`
- Alignment commit: `376970e`
- Architecture decision: AD-026 — Platform Operational Semantics Alignment
- BOOT-001 aligned
- CAP-002 aligned
- CORE-002 aligned
- Production Python changes: none
- Full regression: 256 passed
- `git diff --check`: passed after EOF normalization
- Remote alignment push: verified

RFC-040 is complete.

RFC-041 verification:

- Contract commit: `6a49e92`
- Technical commit: `1693a9b`
- Focused TDD suite: 7 passed
- Impacted regression: 41 passed
- Full regression: 263 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Runtime lifecycle transition behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-041 is technically complete.

RFC-042 verification:

- Contract commit: `3168014`
- Architecture decision: AD-028
- Production Python changes: none
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced
- Full regression baseline remains: 263 passed
- Blocking dependency identified: trusted mandatory-capability availability observation

RFC-042 is complete.

RFC-043 verification:

- Contract commit: `0d30cfb`
- Technical commit: `ed807f0`
- Architecture decision: AD-029
- Focused TDD suite: 15 passed
- Impacted regression: 40 passed
- Full regression: 278 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Production capability sources: none
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-043 is technically complete.

RFC-044 verification:

- Contract commit: `91c6090`
- Technical commit: `a709c0d`
- Architecture decision: AD-030
- Focused TDD suite: 15 passed
- Impacted regression: 55 passed
- Full regression: 293 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Production mandatory-capability policy: `UNCONFIGURED`
- Fabricated mandatory capabilities: none
- Policy-to-availability coverage evaluator: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-044 is technically complete.

RFC-045 verification:

- Contract commit: `9abde19`
- Technical commit: `0b410ce`
- Architecture decision: AD-031
- Focused TDD suite: 16 passed
- Impacted regression: 71 passed
- Full regression: 309 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Multi-source aggregation: not introduced
- Freshness policy: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-045 is technically complete.

RFC-046 verification:

- Contract commit: `2365b68`
- Technical commit: `6aca0a1`
- Architecture decision: AD-032
- Focused TDD suite: 18 passed
- Impacted regression: 32 passed
- Full regression: 327 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Workload correlation: UUID
- Canonical facade-entry evidence: introduced
- Workflow-execution-start evidence: introduced
- Persistent/global evidence recorder: not introduced
- Operational eligibility: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-046 is technically complete.

RFC-047 verification:

- Contract commit: `35004dc`
- Technical commit: `ebc4769`
- Architecture decision: AD-033
- Focused TDD suite: 17 passed
- Impacted regression: 56 passed
- Full regression: 344 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- External evidence aggregation: introduced
- Runtime-owned preconditions: excluded from aggregate
- Operational eligibility: not introduced
- Runtime lifecycle behavior: unchanged
- `OPERATIONAL` transition: not introduced

RFC-047 is technically complete.

RFC-048 verification:

- Contract commit: `ac1c625`
- Technical commit: `b714ceb`
- Architecture decision: AD-034
- Focused TDD suite: 18 passed
- Impacted regression: 93 passed
- Full regression: 362 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Guarded Runtime operational transition: introduced
- Public `mark_operational()` bypass: not introduced
- Runtime readiness after success: preserved
- Request admission after success: preserved
- Rejected transition mutation: none
- Bootstrap automatic operational transition: not introduced
- Workload-triggered lifecycle transition: not introduced
- Independent operational-eligibility authority: not introduced

RFC-048 is technically complete.

RFC-049 verification:

- Contract commit: `ca5ccbf`
- Technical commit: `496fe42`
- Architecture decision: AD-035
- Focused TDD suite: 15 passed
- Impacted regression: 101 passed
- Full regression: 377 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified
- Capability-source composition input: introduced
- Mandatory-capability policy composition input: introduced
- Source identity and ordering: preserved
- Policy identity: preserved
- Default fail-closed composition: preserved
- Deployment-specific capability names: not introduced
- Coverage evaluation during composition: not introduced
- Operational-transition evidence construction: not introduced
- Runtime lifecycle transition during composition: not introduced

RFC-049 is technically complete.

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
- Operational transition coordinator: introduced
- Canonical Runtime, observer and evaluator identity: preserved
- Capability observation per request: exactly one snapshot
- Mandatory-capability coverage evaluation per request: exactly once
- Operational-transition evidence construction: explicit
- Runtime delegation: exactly once
- Automatic transition during composition: not introduced
- Automatic transition during Bootstrap startup: not introduced
- Automatic transition during workload execution: not introduced
- Persistent transition evidence state: not introduced
- Independent lifecycle authority: not introduced
- Runtime remains sole operational-transition authority

RFC-050 is technically complete.

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
- Explicit operational-transition application service: introduced
- Canonical `ApplicationFacade` dependency identity: preserved
- Canonical `OperationalTransitionCoordinator` dependency identity: preserved
- Workload execution per request: exactly once
- Workload evidence identity: preserved
- Coordinator delegation per request: exactly once
- Immutable application result: introduced
- Automatic transition from normal `ApplicationFacade.analyze(...)`: not introduced
- HTTP endpoint: not introduced
- Bootstrap-triggered transition: not introduced
- Health-triggered transition: not introduced
- Persistent transition state: not introduced
- Independent lifecycle authority: not introduced
- Runtime remains sole operational-transition authority

RFC-051 is technically complete.

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
