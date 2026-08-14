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

## RFC-060 — Canonical Enterprise Document Registration Application Boundary

### Status

Contract Accepted — Implementation Gate Pending.

Post-RFC-059 system and architecture integrity review: complete — PASS.

Evidence-based RFC-060 workstream selection: complete.

Architecture decision:

`AD-046 — Canonical Enterprise Document Registration Application Boundary`

AD-046 status: Accepted.

RFC-060 / AD-046 Contract Acceptance Review: passed.

Technical implementation: not authorized until the implementation-entry Git gate is satisfied.

Implementation gate: pending.

### Objective

Establish the first explicit application-level use case for registration of one canonical `EnterpriseDocument` without introducing a generic repository-delegation service or prematurely introducing Document Library, ingestion, parsing, search, revision or AI responsibilities.

RFC-060 SHALL accept caller-supplied registration inputs, construct one canonical immutable `EnterpriseDocument`, persist it through the persistence-neutral `EnterpriseDocumentRepository`, and return that exact canonical Document only after persistence succeeds.

RFC-060 SHALL NOT redesign the canonical Document domain, repository contract, relational adapter or database runtime.

### Architecture Dependencies

RFC-060 depends upon and SHALL preserve:

- AD-043 / RFC-057 — Canonical Enterprise Document Foundation Boundary;
- AD-044 / RFC-058 — Canonical Enterprise Document Repository Foundation Boundary;
- AD-045 / RFC-059 — Canonical Document Relational Persistence Adapter Boundary;
- shared canonical `EntityId`;
- existing Runtime, Bootstrap, Composition and Security boundaries;
- AD-009 source-neutral architecture.

`EnterpriseDocument` remains the canonical representation of one enterprise Document record.

`EnterpriseDocumentRepository` remains the persistence-neutral repository port.

Canonical Document validation remains owned by `app.domain.document`.

Repository Session and transaction semantics remain owned by the RFC-059 infrastructure adapter.

`DatabaseRuntime` remains engine/session-factory lifecycle owner.

### Canonical Registration Application Responsibility

RFC-060 SHALL introduce one specialized application-level Document registration use case.

The canonical application service SHALL be:

`EnterpriseDocumentRegistrationApplicationService`

under:

`app.services.enterprise_document_registration_application_service`

The same module SHALL contain the immutable application input contract:

`EnterpriseDocumentRegistrationRequest`

The application boundary SHALL NOT expose generic repository-equivalent methods such as:

- `add(...)`;
- `get(...)`;
- `update(...)`;
- `delete(...)`;
- `upsert(...)`;
- `save(...)`.

The canonical application operation SHALL represent the business action:

`register(request: EnterpriseDocumentRegistrationRequest) -> EnterpriseDocument`

For one successful registration invocation, the boundary SHALL:

1. receive one immutable registration request;
2. establish one canonical `EntityId`;
3. construct accepted canonical Document value objects;
4. construct one canonical immutable `EnterpriseDocument`;
5. submit that Document through `EnterpriseDocumentRepository.add(...)`;
6. return the same canonical Document only after repository add succeeds.

The Registration boundary SHALL NOT call `EnterpriseDocumentRepository.get(...)` merely to confirm the write or prevent duplicates.

### Registration Request Boundary

`EnterpriseDocumentRegistrationRequest` SHALL contain only the minimum caller-supplied values required to construct one canonical Document:

- `document_type: str`;
- `title: str`;
- `source_type: str`;
- `source_reference: str`.

The caller SHALL NOT provide:

- canonical `EnterpriseDocument.id`;
- a preconstructed `EnterpriseDocument`;
- a preconstructed `DocumentType`;
- a preconstructed `DocumentSourceType`;
- a preconstructed `DocumentSource`.

Canonical domain construction belongs to the Registration application boundary.

The registration request SHALL NOT become:

- an HTTP transport schema;
- a database row model;
- a file-upload model;
- a parsing/OCR result;
- an ingestion payload;
- a Knowledge Capture request;
- a vector payload;
- a graph node;
- a prompt or LLM context.

Future transport, source integration or ingestion boundaries MAY translate their own accepted inputs into `EnterpriseDocumentRegistrationRequest` only under their own accepted architecture contracts.

### Canonical Domain Construction Boundary

The Registration application boundary SHALL construct the canonical Document representation using accepted AD-043 / RFC-057 types:

- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`.

Canonical Document normalization and validation remain authoritative in:

`app.domain.document`

RFC-060 SHALL NOT duplicate Document normalization or invariant rules inside the application service.

Invalid canonical Document input SHALL continue to fail through existing `DomainException` semantics.

RFC-060 SHALL NOT introduce a competing application-level Document validation framework.

### Canonical Identity Boundary

The Registration boundary SHALL use the existing shared canonical:

`EntityId`

for new Document identity.

The default identity source SHALL be:

`EntityId.new()`

The implementation MAY support narrow per-instance injection of an identity-producing callable compatible with:

`() -> EntityId`

for deterministic verification.

The identity source SHALL NOT:

- depend on SQLAlchemy;
- depend on PostgreSQL;
- read repository state to choose an identity;
- retry with a new identity after duplicate failure;
- use `source_reference` as identity;
- require Runtime or Bootstrap availability;
- use process-global mutable state.

RFC-060 SHALL NOT introduce:

- `DocumentId`;
- a platform-wide identity service;
- an identity provider registry;
- a new dependency-injection framework.

### Source Reference Boundary

`DocumentSource.source_reference` remains external/source-system traceability only.

RFC-060 SHALL NOT interpret `source_reference` as:

- canonical PlantMind identity;
- globally unique identity;
- deduplication key;
- repository lookup key;
- database alternate key;
- proof of source authenticity;
- proof of document approval or correctness.

Equal source references MAY occur on different canonical Document identities.

The Registration boundary SHALL NOT perform source-reference lookup before persistence.

### Repository Boundary

`EnterpriseDocumentRegistrationApplicationService` SHALL receive:

`EnterpriseDocumentRepository`

explicitly during construction.

For a registration invocation that reaches persistence:

`EnterpriseDocumentRepository.add(...)`

SHALL be invoked exactly once.

The Registration boundary SHALL NOT call repository `get(...)` as:

- a pre-insert existence check;
- duplicate prevention;
- post-write confirmation;
- source-reference lookup.

`EnterpriseDocumentAlreadyExistsError` remains the repository-boundary duplicate conflict.

Duplicate conflict SHALL propagate without:

- identity regeneration;
- retry;
- overwrite;
- merge;
- conversion to update;
- synthetic success.

Unexpected repository failures SHALL propagate without retry or synthetic success.

### Persistence and Transaction Boundary

RFC-060 SHALL remain persistence-implementation neutral.

The Registration application boundary SHALL NOT construct, own or directly use:

- SQLAlchemy;
- SQLAlchemy Session;
- database engine;
- `DatabaseRuntime`;
- database connection;
- database configuration;
- commit;
- rollback;
- Alembic migration;
- `MetaData.create_all()`.

Repository Session lifetime, commit, rollback and duplicate classification remain governed by AD-045 / RFC-059.

RFC-060 SHALL NOT introduce a Unit of Work or cross-repository transaction coordinator.

### Document Lifecycle Boundary

RFC-060 registers one immutable canonical Document record only.

It SHALL NOT introduce:

- update;
- delete;
- upsert;
- replacement;
- supersession;
- revision numbers;
- version numbers;
- current revision;
- revision history;
- approval lifecycle;
- retention;
- archival;
- mutable document state.

AD-043 revision neutrality remains unchanged.

### Document Library and Binary Boundary

Document registration is not a production Document Library.

RFC-060 SHALL NOT introduce:

- file upload/download;
- file bytes or blobs;
- filesystem storage;
- object storage;
- MIME metadata;
- file hash or checksum;
- document catalogue browsing;
- document retrieval service;
- source synchronization;
- document permissions;
- ownership;
- retention management;
- Document Library API.

### Ingestion, Parsing and Knowledge Boundary

RFC-060 SHALL NOT introduce:

- document ingestion;
- bulk ingestion;
- automatic source synchronization;
- PDF/Word/spreadsheet parsing;
- OCR;
- text extraction;
- table extraction;
- section detection;
- chunking;
- automatic metadata extraction;
- automatic classification;
- document-to-Knowledge transformation;
- calls to `KnowledgeCaptureApplicationService`;
- writes to `KnowledgeRecordRepository`.

Document and Knowledge remain separate canonical concepts.

A future document-to-Knowledge boundary SHALL consume accepted Document and Knowledge Capture contracts without bypassing either.

### Search, Vector, Graph and AI Boundary

RFC-060 SHALL NOT introduce:

- list/browse search;
- keyword search;
- full-text search;
- semantic search;
- similarity search;
- ranking;
- embeddings;
- vector persistence;
- Qdrant;
- Knowledge Graph persistence;
- Neo4j;
- RAG;
- prompts;
- LLM invocation;
- summarization;
- autonomous document agents.

Canonical registration does not imply semantic retrieval or AI readiness.

### Composition and Runtime Boundary

RFC-060 SHALL NOT automatically modify or register the new application boundary through:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`.

RFC-060 SHALL NOT automatically register or expose the relational Document repository in default composition.

Default startup SHALL remain independent from:

- `DATABASE_URL`;
- PostgreSQL availability;
- Document source availability.

Document Registration SHALL NOT become a mandatory Runtime capability merely because the application boundary exists.

Runtime lifecycle, readiness, request admission, Bootstrap, Health and operational-transition responsibilities remain unchanged.

Production Document Registration composition requires a separate accepted architecture boundary.

### Transport and Integration Boundary

RFC-060 SHALL NOT introduce:

- FastAPI routes;
- HTTP endpoints;
- transport DTOs;
- message-bus integration;
- event publication;
- PI System integration;
- DCS integration;
- OPC UA integration;
- CMMS integration;
- SAP integration;
- File Server integration;
- SharePoint integration;
- document-control-system integration.

AD-009 source-neutral architecture remains authoritative.

### Security and Trust Boundary

RFC-060 does not establish:

- authentication;
- authorization;
- RBAC;
- principal identity;
- actor audit;
- Active Directory;
- LDAP;
- MFA;
- document permissions;
- source authenticity verification;
- document approval;
- document correctness;
- compliance approval;
- safety approval.

The existing prototype security implementation SHALL NOT be represented as production enterprise security.

RFC-060 acceptance or implementation SHALL NOT be represented as Cybersecurity approval or production deployment readiness.

### Expected Technical Surface

If implementation is later authorized, the expected minimum production surface is:

- `backend/app/services/enterprise_document_registration_application_service.py`.

Expected verification surface:

- `tests/services/test_enterprise_document_registration_application_service.py`;
- minimum architecture guardrails necessary to prove canonical dependency direction and absence of default composition registration.

Any additional production file or responsibility requires evidence that it is necessary to satisfy the accepted RFC-060 contract.

### TDD Acceptance Requirements

Technical implementation SHALL be test-driven.

Tests SHALL demonstrate at minimum:

- registration request immutability;
- deterministic identity injection;
- default identity generation requires no database;
- dependency source is not invoked merely by service construction;
- canonical Document types are constructed through accepted domain constructors;
- canonical normalization remains domain-owned;
- one successful registration produces the expected canonical `EnterpriseDocument`;
- repository `add()` is invoked exactly once;
- repository `get()` is not used;
- the exact canonical Document passed to the repository is returned after successful persistence;
- invalid canonical input prevents persistence;
- duplicate repository conflict propagates without retry or identity regeneration;
- unexpected repository failure propagates without retry or synthetic success;
- equal source references do not cause application-level deduplication;
- no SQLAlchemy/database ownership enters the application boundary;
- default composition does not automatically register or expose Document Registration;
- Runtime and Bootstrap behavior remain unchanged.

### Contract Acceptance Gate

RFC-060 / AD-046 Contract Acceptance Review: passed.

The review confirmed absence of:

- generic repository-wrapper design;
- competing Document identity;
- source-reference identity or uniqueness semantics;
- duplicate-precheck behavior;
- persistence ownership leakage;
- revision ownership;
- Document Library ownership;
- ingestion or parsing ownership;
- Knowledge-transformation ownership;
- search/vector/graph/RAG/LLM responsibility;
- default-composition coupling;
- Runtime-authority expansion;
- transport/integration expansion;
- unsupported security or production-readiness claims.

### Current Contract State

RFC-060: Contract Accepted — Implementation Gate Pending.

AD-046: Accepted.

Technical implementation remains prohibited until:

1. accepted RFC-060 / AD-046 documentation is committed;
2. the contract commit is pushed;
3. exact local/remote contract commit identity is verified;
4. the working tree is clean.

### Next Exact Action

Commit and push the accepted RFC-060 / AD-046 architecture contract.

Verify exact local/remote contract commit identity and a clean working tree.

Do not implement RFC-060 before the implementation-entry Git gate is satisfied.

---

## RFC-059 — Canonical Document Relational Persistence Adapter Boundary

### Status

Technically Complete.

Post-RFC-058 Source-of-Truth architecture review: complete.

Architecture decision:

`AD-045 — Canonical Document Relational Persistence Adapter Boundary`

AD-045 status: Accepted.

RFC-059 / AD-045 Contract Acceptance Review: passed.

Contract commit:

`61e69e73a0f2460281c91169020b06ef1b5ad1db`

Technical implementation commit:

`c1090919945af826992cfd4940aeec674907df76`

Implementation-entry Git gate: satisfied.

Technical verification:

- Knowledge + Document infrastructure verification: 74 passed;
- full PlantMind regression: 637 passed;
- Python compilation: passed;
- `git diff --check`: passed;
- Alembic head: `0003`;
- migration chain: `0001 → 0002 → 0003`;
- remote technical push: verified;
- exact local/remote technical commit identity: verified;
- technical working tree: clean.

Post-RFC-059 system and architecture integrity review: complete — PASS.

Engineering-memory consistency closure: this documentation update.

### Objective

Establish the minimum canonical relational persistence adapter for `EnterpriseDocument` while preserving:

- AD-043 / RFC-057 canonical Document semantics;
- AD-044 / RFC-058 persistence-neutral repository semantics;
- AD-040 / RFC-054 database runtime and schema-lifecycle ownership.

RFC-059 SHALL implement the existing `EnterpriseDocumentRepository` through the accepted relational infrastructure.

RFC-059 SHALL NOT redesign the Document domain, repository contract or database runtime.

### Architecture Dependencies

RFC-059 SHALL preserve:

- `EnterpriseDocument` as the canonical domain entity;
- `EnterpriseDocumentRepository` as the persistence-neutral port;
- shared canonical `EntityId`;
- `DatabaseRuntime` as engine/session-factory lifecycle owner;
- `DatabaseBase.metadata` as canonical relational metadata authority;
- Alembic as sole canonical schema-migration authority;
- existing Runtime, Bootstrap, Composition and Security boundaries.

### Infrastructure Boundary

RFC-059 SHALL introduce the Document relational adapter under:

`app.infrastructure.document`

The canonical RFC-059 infrastructure contracts SHALL be:

- mapped representation: `EnterpriseDocumentRow`;
- domain-to-row mapper: `document_to_row(document: EnterpriseDocument) -> EnterpriseDocumentRow`;
- row-to-domain mapper: `row_to_document(row: EnterpriseDocumentRow) -> EnterpriseDocument`;
- repository adapter: `SQLAlchemyEnterpriseDocumentRepository`.

The expected modules SHALL be:

- `app.infrastructure.document.models`;
- `app.infrastructure.document.mapping`;
- `app.infrastructure.document.repository`.

The package initializer SHALL NOT establish a competing public Document contract or re-export persistence responsibility into the canonical domain boundary.

SQLAlchemy SHALL NOT leak into:

- `app.domain.document`;
- `app.document.repository`.

### Repository Adapter

RFC-059 SHALL introduce one SQLAlchemy implementation of:

`EnterpriseDocumentRepository`

implementing exactly:

- `add(document: EnterpriseDocument) -> None`;
- `get(document_id: EntityId) -> EnterpriseDocument | None`.

RFC-059 SHALL NOT add:

- update;
- delete;
- upsert;
- replace;
- merge;
- list;
- search;
- filter;
- query;
- source-reference lookup.

### Relational Representation

The canonical table SHALL be:

`enterprise_documents`

It SHALL persist only:

- `id`;
- `document_type`;
- `title`;
- `source_type`;
- `source_reference`.

Expected relational semantics:

- `id`: UUID, non-null;
- `document_type`: non-null string;
- `title`: non-null text;
- `source_type`: non-null string;
- `source_reference`: non-null text.

The canonical primary-key constraint SHALL be:

`pk_enterprise_documents`

The database SHALL NOT generate or replace canonical Document identity.

### Source Reference Boundary

`DocumentSource.source_reference` remains external traceability only.

It SHALL NOT become:

- canonical identity;
- globally unique identity;
- unique database constraint;
- alternate repository key;
- implicit deduplication key.

Different canonical Document identities MAY contain equal source references.

### Mapping Boundary

RFC-059 SHALL define explicit mapping between canonical `EnterpriseDocument` and its infrastructure-owned relational representation.

Relational-to-domain mapping SHALL reconstruct through canonical constructors:

- `EntityId`;
- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`.

Mapping SHALL NOT bypass canonical validation.

Malformed relational state SHALL remain an observable mapping/infrastructure failure.

### Session Boundary

The repository adapter SHALL receive the canonical session-factory dependency explicitly.

It SHALL NOT:

- construct an independent engine;
- construct a competing session factory;
- read hidden global database configuration;
- own a process-global mutable Session;
- reuse mutable Session instances between operations.

Each operation SHALL use a deterministic independent session lifetime.

Every opened Session SHALL be closed after success or failure.

`DatabaseRuntime` remains engine/session-factory lifecycle owner.

### Transaction Boundary

`add()` SHALL execute as one atomic repository transaction.

Successful `add()` SHALL commit once.

Failed `add()` SHALL roll back before termination.

`get()` SHALL remain read-only and SHALL NOT commit application data.

RFC-059 SHALL NOT introduce:

- Unit of Work;
- cross-repository transaction coordination;
- application-workflow transaction ownership.

### Duplicate Identity Boundary

The relational primary key SHALL be the concurrency-safe authority for canonical Document identity.

The adapter SHALL NOT use a pre-insert existence query as authoritative duplicate prevention.

Only a structured database failure positively identifying the canonical primary-key conflict SHALL be translated to:

`EnterpriseDocumentAlreadyExistsError`

For the accepted PostgreSQL boundary, duplicate classification SHALL require:

- SQLSTATE `23505`; and
- diagnostic constraint identity `pk_enterprise_documents`.

SQLSTATE `23505` alone SHALL NOT be sufficient.

Constraint-name matching without the PostgreSQL unique-violation SQLSTATE SHALL NOT be sufficient.

Human-readable database error-message parsing SHALL NOT classify duplicate identity.

Every other integrity, mapping, connection, driver and transaction failure SHALL preserve its infrastructure failure semantics.

Duplicate attempts SHALL NOT overwrite existing canonical Documents.

### Migration Boundary

RFC-059 SHALL introduce exactly one append-only Alembic successor to:

`0002`

The new revision SHALL be:

`0003`

Revision `0003` SHALL create:

`enterprise_documents`

RFC-059 SHALL NOT modify or rewrite:

- `0001`;
- `0002`.

The migration SHALL establish:

- UUID identity;
- document type;
- title;
- source type;
- source reference;
- `pk_enterprise_documents`.

It SHALL NOT introduce:

- revision/version tables;
- Document Library tables;
- ingestion tables;
- search indexes;
- vector tables;
- graph tables;
- LLM persistence.

The migration graph SHALL retain exactly one canonical head.

Application startup SHALL NOT automatically execute migrations.

`MetaData.create_all()` SHALL NOT become the production deployment mechanism.

### Metadata Registration

`enterprise_documents` SHALL register with:

`DatabaseBase.metadata`

Alembic metadata discovery SHALL load the mapped Document registration.

RFC-059 SHALL make the minimum explicit registration import in:

`backend/migrations/env.py`

using the canonical mapped class:

`EnterpriseDocumentRow`

The import SHALL follow the existing metadata-registration pattern and SHALL NOT establish a new runtime dependency.

The registration import SHALL NOT:

- construct an engine;
- create a Session;
- connect to PostgreSQL;
- execute migrations;
- change application startup behavior.

Mapped metadata and migration `0003` SHALL remain schema-aligned.

### Downgrade Boundary

Revision `0003` MAY reverse only schema introduced by `0003`.

Dropping `enterprise_documents` becomes destructive once Document data exists.

Execution of destructive downgrade in a data-bearing environment requires separate deployment/migration review.

Runtime and Bootstrap SHALL NOT execute downgrade automatically.

### Composition and Runtime Boundary

RFC-059 SHALL NOT automatically:

- construct `DatabaseRuntime` in default composition;
- register the relational Document repository in default services;
- expose it from default platform composition;
- require `DATABASE_URL` during normal startup;
- make PostgreSQL mandatory.

Runtime lifecycle, readiness, request admission, Bootstrap and operational-transition authority remain unchanged.

### Revision Boundary

RFC-059 remains revision-neutral.

It SHALL NOT introduce:

- DocumentRevision;
- version numbering;
- supersession;
- current revision;
- historical revision chain;
- revision retention.

### Document Library Boundary

Relational persistence of canonical Document metadata is not a Document Library.

RFC-059 SHALL NOT introduce:

- file upload/download;
- binary storage;
- catalogue browsing;
- retention policy;
- synchronization;
- permissions;
- full-text search;
- semantic search.

### Ingestion and AI Boundary

RFC-059 establishes persistence infrastructure only.

It SHALL NOT introduce:

- document ingestion;
- registration workflow;
- parsing;
- OCR;
- chunking;
- Knowledge transformation;
- vector persistence;
- graph persistence;
- RAG;
- LLM invocation.

### Security and Deployment Boundary

Code-level RFC-059 completion SHALL NOT imply:

- production PostgreSQL connectivity;
- production schema deployment;
- production database configuration;
- authentication readiness;
- authorization readiness;
- Cybersecurity approval;
- production deployment readiness.

Database credentials SHALL remain outside committed source code.

### Expected Technical Surface

If later accepted and authorized, implementation SHALL remain limited to the minimum surface required by this contract:

- `backend/app/infrastructure/document/__init__.py`;
- `backend/app/infrastructure/document/models.py` containing `EnterpriseDocumentRow`;
- `backend/app/infrastructure/document/mapping.py` containing `document_to_row()` and `row_to_document()`;
- `backend/app/infrastructure/document/repository.py` containing `SQLAlchemyEnterpriseDocumentRepository`;
- `backend/migrations/versions/0003_enterprise_documents.py`;
- minimum Document-model registration change in `backend/migrations/env.py`;
- focused mapping, repository-runtime, duplicate-classification, migration-contract and architecture tests.

Any additional production file or responsibility requires evidence that it is necessary to satisfy the accepted RFC-059 contract.

This expected surface does not authorize implementation.

### Contract Acceptance Gate

RFC-059 Contract Acceptance Review was performed and passed before technical implementation.

Before acceptance, review SHALL verify absence of:

- competing Document identity;
- source-reference identity or uniqueness leakage;
- hidden search capability;
- revision ownership;
- Document Library ownership;
- ingestion ownership;
- competing engine/session ownership;
- migration-history rewrite;
- default-composition coupling;
- Runtime authority expansion;
- unsupported security/deployment claims.

Technical implementation SHALL remain prohibited until:

1. RFC-059 Contract Acceptance Review passes;
2. AD-045 is accepted;
3. accepted contract documentation is committed;
4. contract commit is pushed;
5. exact local/remote identity is verified;
6. working tree is clean.

### Contract Acceptance

RFC-059 / AD-045 Contract Acceptance Review: passed.

The review confirmed:

- canonical Document identity remains `EntityId`;
- `source_reference` remains non-unique traceability only;
- relational representation remains infrastructure-owned;
- canonical domain and repository contracts remain SQLAlchemy-free;
- repository operations remain exactly `add()` and `get()`;
- session and transaction ownership remain explicit;
- duplicate classification requires both PostgreSQL SQLSTATE `23505` and `pk_enterprise_documents`;
- migration history remains append-only through proposed revision `0003`;
- `EnterpriseDocumentRow` registration with canonical metadata is explicit;
- no revision, Document Library, ingestion, search, Runtime-authority or default-composition responsibility is introduced;
- no production PostgreSQL, Cybersecurity or deployment-readiness claim is introduced.

### Current Contract State

RFC-059: Technically Complete.

AD-045: Accepted.

Contract acceptance: passed.

Implementation-entry Git gate: satisfied.

Technical commit:

`c1090919945af826992cfd4940aeec674907df76`

Full regression:

637 passed.

Canonical Alembic head:

`0003`

Post-RFC-059 system and architecture integrity review:

PASS.

### Next Exact Action

Commit and push this RFC-059 engineering-memory and architecture-review closure.

After documentation closure, perform evidence-based selection of the next architecture workstream.

Do not preselect, draft or implement RFC-060 until that selection review is complete.


---

## RFC-058 — Canonical Enterprise Document Repository Foundation Boundary

### Status

Technically Complete.

Post-RFC-057 Source-of-Truth architecture review: complete.

RFC-058 / AD-044 Contract Acceptance Review: passed.

Architecture decision:

`AD-044 — Canonical Enterprise Document Repository Foundation Boundary`

AD-044 status: Accepted.

RFC-058 contract acceptance: passed.

Contract commit: `b0af39f5a1a8df63e15203fa51349233136c9d2d`.

Technical commit: `b0f7ffc67100ce1899f0d30d43c2eabf0d2f7a73`.

Remote technical push and exact local/remote commit identity: verified.

Technical verification:

- Focused RFC-058 verification: 14 passed
- Document + repository guardrails: 47 passed
- Full PlantMind regression: 600 passed
- Python compilation: passed
- `git diff --check`: passed
- Working tree after technical push: clean

### Objective

Establish the minimum persistence-neutral repository contract required to store and retrieve canonical `EnterpriseDocument` records without introducing relational infrastructure, document lifecycle semantics, Document Library behavior, ingestion, search or production composition.

RFC-058 SHALL define the canonical persistence port for Document identity persistence.

RFC-058 SHALL NOT implement persistence technology.

### Architecture Dependencies

RFC-058 depends upon and SHALL preserve:

- AD-043 / RFC-057 — Canonical Enterprise Document Foundation Boundary;
- shared `EntityId` from `app.domain.base`;
- canonical `EnterpriseDocument` from `app.domain.document`;
- AD-040 / RFC-054 database-runtime ownership;
- AD-039 through AD-042 Knowledge architecture;
- AD-009 source-neutral architecture;
- existing Runtime, Bootstrap, Composition and Security boundaries.

RFC-058 SHALL NOT redesign any accepted canonical Document or Knowledge contract.

### Persistence-Neutral Namespace Boundary

RFC-058 SHALL introduce the persistence-neutral package:

`app.document`

and repository module:

`app.document.repository`

The canonical Document domain SHALL remain:

`app.domain.document`

Repository responsibility SHALL NOT be placed inside:

- `app.domain.document`;
- `app.infrastructure`;
- `app.services`;
- `app.models`.

The package boundary SHALL preserve the existing architectural pattern in which canonical domain contracts and persistence-neutral repository ports remain separate.

`app.document.__init__.py` SHALL remain empty within RFC-058.

RFC-058 SHALL NOT introduce a new Document-package public re-export API.

### Canonical Repository Port

RFC-058 SHALL introduce:

`EnterpriseDocumentRepository`

as an abstract persistence-neutral repository port.

The canonical contract SHALL expose exactly:

`add(document: EnterpriseDocument) -> None`

and:

`get(document_id: EntityId) -> EnterpriseDocument | None`

No additional repository operation is authorized by RFC-058.

### Add Boundary

`EnterpriseDocumentRepository.add()` SHALL accept one canonical:

`EnterpriseDocument`

The repository contract SHALL represent additive persistence without silent overwrite.

If canonical Document identity already exists, the repository SHALL NOT:

- overwrite the existing Document;
- merge Documents;
- regenerate identity;
- convert the operation into update;
- silently ignore the conflict.

A duplicate canonical identity SHALL be represented by the repository-level conflict:

`EnterpriseDocumentAlreadyExistsError`

### Duplicate Identity Boundary

RFC-058 duplicate semantics SHALL concern only:

`EnterpriseDocument.id`

using canonical:

`EntityId`

A duplicate conflict means that the canonical Document identity already exists in the repository.

RFC-058 SHALL NOT define duplicate semantics using:

- `DocumentSource.source_reference`;
- `DocumentSourceType`;
- title;
- document type;
- filename;
- path;
- URL;
- document number;
- source-system identifier;
- content equality;
- hash;
- checksum.

Two Documents MAY have equal source references without RFC-058 declaring them duplicates.

Two Documents MAY have equal titles without RFC-058 declaring them duplicates.

Two Documents MAY have equal classification values without RFC-058 declaring them duplicates.

Only canonical `EntityId` collision is governed by RFC-058 duplicate semantics.

### Duplicate Exception Boundary

RFC-058 SHALL introduce:

`EnterpriseDocumentAlreadyExistsError`

as a repository-level exception.

It SHALL derive from:

`Exception`

It SHALL NOT derive from:

`DomainException`

because duplicate persistence identity is a repository conflict rather than canonical Document-domain validation failure.

RFC-058 SHALL NOT introduce a general Document exception hierarchy.

### Get Boundary

`EnterpriseDocumentRepository.get()` SHALL perform identity lookup only.

It SHALL accept:

`document_id: EntityId`

and return:

`EnterpriseDocument | None`

If the canonical identity is absent, `get()` SHALL return:

`None`

Absence SHALL NOT be represented by:

- `DomainException`;
- a repository-not-found exception;
- a fabricated empty Document;
- a placeholder Document.

Identity lookup SHALL NOT be represented as document search.

### Source Reference Boundary

AD-043 remains authoritative.

`DocumentSource.source_reference` is external/source-system traceability only.

RFC-058 SHALL NOT establish that a source reference is:

- globally unique;
- a canonical identifier;
- a repository primary key;
- verified;
- authoritative;
- resolvable;
- immutable across source systems;
- guaranteed to identify one Document.

RFC-058 SHALL NOT introduce:

`find_by_source_reference()`

or an equivalent source-reference lookup API.

Any future source-level uniqueness, reconciliation, aliasing, deduplication or lookup contract requires separate architecture evidence and acceptance.

### Search and Listing Boundary

RFC-058 SHALL NOT introduce:

- `list()`;
- `find()`;
- `search()`;
- `filter()`;
- `query()`;
- keyword search;
- full-text search;
- semantic search;
- similarity search;
- browse/catalogue behavior;
- pagination;
- ranking;
- source-reference search.

Repository identity lookup is not Search capability.

### Mutation Boundary

RFC-058 SHALL NOT introduce:

- `update()`;
- `delete()`;
- `remove()`;
- `upsert()`;
- `replace()`;
- `save()` with implicit update semantics;
- patch semantics;
- mutable repository state transitions.

Canonical `EnterpriseDocument` remains immutable under AD-043.

Future mutable lifecycle behavior requires an explicit architecture contract.

### Revision and Version Boundary

RFC-058 SHALL remain revision-neutral.

It SHALL NOT introduce:

- `DocumentRevision`;
- revision number;
- version number;
- revision chain;
- current revision;
- supersession;
- effective dates;
- approval state;
- revision replacement;
- revision rollback.

RFC-058 SHALL NOT decide whether future revisions reuse or replace canonical Document identity.

That question remains separately governed.

### Relational Persistence Boundary

RFC-058 SHALL NOT introduce:

- SQLAlchemy;
- SQLAlchemy Document model;
- SQLAlchemy Document repository;
- Session;
- engine;
- transaction manager;
- commit;
- rollback;
- PostgreSQL-specific behavior;
- database-generated identity.

A future relational Document persistence adapter MAY implement the accepted repository port only under a separate architecture contract.

### Schema Lifecycle Boundary

RFC-058 SHALL NOT introduce:

- Document table;
- Alembic migration;
- database index;
- foreign key;
- uniqueness constraint;
- PostgreSQL schema change;
- `DatabaseRuntime` change.

AD-040 / RFC-054 remains the sole accepted relational database runtime and migration foundation.

### Transaction Ownership Boundary

RFC-058 SHALL NOT define:

- Session lifetime;
- connection lifetime;
- transaction ownership;
- commit ownership;
- rollback ownership;
- Unit of Work;
- retry policy.

Those are persistence-adapter responsibilities, not persistence-neutral repository-port responsibilities.

### Document Library Boundary

RFC-058 SHALL NOT implement a Document Library.

It SHALL NOT introduce:

- catalogue service;
- browse behavior;
- document upload;
- binary retrieval;
- storage management;
- file synchronization;
- document permissions;
- retention;
- archival;
- deletion workflow;
- revision management;
- Document Library API.

A repository port is not a production Document Library.

### Binary and File Boundary

RFC-058 SHALL NOT introduce:

- binary content;
- file bytes;
- blobs;
- MIME type;
- filesystem storage;
- object storage;
- file hash;
- checksum;
- file size;
- network-path behavior.

`EnterpriseDocument` remains a canonical record rather than a file-storage object.

### Ingestion Boundary

RFC-058 SHALL NOT introduce:

- Document ingestion application service;
- document registration workflow;
- file upload workflow;
- bulk ingestion;
- automatic source synchronization;
- document-to-Knowledge transformation.

The previously deferred ingestion boundary remains deferred.

Future ingestion SHALL consume accepted canonical Document boundaries and SHALL NOT invent competing Document persistence semantics.

Whether a future ingestion application boundary depends directly on `EnterpriseDocumentRepository`, another accepted application service, or both remains a future architecture decision.

### Parsing and AI Boundary

RFC-058 SHALL NOT introduce:

- PDF parsing;
- OCR;
- chunking;
- metadata extraction;
- automatic classification;
- embeddings;
- vector persistence;
- Qdrant;
- Knowledge Graph persistence;
- Neo4j;
- RAG;
- prompts;
- LLM invocation;
- AI document agents.

Persistence identity does not imply AI-readiness.

### Knowledge Boundary

RFC-058 SHALL NOT modify:

- `KnowledgeRecord`;
- `KnowledgeRecordRepository`;
- relational Knowledge persistence;
- `KnowledgeCaptureApplicationService`;
- Knowledge provenance;
- document-to-Knowledge transformation semantics.

Document and Knowledge remain separately governed canonical concepts.

### Domain Validation Boundary

RFC-058 SHALL NOT move canonical Document validation out of:

`app.domain.document`

`DocumentType`, `DocumentSourceType`, `DocumentSource` and `EnterpriseDocument` validation remain owned by AD-043 / RFC-057.

The repository port SHALL consume already-canonical Document objects.

Repository duplicate conflicts SHALL remain distinct from `DomainException`.

### Composition Boundary

RFC-058 SHALL NOT modify:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`.

The repository port SHALL NOT be automatically registered or exposed through default production composition.

### Runtime and Bootstrap Boundary

RFC-058 SHALL NOT modify:

- Runtime lifecycle states;
- Runtime readiness;
- mandatory-capability policy;
- request admission;
- Bootstrap startup;
- Bootstrap shutdown;
- Health semantics.

Availability of a repository interface SHALL NOT become Runtime transition authority.

### Security and Trust Boundary

RFC-058 does not establish:

- authentication;
- authorization;
- RBAC;
- actor identity;
- document permissions;
- source authenticity;
- document approval;
- document integrity verification;
- Cybersecurity approval.

The current prototype security implementation SHALL NOT be represented as production security.

RFC-058 acceptance SHALL NOT be represented as production deployment readiness.

### Industrial Integration Boundary

RFC-058 SHALL NOT introduce production integration with:

- PI System;
- DCS;
- OPC UA;
- CMMS;
- SAP;
- File Server;
- SharePoint;
- document-control systems.

AD-009 source-neutral architecture remains authoritative.

### Async and Transport Boundary

RFC-058 SHALL NOT introduce:

- HTTP endpoints;
- FastAPI routes;
- transport DTOs;
- asynchronous repository variants;
- message-bus integration;
- event publication.

The contract remains an internal persistence-neutral repository boundary.

### TDD Boundary

If the RFC-058 contract is accepted and its implementation gate is later satisfied, implementation SHALL be test-driven.

Tests SHALL demonstrate at minimum:

- `EnterpriseDocumentRepository` is abstract;
- the exact abstract operation set is `add` and `get`;
- `add()` accepts canonical `EnterpriseDocument`;
- `get()` accepts canonical `EntityId`;
- `get()` returns canonical `EnterpriseDocument` when identity exists;
- `get()` returns `None` when identity does not exist;
- duplicate canonical identity raises `EnterpriseDocumentAlreadyExistsError`;
- duplicate identity does not silently overwrite;
- `EnterpriseDocumentAlreadyExistsError` derives from `Exception`;
- `EnterpriseDocumentAlreadyExistsError` does not derive from `DomainException`;
- source-reference equality does not define canonical duplicate identity;
- the repository contract imports no SQLAlchemy;
- the repository contract imports no FastAPI;
- the repository contract imports no Pydantic;
- the repository contract does not depend on infrastructure;
- no SQLAlchemy Document adapter is introduced;
- no Document database model is introduced;
- no migration is introduced;
- no source-reference lookup API is introduced;
- no list/search/update/delete/upsert API is introduced;
- default composition remains unchanged;
- existing full regression remains green.

Tests SHALL NOT require:

- PostgreSQL;
- network access;
- File Server;
- SAP;
- SharePoint;
- PI System;
- DCS;
- OPC UA;
- PDF;
- OCR;
- Qdrant;
- Neo4j;
- LLM.

### Architecture Guardrail Boundary

Existing architecture guardrails remain authoritative.

RFC-058 SHALL NOT weaken or remove accepted RFC-053 through RFC-057 tests.

Architecture tests SHALL prove that the persistence-neutral Document repository contract:

- depends on canonical Document/domain primitives only;
- contains no relational persistence dependency;
- contains no source-specific integration dependency;
- exposes no search or mutation expansion;
- does not alter default platform composition.

### Implementation Acceptance Gate

RFC-058 technical implementation SHALL NOT be authorized merely because this draft exists.

Implementation requires all of the following:

- RFC-058 Contract Acceptance Review passes;
- AD-044 is accepted;
- accepted RFC-058 / AD-044 documentation is committed;
- the contract commit is pushed to the remote branch;
- exact local/remote commit identity is verified;
- working tree is clean.

Only after that gate may technical implementation begin.

### Contract Acceptance Review

RFC-058 / AD-044 Contract Acceptance Review: passed.

The review confirmed:

- exact repository operation set remains `add` and `get`;
- canonical duplicate identity is `EntityId` only;
- absence returns `None`;
- source reference remains traceability rather than identity or uniqueness;
- no source-reference lookup is introduced;
- no Search or CRUD expansion is introduced;
- no revision semantics are introduced;
- no relational persistence ownership is introduced;
- no Document Library or ingestion responsibility is introduced;
- no default production composition is introduced;
- no unsupported production-security claim is introduced.

Two refinements were accepted before contract approval:

- `app.document.__init__.py` remains empty and introduces no public re-export API;
- future ingestion dependency shape remains a future architecture decision.

### Technical Completion State

RFC-058 contract: Accepted.

AD-044: Accepted.

RFC-058 technical implementation: complete.

Implemented canonical files:

- `app.document.__init__` remains empty;
- `app.document.repository` provides the accepted persistence-neutral repository contract.

Technical implementation remains strictly within the accepted RFC-058 / AD-044 boundary.

### Contract Acceptance Review Requirements

Before acceptance, RFC-058 SHALL be reviewed against:

- AD-043 / RFC-057;
- `app.domain.document`;
- shared `EntityId`;
- existing `KnowledgeRecordRepository` precedent;
- AD-040 / RFC-054;
- existing repository namespace patterns;
- current composition;
- Runtime and Bootstrap boundaries;
- Security boundaries;
- current regression tests;
- Project Context;
- Session Handoff;
- Engineering Journal;
- Architecture Decisions;
- Active Work Register.

Acceptance SHALL specifically verify that the contract does not accidentally introduce:

- source-reference identity;
- source-reference uniqueness;
- hidden search capability;
- CRUD expansion;
- lifecycle/revision semantics;
- relational persistence ownership;
- Document Library behavior;
- ingestion behavior;
- default production composition;
- unsupported security or production-readiness claims.

### Next Exact Action

Commit and push the RFC-058 engineering-memory closure.

Then perform the required post-RFC-058 Source-of-Truth architecture review before selecting, defining or implementing another architecture RFC.
---

## RFC-057 — Canonical Enterprise Document Foundation Boundary

### Status

Technically Complete.

Post-RFC-056 Source-of-Truth architecture review: complete.

The initial post-review working direction:

`Canonical Document Knowledge Ingestion Application Boundary`

was refined before contract acceptance.

Repository evidence showed that PlantMind does not yet possess a canonical enterprise Document identity or Document domain contract.

A document-ingestion application service introduced before that foundation would either:

- invent document identity and lifecycle semantics inside an application service; or
- become a thin translation wrapper over `KnowledgeCaptureApplicationService`.

Neither outcome is accepted.

Architecture decision:

`AD-043 — Canonical Enterprise Document Foundation Boundary`

AD-043 status: Accepted.

RFC-057 technical implementation is complete within the accepted AD-043 architecture boundary.

Contract commit: `63d9119`.

Technical commit: `a134c7a`.

Remote technical push and exact local/remote commit identity are verified.

Technical verification:

- Focused RFC-057 plus Knowledge architecture verification: 70 passed
- Full PlantMind regression: 586 passed
- Python compilation: passed
- `git diff --check`: passed
- Working tree after technical push: clean

### Objective

Establish the minimum canonical enterprise Document domain required before PlantMind introduces Document Library persistence, document revision lifecycle, parsing, ingestion, search, Knowledge transformation or AI-assisted document capabilities.

RFC-057 SHALL define what one enterprise Document is inside PlantMind.

RFC-057 SHALL establish:

- canonical PlantMind identity for a Document;
- open document classification;
- open source-system classification;
- traceable source reference;
- immutable canonical document title;
- explicit separation between canonical Document-record identity and future revision-lineage, binary, storage and ingestion semantics.

RFC-057 SHALL NOT implement a Document Library.

RFC-057 SHALL NOT implement document ingestion.

### Architecture Dependencies

RFC-057 depends upon and SHALL preserve:

- shared `EntityId` and `DomainEntity` primitives from `app.domain.base`;
- AD-039 / RFC-053 — Canonical Enterprise Knowledge Foundation Boundary;
- AD-040 / RFC-054 — Canonical Database Runtime & Schema Lifecycle Foundation;
- AD-041 / RFC-055 — Canonical Knowledge Relational Persistence Adapter Boundary;
- AD-042 / RFC-056 — Canonical Knowledge Capture Application Boundary;
- AD-009 — PI Is One Knowledge Source.

RFC-057 SHALL NOT redesign any accepted Knowledge, persistence, Capture, Runtime or industrial-integration boundary.

### Canonical Document Domain Module

RFC-057 SHALL introduce:

`app.domain.document`

as the canonical enterprise Document domain module.

The canonical contracts SHALL be:

- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`.

The empty or prototype Procedure components SHALL NOT become the canonical Document domain.

RFC-057 SHALL NOT establish a competing domain hierarchy under `app.models`.

### Shared Identity Boundary

`EnterpriseDocument` SHALL use the existing canonical PlantMind:

`EntityId`

as its identity.

RFC-057 SHALL NOT introduce:

- `DocumentId`;
- document-specific UUID infrastructure;
- database-generated Document identity;
- source-reference-as-primary-identity semantics.

Canonical PlantMind identity and external/source-system document references SHALL remain distinct concepts.

`EntityId` SHALL remain the canonical PlantMind identity of the document entity.

### Enterprise Document Entity

RFC-057 SHALL introduce the immutable canonical entity:

`EnterpriseDocument`

derived from:

`DomainEntity[EntityId]`

The minimum fields SHALL be:

- `id: EntityId`;
- `document_type: DocumentType`;
- `title: str`;
- `source: DocumentSource`.

`EnterpriseDocument` SHALL represent one immutable canonical enterprise Document record inside PlantMind.

It SHALL NOT represent:

- document binary content;
- a filesystem file object;
- a parsed document;
- an OCR result;
- a Knowledge record;
- a document revision object;
- a document approval event;
- a search result;
- a graph node;
- an embedding;
- an LLM context window.

### Document Type Boundary

RFC-057 SHALL introduce:

`DocumentType`

as an immutable open classification value object.

`DocumentType.value` SHALL be a string.

Canonical normalization SHALL:

- require a string;
- trim surrounding whitespace;
- normalize the trimmed classification value to lowercase;
- reject an empty normalized value.

`DocumentType` SHALL remain open rather than a closed enum.

Examples of future valid classifications MAY include:

- procedure;
- manual;
- pid;
- cause_effect;
- operating_philosophy;
- lesson_learned;
- incident_report;
- rca_report;
- engineering_drawing.

These examples SHALL NOT become an exhaustive or hard-coded whitelist in RFC-057.

Open classification is required because PlantMind must support multiple enterprise document families without redesigning the canonical domain for every new source class.

### Document Source Type Boundary

RFC-057 SHALL introduce:

`DocumentSourceType`

as an immutable open classification of the originating or registered source system/context of one canonical Document.

`DocumentSourceType.value` SHALL be a string.

Canonical normalization SHALL:

- require a string;
- trim surrounding whitespace;
- normalize the trimmed classification value to lowercase;
- reject an empty normalized value.

The type SHALL remain open.

Examples MAY include future values such as:

- file_server;
- document_control;
- cmms;
- sap;
- manual_registration.

These examples SHALL NOT become an exhaustive whitelist.

RFC-057 SHALL NOT make PI System the universal Document source.

RFC-057 SHALL preserve AD-009 source-neutral architecture.

### Document Source Boundary

RFC-057 SHALL introduce the immutable value object:

`DocumentSource`

with:

- `source_type: DocumentSourceType`;
- `source_reference: str`.

`source_reference` SHALL be:

- caller/source supplied;
- treated as an opaque source-system reference;
- whitespace-trimmed;
- non-empty;
- case-preserving.

RFC-057 SHALL NOT prescribe that `source_reference` must be:

- a filesystem path;
- URL;
- document number;
- SAP identifier;
- SharePoint identifier;
- database key;
- network path.

Those are source-specific concerns.

`DocumentSource` SHALL provide traceability to an origin/reference without coupling the canonical domain to one storage technology.

### Source Reference Is Not Canonical Identity

`DocumentSource.source_reference` SHALL NOT become canonical PlantMind Document identity.

The canonical identity remains:

`EnterpriseDocument.id`

A source reference SHALL NOT automatically be interpreted as:

- globally unique;
- immutable across enterprise systems;
- authoritative;
- verified;
- approved;
- resolvable;
- accessible;
- current.

RFC-057 SHALL NOT define source-reference uniqueness constraints.

Any future source-level deduplication, aliasing, reconciliation or uniqueness contract requires explicit architecture.

### Title Boundary

`EnterpriseDocument.title` SHALL:

- require a string;
- trim surrounding whitespace;
- reject an empty normalized value;
- preserve meaningful casing and content.

RFC-057 SHALL NOT derive the title automatically from:

- filename;
- file path;
- OCR;
- parser output;
- LLM output;
- document number.

Such derivation belongs to future ingestion/parser/application contracts.

### Immutability Boundary

The RFC-057 canonical Document contracts SHALL be immutable.

They SHALL follow the accepted domain style:

`dataclass(frozen=True, slots=True, kw_only=True)`

where compatible with the existing shared domain primitives.

RFC-057 SHALL NOT introduce mutable document state.

Mutation, lifecycle transitions and revision replacement require separate explicit contracts.

### Validation Ownership Boundary

Canonical Document validation SHALL be owned by:

`app.domain.document`

Domain rule violations SHALL use the existing:

`DomainException`

RFC-057 SHALL NOT introduce:

- Pydantic validation as canonical domain validation;
- FastAPI transport validation as canonical domain validation;
- SQLAlchemy model validation as canonical domain validation;
- document-specific application exception framework.

Canonical domain construction SHALL reject structurally invalid Document contracts before any future persistence boundary receives them.

### Knowledge Independence Boundary

`app.domain.document`

SHALL NOT depend upon:

`app.domain.knowledge`

RFC-057 SHALL NOT make `EnterpriseDocument` a subtype of `KnowledgeRecord`.

A Document and a Knowledge record are distinct canonical concepts.

A future accepted document-to-Knowledge transformation boundary MAY connect them.

RFC-057 SHALL NOT perform that transformation.

### Procedure Boundary

A document classified as:

`document_type="procedure"`

SHALL NOT automatically become an operational Procedure aggregate.

The existing empty:

`app.domain.procedure`

is not promoted or completed by RFC-057.

Document identity and future executable/operational Procedure semantics SHALL remain separate concepts.

A future Procedure domain MAY reference canonical `EnterpriseDocument` identity if explicitly accepted.

RFC-057 SHALL NOT invent operational procedure-step, execution, permit, approval or workflow semantics.

### Revision and Version Boundary

RFC-057 SHALL NOT introduce:

- `DocumentRevision`;
- revision number;
- version number;
- effective date;
- issue date;
- superseded-by relationships;
- revision chain;
- current-revision pointer;
- revision comparison;
- revision approval;
- revision rollback.

`EnterpriseDocument` SHALL establish one immutable canonical Document record and its PlantMind identity.

RFC-057 SHALL remain neutral about future revision representation.

It SHALL NOT decide whether future revisions:

- retain the same canonical Document identity;
- receive independent canonical identity;
- are represented as separate immutable Document records;
- are represented through a dedicated revision entity or aggregate.

Those semantics require a dedicated future architecture contract.

### Binary and Representation Boundary

RFC-057 SHALL NOT introduce:

- file bytes;
- blobs;
- MIME type;
- binary storage;
- object storage;
- filesystem storage;
- file checksum;
- file hash;
- file size;
- page count;
- extracted text;
- rendered pages;
- thumbnails.

A canonical `EnterpriseDocument` record is not equivalent to one physical or digital file representation.

Future representation/binary contracts require separate architecture.

### Repository Boundary

RFC-057 SHALL NOT introduce a production or persistence-neutral Document repository.

It SHALL NOT introduce:

- `EnterpriseDocumentRepository`;
- Document add/get/update/delete ports;
- document persistence adapter;
- source-reference query API;
- document listing API.

Repository semantics are intentionally deferred because Document persistence, lifecycle and uniqueness requirements have not yet been accepted.

A future Document persistence boundary SHALL depend on the accepted canonical Document domain rather than creating a competing document model.

### Database Boundary

RFC-057 SHALL NOT introduce:

- SQLAlchemy Document models;
- Document tables;
- Alembic Document migrations;
- PostgreSQL Document persistence;
- database indexes;
- foreign keys;
- uniqueness constraints;
- `DatabaseRuntime` changes.

AD-040 / RFC-054 database runtime ownership remains unchanged.

### Document Library Boundary

RFC-057 SHALL NOT implement a production Document Library.

It SHALL NOT introduce:

- document catalogue service;
- browse/list behavior;
- document binary storage;
- document retrieval service;
- document upload;
- source synchronization;
- document permissions;
- document ownership;
- approval workflow;
- retention;
- archival;
- deletion;
- revision management.

RFC-057 establishes the canonical Document domain that a future Document Library SHALL consume.

### Parsing and Extraction Boundary

RFC-057 SHALL NOT implement:

- PDF parsing;
- Word parsing;
- spreadsheet parsing;
- image extraction;
- OCR;
- text extraction;
- table extraction;
- section detection;
- chunking;
- automatic classification;
- metadata extraction.

The existing empty:

`backend/app/knowledge/document_parser.py`

SHALL remain unpromoted.

A future parsing boundary SHALL depend on accepted Document contracts where appropriate.

### Document Ingestion Boundary

RFC-057 SHALL NOT introduce:

- Document ingestion application service;
- file-upload workflow;
- bulk ingestion;
- document-registration workflow;
- document-to-Knowledge ingestion;
- automatic source synchronization.

The previously considered:

`DocumentKnowledgeIngestionApplicationService`

is explicitly not introduced by RFC-057.

A future document-ingestion contract SHALL build on accepted canonical Document identity rather than inventing document semantics inside a translation service.

### Knowledge Capture Boundary

RFC-057 SHALL NOT modify:

`KnowledgeCaptureApplicationService`

RFC-057 SHALL NOT:

- call Capture;
- modify `KnowledgeCaptureRequest`;
- construct Knowledge records;
- write to `KnowledgeRecordRepository`;
- alter Knowledge provenance semantics.

AD-042 / RFC-056 remains authoritative.

A future document-to-Knowledge boundary SHALL consume accepted Document and Knowledge Capture contracts without bypassing either architecture.

### Search Boundary

RFC-057 SHALL NOT introduce:

- document search;
- keyword search;
- full-text search;
- semantic search;
- similarity search;
- ranking;
- indexes.

Document identity establishment SHALL NOT be represented as Search capability.

### Vector, Graph and AI Boundary

RFC-057 SHALL NOT introduce:

- embeddings;
- vector persistence;
- Qdrant;
- Knowledge Graph persistence;
- Neo4j;
- RAG;
- prompts;
- LLM invocation;
- automatic summarization;
- automatic Knowledge extraction;
- autonomous document agents.

Canonical Document identity does not imply AI-readiness or semantic retrieval readiness.

### Security and Trust Boundary

RFC-057 SHALL preserve the accepted on-premise enterprise deployment model.

RFC-057 does not establish:

- document authentication;
- user authentication;
- document authorization;
- RBAC;
- actor identity;
- document permissions;
- source authenticity;
- document approval;
- document correctness;
- document integrity verification;
- safety approval;
- compliance approval.

`DocumentSource` records origin/reference information only.

It SHALL NOT be interpreted as proof of trust or correctness.

The current prototype `SecurityManager` SHALL NOT be treated as accepted production security capability.

RFC-057 contract or implementation acceptance SHALL NOT be represented as Cybersecurity approval or production deployment readiness.

### Composition Boundary

RFC-057 SHALL NOT modify:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`.

Canonical Document domain types SHALL not cause automatic production composition.

Default startup SHALL remain independent from document storage or document-source availability.

### Runtime and Bootstrap Boundary

RFC-057 SHALL NOT modify:

- Runtime lifecycle states;
- Runtime readiness;
- request admission;
- mandatory-capability policy;
- Bootstrap startup;
- Bootstrap shutdown;
- Health semantics.

Canonical Document domain availability SHALL NOT become Runtime transition authority.

### Industrial Integration Boundary

RFC-057 SHALL NOT introduce production connectivity to:

- PI System;
- DCS;
- OPC UA;
- CMMS;
- SAP;
- File Server;
- document-control systems.

AD-009 source-neutral architecture remains authoritative.

Source-specific connectors require separate contracts.

### TDD Boundary

RFC-057 technical implementation SHALL be test-driven against the accepted contract.

Tests SHALL demonstrate at minimum:

- `DocumentType` is immutable;
- `DocumentSourceType` is immutable;
- `DocumentSource` is immutable;
- `EnterpriseDocument` is immutable;
- `EnterpriseDocument` uses canonical `EntityId`;
- no `DocumentId` type is introduced;
- valid `DocumentType` values are normalized consistently;
- empty `DocumentType` is rejected;
- non-string `DocumentType` is rejected;
- valid `DocumentSourceType` values are normalized consistently;
- empty `DocumentSourceType` is rejected;
- non-string `DocumentSourceType` is rejected;
- `DocumentSource` requires `DocumentSourceType`;
- `source_reference` whitespace is trimmed;
- `source_reference` meaningful casing is preserved;
- empty source reference is rejected;
- non-string source reference is rejected;
- `EnterpriseDocument` requires canonical `EntityId`;
- `EnterpriseDocument` requires canonical `DocumentType`;
- `EnterpriseDocument` requires canonical `DocumentSource`;
- title whitespace is trimmed;
- title meaningful casing is preserved;
- empty title is rejected;
- non-string title is rejected;
- domain failures use `DomainException`;
- domain types require no database;
- domain types perform no file I/O;
- document domain imports no SQLAlchemy;
- document domain imports no FastAPI;
- document domain imports no Pydantic;
- document domain does not depend on `app.domain.knowledge`;
- no Document repository is introduced;
- no Document database model is introduced;
- no Document migration is introduced;
- no document ingestion service is introduced;
- default CompositionRoot remains unchanged;
- existing full regression remains green.

Tests SHALL NOT require:

- PostgreSQL;
- file server;
- PDF;
- OCR;
- parser;
- Qdrant;
- Neo4j;
- LLM;
- PI System;
- DCS;
- OPC UA.

### Architecture Guardrail Boundary

Existing architecture guardrails protecting RFC-053 through RFC-056 SHALL remain authoritative.

RFC-057 SHALL NOT weaken existing tests to introduce the Document domain.

New architecture tests SHALL prove at minimum:

- canonical Document identity uses shared `EntityId`;
- document domain is independent from Knowledge domain;
- document domain has no relational-infrastructure dependency;
- document domain performs no file I/O;
- document domain introduces no repository;
- default platform composition remains unchanged;
- existing placeholder Document/Procedure components are not promoted.

### Implementation Acceptance Boundary

Contract acceptance SHALL NOT authorize technical implementation until the accepted RFC-057 / AD-043 contract is:

- committed;
- pushed to the remote branch;
- verified for exact local/remote commit identity;
- verified with a clean working tree.

Technical implementation SHALL remain strictly inside the accepted canonical Document foundation.

Technical completion SHALL NOT imply:

- Document Library readiness;
- Document persistence;
- document ingestion;
- document parsing;
- revision/version support;
- search readiness;
- Knowledge transformation;
- authentication or authorization readiness;
- Cybersecurity approval;
- production deployment readiness.

### Verification Boundary

Before RFC-057 may be marked technically complete, verification SHALL include:

- focused canonical Document domain tests;
- architecture-boundary tests;
- impacted domain regression;
- full PlantMind regression;
- Python compilation;
- `git diff --check`;
- Git commit verification;
- remote push verification;
- exact local/remote commit identity;
- clean working tree;
- required Source-of-Truth engineering-memory closure.

No external infrastructure is required to verify this domain foundation.

### Contract Review State

RFC-057 Contract Acceptance Review: passed.

Architecture decision:

`AD-043 — Canonical Enterprise Document Foundation Boundary`

AD-043 status: Accepted.

The Canonical Enterprise Document Foundation Boundary contract is accepted.

Contract review confirmed:

- canonical Document identity uses shared `EntityId`;
- no competing `DocumentId` is introduced;
- Document and Knowledge remain separate canonical domains;
- `EnterpriseDocument` remains neutral about future revision representation;
- source reference remains distinct from canonical PlantMind identity;
- persistence, Document Library, revision lifecycle, parsing and ingestion remain deferred;
- default composition and Runtime remain unchanged;
- no unsupported production-security or Cybersecurity claim is introduced.

RFC-057 technical implementation is complete and verified within the accepted AD-043 boundary.

Technical completion preserves all accepted deferred-capability, composition, Runtime, security and production-readiness guardrails.

### Post-Completion Architecture Review

The required post-RFC-057 Source-of-Truth architecture review is complete.

The evidence-based next architecture direction is RFC-058 — Canonical Enterprise Document Repository Foundation Boundary.

RFC-058 remains contract-not-accepted and implementation-not-authorized.

---

## RFC-056 — Canonical Knowledge Capture Application Boundary

### Status

Technically Complete.

AD-042 is accepted.

RFC-056 technical implementation is complete within the accepted AD-042 architecture boundary.

Technical commit: `66c24f0`.

Remote technical push and exact local/remote commit identity are verified.

The required post-RFC-056 Source-of-Truth architecture review is complete.

The evidence-based next architecture direction is RFC-057 — Canonical Document Knowledge Ingestion Application Boundary.

### Objective

Establish the first explicit application-level use case for canonical enterprise Knowledge capture without introducing a generic delegation service over `KnowledgeRecordRepository`.

RFC-056 SHALL define the application boundary that accepts one Knowledge capture request, constructs one canonical immutable `KnowledgeRecord`, persists that record through the persistence-neutral `KnowledgeRecordRepository`, and returns the captured canonical record.

RFC-056 SHALL NOT redesign the canonical Knowledge domain, relational persistence adapter or database runtime.

### Architecture Dependencies

RFC-056 depends upon and SHALL preserve:

- AD-039 / RFC-053 — Canonical Enterprise Knowledge Foundation Boundary;
- AD-040 / RFC-054 — Canonical Database Runtime & Schema Lifecycle Foundation;
- AD-041 / RFC-055 — Canonical Knowledge Relational Persistence Adapter Boundary.

`KnowledgeRecord` remains the canonical representation of one enterprise Knowledge item.

`KnowledgeRecordRepository` remains the canonical persistence-neutral repository port.

Canonical domain invariants remain owned by `app.domain.knowledge`.

Repository Session and transaction semantics remain owned by the RFC-055 infrastructure adapter.

`DatabaseRuntime` remains the owner of relational engine and session-factory lifecycle.

### Canonical Capture Application Responsibility

RFC-056 SHALL introduce one specialized application-level Knowledge capture use case.

The canonical application service SHALL be:

`KnowledgeCaptureApplicationService`

under:

`app.services.knowledge_capture_application_service`

The RFC-056 application contracts:

- `KnowledgeCaptureApplicationService`;
- `KnowledgeCaptureRequest`;
- `KnowledgeCaptureSubject`;

SHALL reside in that same module.

This follows the existing specialized Application Service namespace and keeps the first Capture use case cohesive without introducing a competing `app.application` hierarchy or a premature Knowledge application package.

The application boundary SHALL NOT expose generic repository-equivalent application methods such as:

- `add(...)`;
- `get(...)`;
- `update(...)`;
- `delete(...)`;
- `upsert(...)`.

The canonical application operation SHALL represent the business action:

`capture(request: KnowledgeCaptureRequest) -> KnowledgeRecord`

The Capture boundary SHALL:

1. receive one immutable Knowledge capture request;
2. construct canonical Knowledge value objects required by that request;
3. establish one canonical `EntityId` for the new record;
4. establish one provenance capture timestamp;
5. construct one canonical immutable `KnowledgeRecord`;
6. submit that record through `KnowledgeRecordRepository.add(...)`;
7. return the captured `KnowledgeRecord` only after repository add succeeds.

The Capture boundary SHALL NOT call `KnowledgeRecordRepository.get(...)` merely to confirm the write.

### Knowledge Capture Request Boundary

RFC-056 SHALL introduce immutable application input contracts:

- `KnowledgeCaptureRequest`;
- `KnowledgeCaptureSubject`.

`KnowledgeCaptureSubject` SHALL contain:

- `subject_type: str`;
- `subject_id: EntityId`.

`KnowledgeCaptureSubject` is an application input contract and SHALL NOT become a second canonical Knowledge subject domain model.

`KnowledgeCaptureRequest` SHALL contain the minimum caller-supplied inputs required to construct canonical Knowledge:

- `kind: str`;
- `title: str`;
- `content: str`;
- `source_type: str`;
- `source_reference: str`;
- `subject: KnowledgeCaptureSubject | None`.

The caller SHALL NOT provide:

- canonical `KnowledgeRecord.id`;
- canonical provenance `captured_at`;
- a preconstructed `KnowledgeRecord`;
- a preconstructed `KnowledgeProvenance`;
- a preconstructed canonical `KnowledgeSubject`.

Canonical domain construction belongs to the Capture application boundary.

The Capture request and Capture subject input SHALL NOT become:

- HTTP transport schemas;
- database row models;
- document-ingestion models;
- vector payloads;
- graph nodes;
- prompts;
- reasoning results.

Future transport or ingestion boundaries MAY translate their own inputs into `KnowledgeCaptureRequest` only after their own architecture contracts are accepted.

### Canonical Domain Construction Boundary

The Capture application boundary SHALL construct the canonical domain representation using the accepted RFC-053 types.

It SHALL use the canonical Knowledge domain to construct:

- `KnowledgeKind`;
- `KnowledgeSourceType`;
- `KnowledgeProvenance`;
- `KnowledgeSubjectType` when a subject is supplied;
- `KnowledgeSubject` when a subject is supplied;
- `KnowledgeRecord`.

Canonical Knowledge domain validation SHALL remain authoritative.

RFC-056 SHALL NOT duplicate domain normalization or invariant rules inside the application service.

Invalid canonical Knowledge input SHALL continue to fail through the accepted domain exception semantics.

RFC-056 SHALL NOT introduce a competing application-level Knowledge validation framework.

### Application Dependency Injection Boundary

`KnowledgeCaptureApplicationService` SHALL receive the persistence-neutral:

`KnowledgeRecordRepository`

explicitly during construction.

The service SHALL also support narrow per-instance injection of:

- an identity source compatible with `() -> EntityId`;
- a capture-time source compatible with `() -> datetime`.

The default identity source SHALL use `EntityId.new()`.

The default capture-time source SHALL obtain the current timezone-aware UTC time when the Capture operation requires it.

Identity and capture-time sources SHALL NOT:

- be evaluated during module import;
- be evaluated merely because the service is constructed;
- require process-global mutable state;
- require database availability;
- require Runtime or Bootstrap availability.

Injected deterministic sources SHALL belong to the constructed service instance and SHALL NOT require global monkey-patching or global mutation.

RFC-056 SHALL NOT introduce a general Clock service, identity service, provider registry or dependency-injection framework merely to satisfy this boundary.

### Canonical Identity Boundary

The Capture boundary SHALL create exactly one canonical `EntityId` for each attempted canonical record construction that reaches identity creation.

The default canonical identity source SHALL remain:

`EntityId.new()`

RFC-056 SHALL NOT introduce a platform-wide identity-generation framework.

For deterministic testing, the Capture implementation SHALL permit narrow injection of an identity-producing callable compatible with:

`() -> EntityId`

For one Capture invocation that reaches canonical identity creation, the configured identity source SHALL be invoked exactly once.

The identity source SHALL NOT:

- depend on SQLAlchemy;
- depend on PostgreSQL;
- read repository state to select an identity;
- retry with a new identity after repository duplicate conflict;
- replace canonical `EntityId` with a persistence-generated identifier.

A duplicate repository conflict SHALL NOT cause silent identity regeneration.

### Provenance Capture-Time Boundary

`KnowledgeProvenance.captured_at` SHALL represent the time PlantMind executes the canonical capture use case.

The caller SHALL NOT set canonical `captured_at` through `KnowledgeCaptureRequest`.

The default capture-time source SHALL produce a timezone-aware UTC `datetime`.

RFC-056 SHALL NOT introduce a platform-wide Clock framework merely for this use case.

For deterministic testing, the Capture implementation SHALL permit narrow injection of a time-producing callable compatible with:

`() -> datetime`

For one Capture invocation that successfully obtains canonical identity and reaches provenance construction, the configured capture-time source SHALL be invoked exactly once.

If identity creation fails, the capture-time source SHALL NOT be invoked.

Repository failure SHALL NOT cause either identity or capture-time source to be invoked again.

The returned time remains subject to canonical RFC-053 domain validation and UTC normalization.

RFC-056 SHALL NOT interpret `captured_at` as:

- document creation time;
- document effective date;
- equipment-event time;
- PI observation time;
- approval time;
- source-system modification time.

Any future source-event or document-effective timestamp requires its own explicit provenance contract.

### Knowledge Subject Boundary

`KnowledgeCaptureRequest.subject` MAY contain one immutable application input:

`KnowledgeCaptureSubject`

or `None`.

When present, the Capture application boundary SHALL construct one canonical `KnowledgeSubject` using:

- canonical `KnowledgeSubjectType` constructed from `subject_type`;
- the supplied canonical `EntityId` from `subject_id`.

The caller SHALL NOT be required to construct canonical `KnowledgeSubject` merely to invoke the Capture use case.

RFC-056 SHALL preserve the accepted RFC-053 semantics that canonical `KnowledgeSubject` is a typed contextual reference rather than an exhaustive relationship model.

RFC-056 SHALL NOT:

- load the referenced entity;
- verify referenced entity existence;
- verify caller access to the referenced entity;
- verify subject-type correspondence;
- introduce an Asset Library;
- introduce a subject resolver;
- create a relational foreign-key dependency to a specific subject aggregate.

Subject existence, accessibility and type verification remain deferred to a future explicit application or integration contract.

### Repository Interaction Boundary

The Capture application boundary SHALL receive:

`KnowledgeRecordRepository`

explicitly.

It SHALL remain persistence-implementation neutral.

For one capture invocation that reaches persistence, the application boundary SHALL call:

`KnowledgeRecordRepository.add(record)`

exactly once.

The exact canonical record supplied to `add(...)` SHALL be the record returned after successful persistence.

The application boundary SHALL NOT:

- construct SQLAlchemy Session objects;
- construct a database engine;
- construct `DatabaseRuntime`;
- commit or roll back transactions;
- execute Alembic migrations;
- call `MetaData.create_all()`;
- query the repository before add to prevent duplicates;
- perform hidden repository retries.

Repository-operation transaction semantics remain owned by RFC-055.

### Duplicate Identity Boundary

`KnowledgeRecordAlreadyExistsError` remains the accepted repository-boundary duplicate-identity conflict.

RFC-056 SHALL NOT translate a duplicate identity conflict into success.

RFC-056 SHALL NOT:

- regenerate identity automatically;
- overwrite the existing canonical record;
- retry the capture with another identity;
- perform a pre-add existence query as authoritative duplicate prevention.

Unless a future application contract requires explicit translation, the accepted repository duplicate conflict SHALL propagate unchanged through the Capture boundary.

### Failure Boundary

Canonical domain validation failures SHALL preserve canonical domain failure semantics.

`KnowledgeRecordAlreadyExistsError` SHALL preserve repository conflict semantics.

Unexpected repository failures SHALL propagate and SHALL NOT become synthetic success.

Identity-source failures SHALL propagate.

Capture-time-source failures SHALL propagate.

RFC-056 SHALL introduce no automatic retry.

RFC-056 SHALL introduce no platform-wide application exception taxonomy.

A failed persistence operation SHALL NOT return a successfully captured `KnowledgeRecord`.

### ApplicationFacade Boundary

RFC-056 SHALL NOT modify:

`ApplicationFacade`

The existing `ApplicationFacade` remains the stable entry boundary for the existing analysis/orchestration workload.

Knowledge capture SHALL remain a distinct specialized application use case.

RFC-056 SHALL NOT route Knowledge capture through the reasoning workflow merely to reuse an existing facade.

Future unification of product-facing application entry points requires a separate explicit architecture decision.

### Composition Boundary

RFC-056 SHALL NOT automatically:

- construct `DatabaseRuntime` from default `CompositionRoot.build()`;
- construct the relational Knowledge repository in default platform composition;
- register `KnowledgeRecordRepository` in the default `ServiceContainer`;
- register the Knowledge Capture application service in default `ServiceContainer`;
- expose Knowledge capture from default `PlatformComposition`;
- require `DATABASE_URL` during default application startup.

Existing zero-argument `CompositionRoot.build()` behavior SHALL remain compatible.

Production Knowledge persistence and Capture composition require a separately accepted composition boundary.

### Runtime and Bootstrap Boundary

RFC-056 SHALL NOT modify:

- Runtime lifecycle states;
- readiness semantics;
- request admission;
- mandatory-capability policy;
- operational-transition evidence;
- Bootstrap startup;
- Bootstrap shutdown;
- Health semantics.

Knowledge capture failure SHALL NOT independently become Runtime transition authority.

The existence of a Knowledge Capture application service SHALL NOT make relational Knowledge persistence a mandatory Runtime capability.

### API and Transport Boundary

RFC-056 SHALL introduce no:

- Knowledge HTTP endpoint;
- REST schema;
- GraphQL schema;
- CLI command;
- message-bus contract;
- file-upload contract.

Transport boundaries SHALL NOT be implied merely because the Capture application contract exists.

A future API SHALL depend upon the Capture application boundary rather than bypassing it and calling the repository directly.

### Document and Ingestion Boundary

RFC-056 SHALL NOT implement:

- Document Library behavior;
- file upload;
- PDF parsing;
- OCR;
- chunking;
- document versioning;
- document storage;
- document-to-Knowledge transformation;
- bulk ingestion.

A future document-ingestion boundary MAY construct one or more `KnowledgeCaptureRequest` values and invoke the accepted Capture application boundary.

RFC-056 SHALL NOT promote the existing empty `document_parser.py` into production capability.

### Search, Graph, Vector and RAG Boundary

RFC-056 SHALL NOT introduce:

- keyword search;
- full-text search;
- semantic search;
- similarity search;
- ranking;
- embeddings;
- vector persistence;
- Qdrant integration;
- Knowledge Graph persistence;
- Neo4j integration;
- graph traversal;
- RAG;
- LLM invocation.

Identity-based repository lookup remains distinct from Search.

Knowledge capture SHALL establish canonical records for future capabilities without implementing those capabilities.

### PI and Operational Data Boundary

RFC-056 SHALL NOT introduce:

- production PI connectivity;
- DCS connectivity;
- OPC UA connectivity;
- automatic PI-to-Knowledge conversion;
- automatic Observation-to-Knowledge conversion;
- automatic Knowledge-to-Observation conversion.

Captured Knowledge SHALL NOT automatically become trusted operational evidence.

Any such integration requires a future accepted contract.

### Security and Trust Boundary

RFC-056 SHALL preserve the accepted on-premise enterprise deployment model.

RFC-056 does not by itself establish:

- user authentication;
- authorization to capture Knowledge;
- source authenticity;
- source approval;
- correctness of captured content;
- operational trust;
- safety approval;
- compliance approval.

`KnowledgeProvenance` records origin information but SHALL NOT be interpreted as proof of trust or correctness.

Authentication, authorization and trust policy require separately accepted security/application contracts.

Because RFC-056 does not establish authentication, capture authorization or actor-audit semantics, RFC-056 SHALL NOT authorize external or production transport exposure of the Capture use case.

Database credentials SHALL remain outside committed source code.

Code-level RFC-056 acceptance SHALL NOT be represented as Cybersecurity approval or production deployment readiness.

### Observability Boundary

RFC-056 SHALL NOT introduce a new platform-wide logging, metrics or tracing framework merely to support Knowledge capture.

The application service SHALL NOT retain mutable capture history as process-global state.

Future audit, capture-history, event-publication or observability behavior requires an explicit contract.

### TDD Boundary

RFC-056 technical implementation SHALL be test-driven against the accepted contract.

Tests SHALL demonstrate at minimum:

- `KnowledgeCaptureRequest` is immutable;
- `KnowledgeCaptureSubject` is immutable;
- Capture application service receives `KnowledgeRecordRepository` explicitly;
- identity and capture-time sources are not invoked during module import or service construction;
- configured identity source is invoked exactly once when canonical identity creation is reached;
- configured capture-time source is invoked exactly once when provenance construction is reached;
- identity-source failure prevents capture-time-source invocation;
- repository failure does not re-invoke identity or capture-time sources;
- deterministic injected sources require no global mutation;
- canonical `KnowledgeKind` is constructed from request input;
- canonical `KnowledgeSourceType` is constructed from request input;
- canonical provenance source reference is preserved according to domain rules;
- canonical record title and content preserve RFC-053 normalization semantics;
- one canonical `EntityId` is created through the configured identity source;
- one capture timestamp is created through the configured time source;
- capture timestamp is preserved through canonical UTC normalization;
- supplied Capture subject type constructs canonical `KnowledgeSubjectType`;
- supplied Capture subject identity is preserved in canonical `KnowledgeSubject`;
- callers do not need to preconstruct canonical `KnowledgeSubject`;
- absent subject remains `None`;
- repository `add(...)` is called exactly once for a persistence-reaching capture;
- repository `get(...)` is not called by the Capture use case;
- the exact record passed to `add(...)` is returned on success;
- duplicate conflict propagates without retry or identity regeneration;
- unexpected repository failure propagates;
- domain validation failure is not converted into success;
- default identity/time behavior requires no database;
- injected deterministic identity/time sources can be tested without global mutation;
- Capture implementation imports no SQLAlchemy;
- Capture implementation constructs no engine or Session;
- default `CompositionRoot` remains unchanged and database-independent;
- existing ApplicationFacade behavior remains unchanged;
- existing full regression remains green.

Tests SHALL NOT require live PostgreSQL merely to verify the RFC-056 application contract.

### Architecture Guardrail Boundary

Existing architecture tests protecting RFC-053, RFC-054 and RFC-055 SHALL remain authoritative unless RFC-056 explicitly and narrowly evolves one accepted boundary.

Guardrails SHALL NOT be deleted or weakened merely to make RFC-056 implementation tests pass.

The default-composition guardrails SHALL continue to prove that Knowledge persistence and Capture are not automatically registered or exposed.

### Implementation Acceptance Boundary

Contract acceptance SHALL NOT authorize implementation until the accepted contract is:

- committed;
- pushed to the remote branch;
- verified for exact local/remote commit identity;
- verified with a clean working tree.

Technical implementation SHALL remain inside the accepted RFC-056 boundary.

Technical completion SHALL NOT imply:

- production PostgreSQL integration;
- production Capture composition;
- production API exposure;
- Cybersecurity approval;
- production deployment readiness.

Those remain separate gates.

### Verification Boundary

Before RFC-056 may be marked technically complete, verification SHALL include:

- focused RFC-056 unit tests;
- architecture-boundary tests;
- full regression suite;
- Python compilation;
- `git diff --check`;
- Git commit verification;
- remote push verification;
- exact local/remote commit identity;
- clean working tree;
- required Source-of-Truth documentation closure.

No live PostgreSQL verification is required merely for application-boundary code acceptance because RFC-056 does not authorize production relational composition.

### Contract Review State

RFC-056 Contract Acceptance Review: passed.

Architecture decision: AD-042.

The Canonical Knowledge Capture Application Boundary contract is accepted.

The accepted contract was reviewed against:

- RFC-053 / AD-039;
- RFC-054 / AD-040;
- RFC-055 / AD-041;
- canonical Knowledge domain implementation;
- canonical `KnowledgeRecordRepository` port;
- RFC-055 relational repository implementation;
- existing specialized Application Service pattern;
- CompositionRoot and ServiceContainer guardrails;
- current regression tests;
- Project Context;
- Session Handoff;
- Engineering Journal;
- Active Work Register.

Contract review found no conflicting ownership, duplicated repository responsibility, hidden relational coupling, premature production composition or unsupported production-security claim.

Technical implementation is complete within the accepted RFC-056 / AD-042 architecture boundary.

Technical verification:

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

Production Knowledge Capture composition, external transport exposure, authentication, authorization, actor-audit semantics, PostgreSQL deployment verification and Cybersecurity approval remain separately gated.

### Historical Next Action at That Stage

At that stage, the working direction was to draft RFC-057 as a Canonical Document Knowledge Ingestion Application Boundary.

That direction was later refined before RFC-057 contract acceptance, after repository review established that PlantMind first required a Canonical Enterprise Document Foundation.

---

## RFC-055 — Canonical Knowledge Relational Persistence Adapter Boundary

### Status

Complete.

AD-041 is accepted.

Technical implementation is complete within the accepted RFC-055 / AD-041 architecture boundary.

Technical implementation commit: `9fc34c7`.

Engineering-memory closure commit: `19c3954`.

Post-RFC-055 architecture review closure: `1624f7e`.

Post-RFC-055 architecture-direction refinement: `48f252d`.

Production PostgreSQL connectivity, production schema deployment and Cybersecurity approval remain separately gated and intentionally unclaimed.

### Objective

Establish the first canonical production relational persistence adapter for RFC-053 enterprise Knowledge while preserving the persistence-neutral Knowledge domain and the RFC-054 database runtime and schema-lifecycle boundaries.

RFC-055 SHALL implement the existing `KnowledgeRecordRepository` port through the canonical relational database foundation.

RFC-055 SHALL NOT redesign the Knowledge domain or the canonical database runtime.

### Architecture Dependencies

RFC-055 depends upon and SHALL preserve:

- AD-039 / RFC-053 — Canonical Enterprise Knowledge Foundation Boundary;
- AD-040 / RFC-054 — Canonical Database Runtime & Schema Lifecycle Foundation.

`KnowledgeRecord` remains the canonical domain representation.

`KnowledgeRecordRepository` remains the canonical persistence-neutral repository port.

`DatabaseRuntime` remains the canonical owner of relational engine and session-factory lifecycle.

`DatabaseBase.metadata` remains the canonical relational schema metadata authority.

Alembic remains the sole canonical relational schema-migration authority.

### Canonical Repository Adapter Responsibility

RFC-055 SHALL introduce one infrastructure-owned relational implementation of:

`KnowledgeRecordRepository`

The adapter SHALL implement the existing repository contract exactly:

- `add(record: KnowledgeRecord) -> None`;
- `get(record_id: EntityId) -> KnowledgeRecord | None`.

RFC-055 SHALL NOT add relational or SQLAlchemy-specific methods to the canonical repository port merely for persistence convenience.

The relational adapter SHALL NOT become the owner of canonical Knowledge semantics.

### Relational Representation Boundary

RFC-055 SHALL introduce an infrastructure-owned SQLAlchemy mapped representation distinct from the canonical `KnowledgeRecord` domain entity.

The mapped representation SHALL NOT replace, subclass or become the canonical Knowledge domain entity.

The canonical relational table SHALL be:

`knowledge_records`

The relational representation SHALL preserve:

- canonical record UUID identity;
- Knowledge kind;
- title;
- content;
- provenance source type;
- provenance source reference;
- timezone-aware provenance capture timestamp;
- optional Knowledge subject type;
- optional Knowledge subject UUID identity.

Canonical record identity SHALL be protected by the table primary key.

Canonical record and subject identities SHALL preserve UUID semantics.

The provenance timestamp SHALL preserve timezone-aware semantics.

Subject type and subject identity SHALL either both be absent or both be present.

The relational schema SHALL enforce that subject-pair invariant.

RFC-055 SHALL NOT add persistence fields for:

- embeddings;
- vectors;
- graph identifiers;
- search ranking;
- LLM metadata;
- PI values;
- reasoning results;
- document-ingestion workflow state.

Those capabilities remain outside the RFC-055 persistence boundary.

### Persistence Identity and Mutation Boundary

Canonical Knowledge identity and provenance values SHALL originate from the canonical domain record.

The relational database SHALL NOT generate or replace the canonical `KnowledgeRecord` identity.

The relational database SHALL NOT generate or replace the canonical provenance capture timestamp.

RFC-055 SHALL implement persistence only through the existing `add()` and `get()` repository operations.

RFC-055 SHALL NOT introduce:

- update;
- delete;
- upsert;
- merge-based overwrite;
- database-generated canonical Knowledge identity.

Any future Knowledge mutation or retention semantics require a separate accepted architecture contract.

### Duplicate Conflict Identification Boundary

The canonical primary-key constraint for `knowledge_records` SHALL have an explicit stable constraint identity shared by the mapped schema and Alembic migration.

Duplicate translation SHALL rely upon structured database or driver failure information sufficient to identify the canonical record-identity constraint.

RFC-055 SHALL NOT identify duplicate canonical identity by parsing human-readable database error-message text.

Only a failure positively identified as a violation of the canonical `knowledge_records` identity constraint SHALL become `KnowledgeRecordAlreadyExistsError`.

Other integrity failures SHALL preserve their infrastructure failure semantics.

### Domain Mapping Boundary

RFC-055 SHALL define explicit mapping between:

- canonical `KnowledgeRecord`;
- infrastructure-owned relational representation.

Domain-to-relational mapping SHALL persist canonical normalized domain values.

Relational-to-domain mapping SHALL reconstruct canonical domain objects through their approved domain constructors.

Relational persistence SHALL NOT bypass canonical Knowledge domain validation.

The mapping SHALL preserve:

- `EntityId`;
- `KnowledgeKind`;
- `KnowledgeSourceType`;
- `KnowledgeProvenance`;
- optional `KnowledgeSubjectType`;
- optional subject `EntityId`;
- title;
- content;
- provenance timestamp semantics.

A relational row SHALL NOT become or replace the canonical domain entity.

SQLAlchemy SHALL NOT leak into:

- `app.domain`;
- `KnowledgeRecordRepository`;
- other persistence-neutral Knowledge contracts.

### Session Ownership Boundary

The relational repository adapter SHALL receive the approved canonical session-factory boundary explicitly.

The adapter SHALL NOT:

- construct an independent SQLAlchemy engine;
- construct a competing canonical session factory;
- read global database settings as a hidden dependency;
- own a mutable process-global Session;
- share mutable Session instances between repository operations.

Each repository operation SHALL use an independent deterministic session lifetime.

Every session opened by the repository SHALL be closed after the operation completes or fails.

`DatabaseRuntime` SHALL remain the owner of engine and session-factory lifecycle.

The Knowledge repository SHALL NOT assume ownership of `DatabaseRuntime` disposal.

### Transaction Ownership Boundary

RFC-054 intentionally did not assign repository transaction semantics to `DatabaseRuntime`.

RFC-055 SHALL establish repository-operation transaction ownership for the relational Knowledge adapter.

`add()` SHALL execute as one atomic repository transaction.

A successful `add()` SHALL complete one transaction commit.

A failed `add()` SHALL NOT leave a partially persisted Knowledge record.

Failure during `add()` SHALL cause rollback through the approved SQLAlchemy transaction boundary before the repository operation terminates.

`get()` SHALL be a read operation and SHALL NOT perform an application-data commit.

Transaction handling SHALL NOT silently discard or misclassify the original operation failure. If rollback or cleanup itself fails, that secondary infrastructure failure SHALL remain observable while preserving the original operation failure as exception context where supported. Repository-boundary exception translation is permitted only where RFC-055 explicitly authorizes it.

RFC-055 SHALL NOT introduce a Unit of Work abstraction.

RFC-055 SHALL NOT introduce cross-repository transaction coordination.

Any future transaction spanning:

- multiple repositories;
- multiple aggregate operations;
- application workflow boundaries;

requires a separate accepted architecture contract.

### Duplicate Identity Boundary

Canonical Knowledge record identity SHALL be protected by the relational primary key of `knowledge_records`.

`add()` SHALL NOT silently overwrite an existing canonical identity.

The repository SHALL NOT use an application-side pre-insert existence check as the authoritative duplicate-prevention mechanism.

The relational uniqueness constraint SHALL remain the concurrency-safe authority for canonical identity.

Only an integrity failure that can be positively identified as a canonical identity conflict for `knowledge_records` SHALL be translated to:

`KnowledgeRecordAlreadyExistsError`

The adapter SHALL NOT translate every SQLAlchemy `IntegrityError` into `KnowledgeRecordAlreadyExistsError`.

Failures involving:

- subject-pair constraints;
- malformed relational state;
- unrelated integrity constraints;
- mapping defects;
- connection failures;
- driver failures;
- transaction failures;

SHALL preserve their infrastructure failure semantics and SHALL NOT be misclassified as duplicate canonical identity.

After a duplicate-identity attempt:

- the original persisted Knowledge record SHALL remain unchanged;
- the duplicate record SHALL NOT replace or partially modify it;
- the failed repository transaction SHALL be rolled back before the operation terminates.

Duplicate-conflict diagnostics SHALL identify the canonical record identity without exposing full Knowledge content or database credentials.

### Subject Reference Boundary

`KnowledgeSubject` is an open typed domain reference.

RFC-055 SHALL persist the subject as:

- optional subject type;
- optional subject UUID identity.

RFC-055 SHALL NOT introduce a relational foreign key from `knowledge_records` to one specific subject table.

The subject reference is polymorphic at the domain boundary and SHALL NOT be incorrectly constrained to one relational aggregate.

Subject type and subject identity SHALL satisfy the invariant:

- both absent; or
- both present.

Any future cross-domain relational referential-integrity mechanism requires a separate architecture review.

### Migration Boundary

RFC-055 SHALL introduce one new append-only Alembic migration after revision:

`0001`

The new revision SHALL establish the canonical `knowledge_records` relational schema.

RFC-055 SHALL NOT modify, rewrite or repurpose migration revision `0001`.

The infrastructure-owned mapped representation SHALL register `knowledge_records` with the canonical `DatabaseBase.metadata` schema authority.

The Alembic migration SHALL remain schema-aligned with that canonical metadata.

The migration SHALL establish at minimum:

- canonical UUID primary-key identity;
- Knowledge kind storage;
- title storage;
- Knowledge content storage;
- provenance source-type storage;
- provenance source-reference storage;
- timezone-aware provenance timestamp storage;
- nullable subject-type storage;
- nullable subject-UUID storage;
- enforcement of the subject-pair invariant.

The migration SHALL NOT introduce:

- Knowledge Graph tables;
- vector tables;
- embedding columns;
- search indexes unrelated to canonical identity;
- document-ingestion tables;
- LLM persistence;
- PI persistence.

The migration graph SHALL retain exactly one canonical head after RFC-055.

Applied migration history SHALL remain append-only.

Application startup SHALL NOT automatically execute Alembic migrations.

`MetaData.create_all()` SHALL NOT become the production schema-deployment mechanism.

RFC-055 SHALL NOT claim successful production schema deployment merely because the migration definition exists or migration tests pass.

Production schema application requires a separately approved deployment environment.

### Downgrade Safety Boundary

Migration `0002` MAY define reversal of only the relational schema introduced by `0002`.

Reversal MAY include removal of the `knowledge_records` table.

Such removal SHALL be treated as destructive once canonical Knowledge data exists.

The presence of a destructive `downgrade()` definition SHALL NOT constitute authorization to execute that downgrade against a data-bearing environment.

Execution of a destructive RFC-055 downgrade against a data-bearing environment requires a separate explicit migration and deployment review.

The RFC-055 downgrade SHALL NOT modify revision `0001` or unrelated relational schema.

Runtime and Bootstrap SHALL NOT automatically execute the downgrade.

RFC-055 tests MAY exercise downgrade behavior only in isolated disposable test environments.

Successful downgrade testing SHALL NOT be represented as production rollback approval.

### Metadata Registration and Schema Alignment Boundary

The canonical `knowledge_records` mapped table SHALL be registered with `DatabaseBase.metadata`.

Mapped-table registration SHALL NOT:

- create a database engine;
- create a Session;
- open a database connection;
- read hidden database configuration;
- execute schema migration.

The Alembic environment SHALL load the canonical mapped-table registration before using `DatabaseBase.metadata` for schema comparison or migration tooling.

RFC-055 SHALL establish one linear migration successor to `0001`:

`0002`

The mapped schema and migration `0002` SHALL remain aligned for:

- table identity;
- column semantics;
- UUID identity semantics;
- timezone-aware provenance timestamp semantics;
- nullability;
- primary-key identity;
- subject-pair enforcement.

Canonical record identity, Knowledge kind, title, content, provenance source type, provenance source reference and provenance capture timestamp SHALL be non-null relational values.

Subject type and subject identity SHALL remain nullable only as the approved both-absent or both-present pair.

The canonical record primary-key constraint SHALL have the stable explicit identity:

`pk_knowledge_records`

The subject-pair constraint SHALL have the stable explicit identity:

`ck_knowledge_records_subject_pair`

Schema metadata registration SHALL NOT make database availability mandatory during application import or startup.

### Composition Boundary

RFC-055 SHALL implement the canonical relational Knowledge adapter without automatically making relational Knowledge persistence part of default platform composition.

The adapter MAY be constructed explicitly with the approved canonical session-factory boundary for focused verification and future production composition.

RFC-055 SHALL NOT automatically:

- construct `DatabaseRuntime` from `CompositionRoot.build()`;
- register `KnowledgeRecordRepository` in the default `ServiceContainer`;
- expose a Knowledge repository from default `PlatformComposition`;
- require `DATABASE_URL` during default application startup;
- make PostgreSQL availability a mandatory platform dependency.

Default `CompositionRoot.build()` SHALL remain usable without relational database configuration.

Existing zero-argument CompositionRoot construction behavior SHALL remain compatible.

Production composition of the relational Knowledge adapter SHALL be deferred until an accepted production application capability requires Knowledge persistence and explicitly defines ownership of that composition.

### Bootstrap and Runtime Boundary

RFC-055 SHALL NOT modify:

- Runtime states;
- Runtime transition authority;
- Runtime readiness semantics;
- request admission;
- operational-transition evidence;
- mandatory-capability policy;
- capability availability semantics;
- Health behavior;
- Bootstrap startup semantics;
- Bootstrap shutdown semantics.

Database persistence availability SHALL NOT automatically become a mandatory Runtime capability.

A repository operation failure SHALL NOT independently transition Runtime state.

Bootstrap SHALL NOT automatically connect to PostgreSQL merely because the relational Knowledge adapter exists.

Runtime remains the sole lifecycle-transition authority.

### Application Boundary

RFC-055 establishes persistence infrastructure only.

RFC-055 SHALL NOT introduce a production Knowledge application service.

RFC-055 SHALL NOT introduce a Knowledge HTTP transport boundary.

RFC-055 SHALL NOT change `ApplicationFacade`, orchestration, reasoning or operational-transition responsibilities.

A future application capability SHALL explicitly define when Knowledge is written or read and how production repository composition is owned.

### Failure Boundary

Unexpected relational infrastructure failures SHALL propagate explicitly.

RFC-055 SHALL NOT introduce:

- automatic database retry;
- hidden retry loops;
- synthetic persistence success;
- silent data loss;
- silent overwrite;
- fallback to in-memory persistence;
- broad platform-wide database exception translation.

Only a positively identified canonical record identity conflict SHALL be translated to `KnowledgeRecordAlreadyExistsError`.

All other unexpected infrastructure failures SHALL retain their actual failure semantics.

Rollback and session cleanup SHALL be deterministic. A secondary rollback or cleanup failure SHALL remain observable and SHALL NOT silently erase the original operation failure context where exception chaining is supported.

RFC-055 SHALL NOT modify Runtime lifecycle state in response to repository failure.

### Observability Boundary

RFC-055 MAY provide diagnostics required to identify repository operation failure classes.

Diagnostics SHALL NOT expose:

- database passwords;
- credential-bearing database URLs;
- full canonical Knowledge content;
- secrets contained in Knowledge content.

Repository diagnostics MAY identify safe operational metadata such as operation type, canonical record identity, repository boundary and failure class.

Logging consolidation remains outside RFC-055 scope.

### Security Boundary

RFC-055 SHALL preserve the accepted on-premise enterprise deployment model.

RFC-055 SHALL NOT introduce external hosted persistence or new outbound data transfer.

Database credentials SHALL remain outside committed source code.

RFC-055 SHALL NOT claim completion of production PostgreSQL authentication, certificate policy, network segmentation, database encryption policy, backup policy, database hardening or Cybersecurity deployment approval.

Those remain deployment and Cybersecurity responsibilities until separately reviewed and verified.

### Prototype and Advanced Capability Boundary

RFC-055 SHALL NOT promote existing prototype or placeholder Knowledge components into production.

RFC-055 SHALL NOT introduce:

- Document Library behavior;
- Asset Library behavior;
- document ingestion;
- semantic search;
- vector persistence;
- Qdrant integration;
- Knowledge Graph persistence;
- Neo4j integration;
- RAG;
- LLM invocation;
- Knowledge HTTP APIs;
- production PI connectivity.

The purpose of RFC-055 is canonical relational persistence of RFC-053 Knowledge only.

### Infrastructure Namespace and Guardrail Evolution Boundary

The canonical RFC-055 relational Knowledge implementation SHALL be owned by:

`app.infrastructure.knowledge`

RFC-055 SHALL NOT place SQLAlchemy relational implementation inside:

- `app.domain`;
- `app.knowledge`.

`app.knowledge` SHALL remain the persistence-neutral Knowledge contract boundary.

`app.infrastructure.database` SHALL remain the canonical generic relational runtime, metadata and database-lifecycle foundation and SHALL NOT become the owner of Knowledge repository semantics.

The infrastructure-owned Knowledge persistence package MAY depend upon:

- canonical Knowledge domain contracts;
- `KnowledgeRecordRepository`;
- canonical database metadata and session-factory boundaries;
- SQLAlchemy.

The generic database infrastructure SHALL NOT acquire a reverse dependency upon the Knowledge persistence adapter.

Alembic migration tooling MAY explicitly load infrastructure-owned Knowledge mapped-table registration for canonical metadata discovery without transferring Knowledge ownership to the database runtime package.

Existing RFC-054 regression guardrails SHALL evolve narrowly where RFC-055 intentionally introduces Knowledge persistence.

RFC-055 SHALL NOT delete or weaken an RFC-054 architecture guardrail merely because the new adapter would otherwise fail it.

The existing RFC-054 containment test that prohibits Knowledge persistence across all infrastructure SHALL be refined so that it continues to prove:

- `app.infrastructure.database` remains Knowledge-neutral;
- default `CompositionRoot` remains free of Knowledge persistence registration;
- default `PlatformComposition` remains free of Knowledge repository exposure;

while permitting the accepted RFC-055 adapter under `app.infrastructure.knowledge`.

Existing tests requiring `app.domain` and `app.knowledge` to remain SQLAlchemy-free SHALL remain enforced.

Database startup-containment regression coverage SHALL include the authoritative:

`app.core.bootstrap_manager`

in addition to compatibility and application startup boundaries.

### TDD Boundary

Before production implementation, focused tests SHALL establish:

- the canonical Knowledge domain remains free of SQLAlchemy dependencies;
- `KnowledgeRecordRepository` remains persistence-neutral;
- the relational mapped representation remains infrastructure-owned;
- domain-to-relational mapping preserves canonical values;
- relational-to-domain mapping reconstructs canonical domain objects;
- canonical record UUID identity round-trips without change;
- Knowledge kind round-trips without change;
- title and content round-trip without change;
- provenance source type and source reference round-trip without change;
- timezone-aware provenance timestamps preserve canonical UTC semantics;
- absent Knowledge subject round-trips as `None`;
- present Knowledge subject type and identity round-trip correctly;
- partially populated subject references are rejected by the relational schema;
- `add()` persists one canonical Knowledge record;
- `get()` returns the canonical domain value;
- `get()` returns `None` for missing identity;
- duplicate canonical identity raises `KnowledgeRecordAlreadyExistsError`;
- duplicate insertion does not overwrite the original record;
- unrelated integrity failures are not misclassified as duplicate identity;
- repository operations use deterministic independent session lifetimes;
- successful `add()` completes one repository-operation transaction;
- failed `add()` rolls back;
- `get()` performs no application-data commit;
- no Unit of Work abstraction is introduced;
- no independent database engine or competing session factory is introduced;
- Alembic revision `0001` remains unchanged;
- a new append-only migration follows `0001`;
- the migration graph retains exactly one canonical head;
- application startup does not automatically execute schema migration;
- default `CompositionRoot.build()` remains database-independent;
- default `CompositionRoot` does not register or expose Knowledge persistence;
- Bootstrap behavior remains unchanged;
- Runtime lifecycle behavior remains unchanged.

### Persistence Hardening Test Boundary

Focused tests SHALL additionally establish:

- the database does not generate or replace canonical `KnowledgeRecord` identity;
- the database does not generate or replace canonical provenance capture timestamp;
- RFC-055 introduces no update, delete, upsert or overwrite persistence path;
- duplicate classification does not parse human-readable database error text;
- duplicate translation requires structured identification of the canonical record-identity constraint;
- the canonical primary-key constraint is `pk_knowledge_records`;
- the subject-pair constraint is `ck_knowledge_records_subject_pair`;
- the mapped `knowledge_records` table is registered with `DatabaseBase.metadata`;
- mapped-table registration creates no Engine, Session or database connection;
- mapped-table registration does not execute migration or require database configuration;
- Alembic migration `0002` follows `0001`;
- migration `0002` and canonical mapped metadata remain schema-aligned;
- required canonical Knowledge fields are relationally non-null;
- subject type and subject identity remain nullable only as an invariant-preserving pair;
- `0001` remains unchanged;
- exactly one canonical Alembic head remains after `0002`.

### Implementation Acceptance and Deployment Readiness Boundary

RFC-055 technical implementation acceptance SHALL establish conformity with the accepted production-grade persistence architecture.

Technical implementation acceptance SHALL NOT by itself mean that relational Knowledge persistence is approved for production deployment.

A live production PostgreSQL environment SHALL NOT be required merely to accept the RFC-055 architecture contract or complete code-level implementation verification.

Before relational Knowledge persistence is declared production-deployment ready, a separate approved PostgreSQL integration verification SHALL demonstrate at minimum:

- migration `0002` applies correctly from canonical revision `0001`;
- the deployed relational schema is aligned with canonical mapped metadata;
- canonical Knowledge `add()` and `get()` behavior operates correctly through PostgreSQL;
- canonical UUID identity semantics are preserved;
- timezone-aware provenance timestamp semantics are preserved;
- canonical duplicate identity is classified through structured database or driver diagnostics;
- unrelated integrity failures are not misclassified as duplicate canonical identity;
- failed writes preserve atomic rollback semantics;
- repository session lifetime remains deterministic;
- application startup remains independent from automatic database migration and mandatory PostgreSQL availability.

Production integration verification SHALL occur in an approved controlled environment.

Successful RFC-055 unit, architecture, migration-definition and regression testing SHALL NOT be represented as evidence that production PostgreSQL connectivity, deployment configuration or Cybersecurity approval is complete.

Production deployment readiness remains subject to separately verified integration, deployment and Cybersecurity gates.

### Verification Boundary

RFC-055 technical implementation SHALL pass:

- focused Knowledge relational persistence tests;
- domain-relational mapping tests;
- repository transaction tests;
- duplicate-conflict tests;
- migration architecture tests;
- RFC-053 Knowledge regression tests;
- RFC-054 database-foundation regression tests;
- relevant CompositionRoot and Bootstrap regression tests;
- full PlantMind regression;
- Python compilation checks;
- `git diff --check`;
- Git review;
- remote push verification;
- local and remote commit identity verification;
- clean working-tree verification.

A real production PostgreSQL deployment SHALL NOT be required to validate the RFC-055 implementation boundary.

RFC-055 SHALL NOT claim production PostgreSQL deployment, production schema application or Cybersecurity approval unless separately verified in an approved deployment environment.

### Contract Review State

RFC-055 Architecture Contract Review: passed.

Architecture decision: AD-041.

AD-041 is accepted.

RFC-055 technical implementation is complete within the accepted AD-041 architecture boundary.

Technical verification:

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

Production PostgreSQL deployment, production schema application and Cybersecurity approval remain intentionally unclaimed and require separately approved integration and deployment verification.

The accepted RFC-055 / AD-041 contract was reviewed against:

- committed code and tests current at contract acceptance;
- AD-039 / RFC-053;
- AD-040 / RFC-054;
- the Active Work Register;
- Project Context;
- Session Handoff;
- Engineering Journal;
- the completed post-RFC-054 Source-of-Truth architecture review.

Contract acceptance confirmed that RFC-055 introduced no conflicting ownership, duplicated database responsibility, domain persistence leakage, unintended Runtime coupling or premature production composition.

### Post-RFC-055 Architecture Review Outcome

The required post-RFC-055 Source-of-Truth architecture review is complete.

The review confirmed that RFC-053 / AD-039, RFC-054 / AD-040 and RFC-055 / AD-041 remain authoritative.

The initial post-RFC-055 review identified an application-level Knowledge boundary as the next architecture area.

A deeper contract review against AD-039 / RFC-053 established that a generic application service exposing only repository-equivalent `add()` and `get()` behavior would not yet own a distinct application responsibility and would introduce an unnecessary delegation layer.

The refined selected engineering direction is:

`Canonical Knowledge Capture Application Boundary`

This refined direction was subsequently formalized as:

`RFC-056 — Canonical Knowledge Capture Application Boundary`

The RFC-056 contract defines an explicit Knowledge capture use case that:

- receives approved capture inputs rather than a preconstructed `KnowledgeRecord`;
- constructs one canonical immutable `KnowledgeRecord`;
- establishes canonical record identity at the application capture boundary;
- establishes the provenance capture timestamp at the application capture boundary;
- delegates canonical domain validation to the accepted Knowledge domain types;
- persists the resulting record through `KnowledgeRecordRepository`;
- remains persistence-implementation neutral;
- does not own repository transaction semantics;
- does not own SQLAlchemy Session or engine lifecycle;
- does not make PostgreSQL mandatory during default application startup;
- does not automatically modify `ApplicationFacade`;
- does not introduce subject existence/type verification;
- does not introduce update, delete, upsert, search, document ingestion, graph, vector, RAG or LLM responsibilities.

The RFC-056 architecture contract has completed acceptance review and AD-042 is accepted.

No general Clock framework or identity-generation framework is introduced by RFC-056. Deterministic identity/time sourcing is governed narrowly by the accepted Capture application boundary.

Technical implementation is complete within the accepted RFC-056 / AD-042 architecture boundary.

Verification:

- Contract commit: `6998f32`
- Technical commit: `66c24f0`
- Focused RFC-056 and architecture verification: 19 passed
- Broader Knowledge verification: 96 passed
- Full PlantMind regression: 558 passed
- Python compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Exact local/remote technical commit identity: verified
- Working tree after technical push: clean

### Historical Next Action at That Stage

At that stage, the working direction was to draft RFC-057 as a Canonical Document Knowledge Ingestion Application Boundary.

That direction was later refined before RFC-057 contract acceptance, after repository review established that PlantMind first required a Canonical Enterprise Document Foundation.

---

## RFC-054 — Canonical Database Runtime & Schema Lifecycle Foundation

### Status

Contract Accepted.

AD-040 is accepted.

RFC-054 technical implementation is complete within the accepted AD-040 architecture boundary.

Production Knowledge persistence remains outside RFC-054 scope.

### Objective

Establish the canonical relational database runtime and schema-lifecycle foundation required before PlantMind introduces production persistence adapters.

RFC-054 SHALL establish the minimum production-grade infrastructure required for:

- explicit relational database dependency ownership;
- canonical SQLAlchemy engine ownership;
- canonical SQLAlchemy session-factory ownership;
- canonical relational schema metadata ownership;
- versioned Alembic migration ownership;
- deterministic database-resource disposal;
- explicit database infrastructure failure behavior.

RFC-054 SHALL establish infrastructure only.

It SHALL NOT implement production enterprise Knowledge persistence.

### Architectural Position

RFC-053 established the canonical persistence-neutral enterprise knowledge domain and `KnowledgeRecordRepository` port.

The required post-RFC-053 Source-of-Truth architecture review established that production Knowledge persistence cannot safely be introduced before the relational database runtime and schema lifecycle have canonical ownership.

The review established that:

- `backend/app/database.py` is preliminary isolated SQLAlchemy infrastructure;
- `app.database` has no current production consumer;
- the authoritative root `.venv` does not currently provide SQLAlchemy;
- the declared backend dependencies do not currently establish SQLAlchemy, a PostgreSQL driver or Alembic;
- no canonical ORM schema exists;
- no canonical schema metadata ownership boundary exists;
- no relational migration lifecycle exists;
- no database-focused test foundation exists;
- database readiness is not currently a mandatory Runtime capability.

RFC-054 SHALL resolve the database-foundation gap without promoting Knowledge persistence or changing Runtime lifecycle responsibilities.

### Canonical Database Responsibility

PlantMind SHALL establish one canonical infrastructure-owned relational database runtime.

That runtime SHALL own:

- one SQLAlchemy `Engine` per canonical database-runtime instance;
- the session factory bound to that engine;
- deterministic disposal of engine-owned resources.

The database runtime SHALL remain infrastructure.

It SHALL NOT:

- perform engineering reasoning;
- own canonical enterprise knowledge;
- become an application service;
- become a repository implementation;
- become Runtime lifecycle authority.

### Technology Boundary

PostgreSQL remains the approved PlantMind relational database target.

SQLAlchemy SHALL be the canonical Python relational database runtime and mapping toolkit.

RFC-054 SHALL use the synchronous SQLAlchemy:

- `Engine`;
- `Session`.

RFC-054 SHALL NOT introduce:

- `AsyncEngine`;
- `AsyncSession`.

Any future asynchronous relational persistence runtime requires a separate accepted architecture contract.

Psycopg 3 through the `psycopg` package SHALL be the canonical PostgreSQL DBAPI driver.

Canonical PostgreSQL SQLAlchemy URLs SHALL identify the approved Psycopg driver explicitly rather than relying on environment-dependent driver selection.

Alembic SHALL be the sole canonical relational schema-migration authority.

Database technologies SHALL NOT leak into PlantMind domain contracts.

### Dependency Ownership

RFC-054 SHALL explicitly declare the dependencies required for:

- SQLAlchemy;
- Alembic;
- PostgreSQL connectivity through Psycopg 3.

Required dependencies SHALL be maintained through the existing backend dependency manifest.

Implementation SHALL NOT rely upon packages that happen to exist only in a developer environment.

The authoritative Python environment remains:

`.venv`

RFC-054 SHALL NOT establish or depend upon:

`backend/.venv`

Exact dependency versions SHALL follow the existing backend dependency-management mechanism.

### Explicit Construction Boundary

The canonical database runtime SHALL be constructed explicitly.

Importing PlantMind modules SHALL NOT:

- create the canonical database engine;
- open a PostgreSQL connection;
- create a hidden process-wide database session.

A mutable global SQLAlchemy `Session` SHALL NOT be introduced.

Engine construction SHALL occur only through the canonical database runtime or its approved construction boundary.

No second module SHALL independently own another canonical engine for the same PlantMind relational persistence responsibility.

### Configuration Boundary

The canonical database runtime SHALL receive resolved database configuration explicitly.

The canonical infrastructure implementation SHALL NOT read the global `settings` object as a hidden dependency during module import.

Database configuration SHALL remain environment-driven.

Database credentials SHALL NOT be embedded as production secrets in source code.

RFC-054 implementation SHALL retire the committed credential-bearing default value currently associated with `DATABASE_URL`.

While no accepted production capability requires relational persistence, absence of configured database capability MAY be represented through an unset or optional database URL.

Development and test database credentials SHALL be supplied through explicit local environment configuration or test fixtures.

PlantMind-controlled logging and diagnostics SHALL NOT expose:

- database passwords;
- complete credential-bearing connection URLs.

RFC-054 SHALL NOT make `DATABASE_URL` a mandatory condition of the existing general `ConfigurationProvider.validate()` contract.

Database-specific configuration SHALL be validated when the database capability is explicitly constructed or invoked.

Absence of database configuration SHALL NOT by itself prevent PlantMind core Bootstrap from operating while no accepted production capability requires the database.

### Engine Boundary

Engine construction SHALL NOT itself prove database availability.

RFC-054 introduces no production database connectivity probe.

RFC-054 introduces no automatic database connection retry.

Database connection failures SHALL NOT become synthetic success.

Engine-owned resources SHALL support explicit deterministic disposal.

### Session Boundary

The canonical database runtime SHALL expose one approved session-factory boundary.

Each session request SHALL create an independent SQLAlchemy session instance.

Sessions SHALL NOT be shared as mutable global state.

Session lifecycle SHALL support deterministic close behavior.

Session creation SHALL NOT imply application or repository transaction ownership.

The canonical database runtime SHALL NOT automatically commit application or repository work.

RFC-054 SHALL NOT define repository-specific transaction semantics.

RFC-054 SHALL NOT introduce a Unit of Work abstraction.

Future repository and application contracts SHALL define transaction ownership appropriate to their use cases.

### Canonical Schema Metadata

PlantMind SHALL establish one canonical relational schema metadata authority.

Future production SQLAlchemy mapped models SHALL participate in the approved metadata authority unless a future accepted architecture decision explicitly establishes another database boundary.

PlantMind domain entities SHALL NOT inherit from SQLAlchemy declarative infrastructure.

SQLAlchemy mapped classes SHALL remain infrastructure representations.

A database row SHALL NOT replace a canonical PlantMind domain entity.

RFC-054 SHALL NOT introduce a `KnowledgeRecord` ORM model.

### Migration Authority

Alembic SHALL be the sole canonical production relational schema-evolution mechanism.

PlantMind application startup SHALL NOT automatically run Alembic migrations.

Runtime Bootstrap SHALL NOT automatically:

- upgrade the database schema;
- downgrade the database schema.

`MetaData.create_all()` SHALL NOT become the production schema-deployment mechanism.

Production relational schema evolution SHALL occur through explicit ordered Alembic revisions.

Applied migration history SHALL be treated as append-only engineering history.

An accepted migration revision SHALL NOT be silently rewritten to represent another schema state.

Breaking or destructive schema evolution requires explicit future architecture and migration review.

The migration graph SHALL maintain one canonical head unless a future accepted architecture decision explicitly authorizes branching.

### Migration Configuration

Alembic configuration SHALL use the canonical PlantMind relational schema metadata authority.

Migration configuration SHALL NOT contain production database credentials.

Migration database configuration SHALL be supplied through an approved environment-driven boundary.

RFC-054 MAY establish an intentionally schema-neutral initial migration revision to create the canonical migration lineage before application persistence tables exist.

RFC-054 SHALL NOT create enterprise Knowledge tables.

### Failure Boundary

Invalid database-specific configuration SHALL fail explicitly when the database capability is constructed or invoked.

Missing database dependencies SHALL remain an environment or build defect.

Missing dependencies SHALL NOT be converted into synthetic database availability.

Unexpected engine, session or migration failures SHALL propagate as explicit infrastructure failures.

RFC-054 SHALL NOT introduce:

- automatic database retry;
- a platform-wide database exception taxonomy.

Database infrastructure failures SHALL NOT independently modify PlantMind Runtime lifecycle state.

Any future coupling between database availability and mandatory-capability readiness requires a separate accepted architecture contract.

### Bootstrap and Runtime Boundary

RFC-054 SHALL NOT modify:

- Runtime states;
- Runtime transition authority;
- Runtime readiness semantics;
- request admission;
- operational-transition evidence;
- mandatory-capability policy;
- Health behavior.

Database readiness SHALL NOT automatically become a mandatory Runtime capability.

Bootstrap SHALL NOT automatically connect to PostgreSQL merely because the database foundation exists.

Runtime remains the sole lifecycle-transition authority.

### Composition Boundary

RFC-054 establishes infrastructure for future persistence adapters.

RFC-054 SHALL NOT:

- implement a production `KnowledgeRecordRepository`;
- register `KnowledgeRecordRepository` in `ServiceContainer`;
- wire production Knowledge persistence into `CompositionRoot`;
- create a database-backed Knowledge application service.

A future accepted persistence contract SHALL define composition between the canonical database runtime and production repository adapters.

### Legacy Database Module

`backend/app/database.py`

is preliminary isolated infrastructure.

It SHALL NOT remain a competing owner of canonical engine or session-factory construction after RFC-054 implementation.

Preserve-before-delete remains authoritative.

Before changing or removing the module, implementation SHALL re-verify:

- current repository dependencies;
- import dependencies;
- compatibility impact.

If no dependency requires the legacy module, duplicate database-runtime responsibility SHALL be retired.

If compatibility is required, the compatibility path SHALL delegate to the canonical database foundation or be separately documented before implementation proceeds.

Duplicate canonical engine ownership SHALL NOT be retained merely for legacy compatibility.

### Security Boundary

RFC-054 SHALL preserve the accepted on-premise enterprise deployment model.

RFC-054 SHALL NOT introduce an external hosted database service.

Database secrets SHALL remain outside committed source code.

RFC-054 SHALL NOT claim completion of:

- production PostgreSQL authentication policy;
- certificate policy;
- network segmentation;
- production database hardening;
- Cybersecurity deployment approval.

Those remain deployment and Cybersecurity responsibilities until separately verified.

### Knowledge Boundary

RFC-053 remains authoritative.

RFC-054 SHALL NOT redesign:

- `KnowledgeRecord`;
- `KnowledgeKind`;
- `KnowledgeSourceType`;
- `KnowledgeSubjectType`;
- `KnowledgeProvenance`;
- `KnowledgeSubject`;
- `KnowledgeRecordRepository`;
- `KnowledgeRecordAlreadyExistsError`.

RFC-054 SHALL NOT implement `KnowledgeRecordRepository`.

RFC-054 SHALL NOT create relational persistence tables for canonical enterprise Knowledge.

The first production Knowledge persistence adapter requires a future explicit accepted architecture contract.

### Prototype and Advanced Capability Boundary

RFC-054 SHALL NOT promote existing prototype or placeholder Knowledge components into production.

RFC-054 SHALL NOT introduce:

- Document Library behavior;
- Asset Library behavior;
- Search Engine behavior;
- Knowledge Graph persistence;
- Neo4j persistence;
- semantic retrieval;
- vector storage;
- Qdrant integration;
- RAG;
- LLM invocation;
- PI production connectivity.

### Non-Goals

RFC-054 SHALL NOT:

- implement production Knowledge persistence;
- introduce a Knowledge ORM model;
- add a Knowledge HTTP API;
- implement document ingestion;
- implement search;
- implement graph persistence;
- implement vector persistence;
- implement RAG;
- modify the reasoning subsystem;
- redesign the equipment domain;
- add automatic database retry;
- run automatic schema migration during application startup;
- make PostgreSQL availability a mandatory Runtime capability;
- perform a broad application-configuration refactor;
- introduce another lifecycle authority.

### TDD Boundary

Before RFC-054 production implementation, focused tests SHALL establish:

- database infrastructure dependencies are explicitly declared;
- the authoritative root `.venv` can import the approved database dependencies after dependency installation;
- canonical database infrastructure can be imported without creating a database connection;
- importing PlantMind core modules does not construct the canonical database engine as a hidden side effect;
- canonical database runtime construction is explicit;
- the database runtime owns its engine and session factory;
- independent session requests return independent session instances;
- session lifecycle supports deterministic close behavior;
- database runtime disposal releases engine-owned resources;
- canonical relational metadata has one approved ownership boundary;
- PlantMind domain modules do not depend on SQLAlchemy;
- PlantMind domain entities do not inherit SQLAlchemy mapped classes;
- Alembic configuration uses the canonical metadata authority;
- Alembic configuration contains no committed production credentials;
- the migration graph has one canonical head;
- the initial migration lineage resolves deterministically;
- application startup does not automatically execute Alembic migrations;
- application startup does not automatically call `MetaData.create_all()`;
- canonical database runtime does not automatically commit repository or application work;
- Bootstrap behavior remains unchanged;
- Runtime lifecycle behavior remains unchanged;
- no production Knowledge repository is introduced;
- no production Knowledge persistence is composed or registered;
- `backend/app/database.py` no longer owns a competing canonical engine or session factory after the accepted migration path is applied.

### Verification Boundary

RFC-054 implementation SHALL pass:

- focused database-foundation tests;
- relevant configuration regression tests;
- relevant Bootstrap regression tests;
- architecture dependency tests;
- full PlantMind regression;
- Python compilation checks;
- `git diff --check`;
- Git review;
- remote push verification;
- clean working-tree verification.

A real production PostgreSQL connection is not required to accept the RFC-054 architecture contract.

RFC-054 SHALL NOT claim production PostgreSQL connectivity until separately verified against an approved deployment environment.

### Contract Acceptance

The RFC-054 architecture contract has been reviewed against:

- current committed code and tests;
- accepted ADR, ARCH, CORE and prior RFC decisions;
- Active Work Register;
- Project Context;
- Session Handoff;
- Engineering Journal;
- the post-RFC-053 Source-of-Truth architecture review.

Contract Acceptance Review: passed.

Architecture decision: AD-040.

Contract commit: `8659acd`.

Remote contract push: verified.

Local and remote contract commit identity: verified.

Working tree after contract push: clean.

Technical implementation: complete.

Technical commit: `0e483d5`.

Focused RFC-054 verification: 32 passed.

Full PlantMind regression: 506 passed.

Python compilation: passed.

`git diff --check`: passed.

Alembic canonical migration head: `0001`.

Remote technical push: verified.

Local and remote technical commit identity: verified.

Working tree after technical push: clean.

Production Knowledge persistence: not authorized by RFC-054.

Production PostgreSQL connectivity and Cybersecurity deployment approval: not claimed by RFC-054.

### Technical Completion

RFC-054 established the canonical infrastructure-owned synchronous SQLAlchemy runtime, canonical database URL validation, canonical relational metadata ownership and Alembic schema lifecycle.

The legacy `backend/app/database.py` competing engine/session owner was retired after dependency and compatibility review confirmed no production consumer required it.

The schema-neutral Alembic revision `0001` is the single canonical migration head.

RFC-054 introduced no production Knowledge repository adapter, Knowledge ORM mapping, Knowledge persistence composition, automatic startup migration, automatic database retry, production connectivity probe, mandatory database Runtime capability or additional lifecycle authority.

### Post-RFC-054 Source-of-Truth Architecture Review

The required post-RFC-054 Source-of-Truth architecture review is complete.

The review confirmed that RFC-053 and RFC-054 remain authoritative and SHALL NOT be redesigned by the next workstream.

The review established that:

- `KnowledgeRecordRepository` remains the canonical persistence-neutral Knowledge repository port;
- no production relational implementation of `KnowledgeRecordRepository` currently exists;
- no production Knowledge relational mapping currently exists;
- no production Knowledge relational table currently exists;
- no production Unit of Work abstraction currently exists;
- `DatabaseRuntime` owns engine and session-factory lifecycle but does not own repository transaction semantics;
- Alembic revision `0001` remains intentionally schema-neutral and SHALL NOT be rewritten;
- future Knowledge schema evolution requires a new append-only migration revision;
- default `CompositionRoot` does not register or expose Knowledge persistence;
- application startup remains independent from database configuration;
- existing Knowledge Graph, RAG, semantic-search, memory and agent seams remain prototype, placeholder or intentionally unimplemented.

The selected engineering direction is:

`Canonical Knowledge Relational Persistence Adapter Boundary`

This is an engineering direction only.

It is not yet an accepted architecture contract and implementation is not yet authorized.

A future architecture contract should define:

- infrastructure-owned SQLAlchemy representation of canonical `KnowledgeRecord`;
- explicit Domain-to-Relational and Relational-to-Domain mapping;
- a new append-only Alembic migration;
- production relational implementation of `KnowledgeRecordRepository`;
- preservation of canonical identity and duplicate-identity semantics;
- preservation of provenance, UTC timestamp semantics and optional typed subject references;
- explicit repository-operation transaction ownership;
- deterministic session lifetime;
- infrastructure failure and duplicate-conflict behavior.

The next contract SHALL NOT automatically introduce:

- a Unit of Work abstraction;
- shared mutable database sessions;
- mandatory PostgreSQL startup;
- default `CompositionRoot` Knowledge persistence wiring;
- Runtime lifecycle changes;
- Bootstrap lifecycle changes;
- Knowledge HTTP APIs;
- document ingestion;
- semantic or vector retrieval;
- Knowledge Graph persistence;
- RAG;
- LLM invocation;
- production PI connectivity.

### Next Exact Action

Draft and review the architecture contract for the Canonical Knowledge Relational Persistence Adapter Boundary before any implementation.

Do not assign production composition responsibility or begin persistence implementation before contract acceptance.

---

## RFC-053 — Canonical Enterprise Knowledge Foundation Boundary

### Status

Complete.

The RFC-053 architecture contract remains accepted.

The RFC-053 technical implementation is complete within the accepted scope.

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
- Contract commit: `37112a2`.
- Architecture decision: AD-039.
- Technical implementation: complete.
- Technical commit: `ee18bc8`.
- Focused RFC-053 verification: 44 passed.
- Full regression: 476 passed.
- Compilation: passed.
- `git diff --check`: passed.
- Remote technical push: verified.
- Production knowledge database adapter: not introduced.
- Production knowledge composition or registration: not introduced.

### Post-RFC-053 Architecture Review

The required post-RFC-053 Source-of-Truth architecture review is complete.

The review established that:

- the RFC-053 canonical knowledge foundation is complete and SHALL NOT be redesigned by the next workstream;
- existing knowledge graph, RAG, semantic-search, memory and agent components remain prototype, placeholder or intentionally unimplemented;
- `backend/app/database.py` is preliminary isolated SQLAlchemy infrastructure and is not the canonical database runtime;
- the authoritative `.venv` does not currently provide SQLAlchemy;
- the declared backend dependencies do not currently establish SQLAlchemy, a PostgreSQL driver or Alembic;
- no canonical ORM schema, schema metadata ownership, migration lifecycle or database test foundation currently exists;
- no production code currently consumes `app.database`;
- database readiness SHALL NOT automatically become a mandatory Runtime capability;
- Knowledge persistence SHALL NOT be implemented before an approved database runtime and schema-lifecycle boundary exists.

The selected engineering direction is:

`Canonical Database Runtime & Schema Lifecycle Foundation`

This is an engineering direction only.

No implementation is authorized until the corresponding architecture contract is drafted, reviewed and accepted.

### Next Exact Action

Draft and review the architecture contract for the Canonical Database Runtime & Schema Lifecycle Foundation before any implementation.

Do not introduce database dependencies, schema migrations, ORM models, production Knowledge persistence or database composition before contract acceptance.

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
