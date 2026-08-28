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

---

## RFC-070 Final Source-of-Truth Reconciliation Verification

### Status

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Selected workstream:

RFC-070 — Canonical Binary Document Content Store / Access Foundation

Architecture Decision:

**AD-056 — ACCEPTED**

Verified commit chain:

- selection: `13cfccc08d8c0a3b891990d38edaf9fc48874a5e`;
- accepted contract: `cfd45d35144574d27a40e0f350b571a6298afd59`;
- technical implementation: `389ce20b9e01b99cf9b7c1a066a0e9a55bc71223`;
- engineering closure: `ab4438b02a8f34f83b462e3d8a86b4b5ab5d1092`;
- post-closure reconciliation: `4fc3e86bf495bbf93158d8e575645e4d556eda39`.

### Final Reconciliation Git Verification

- reconciliation parent: `ab4438b02a8f34f83b462e3d8a86b4b5ab5d1092`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- exact five Source-of-Truth document surface: **PASS**;
- production-code changes: none;
- test-file changes: none.

### Verified Technical Baseline

- full PlantMind regression: **928 passed**;
- canonical Alembic head: **0005**;
- canonical boundary: `app.document_content.store`;
- production surface: `backend/app/document_content/store.py`.

Concrete-adapter behavioral conformance remains:

**NOT YET APPLICABLE / BLOCKED BY ABSENCE OF CONCRETE ADAPTER**

### Governed State After RFC-070

There is no active RFC or selected successor workstream.

Successor-workstream selection has not started.

Any successor must be selected separately through evidence-based governance.

This state is intentionally non-self-referential and records only already
verified commits through reconciliation commit `4fc3e86bf495bbf93158d8e575645e4d556eda39`.

## Post-RFC-069 Successor Architecture Workstream Selection Draft

### Status

**DRAFT SELECTION — REVIEW / GIT GATE PENDING**

Selection baseline:

`ffd0ec9c6df3d117792a72b394ee9532eb64de8d`

RFC-069:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Draft selected successor workstream:

**Canonical Binary Document Content Store / Access Foundation**

Proposed numbering:

**RFC-070 — NUMBERING CANDIDATE ONLY; NOT ACTIVE**

Latest Accepted Architecture Decision:

**AD-055**

### Evidence

Completed canonical foundations:

- Document Content Domain descriptor semantics;
- persistence-neutral `DocumentContentRepository`;
- relational descriptor persistence under
  `app.infrastructure.document_content`;
- canonical Alembic head `0005`.

Missing dependency-unlocking foundation:

- canonical binary Document Content store/access contract.

Current canonical backend has no `DocumentContentStore` or accepted raw-byte
access/read/open/stream contract.

The prior evidence-based ordering placed binary store/access immediately
after descriptor relational persistence.

Content-establishment/application coordination remains separately governed
because it must later decide any atomicity involving Enterprise Document,
descriptor persistence and binary payload persistence.

Document Library, parser/OCR/chunking remain premature until binary
content-access architecture is accepted.

Search/Vector/Graph/RAG/LLM remain higher-level dependent work.

### Selection Restrictions

This draft does not:

- create AD-056;
- activate RFC-070;
- accept an RFC-070 architecture contract;
- authorize implementation;
- select binary storage technology;
- define byte/stream API semantics;
- define transaction coordination;
- authorize Document Library/parser/OCR/chunking;
- authorize Search/Vector/Graph/RAG/LLM;
- create production-security or Cybersecurity claims.

### Next Exact Action

Review the complete five-document successor-selection diff.

No staging or commit until the review passes.

## RFC-069 Final Source-of-Truth Reconciliation Verification

### Status

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Selected workstream:

RFC-069 — Canonical Document Content Relational Persistence Adapter Boundary

Architecture Decision:

**AD-055 — ACCEPTED**

Selection commit:

`5d7794352029576e0b62c2ac8cbfa248fe11961d`

Accepted-contract commit:

`467440b6c5d16e599fbc0d0f5c820d31725fd29b`

Technical implementation commit:

`4572b40cedecc263577453b95ca63ecab6e61428`

Engineering-memory closure commit:

`63790de5312c69c709e2249b56e91995a00426b6`

Post-closure Source-of-Truth reconciliation commit:

`231e0cc66862c797e299fdb71ff20da8a39e8ae2`

### Final Reconciliation Git Verification

- reconciliation commit parent: `63790de5312c69c709e2249b56e91995a00426b6`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- reconciliation surface: exactly five maintained Source-of-Truth documents;
- production-code changes in reconciliation: none;
- test-file changes in reconciliation: none.

### Verified Technical Baseline

- focused RFC-069 verification: **46 passed**;
- impacted regression: **151 passed**;
- full PlantMind regression: **912 passed**;
- canonical Alembic chain: `0003 -> 0004 -> 0005`;
- canonical Alembic head: **0005**.

### Preserved Boundary

RFC-069 remains limited to the accepted relational descriptor persistence
adapter boundary.

It does not authorize:

- raw binary payload storage/access;
- Enterprise Document foreign-key ownership;
- surrogate content identity;
- digest uniqueness;
- a new CheckConstraint;
- cross-repository transaction coordination;
- application-service/default-composition expansion;
- Document Library, parser, OCR, chunking, Search, Vector, Graph, RAG or LLM
  promotion;
- production-readiness, production-security or Cybersecurity-approval claims.

### Governed State After RFC-069

There is no active RFC or selected successor architecture workstream.

Successor-workstream selection has not started.

Any successor must be selected separately from current repository,
architecture, project-charter and technical evidence.

This final RFC-069 state is non-self-referential and records only already
verified commits through reconciliation commit `231e0cc66862c797e299fdb71ff20da8a39e8ae2`.

## Historical RFC-068 Closed Workstream State Before Final Verification Push

### Status

**RFC-068 FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

### Current Technical State

Accepted-contract commit:

`6ac09336e223cfb18e049528d62d10b4753e8ee3`

Technical implementation commit:

`a88f046567b2b56795f590a4852dbd144b7c2fde`

Technical verification:

- focused RFC-068 contract suite: **16 passed**;
- impacted Document / Document Content regression: **91 passed**;
- full PlantMind regression: **866 passed**;
- Python compilation: **PASS**;
- canonical Alembic head: **0004**;
- technical commit push: **PASS**;
- exact local / tracking / remote technical identity: **PASS**;
- working tree after technical verification: **clean**.

RFC-068 technical implementation is complete.

Engineering-memory closure is complete, pushed and verified.

Engineering closure commit:

`bcf2fc8b20c866584db8596341c8abdb965358ea`

Post-closure Source-of-Truth reconciliation is complete, pushed and verified.

Reconciliation commit:

`074e534e0d97a927b6434341ad5d1c8671bfa381`

Verified reconciliation Git state:

- reconciliation commit parent: `bcf2fc8b20c866584db8596341c8abdb965358ea`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**.

RFC-068 is therefore:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

At that historical stage, the final verification Source-of-Truth record itself remained uncommitted.

### Historical Next Governed Activity at That Stage

RFC-068 has no remaining architecture, implementation, closure or
Source-of-Truth reconciliation work item.

The next separate governed activity is evidence-based successor-workstream
selection.

Before that separate activity begins, the Final Verification record Git gate
SHALL be externally verified: review, commit, push, exact local / tracking /
remote identity and a clean working tree.

No successor RFC or architecture workstream is selected or preselected
here.

### Historical Stage Records

The selection and architecture-acceptance chronology below is retained as
historical stage evidence. Earlier implementation prohibitions describe the
state at those earlier gates and do not supersede this current technical
completion state.

This section records the evidence-based successor-workstream selection
following full closure and Source-of-Truth reconciliation of RFC-067.

Selection baseline:

`ed7106c1c232d18c04319559cc2c899e2ebfb61a`

Selection commit:

`287f3328f49627ce1e19a20d55d56f8bfbb76c58`

Selected successor RFC:

**RFC-068 — SELECTED; CONTRACT ACCEPTED — IMPLEMENTATION GATE PENDING**

This selection does not constitute:

- architecture-contract acceptance;
- implementation authorization;
- production-readiness approval;
- storage-technology selection;
- security or Cybersecurity approval.

### Evidence Review Result

The post-RFC-067 review confirms:

- RFC-067 is fully closed and Source-of-Truth reconciled;
- the current branch and remote are identical at `ed7106c1c232d18c04319559cc2c899e2ebfb61a`;
- the working tree was clean at selection baseline;
- the verified full PlantMind regression baseline remains **850 passed**;
- canonical Alembic head remains `0004`;
- RFC-067 removed the identified Core-to-Services workload-evidence
  dependency-direction debt;
- maintained non-test consumers use the canonical
  `app.domain.operational_workload_evidence` contract path;
- the legacy workload-evidence Services module remains only a temporary
  exact-class-identity compatibility boundary;
- no Domain-to-Services, Domain-to-Infrastructure or Domain-to-API
  dependency violation was identified by the post-RFC-067 static review;
- no test skip / xfail / TODO signal was identified by that review;
- the adjacent `OperationalTransitionEvidence` Core placement remains
  outside RFC-067, but current evidence does not establish that placement
  as a defect requiring immediate remediation;
- unused Neo4j URI / username / password defaults remain a separate
  non-blocking configuration-hygiene debt;
- PI connector migration, logging consolidation and Session Memory naming
  remain separately deferred maintenance items;
- RFC-066 established canonical Document Content semantics while explicitly
  deferring content repository/store, binary persistence and retrieval;
- Document Library, upload/download, source synchronization, parsing, PDF
  extraction, OCR, chunking, revision lifecycle, semantic retrieval,
  embeddings, vector persistence, graph persistence, RAG and LLM remain
  separately deferred;
- those higher-level Document Intelligence capabilities require a canonical
  lower-level content access/persistence-neutral repository boundary before
  they can be promoted safely.

### Candidate Ranking

1. **Canonical Document Content Repository Foundation Boundary — SELECTED IN DRAFT**
2. `OperationalTransitionEvidence` Placement Review — not selected;
   insufficient evidence currently establishes a placement defect.
3. Operational Workload Evidence Legacy Compatibility Removal — not
   selected; breaking-change review is required and product unlock is lower.
4. Neo4j Legacy Configuration Hygiene — not selected; valid cleanup debt but
   not the highest dependency-completing platform foundation.
5. PI Connector / Logging / Session Memory maintenance — not selected;
   separately deferred maintenance work.
6. OCR / Search / Vector / Graph / RAG / Agents — not selected; these remain
   dependent on lower-level Document Content access and persistence
   foundations.

### Selection Rationale

PlantMind already has canonical:

- Enterprise Document identity;
- Enterprise Document repository semantics;
- relational Enterprise Document persistence;
- Document registration application semantics;
- Knowledge identity and capture semantics;
- Knowledge relational persistence;
- Document-to-Knowledge lineage identity;
- lineage repository semantics;
- relational lineage persistence;
- coordinated Knowledge / lineage transaction semantics;
- Document-to-Knowledge ingestion application semantics;
- canonical Document Content Domain semantics.

The next minimum dependency-completing architecture foundation is therefore
a persistence-neutral repository boundary for canonical Document Content.

This continues the established PlantMind progression:

**Domain contract → persistence-neutral repository contract → Infrastructure
adapter → application capability**

rather than allowing Document Library, parser/OCR, search or AI layers to
depend directly on storage technology.

### Objective

Review and define the minimum canonical persistence-neutral repository
foundation for RFC-066 Document Content associated with an existing canonical
`EnterpriseDocument`.

The architecture contract must determine, without prematurely implementing:

1. architectural ownership of the repository port;
2. repository responsibility and dependency direction;
3. canonical Document identity used for content association/access;
4. content-presence and not-found semantics;
5. retrieval semantics required by future Infrastructure and application
   consumers;
6. whether write/register semantics belong in this repository foundation or
   a later application boundary;
7. atomicity and failure boundaries without changing RFC-064 / RFC-065
   responsibilities;
8. compatibility with future Document revision / supersession semantics;
9. how RFC-066 content immutability and digest semantics remain authoritative;
10. whether a future persistence adapter requires schema/Alembic work or a
    non-relational binary/content store;
11. how storage-neutral Domain/Application layers remain free of filesystem,
    object-store and database-specific behavior;
12. exact tests needed to enforce architectural ownership and dependency
    direction.

### Explicitly Not Decided by Selection

This draft selection does not choose:

- repository method names or exact Python signatures;
- relational vs filesystem vs object-storage persistence;
- database schema;
- Alembic migration;
- binary persistence representation;
- filesystem layout;
- object-store bucket/key layout;
- Document Library behavior;
- upload/download API;
- source synchronization;
- revision / supersession model;
- parser implementation;
- PDF extraction;
- OCR engine;
- chunking strategy;
- semantic-search implementation;
- embedding model;
- vector database;
- graph persistence;
- Neo4j production wiring;
- RAG orchestration;
- LLM provider/model;
- production authentication or authorization;
- RBAC or Active Directory;
- production-security or Cybersecurity readiness.

### Preserved Boundaries

The future architecture contract SHALL preserve unless explicitly reviewed:

- RFC-057 canonical Enterprise Document identity;
- RFC-058 repository semantics;
- RFC-059 relational Document persistence;
- RFC-060 Document Registration application semantics;
- RFC-064 transaction-coordination semantics;
- RFC-065 Document-to-Knowledge ingestion semantics;
- RFC-066 canonical Document Content semantics;
- RFC-067 workload-evidence ownership and compatibility boundaries;
- Runtime lifecycle authority;
- Bootstrap authority;
- default Composition behavior;
- current security and production-readiness non-claims.

### Historical Governance State Before the Accepted-Contract Git Gate

At that stage, successor-workstream selection was complete.

Selection commit:

`287f3328f49627ce1e19a20d55d56f8bfbb76c58`

The selection commit had been pushed and exact local / remote identity had
been verified.

`RFC-068` had become the active architecture workstream.

Architecture Decision:

**AD-054 — ACCEPTED**

At that stage, production implementation was not yet authorized.

### Historical Next Exact Action Before TDD RED

The next action at that stage was to review the complete RFC-068 / AD-054
five-document acceptance-propagation diff.

The required sequence at that stage was:

1. stage exactly the five maintained Source-of-Truth documents;
2. verify staged blobs matched the reviewed working tree;
3. preserve Engineering Journal and historical Architecture Decision history;
4. verify no backend or test file was staged;
5. create the accepted architecture-contract documentation commit separately;
6. push it;
7. verify exact local / remote accepted-contract commit identity;
8. verify a clean working tree.

Technical implementation and TDD RED were prohibited at that historical
stage until those gates passed.

---

## RFC-068 — Canonical Document Content Repository Foundation Boundary

### Status

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Selection commit:

`287f3328f49627ce1e19a20d55d56f8bfbb76c58`

Architecture Decision:

**AD-054 — Accepted**

Latest Accepted Architecture Decision:

**AD-054**

Prior Accepted Architecture Decision:

**AD-053**

Full PlantMind regression baseline entering RFC-068:

**850 passed**

Canonical Alembic head entering RFC-068:

`0004`

### Context

RFC-066 / AD-052 established the canonical immutable Document Content Domain
foundation:

- `DocumentContentMediaType`;
- `DocumentContentDigest`;
- `DocumentContentDescriptor`.

The canonical content association is:

`EnterpriseDocument.id -> zero-or-one DocumentContentDescriptor`

RFC-066 deliberately introduced no repository, content store, persistence,
binary storage, retrieval or application-registration responsibility.

Its accepted contract explicitly required a later architecture workstream to
define persistence-neutral content persistence/access semantics.

The RFC-068 successor-selection review determined that the next minimum
dependency-completing foundation is a canonical persistence-neutral Document
Content repository boundary.

### Architecture Resolution

RFC-068 SHALL establish the repository for canonical
`DocumentContentDescriptor` persistence and exact retrieval.

RFC-068 SHALL NOT combine that descriptor repository with binary payload
storage or byte streaming.

This is an explicit responsibility split.

The canonical descriptor repository and future binary content store/access
boundary are related prerequisites but are not the same architectural
responsibility.

Combining them now would prematurely decide payload transport, resource
lifecycle, storage technology and large-content loading behavior without
sufficient evidence.

### Canonical Namespace

RFC-068 SHALL establish:

`app.document_content.repository`

implemented at:

`backend/app/document_content/repository.py`

The package:

`app.document_content`

shall be established with:

`backend/app/document_content/__init__.py`

The package initializer SHALL remain empty under RFC-068.

It SHALL NOT create a package-level re-export API.

### Canonical Repository Surface

The repository module SHALL expose exactly:

- `DocumentContentAlreadyExistsError`;
- `DocumentContentRepository`.

`DocumentContentRepository`

SHALL be an abstract persistence-neutral repository port.

Its canonical operations SHALL be exactly:

`add(descriptor: DocumentContentDescriptor) -> None`

and:

`get(document_id: EntityId) -> DocumentContentDescriptor | None`

No generic CRUD interface is authorized.

### Repository Conflict Semantics

`DocumentContentAlreadyExistsError`

SHALL represent a repository-level conflict.

It SHALL derive from:

`Exception`

and SHALL NOT derive from:

`DomainException`.

The repository duplicate identity SHALL be exactly:

`DocumentContentDescriptor.document_id`

which references canonical:

`EnterpriseDocument.id`.

Because RFC-066 establishes zero-or-one canonical content descriptor per
canonical Document identity, a repository cannot accept a second descriptor
for the same `document_id`.

Re-adding the exact same descriptor SHALL raise
`DocumentContentAlreadyExistsError`.

Adding a different descriptor carrying the same `document_id` SHALL also
raise `DocumentContentAlreadyExistsError`.

The repository SHALL NOT silently overwrite.

The repository SHALL NOT treat duplicate add as successful idempotency.

### Identity Preservation

RFC-068 SHALL NOT introduce:

- `DocumentContentId`;
- content entity identity;
- digest identity;
- source-reference identity;
- media-type identity;
- byte-length identity;
- storage-location identity.

Canonical Document Content association remains anchored to:

`EnterpriseDocument.id`

through:

`DocumentContentDescriptor.document_id`.

`DocumentContentDigest`

continues to describe SHA-256 integrity only.

It SHALL NOT become:

- repository key beyond being descriptor data;
- uniqueness identity;
- deduplication identity;
- idempotency identity;
- lookup identity.

RFC-068 SHALL NOT introduce:

`get_by_digest(...)`

or equivalent digest lookup.

### Exact Retrieval Semantics

`get(document_id: EntityId)`

SHALL perform exact canonical Document identity lookup only.

When canonical content descriptor exists, it SHALL return the canonical:

`DocumentContentDescriptor`.

When no descriptor exists, it SHALL return:

`None`.

No repository-level not-found exception is required.

Absence remains valid because RFC-066 explicitly allows an
`EnterpriseDocument` to exist without canonical content.

Exact identity lookup is not Search capability.

### Cardinality Preservation

RFC-066 remains authoritative:

`EnterpriseDocument.id -> zero-or-one DocumentContentDescriptor`

RFC-068 repository semantics SHALL preserve that rule.

The repository SHALL NOT establish:

- attachments;
- alternate renditions;
- multiple independent content artifacts;
- revision-specific content multiplicity.

Repository storage capability SHALL NOT be interpreted as authorization for
future revision or multi-artifact policy.

### Canonical Domain Ownership

Canonical content validation remains owned exclusively by:

`app.domain.document_content`.

RFC-068 SHALL consume existing:

- `EntityId`;
- `DocumentContentDescriptor`.

The repository SHALL NOT:

- generate Document identity;
- generate content identity;
- reconstruct descriptor values from unrelated primitive inputs;
- normalize media type;
- calculate SHA-256;
- validate digest format;
- validate byte length;
- mutate canonical descriptor values;
- duplicate RFC-066 Domain rules.

RFC-068 implementation SHALL NOT modify:

`backend/app/domain/document_content.py`.

RFC-068 implementation SHALL NOT modify:

`backend/app/domain/document.py`.

### Enterprise Document Existence Boundary

The repository port SHALL NOT depend on:

`EnterpriseDocumentRepository`.

It SHALL NOT perform cross-repository existence validation.

It SHALL store and retrieve already-constructed canonical
`DocumentContentDescriptor` values only.

AD-052 remains authoritative that a future application boundary which
establishes persisted canonical content SHALL verify that the referenced
canonical:

`EnterpriseDocument.id`

exists before treating content establishment as successful.

RFC-068 therefore establishes no orphan-content application policy.

### Source Reference Boundary

`DocumentSource.source_reference`

remains external/source-system traceability only.

RFC-068 SHALL NOT interpret it as:

- repository identity;
- repository alternate key;
- filesystem path;
- URI;
- content locator;
- storage locator;
- object-store key;
- binary-store key;
- deduplication identity.

The repository SHALL introduce no source-reference lookup.

### Raw Payload and Binary Store Boundary

RFC-068 repository operations SHALL persist and retrieve canonical descriptor
semantics only.

The repository contract SHALL contain no:

- raw `bytes`;
- `bytearray`;
- memory buffer;
- stream;
- file handle;
- filesystem path;
- URI;
- storage key.

RFC-068 SHALL NOT introduce:

- `DocumentContentStore`;
- `read_bytes(...)`;
- `read(...)`;
- `open(...)`;
- `stream(...)`;
- download;
- byte range;
- resource lifecycle.

Binary content access/storage remains a separately governed future
architecture workstream.

That future workstream must consume RFC-066 descriptor semantics and SHALL
not reinterpret `source_reference` as canonical content access.

### Persistence Technology Boundary

RFC-068 is persistence-neutral.

It SHALL NOT introduce:

- SQLAlchemy;
- PostgreSQL-specific behavior;
- relational row/model;
- database BLOB;
- filesystem adapter;
- network filesystem adapter;
- object-storage adapter;
- file-server adapter;
- Infrastructure repository implementation.

A future persistence adapter may implement the accepted repository contract
only after separate evidence-based architecture authorization.

RFC-068 itself SHALL NOT decide whether descriptor persistence eventually
uses relational storage or another technology.

### DatabaseRuntime, Schema and Alembic Boundary

RFC-068 SHALL NOT own or modify:

- `DatabaseRuntime`;
- engine construction;
- Session factory;
- canonical SQLAlchemy metadata;
- migration lifecycle.

RFC-068 introduces:

- no new table;
- no new column;
- no new foreign key;
- no new index;
- no new uniqueness constraint;
- no Alembic revision.

Canonical Alembic head remains:

`0004`.

### Mutation and Revision Boundary

RFC-068 SHALL NOT introduce:

- update;
- replace;
- delete;
- upsert;
- mutation;
- revision;
- supersession;
- current/latest pointer.

RFC-066 descriptor immutability remains authoritative.

If future Document revision architecture changes the zero-or-one assumption,
RFC-066 and RFC-068 SHALL both be explicitly reviewed.

### Transaction and Atomicity Boundary

RFC-068 establishes no application transaction.

It SHALL NOT define atomicity across:

- Enterprise Document registration;
- Document Content descriptor persistence;
- binary payload persistence;
- Document-to-Knowledge ingestion.

RFC-068 SHALL NOT modify:

- RFC-060 Document Registration;
- RFC-064 Knowledge / lineage transaction coordination;
- RFC-065 Document-to-Knowledge ingestion.

The repository foundation SHALL NOT introduce:

- Session ownership;
- commit;
- rollback;
- transaction coordinator;
- distributed transaction;
- compensation;
- outbox;
- retry.

Future content-registration/application architecture must explicitly decide
cross-boundary failure and atomicity behavior.

### Application Boundary

RFC-068 SHALL NOT introduce a Document Content registration application
service.

It SHALL NOT modify:

- `EnterpriseDocumentRegistrationApplicationService`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeCaptureApplicationService`;
- `KnowledgeLineageTransactionCoordinator`.

The future application boundary responsible for establishing canonical
Document Content remains separately governed.

### Parser and Extraction Boundary

RFC-068 SHALL NOT implement:

- PDF parsing;
- OCR;
- DOCX extraction;
- spreadsheet extraction;
- text extraction;
- character-encoding detection;
- metadata extraction;
- chunking.

Future parser architecture still requires an accepted binary content
access/store boundary.

A parser SHALL NOT open:

`DocumentSource.source_reference`

as canonical content access.

### Document Library Boundary

RFC-068 is not a Document Library.

It SHALL NOT implement:

- upload;
- download;
- browse;
- catalogue;
- folder hierarchy;
- source synchronization;
- retention;
- permissions;
- approval workflow;
- revision history.

### Search, Vector, Graph and AI Boundary

RFC-068 SHALL NOT establish:

- keyword search;
- semantic search;
- full-text indexing;
- embeddings;
- vector persistence;
- Qdrant;
- graph persistence;
- Neo4j production integration;
- RAG;
- LLM;
- AI Agent behavior.

Repository identity lookup SHALL NOT be represented as Search capability.

### Composition, Runtime and Bootstrap Boundary

RFC-068 SHALL NOT modify default:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`.

RFC-068 SHALL NOT modify:

- Runtime lifecycle;
- Bootstrap;
- Health;
- readiness;
- request admission;
- operational-transition authority;
- mandatory-capability policy.

The existence of a repository interface SHALL NOT make content persistence a
mandatory default Runtime capability.

### Security and Trust Boundary

RFC-068 SHALL NOT establish:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- LDAP;
- MFA;
- actor identity;
- actor audit;
- Document permission policy;
- source authenticity;
- malware scanning;
- content approval;
- Document approval;
- trust classification;
- compliance approval;
- Cybersecurity approval;
- production-security readiness.

A persisted descriptor or SHA-256 digest SHALL NOT imply trust.

### Dependency Boundary

The repository contract SHALL depend only on the minimum canonical contracts
required to express its interface.

The expected imports are limited to:

- Python standard-library abstraction support;
- `app.domain.base.EntityId`;
- `app.domain.document_content.DocumentContentDescriptor`.

It SHALL NOT depend on:

- `app.domain.document`;
- `app.document.repository`;
- `app.services`;
- `app.infrastructure`;
- SQLAlchemy;
- FastAPI;
- Pydantic;
- filesystem libraries;
- network clients;
- parser;
- OCR;
- vector infrastructure;
- graph infrastructure;
- RAG;
- LLM.

ARCH-001, ARCH-003, CORE-002 and CORE-003 remain authoritative.

### Existing Responsibilities Preserved

RFC-068 SHALL NOT silently redesign:

- `EntityId`;
- `DomainEntity`;
- `EnterpriseDocument`;
- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocumentRepository`;
- canonical Enterprise Document relational persistence;
- `EnterpriseDocumentRegistrationApplicationService`;
- `DocumentContentMediaType`;
- `DocumentContentDigest`;
- `DocumentContentDescriptor`;
- `KnowledgeRecord`;
- `KnowledgeRecordRepository`;
- `KnowledgeCaptureApplicationService`;
- `DocumentKnowledgeLineage`;
- `DocumentKnowledgeLineageRepository`;
- `KnowledgeLineageTransactionCoordinator`;
- `DocumentKnowledgeIngestionApplicationService`;
- `DatabaseRuntime`;
- canonical SQLAlchemy metadata authority;
- canonical Alembic lifecycle;
- `ApplicationFacade`;
- default `CompositionRoot`;
- Runtime;
- Bootstrap.

### Expected Technical Change Surface If Accepted

If and only if RFC-068 / AD-054 is accepted, committed, pushed and the
implementation-entry Git gate passes, the expected production-code change
surface is limited to new files:

- `backend/app/document_content/__init__.py`;
- `backend/app/document_content/repository.py`.

The package initializer SHALL remain empty.

Expected verification changes may include new focused repository-contract and
architecture-guardrail tests.

No modification is expected to:

- `backend/app/domain/document_content.py`;
- `backend/app/domain/document.py`;
- existing Document repository;
- existing relational Document persistence;
- existing application services;
- Composition;
- Runtime;
- Bootstrap;
- migrations.

Any implementation need outside the accepted technical surface SHALL stop for
architecture review before expansion.

### TDD Entry Contract

Technical implementation SHALL begin with RED tests only after all of the
following are true:

1. RFC-068 architecture review passes;
2. AD-054 architecture review passes;
3. RFC-068 and AD-054 are confirmed materially and semantically equivalent;
4. both are Accepted;
5. accepted architecture documentation is committed separately;
6. accepted contract commit is pushed;
7. exact local / remote accepted-contract identity is verified;
8. working tree is clean.

Before those gates pass:

**NO TDD RED AND NO PRODUCTION IMPLEMENTATION ARE AUTHORIZED.**

Initial RED evidence SHALL fail because the accepted canonical repository
package/module/contracts do not yet exist.

Unrelated regression failure SHALL NOT count as valid RED evidence.

### Required GREEN Architecture Guardrails

Technical acceptance SHALL include tests proving at minimum:

1. canonical repository ownership is
   `app.document_content.repository`;
2. the repository family contains exactly
   `DocumentContentAlreadyExistsError` and `DocumentContentRepository`;
3. the package initializer remains empty;
4. repository public operations remain exactly `add()` and `get()`;
5. exact signatures remain canonical;
6. duplicate identity is `document_id` only;
7. duplicate add cannot silently overwrite;
8. exact missing lookup returns `None`;
9. digest/source reference/media type/byte length are not alternate keys;
10. no raw binary payload or byte-access operation enters the repository;
11. no `DocumentContentStore` is introduced;
12. no generic CRUD/search/list API is introduced;
13. no Enterprise Document existence lookup enters the repository;
14. RFC-066 Domain module remains unchanged;
15. RFC-057 Document Domain module remains unchanged;
16. repository dependencies remain persistence-neutral;
17. no Infrastructure/service/SQLAlchemy/FastAPI/Pydantic dependency enters;
18. no file/network I/O enters;
19. no migration/schema change occurs;
20. default Composition, Runtime and Bootstrap remain unchanged.

### Verification Contract

Technical verification, if later authorized, SHALL include:

- focused RFC-068 repository contract tests;
- Document Content Domain regression;
- canonical Document repository regression;
- Document / Knowledge / lineage boundary regression;
- architecture guardrails;
- full PlantMind regression;
- Python compilation verification;
- dependency/import static verification;
- canonical Alembic-head verification;
- `git diff --check`;
- exact technical-commit local / remote identity;
- clean working tree after technical push.

No technical acceptance shall rely only on focused tests.

### Documentation and Commit Separation

RFC-068 / AD-054 architecture-contract acceptance SHALL be committed
separately from future technical implementation.

Technical implementation SHALL NOT be committed together with contract
acceptance.

Post-implementation engineering-memory closure SHALL remain a separate
governed step after technical verification.

### Acceptance Requirements

Before RFC-068 / AD-054 may become Accepted, architecture review SHALL
confirm:

1. RFC-068 introduces no new ARCH-001 architectural layer;
2. the canonical repository namespace is exactly
   `app.document_content.repository`;
3. the technical package is exactly `app.document_content` and its
   `__init__.py` remains empty under RFC-068;
4. the canonical repository module introduces exactly
   `DocumentContentAlreadyExistsError` and `DocumentContentRepository`;
5. `DocumentContentAlreadyExistsError` derives from `Exception`, not
   `DomainException`;
6. `DocumentContentRepository` is a persistence-neutral abstract repository
   port;
7. the repository exposes exactly two canonical operations: `add()` and
   `get()`;
8. `add()` has the canonical contract
   `add(descriptor: DocumentContentDescriptor) -> None`;
9. `get()` has the canonical contract
   `get(document_id: EntityId) -> DocumentContentDescriptor | None`;
10. RFC-068 introduces no `DocumentContentId` or other independent content
    identity;
11. canonical content association remains anchored only to existing
    `EnterpriseDocument.id`;
12. repository duplicate identity is exactly
    `DocumentContentDescriptor.document_id`;
13. re-adding an identical descriptor for the same Document identity raises
    `DocumentContentAlreadyExistsError`;
14. adding a different descriptor for an already-associated Document identity
    also raises `DocumentContentAlreadyExistsError`;
15. repository `add()` never silently overwrites existing canonical content
    association;
16. RFC-068 introduces no upsert or repository-level idempotent-success
    semantics;
17. SHA-256 digest remains integrity description only and never becomes
    repository identity, uniqueness identity, lookup identity, deduplication
    identity or idempotency identity;
18. media type, byte length and `DocumentSource.source_reference` do not
    become repository identities or alternate keys;
19. RFC-066 zero-or-one content-descriptor cardinality per canonical Document
    identity is preserved;
20. an Enterprise Document may continue to exist with no canonical content
    descriptor;
21. exact identity lookup returns `None` when no canonical descriptor exists;
22. RFC-068 introduces no repository-level not-found exception for `get()`;
23. no list, find, search, filter, query, pagination, ranking or
    `get_by_digest()` operation is introduced;
24. repository behavior consumes the existing canonical
    `DocumentContentDescriptor` without duplicating its Domain validation;
25. `app.domain.document_content` remains unchanged by RFC-068 implementation;
26. RFC-057 `app.domain.document` and canonical `EnterpriseDocument` remain
    unchanged;
27. `DocumentContentRepository` does not depend on
    `EnterpriseDocumentRepository`;
28. the repository performs no cross-repository Enterprise Document existence
    lookup;
29. a future application boundary establishing persisted canonical content
    remains responsible for verifying that `EnterpriseDocument.id` exists;
30. RFC-068 does not authorize orphan-content application semantics;
31. no raw `bytes`, `bytearray`, memory buffer, file handle, path, URI,
    stream or storage key enters the repository contract;
32. RFC-068 introduces no byte-read, content-read, streaming, download or
    resource-lifecycle operation;
33. RFC-068 introduces no `DocumentContentStore` or binary-store contract;
34. binary payload access/storage remains a separately governed future
    persistence-neutral contract;
35. no filesystem, network filesystem, database BLOB, object store, file
    server or other binary-storage technology is selected;
36. the repository module performs no filesystem I/O or network I/O;
37. RFC-068 introduces no SQLAlchemy or Infrastructure persistence adapter;
38. RFC-068 introduces no relational schema, table, column, index, constraint
    or Alembic revision and canonical Alembic head remains `0004`;
39. RFC-068 introduces no Session ownership, commit, rollback, transaction
    coordinator, distributed transaction, compensation, outbox or retry
    policy;
40. RFC-060 Document Registration, RFC-064 Knowledge/lineage transaction
    coordination and RFC-065 Document-to-Knowledge ingestion responsibilities
    remain unchanged;
41. RFC-068 introduces no content-registration application service;
42. default `CompositionRoot`, `ServiceContainer`, `PlatformComposition` and
    `ApplicationFacade` remain unchanged;
43. Runtime, Bootstrap, Health, readiness, request admission and
    operational-transition authority remain unchanged;
44. update, replace, delete, revision, supersession and mutable-content
    lifecycle semantics remain deferred;
45. parser, PDF extraction, OCR, text extraction, character-encoding
    detection and chunking remain deferred;
46. Document Library, upload, download, browse, catalogue, source
    synchronization, retention, permissions and approval workflow remain
    deferred;
47. search, embeddings, vector persistence, graph persistence, Neo4j, RAG,
    LLM and AI Agent behavior remain deferred;
48. authentication, authorization, RBAC, Active Directory, trust, approval,
    malware scanning, compliance and Cybersecurity approval remain outside
    RFC-068;
49. dependency direction remains explicit, acyclic and compatible with
    ARCH-001, ARCH-003, CORE-002 and CORE-003;
50. TDD RED begins only after RFC-068 / AD-054 are accepted, committed,
    pushed, exact local / remote accepted-contract identity is verified and
    the working tree is clean;
51. technical verification, if later authorized, includes focused contract
    tests, architecture guardrails, impacted regression, full PlantMind
    regression, Python compilation and `git diff --check`;
52. RFC-068 introduces no production-readiness, production-security or
    Cybersecurity-approval claim.

### Historical Contract Acceptance State Before Implementation Entry

Status at that stage:

**PASSED — RFC-068 / AD-054 ACCEPTED**

Formal Contract Acceptance Review completed successfully.

Review result:

- Gate 0 — Reviewed Git State: PASS;
- Gate 1 — Governance & Decision State: PASS;
- Gate 2 — RFC / AD Contract Equivalence: PASS;
- Gate 3 — Ownership / Namespace / Public Surface: PASS;
- Gate 4 — Identity / Cardinality / Conflict: PASS;
- Gate 5 — Descriptor / Binary Responsibility Separation: PASS;
- Gate 6 — Application / Existence / Transaction Boundaries: PASS;
- Gate 7 — Persistence / Database / Alembic: PASS;
- Gate 8 — Existing Implementation Compatibility: PASS;
- Gate 9 — Deferred Capabilities: PASS;
- Gate 10 — Composition / Runtime / Security: PASS;
- Gate 11 — Dependency Direction / Change Surface: PASS;
- Gate 12 — TDD / Git Governance: PASS;
- Gate 13 — Acceptance Requirement Disposition: PASS;
- Final Static Contract Review: PASS;
- Semantic Contradiction Scan: PASS;
- RFC / AD Material Equivalence: PASS;
- Acceptance Requirements: **52 PASS / 0 REFINE / 0 BLOCKED**.

AD-054 is Accepted.

RFC-068 architecture contract is Accepted.

At that historical contract-acceptance stage, technical implementation
remained prohibited until the accepted architecture documentation was
committed separately, pushed, exact local / remote accepted-contract identity
was verified and the working tree was clean.

No implementation-entry Git gate was open at that stage.


---

## Selected Architecture Workstream — Operational Workload Evidence Contract Placement Remediation

### Status

Selection Record Ready for Commit — Five-Document Source-of-Truth
Propagation Complete; Selection Consistency Review Passed; Architecture
Contract Not Yet Authored or Accepted.

This section records the evidence-based successor-workstream selection
following completion of the broad post-RFC-066 architecture and system
review.

This selection does not constitute RFC contract acceptance, implementation
authorization, production-readiness approval or permission to change
accepted operational-transition semantics.

Selection baseline:

`1d7f09d5106b7714421a1035877ff82a0538d39e`

### Selection Evidence

The broad post-RFC-066 architecture and system review established:

- RFC-066 is fully closed and Source-of-Truth reconciled;
- local and remote Git identity are exact at the selection baseline;
- the working tree is clean;
- full PlantMind regression is **840 passed**;
- **342** Python files compile with zero failures;
- Alembic lineage remains exactly `0001 -> 0002 -> 0003 -> 0004`;
- `CompositionRoot.build()` passes its final smoke verification;
- Domain dependency direction remains clean;
- Infrastructure does not contain an identified upward dependency violation;
- persistence and RFC-064 / RFC-065 transaction ownership remain coherent;
- RFC-066 Document Content remains isolated from persistence, retrieval,
  parsing, OCR, vector, graph, RAG, LLM and default Composition;
- deferred prototypes remain contained and are not production authorities;
- the current Neo4j URI / username / password defaults are unused legacy
  configuration and remain a separate configuration-hygiene debt;
- outside the approved composition boundary, the broad dependency audit
  identified exactly two Core imports of
  `app.services.orchestration.workload_evidence`;
- those imports occur in:
  `app.core.operational_transition_coordinator` and
  `app.core.operational_transition_evidence`;
- AD-032, AD-033, AD-036 and AD-037 establish and preserve the accepted
  `OperationalWorkloadEvidence` semantics and operational-transition
  evidence flow;
- no functional, Runtime-authority or transaction defect was identified in
  those accepted semantics;
- the remaining issue is therefore an isolated physical package-placement
  and dependency-direction architecture debt.

Broad-review judgment:

**PASS WITH REGISTERED NON-BLOCKING DEBT**

### Selection Rationale

Accepted operational-transition semantics require Core transition
coordination and evidence aggregation to consume canonical
`OperationalWorkloadEvidence`.

The current physical location of that contract under
`app.services.orchestration` causes Core modules to depend outward on a
Services package.

The semantic contract is accepted and working, but allowing this physical
dependency to remain as the platform expands would weaken dependency
direction, make package ownership less explicit and create a precedent for
future Core-to-Service coupling.

The minimum architecture-remediation workstream is therefore:

**Operational Workload Evidence Contract Placement Remediation**

The exact replacement package, namespace and compatibility strategy are not
decided by this selection. They require a reviewed architecture contract.

### Objective

Define the minimum architecture change required so canonical Core
operational-transition components can consume
`OperationalWorkloadEvidence` without depending outward on
`app.services.*`, while preserving all accepted workload, transition,
Runtime and composition semantics.

### Required Architecture Questions

The architecture contract for this workstream shall explicitly resolve:

1. which architectural responsibility canonically owns
   `OperationalWorkloadEvidence`;
2. the correct persistence-neutral and behavior-neutral package namespace
   for that contract;
3. whether remediation requires relocation, extraction or another narrowly
   justified contract-placement mechanism;
4. how exact `OperationalWorkloadEvidence` type and object-identity
   semantics remain preserved;
5. how AD-032, AD-033, AD-036 and AD-037 remain authoritative;
6. whether any accepted prior ADR requires explicit amendment rather than
   silent reinterpretation;
7. whether temporary import compatibility is required and, if so, its exact
   removal boundary;
8. which imports and tests may change;
9. which imports and responsibilities shall remain unchanged;
10. how CORE-002 and CORE-003 dependency rules are enforced after
    remediation;
11. how `ApplicationFacade`, `IntegrationGateway`,
    `OrchestrationService` and `WorkflowExecutor` responsibilities remain
    unchanged;
12. how `OperationalTransitionCoordinator`,
    `OperationalTransitionEvidence` and
    `OperationalTransitionApplicationService` semantics remain unchanged;
13. how Runtime remains the sole operational-transition authority;
14. how default `CompositionRoot` behavior remains unchanged;
15. which architecture tests shall prevent recurrence of Core-to-Service
    contract-placement leakage;
16. the exact TDD RED/GREEN and full-regression evidence required before
    implementation may be accepted.

### Existing Responsibilities That Shall Be Preserved

Selection of this workstream does not authorize silent redesign of:

- `OperationalWorkloadEvidence`;
- `ApplicationFacade`;
- `IntegrationGateway`;
- `OrchestrationService`;
- `WorkflowExecutor`;
- `OperationalTransitionEvidence`;
- `OperationalTransitionCoordinator`;
- `OperationalTransitionApplicationService`;
- mandatory-capability availability, policy and coverage responsibilities;
- Runtime transition authority;
- Bootstrap authority;
- default `CompositionRoot`;
- request-admission ownership;
- ARCH-001;
- CORE-002;
- CORE-003;
- AD-032;
- AD-033;
- AD-036;
- AD-037.

If remediation requires changing an accepted prior contract, that change
must be identified and reviewed explicitly before implementation.

### Explicit Non-Goals

This selection does not authorize:

- production implementation;
- behavioral changes to operational workload execution;
- new operational-transition eligibility semantics;
- new Runtime lifecycle state;
- new application facade, gateway, orchestrator or workflow executor;
- new Core Service;
- a seventh ARCH-001 layer;
- persistence changes;
- schema or Alembic changes;
- Document Content persistence or retrieval;
- Document Library implementation;
- parser, OCR or chunking implementation;
- vector, graph, RAG or LLM implementation;
- PI production connectivity;
- Neo4j production integration;
- remediation of the separate unused Neo4j configuration defaults;
- authentication, authorization, RBAC or Active Directory implementation;
- Cybersecurity approval;
- production-readiness claims.

### Completed Work

- RFC-066 technical implementation completed and verified;
- RFC-066 engineering closure completed and verified;
- RFC-066 Source-of-Truth reconciliation completed and verified;
- broad post-RFC-066 architecture/system review completed;
- dependency-direction audit completed;
- persistence and transaction audit completed;
- deferred-capability and prototype-containment audit completed;
- configuration/security-hygiene audit completed;
- final repository integrity gate completed;
- successor architecture debt prioritized from repository evidence;
- Operational Workload Evidence Contract Placement Remediation selected;
- ROADMAP successor-workstream selection record reviewed;
- draft successor-selection state propagated through all five required
  Source-of-Truth documents in the current working tree;
- committed AD-001 through AD-052 history preserved while adding the
  non-decision architecture-governance record;
- committed Engineering Journal history preserved while adding the
  successor-selection record append-only.

### Remaining Work

- commit the reviewed successor-selection documentation separately from
  any future architecture contract;
- push the selection commit;
- verify exact local / remote selection commit identity;
- verify the working tree is clean;
- only then begin architecture-contract drafting for the selected
  remediation workstream.

### Dependencies

This workstream depends on the accepted operational workload and transition
architecture established through AD-032, AD-033, AD-036 and AD-037.

Those semantic prerequisites are satisfied.

The workstream also depends on completion of the broad post-RFC-066
architecture/system review.

That review is complete and passed with registered non-blocking debt.

### Resume Condition

Draft Source-of-Truth propagation is complete.

The complete five-document successor-selection consistency review passed.

The prior automated clean-working-tree failure was verified as a checker
false negative; the required gate is present in the architecture record and
no Source-of-Truth correction was required for that finding.

Technical implementation remains prohibited.

Architecture-contract drafting shall not begin until the reviewed selection
record is committed and pushed, exact local / remote selection identity is
verified and the working tree is clean.

### Next Exact Action

Open the successor-selection documentation commit gate.

Stage and review exactly the five maintained Source-of-Truth documents
before creating the selection commit.

Do not begin architecture-contract drafting before the separate selection
commit is pushed, exact local / remote identity is verified and the working
tree is clean.

---

## RFC-067 — Operational Workload Evidence Contract Placement Remediation

### Status

**Fully Closed and Source-of-Truth Reconciled**

Matching Architecture Decision:

**AD-053 — Accepted**

Accepted architecture-contract commit:

`d5f743fc0d6d416a5e52d21a6aba0b0108cd7b08`

Technical implementation:

**COMPLETE — VERIFIED AND COMMITTED**

Verified technical implementation commit:

`48f245b1064a5f0f203ae0705556bb86628f7403`

Engineering-memory closure:

**COMPLETE — COMMITTED, PUSHED AND VERIFIED**

Verified engineering-memory closure commit:

`76e59a3fe37628f8c60ba0243995ddd5a44bf0a6`

Post-closure Source-of-Truth reconciliation:

**COMPLETE AND VERIFIED**

Verified reconciliation commit:

`33a10d287111539d63c1042948233597b6ab4ed7`

Reconciliation Git verification:

- reconciliation push: **PASS**;
- exact local / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**.

RFC-067 is fully closed and Source-of-Truth reconciled.

No successor RFC or architecture workstream is selected or preselected by
this closure.

Successor-workstream selection baseline:

`1d7f09d5106b7714421a1035877ff82a0538d39e`

RFC-067 architecture-contract drafting baseline:

`4ed69096aff2f201f6c5aa8d96c4ec96d43e4122`

### Context

The broad post-RFC-066 architecture and system review identified one
isolated dependency-direction debt.

Canonical operational-transition Core components currently consume:

`OperationalWorkloadEvidence`

from:

`app.services.orchestration.workload_evidence`

The two identified Core consumers are:

- `app.core.operational_transition_evidence`;
- `app.core.operational_transition_coordinator`.

The accepted behavior itself is not defective.

AD-032 established trusted correlated operational-workload evidence.

AD-033 established immutable operational-transition evidence aggregation.

AD-036 established operational-transition coordination.

AD-037 established the explicit operational-transition application
boundary.

Those accepted semantics remain authoritative.

The architecture debt is physical contract placement:

Core currently depends outward on a Services-owned package for an
immutable evidence contract.

CORE-002 permits Core dependencies on shared models and value objects but
prohibits Core dependencies on Business Services and Workflows.

CORE-003 permits dependencies on Contracts and Value Objects while
requiring dependency direction to remain explicit and acyclic.

ARCH-003 requires Contracts to belong to Domain Architecture rather than
Services, Infrastructure, APIs, Engines or external frameworks.

RFC-067 therefore addresses package ownership and dependency direction
only.

### Decision

RFC-067 SHALL relocate the existing operational-workload evidence
contract family to one canonical Domain Architecture module:

`backend/app/domain/operational_workload_evidence.py`

with canonical Python import path:

`app.domain.operational_workload_evidence`

The canonical contract family SHALL remain exactly:

- `ApplicationFacadeEntryEvidence`;
- `WorkflowExecutionStartEvidence`;
- `OperationalWorkloadEvidence`.

RFC-067 SHALL NOT create:

- `app.shared`;
- `app.contracts`;
- another architectural layer;
- another Core Service;
- another workload-evidence abstraction;
- another operational workload identity;
- duplicate evidence classes.

### Architectural Owner

The operational-workload evidence contract family SHALL have exactly one
architectural owner:

**Domain Architecture — Operational Workload Provenance Evidence**

The producer components remain responsible for producing the evidence
instances defined by the Domain contract.

Contract ownership SHALL NOT transfer workload execution, orchestration
or lifecycle authority into Domain Architecture.

Domain owns the immutable information contract.

Existing application and orchestration components retain their accepted
behavioral responsibilities.

### ARCH-001 Layer Clarification

The term:

`Domain Architecture`

in RFC-067 describes architectural ownership and the canonical namespace
for behavior-neutral information contracts.

It SHALL NOT be interpreted as a new primary PlantMind architectural
layer.

RFC-067 introduces no seventh ARCH-001 layer.

ARCH-001 remains authoritative for the six primary architectural layers
and dependency direction.

Placement under:

`app.domain`

expresses contract ownership and dependency neutrality only.

### Distinction from Existing Engineering Evidence

RFC-067 SHALL NOT merge operational-workload provenance evidence with:

`app.domain.evidence`

The existing:

- `Evidence`;
- `EvidenceType`;

represent engineering evidence consumed by reasoning and intelligence
components.

They are a separate Domain concept.

RFC-067 SHALL NOT modify:

`backend/app/domain/evidence.py`

and SHALL NOT reinterpret engineering evidence as operational-workload
provenance evidence.

### Canonical Contract Schema

RFC-067 SHALL preserve the existing AD-032 schema exactly.

#### ApplicationFacadeEntryEvidence

Canonical structure:

`workload_id: UUID`

It SHALL remain an immutable:

`@dataclass(frozen=True, slots=True)`

RFC-067 SHALL NOT:

- add fields;
- remove fields;
- rename fields;
- change the UUID type;
- make the constructor keyword-only;
- introduce an EntityId;
- add behavioral responsibilities.

#### WorkflowExecutionStartEvidence

Canonical structure:

`workload_id: UUID`

It SHALL remain an immutable:

`@dataclass(frozen=True, slots=True)`

RFC-067 SHALL NOT:

- add fields;
- remove fields;
- rename fields;
- change the UUID type;
- make the constructor keyword-only;
- introduce an EntityId;
- add behavioral responsibilities.

#### OperationalWorkloadEvidence

Canonical structure:

- `facade_entry: ApplicationFacadeEntryEvidence`;
- `execution_start: WorkflowExecutionStartEvidence`.

It SHALL remain an immutable:

`@dataclass(frozen=True, slots=True)`

Construction SHALL continue to reject mismatched workload identities with:

`ValueError`

The accepted failure message SHALL remain:

`Operational workload evidence requires matching workload identities.`

RFC-067 SHALL NOT introduce additional correlation policy, validation
policy, identity generation or business behavior.

### Workload Identity Semantics

AD-032 remains authoritative.

Each canonical `ApplicationFacade.analyze(...)` invocation SHALL continue
to generate exactly one workload UUID.

That same workload identity SHALL continue to propagate unchanged through:

`ApplicationFacade`
→ `IntegrationGateway`
→ `OrchestrationService`
→ `WorkflowExecutor`

Intermediate components SHALL NOT regenerate or replace the workload
identity.

RFC-067 changes only the module from which the evidence contract classes
are imported.

### Producer Ownership

RFC-067 SHALL preserve producer ownership exactly.

`ApplicationFacade` SHALL remain the canonical producer of:

`ApplicationFacadeEntryEvidence`

`WorkflowExecutor` SHALL remain the canonical producer of:

`WorkflowExecutionStartEvidence`

and of the correlated:

`OperationalWorkloadEvidence`

when canonical facade-entry evidence was supplied.

RFC-067 SHALL NOT move evidence production into:

- Core;
- Runtime;
- `OperationalTransitionCoordinator`;
- `OperationalTransitionEvidence`;
- `OperationalTransitionApplicationService`;
- CompositionRoot;
- API transport;
- Domain factory services.

### Propagation Semantics

`IntegrationGateway` SHALL continue forwarding the exact supplied
`ApplicationFacadeEntryEvidence` unchanged.

`OrchestrationService` SHALL continue forwarding the exact supplied
`ApplicationFacadeEntryEvidence` unchanged.

`WorkflowExecutor` SHALL continue constructing execution-start evidence
from the exact propagated workload identity.

Direct internal workflow invocation without canonical facade-entry
evidence SHALL continue to produce:

`operational_workload_evidence = None`

No synthetic canonical workload provenance SHALL be fabricated.

### WorkflowExecution Boundary

The accepted `WorkflowExecution` contract SHALL remain unchanged.

It SHALL continue to expose:

`operational_workload_evidence: OperationalWorkloadEvidence | None`

RFC-067 SHALL NOT modify:

- workflow result semantics;
- workflow stages;
- completion semantics;
- ordinary workload execution behavior.

### Evidence Object Identity

AD-033, AD-036 and AD-037 identity-preservation semantics remain
authoritative.

Consumers SHALL receive the exact produced `OperationalWorkloadEvidence`
object.

RFC-067 SHALL NOT:

- copy it;
- wrap it;
- normalize it;
- reconstruct it;
- subclass it;
- translate it into another workload-evidence type.

The same object shall continue to flow from canonical workload execution
into operational-transition coordination.

### Canonical Import Boundary

After accepted technical remediation, all maintained non-test Python
consumers of this contract family SHALL import from:

`app.domain.operational_workload_evidence`

This includes the current consumers in:

- `app.services.application_facade`;
- `app.services.integration_gateway`;
- `app.services.orchestration.orchestration_service`;
- `app.services.orchestration.workflow`;
- `app.services.orchestration.workflow_executor`;
- `app.core.operational_transition_evidence`;
- `app.core.operational_transition_coordinator`.

The exact implementation review SHALL verify the complete import graph
again before technical acceptance.

### Core Dependency Remediation

After RFC-067 remediation:

`app.core.operational_transition_evidence`

and:

`app.core.operational_transition_coordinator`

SHALL NOT import operational-workload evidence from:

`app.services.*`

Both SHALL consume the canonical Domain contract.

RFC-067 SHALL NOT establish a general exception permitting Core to depend
on Services.

RFC-067 removes the identified exception-shaped package coupling rather
than legitimizing it.

### Legacy Import Compatibility Boundary

The existing module:

`app.services.orchestration.workload_evidence`

SHALL remain temporarily available as a compatibility import boundary.

It SHALL cease owning independent class definitions.

It SHALL re-export the exact three canonical Domain classes:

- `ApplicationFacadeEntryEvidence`;
- `WorkflowExecutionStartEvidence`;
- `OperationalWorkloadEvidence`.

The legacy module SHALL NOT:

- define duplicate dataclasses;
- subclass canonical evidence classes;
- wrap canonical evidence classes;
- introduce conversion functions;
- introduce factories;
- introduce validation;
- introduce state;
- introduce I/O;
- introduce orchestration behavior.

### Exact Python Type Identity

Legacy compatibility SHALL preserve exact Python class identity.

For each canonical contract:

`LegacyClass is CanonicalClass`

SHALL evaluate to:

`True`

Objects imported through the legacy module SHALL therefore remain valid
for canonical `isinstance(...)` checks.

RFC-067 SHALL NOT maintain two Python class definitions representing the
same architectural contract.

### Canonical Module Provenance

After remediation, the canonical class definitions SHALL physically
reside in:

`app.domain.operational_workload_evidence`

The canonical classes' Python module provenance may therefore identify the
new Domain module.

That module-path provenance change is intentional and is limited to
correcting architectural ownership.

The legacy import path remains available through exact re-export
compatibility.

RFC-067 does not establish compatibility guarantees for undocumented
string comparisons against historical `__module__` values.

### Compatibility Removal Boundary

RFC-067 SHALL NOT remove:

`app.services.orchestration.workload_evidence`

Removal of the compatibility module requires a separate reviewed
breaking-change decision after:

1. all maintained in-repository consumers use the canonical Domain path;
2. maintained tests no longer depend on the legacy path except explicit
   compatibility verification;
3. any relevant supported external Python consumers have been assessed;
4. backward-compatibility impact has been explicitly reviewed.

No automatic deprecation-removal date is introduced by RFC-067.

### Internal Test Import Migration

Maintained tests that validate canonical contract behavior SHALL use:

`app.domain.operational_workload_evidence`

as their canonical import path.

A narrow dedicated compatibility verification MAY continue importing the
legacy Services path solely to prove exact re-export identity.

Tests SHALL NOT preserve obsolete Services ownership merely to keep old
test imports unchanged.

### Canonical Domain Dependency Contract

`backend/app/domain/operational_workload_evidence.py`

SHALL remain dependency-light.

Its implementation dependencies SHALL be limited to Python standard
library facilities required by the existing contract semantics, currently:

- `dataclasses.dataclass`;
- `uuid.UUID`;
- `__future__.annotations`.

The canonical module SHALL NOT import:

- `app.services`;
- `app.core`;
- `app.infrastructure`;
- `app.api`;
- `app.engines`;
- repositories;
- connectors;
- databases;
- frameworks;
- logging systems;
- Runtime;
- CompositionRoot.

### Domain Package Public Surface

RFC-067 SHALL NOT require a broad re-export from:

`app.domain.__init__`

Canonical consumption SHALL use the explicit module path:

`app.domain.operational_workload_evidence`

unless a separately reviewed Domain public-API policy later establishes
another export boundary.

### AD-032 Preservation

RFC-067 SHALL NOT amend the accepted semantic responsibilities of AD-032.

The following remain unchanged:

- one UUID per canonical facade invocation;
- exact workload identity propagation;
- facade-entry evidence ownership;
- workflow-execution-start evidence ownership;
- correlation validation;
- direct-internal-invocation behavior;
- `WorkflowExecution` evidence exposure;
- failure boundaries;
- Runtime separation;
- Composition separation.

RFC-067 changes physical contract ownership and import placement only.

### AD-033 Preservation

RFC-067 SHALL NOT amend AD-033 operational-transition evidence
aggregation semantics.

`OperationalTransitionEvidence` SHALL continue to consume existing
validated `OperationalWorkloadEvidence`.

It SHALL continue to preserve the exact supplied object.

It SHALL NOT recreate workload provenance or repeat workload-correlation
validation.

### AD-036 Preservation

RFC-067 SHALL NOT amend AD-036 coordination semantics.

`OperationalTransitionCoordinator.request_operational(...)`

SHALL continue to accept:

`OperationalWorkloadEvidence | None`

The coordinator SHALL continue to:

- observe capabilities exactly as already accepted;
- evaluate mandatory-capability coverage exactly as already accepted;
- construct one `OperationalTransitionEvidence`;
- preserve exact evidence identity;
- invoke `Runtime.request_operational(...)` exactly as already accepted.

Runtime remains the sole lifecycle-transition authority.

### AD-037 Preservation

RFC-067 SHALL NOT amend AD-037 application-use-case semantics.

`OperationalTransitionApplicationService` SHALL continue obtaining
workload evidence only from:

`WorkflowExecution.operational_workload_evidence`

and SHALL forward the exact value, including `None`, unchanged to the
canonical coordinator.

It SHALL NOT construct, reconstruct or independently validate operational
workload evidence.

### Prior ADR Amendment Determination

RFC-067 explicitly reviewed the accepted contracts established by:

- AD-032;
- AD-033;
- AD-036;
- AD-037.

Those accepted decisions define workload-evidence meaning, ownership of
production, propagation, aggregation, coordination, object-identity and
Runtime-authority semantics.

They do not normatively require the operational-workload evidence classes
to remain physically defined under:

`app.services.orchestration.workload_evidence`

The RFC-067 package relocation therefore does not require historical
amendment of AD-032, AD-033, AD-036 or AD-037.

Their historical accepted text SHALL remain unchanged.

AD-053, if later accepted, SHALL be the new architecture decision that
explicitly authorizes the canonical Domain placement and temporary legacy
re-export compatibility boundary.

RFC-067 SHALL NOT silently reinterpret any accepted prior ADR.

If later review identifies a prior accepted requirement that fixes the old
physical package location, implementation SHALL stop and that prior
contract change SHALL be reviewed explicitly before proceeding.

### Adjacent OperationalTransitionEvidence Placement Boundary

The current:

`OperationalTransitionEvidence`

class remains physically located under:

`app.core.operational_transition_evidence`

RFC-067 SHALL NOT relocate that class.

RFC-067 SHALL NOT claim that its physical placement has been reviewed,
remediated or certified as fully compliant with ARCH-003.

Its accepted AD-033 aggregation semantics remain unchanged.

Whether its physical package placement requires separate remediation is an
adjacent pre-existing architecture question outside the selected RFC-067
workstream.

That question MAY be considered only through a future evidence-based
architecture review and workstream-selection process.

RFC-067 does not preselect that future work.

### ARCH-003 Contract Governance

RFC-067 recognizes the operational-workload evidence family as an
existing Evidence Contract family governed by ARCH-003.

RFC-067 SHALL NOT enlarge the accepted runtime schema merely to perform a
package-placement remediation.

For architecture-documentation purposes, RFC-067 SHALL record the
preserved existing schema as:

- documentation contract version: `1.0`;
- architectural owner:
  `Domain Architecture — Operational Workload Provenance Evidence`.

The `1.0` declaration documents the existing preserved contract shape.

It SHALL NOT:

- add a runtime version field;
- imply that an earlier runtime versioning mechanism existed;
- change any accepted AD-032 field or behavior;
- establish a schema-version migration mechanism.

RFC-067 SHALL NOT assign a new information-security classification to the
contract family.

Security classification can affect storage, transport, access and audit
policy and therefore requires separately reviewed security context rather
than an assumption inside a package-placement remediation.

RFC-067 SHALL NOT add runtime fields for:

- contract version;
- security classification;
- producer metadata;
- timestamps;
- serialization metadata.

RFC-067 introduces no:

- transport serializer;
- protocol adapter;
- persistence representation;
- schema registry;
- contract translation service.

RFC-067 does not claim that previously unverified ARCH-003 serialization,
security-classification or publication-readiness requirements have been
completed merely by relocating the contract.

Any such pre-existing governance gap remains separately governed.

A future serialization, classification, schema-version or additional
metadata decision requires separate architecture review.

RFC-067 does not establish a general exemption from ARCH-003.

If AD-053 is later accepted, its authority SHALL be limited to the
placement, compatibility and preservation decisions expressly defined by
RFC-067.

### Runtime Boundary

Runtime SHALL remain the sole authoritative owner of platform lifecycle
state.

RFC-067 SHALL NOT:

- modify Runtime state;
- add Runtime states;
- change `Runtime.request_operational(...)`;
- modify readiness;
- modify request admission;
- create automatic operational transitions;
- change operational eligibility.

Operational-workload evidence remains evidence only.

### Composition Boundary

RFC-067 SHALL NOT modify default `CompositionRoot` responsibilities.

No new:

- service instance;
- registry entry;
- provider;
- factory;
- runtime dependency;
- composition lifecycle object;

is required merely because an immutable contract changes canonical
package ownership.

Existing composed component identity SHALL remain unchanged.

### Bootstrap and Health Boundaries

RFC-067 SHALL NOT modify:

- BootstrapManager;
- service startup;
- shutdown;
- HealthCapability;
- readiness evaluation;
- mandatory-capability policy.

No startup or health behavior shall be coupled to contract relocation.

### API and Transport Boundary

RFC-067 SHALL NOT modify:

- FastAPI routes;
- request schemas;
- response schemas;
- request-admission ownership;
- client-visible operational-transition semantics.

External clients SHALL continue to be unable to supply trusted internal
operational-workload evidence.

RFC-067 introduces no public transport representation of the evidence
contract.

### Persistence and Transaction Boundary

RFC-067 introduces no:

- repository;
- persistence adapter;
- database table;
- relational mapping;
- Alembic revision;
- transaction coordinator;
- commit;
- rollback;
- evidence history;
- evidence store.

Existing RFC-060, RFC-064 and RFC-065 transaction semantics remain
unchanged.

Canonical Alembic authority remains unchanged.

### State Boundary

RFC-067 introduces no:

- mutable evidence registry;
- global workload-evidence collector;
- evidence cache;
- evidence queue;
- evidence history;
- singleton evidence object.

The relocated evidence contracts remain immutable per-execution values.

### Security Boundary

RFC-067 SHALL NOT establish or claim:

- authentication;
- authorization;
- RBAC;
- Active Directory integration;
- cryptographic attestation;
- distributed trace authentication;
- external identity verification;
- Cybersecurity approval;
- production security readiness.

RFC-067 assigns no information-security classification to this
contract family.

No absence of a classification shall be interpreted as authorization,
reduced sensitivity or production-security readiness.

Any future information-security classification requires separately
reviewed security context and does not alter authentication,
authorization or access-control authority merely by being documented.

### Explicit Non-Goals

RFC-067 SHALL NOT implement or redesign:

- workload execution behavior;
- workflow stages;
- reasoning;
- operational-transition eligibility;
- capability availability semantics;
- mandatory-capability coverage semantics;
- Runtime lifecycle semantics;
- request admission;
- persistence;
- database schema;
- Document architecture;
- Knowledge architecture;
- Document Content architecture;
- parser or OCR;
- vector search;
- graph behavior;
- RAG;
- LLM behavior;
- PI production connectivity;
- Neo4j production integration;
- authentication or RBAC;
- deployment architecture.

The separate unused Neo4j configuration-hygiene debt remains outside
RFC-067.

### Expected Technical Change Surface If Accepted

If and only if the RFC-067 / AD-053 architecture contract is accepted,
committed, pushed and passes the implementation-entry Git gate, the
expected technical change surface is limited to:

New canonical Domain module:

- `backend/app/domain/operational_workload_evidence.py`.

Legacy compatibility module:

- `backend/app/services/orchestration/workload_evidence.py`.

Current non-test import consumers:

- `backend/app/services/application_facade.py`;
- `backend/app/services/integration_gateway.py`;
- `backend/app/services/orchestration/orchestration_service.py`;
- `backend/app/services/orchestration/workflow.py`;
- `backend/app/services/orchestration/workflow_executor.py`;
- `backend/app/core/operational_transition_evidence.py`;
- `backend/app/core/operational_transition_coordinator.py`.

Maintained tests importing the legacy contract path may require canonical
import updates.

RFC-067 architecture tests SHALL be added to enforce the accepted
placement and compatibility boundaries.

The expected RFC-067 technical surface SHALL NOT include relocation or
redesign of:

`app.core.operational_transition_evidence`

or the `OperationalTransitionEvidence` class.

Any implementation need outside this expected surface SHALL stop for
architecture review before expansion.

### TDD Entry Contract

Technical implementation SHALL begin with RED tests only after all of the
following are true:

1. RFC-067 architecture review passes;
2. matching AD-053 is reviewed;
3. RFC-067 and AD-053 are confirmed materially and semantically
   equivalent;
4. both are Accepted;
5. the accepted architecture documentation is committed separately from
   technical implementation;
6. the accepted contract commit is pushed;
7. exact local / remote accepted-contract identity is verified;
8. the working tree is clean.

Before those gates pass:

**NO TDD RED AND NO PRODUCTION IMPLEMENTATION ARE AUTHORIZED.**

### Required RED Evidence

The initial RED verification SHALL prove the current architecture debt
before remediation.

At minimum it SHALL detect that:

- the canonical Domain module does not yet provide the contract family;
  and/or
- Core still imports `OperationalWorkloadEvidence` through
  `app.services.orchestration.workload_evidence`.

The RED stage SHALL fail for the intended contract-placement reason.

Unrelated regression failures SHALL NOT be accepted as valid RED
evidence.

### Required GREEN Architecture Guardrails

Technical acceptance SHALL include tests proving at minimum:

1. the canonical Domain module owns all three class definitions;
2. canonical class schemas remain unchanged;
3. mismatch validation remains unchanged;
4. the legacy module re-exports the canonical classes;
5. legacy and canonical imports have exact class identity;
6. no duplicate operational-workload evidence class definition exists;
7. both Core consumers import the Domain contract rather than Services;
8. maintained non-test Python consumers use the canonical Domain path;
9. direct internal workflow invocation still produces no fabricated
   operational-workload evidence;
10. exact workload-evidence object identity remains preserved through the
    operational-transition path;
11. Runtime authority remains unchanged;
12. CompositionRoot behavior remains unchanged;
13. `app.domain.evidence` remains separate and unchanged;
14. the canonical Domain contract module contains no prohibited outward
    dependency.

### Verification Contract

Technical verification, if later authorized, SHALL include:

- focused RFC-067 contract tests;
- impacted Core regression;
- impacted Services / orchestration regression;
- operational-transition application-service regression;
- API operational-transition regression;
- Composition regression;
- full PlantMind regression;
- Python compilation verification;
- dependency/import static verification;
- `git diff --check`;
- exact technical-commit local / remote identity;
- clean working tree after technical push.

No technical acceptance shall be based only on focused tests.

### Documentation and Commit Separation

The RFC-067 / AD-053 architecture-contract commit SHALL remain separate
from the future technical implementation commit.

Technical implementation SHALL NOT be committed together with contract
acceptance.

Post-implementation engineering-memory closure SHALL remain a separate
governed step after technical verification.

### Acceptance Requirements

Before RFC-067 / AD-053 may become Accepted, architecture review SHALL
confirm:

1. RFC-067 introduces no new ARCH-001 architectural layer and `Domain Architecture` is explicitly an ownership / namespace designation rather than a seventh layer;
2. RFC-067 creates no new Core Service;
3. the workstream remains package-placement remediation only;
4. Domain Architecture becomes the single architectural owner of the
   operational-workload evidence contract family;
5. the canonical module is exactly
   `app.domain.operational_workload_evidence`;
6. RFC-067 creates no `app.shared` or `app.contracts` package;
7. the canonical family remains exactly the three accepted evidence
   classes;
8. `ApplicationFacadeEntryEvidence` remains exactly one UUID field;
9. `WorkflowExecutionStartEvidence` remains exactly one UUID field;
10. `OperationalWorkloadEvidence` remains exactly the accepted two-field
    correlated aggregate;
11. all three contracts retain frozen and slotted dataclass semantics;
12. existing positional / keyword constructor compatibility is preserved
    and `kw_only` is not introduced;
13. workload identity remains `UUID`;
14. mismatch validation remains `ValueError` with accepted semantics;
15. AD-032 workload-correlation meaning remains unchanged;
16. `ApplicationFacade` remains facade-entry evidence producer;
17. `IntegrationGateway` preserves exact evidence propagation;
18. `OrchestrationService` preserves exact evidence propagation;
19. `WorkflowExecutor` retains execution-start and correlated-evidence
    production ownership;
20. direct internal execution without facade-entry evidence still
    fabricates no canonical workload evidence;
21. `WorkflowExecution.operational_workload_evidence` remains unchanged;
22. exact evidence object-identity semantics remain preserved;
23. explicit prior-ADR review confirms AD-032, AD-033, AD-036 and
    AD-037 do not normatively fix the old physical package location and
    require no historical amendment for RFC-067;
24. AD-032 and AD-033 accepted semantics remain unchanged;
25. AD-036 accepted semantics remain unchanged;
26. AD-037 accepted semantics remain unchanged;
27. Runtime remains the sole lifecycle-transition authority;
28. `OperationalTransitionApplicationService` continues forwarding the
    exact workload-evidence value unchanged;
29. the legacy Services workload-evidence module remains as a temporary
    re-export compatibility boundary;
30. legacy imports resolve to the exact canonical class objects;
31. no duplicate classes, wrappers, subclasses or translation objects are
    introduced;
32. maintained non-test imports migrate to the canonical Domain path;
33. maintained tests use the canonical path except dedicated compatibility
    verification;
34. removal of the legacy compatibility module remains separately
    governed and outside RFC-067;
35. the canonical Domain module remains dependency-light and standard
    library only;
36. the two identified Core consumers no longer import workload evidence
    from `app.services.*`;
37. RFC-067 creates no general Core-to-Services dependency exception;
38. `app.domain.evidence` remains a distinct unchanged Domain concept
    and RFC-067 requires no broad `app.domain.__init__` re-export;
39. `OperationalTransitionEvidence` physical Core placement remains
    outside RFC-067 and is not declared remediated or ARCH-003 compliant
    by this workstream;
40. default CompositionRoot behavior and authority remain unchanged;
41. Bootstrap, Health and readiness responsibilities remain unchanged;
42. API transport and request-admission behavior remain unchanged;
43. no repository, persistence, schema or Alembic change is introduced;
44. no existing transaction responsibility is changed;
45. no registry, global evidence collector, cache or mutable evidence
    state is introduced;
46. no authentication, authorization, Cybersecurity or production-readiness
    claim is introduced;
47. ARCH-003 documentation version and architectural ownership are
    recorded without changing runtime contract fields, while unverified
    serialization, security-classification and publication-readiness
    requirements are explicitly not claimed as completed by RFC-067;
48. no serializer, protocol adapter, contract translation service or
    schema-version migration is introduced;
49. implementation begins with intentional RED evidence only after the
    accepted-contract Git gate is satisfied;
50. architecture tests verify canonical ownership, dependency direction
    and exact legacy re-export identity;
51. technical acceptance requires focused, impacted, full-regression,
    compilation and static dependency evidence;
52. architecture documentation, technical implementation and
    post-implementation closure remain separate governed commits.

### RFC-067 Draft Architecture Review

Status:

**PASSED — 52 / 52 RFC-067 Draft Acceptance Requirements**

Formal RFC-side architecture review is complete.

Disposition:

- PASS: 52;
- REFINE: 0;
- BLOCKED: 0.

The review confirmed consistency with:

- ARCH-001;
- ARCH-003;
- CORE-002;
- CORE-003;
- AD-032;
- AD-033;
- AD-036;
- AD-037;
- current workload-execution implementation;
- current operational-transition implementation;
- current import and test graph;
- the evidence-based successor-workstream selection.

The review confirms that RFC-067:

- remediates physical contract placement without redesigning accepted
  workload semantics;
- establishes
  `app.domain.operational_workload_evidence`
  as the canonical Domain contract namespace;
- preserves the existing three-class schema;
- preserves exact workload and evidence object identity;
- preserves producer and propagation responsibilities;
- removes the identified Core-to-Services contract dependency;
- preserves a temporary exact-identity legacy re-export boundary;
- introduces no seventh ARCH-001 layer;
- does not historically amend AD-032, AD-033, AD-036 or AD-037;
- does not claim adjacent `OperationalTransitionEvidence` placement is
  remediated;
- does not claim completion of previously unverified ARCH-003
  serialization, security-classification or publication-readiness
  requirements;
- preserves Runtime, Composition, Bootstrap, API, persistence and
  transaction authority;
- introduces no production-readiness or Cybersecurity claim.

This is an RFC-side draft review only.

It does NOT:

- accept RFC-067;
- create or accept AD-053;
- authorize TDD RED;
- authorize production implementation.

A matching AD-053 draft and a combined RFC-067 / AD-053
semantic-consistency review remain mandatory before acceptance.

### Contract Acceptance Review

Status:

**PASSED — RFC-067 / AD-053 ACCEPTED**

RFC-067 formal architecture review:

**52 PASS / 0 REFINE / 0 BLOCKED**

AD-053 formal architecture review:

**52 PASS / 0 REFINE / 0 BLOCKED**

Combined RFC-067 / AD-053 semantic-consistency review:

**PASS**

The review confirmed that the RFC-067 and AD-053 normative architecture
contracts are byte-for-byte equivalent.

Their 52 Acceptance Requirements are byte-for-byte equivalent and remain
numbered exactly 1 through 52.

No broader, narrower or contradictory architecture requirement was
identified in AD-053.

The accepted contract preserves:

- ARCH-001;
- ARCH-003;
- CORE-002;
- CORE-003;
- AD-032;
- AD-033;
- AD-036;
- AD-037;
- workload identity and provenance semantics;
- exact evidence object identity;
- producer and propagation responsibilities;
- Runtime lifecycle authority;
- CompositionRoot authority;
- Bootstrap and Health boundaries;
- API and request-admission boundaries;
- persistence and transaction boundaries.

RFC-067 is Accepted.

AD-053 is Accepted.

Technical implementation remains unauthorized until the accepted-contract
Git gate is satisfied.

### Technical Implementation Verification

RFC-067 technical implementation is complete and verified.

Accepted architecture-contract commit:

`d5f743fc0d6d416a5e52d21a6aba0b0108cd7b08`

Technical implementation commit:

`48f245b1064a5f0f203ae0705556bb86628f7403`

TDD evidence:

- intentional RED: **2 expected failures**;
- RED failure reason matched the accepted package-placement debt;
- focused GREEN verification: **101 passed**;
- full PlantMind regression: **850 passed**;
- Python compilation: **PASS**;
- `CompositionRoot.build()`: **PASS**;
- static dependency / import integrity: **PASS**;
- `git diff --check`: **PASS**.

Implementation verification also confirmed:

- the canonical contract definitions now reside in
  `app.domain.operational_workload_evidence`;
- the canonical Domain implementation preserves the pre-RFC contract
  definitions byte-for-byte;
- all three canonical class definitions have one backend owner;
- the legacy Services module owns no duplicate class definitions;
- legacy imports re-export the exact canonical Python class objects;
- all maintained non-test backend consumers use the canonical Domain path;
- the two identified Core consumers no longer import workload evidence
  from `app.services.*`;
- maintained tests use the canonical path except the dedicated compatibility
  verification;
- `app.domain.evidence` remains byte-for-byte unchanged;
- Composition, Runtime, Bootstrap, API, Infrastructure and migration
  surfaces remain untouched;
- no `NotImplementedError` placeholder was introduced;
- the verified technical change surface contained exactly 15 files.

Technical commit Git verification:

- push: **PASS**;
- exact local / remote identity: **PASS**;
- working tree after push: **clean**.

RFC-067 technical implementation therefore conforms to the accepted
RFC-067 / AD-053 architecture contract.

This technical verification does not itself complete engineering-memory
or Source-of-Truth closure.

### Implementation Authorization

Status:

**SATISFIED — TECHNICAL IMPLEMENTATION COMPLETED AND VERIFIED**

The implementation-entry Git gate was satisfied before RFC-067 TDD RED.

Technical implementation has been completed, verified, committed and
pushed.

Exact local / remote technical commit identity was verified at:

`48f245b1064a5f0f203ae0705556bb86628f7403`

The working tree after technical push was clean.

No additional RFC-067 production-code modification is authorized merely
by this completion record.

Any further technical change requires its own applicable architecture and
change-control basis.

### Engineering-Memory Closure Verification

RFC-067 engineering-memory closure is complete.

Verified closure commit:

`76e59a3fe37628f8c60ba0243995ddd5a44bf0a6`

Closure Git verification:

- closure commit creation: **PASS**;
- commit message: `RFC-067: close engineering memory`;
- closure commit parent:
  `48f245b1064a5f0f203ae0705556bb86628f7403`;
- closure surface: exactly the five maintained Source-of-Truth documents;
- production-code changes in closure commit: none;
- test-file changes in closure commit: none;
- reviewed staged document blobs matched the committed blobs;
- Engineering Journal historical prefix: preserved byte-for-byte;
- AD-001 through AD-053 historical records: preserved;
- AD-053 remains the final accepted Architecture Decision;
- AD-054: not created;
- closure push: **PASS**;
- exact local / remote closure identity: **PASS**;
- working tree after closure push: **clean**.

Engineering-memory closure is therefore:

**COMPLETE — COMMITTED, PUSHED AND VERIFIED**

This closure verification does not itself complete post-closure
Source-of-Truth reconciliation.

### Final Source-of-Truth Reconciliation Verification

RFC-067 post-closure Source-of-Truth reconciliation is complete and
verified.

Engineering closure commit:

`76e59a3fe37628f8c60ba0243995ddd5a44bf0a6`

Reconciliation commit:

`33a10d287111539d63c1042948233597b6ab4ed7`

Final verification:

- reconciliation commit parent is the verified engineering closure commit;
- reconciliation documentation surface contains exactly the five maintained
  Source-of-Truth documents;
- reconciliation push: **PASS**;
- exact local / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- production-code changes: none;
- test-file changes: none;
- historical Engineering Journal prefix: preserved;
- historical AD-001 through AD-053 content: preserved;
- AD-053 remains Accepted;
- AD-054 was not created;
- technical baseline remains 850 passed;
- canonical Alembic head remains `0004`;
- canonical workload-evidence Domain ownership remains unchanged;
- legacy compatibility boundary remains unchanged;
- `OperationalTransitionEvidence` placement remains outside RFC-067;
- documented security and production-readiness non-claims remain unchanged.

RFC-067 is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

### Next Exact Action

Perform evidence-based selection of the next architecture workstream.

No successor RFC or architecture workstream is assumed, selected or
preselected by RFC-067 closure.

Any future implementation remains prohibited until its own architecture
contract is reviewed, accepted, committed, pushed and its implementation-
entry Git gate is satisfied.

## Selected Architecture Workstream — Canonical Enterprise Document Content Foundation Boundary

### Status

Selection Record Complete — RFC-066 Fully Closed and Source-of-Truth Reconciled; Broad Architecture/System Review Pending.

This section preserves the evidence-based workstream-selection record that
preceded RFC-066 / AD-052 acceptance and technical implementation.

The selection record itself did not constitute contract acceptance,
implementation authorization or a production-readiness claim.

Selection baseline:

`70a094b2c2154b6555a21f3ad3d31abfe571d1db`

### Selection Evidence

The post-RFC-065 architecture and repository review confirms:

- RFC-065 is fully closed and Source-of-Truth reconciled;
- AD-051 remains Accepted;
- RFC-065 full PlantMind regression baseline is **779 passed**;
- canonical `EnterpriseDocument` identity and Domain semantics exist;
- persistence-neutral Enterprise Document repository semantics exist;
- relational Enterprise Document persistence exists;
- `EnterpriseDocumentRegistrationApplicationService` exists;
- canonical Knowledge identity, capture and relational persistence exist;
- canonical Document-to-Knowledge lineage exists;
- canonical lineage relational persistence exists;
- RFC-064 provides coordinated Knowledge / lineage persistence;
- RFC-065 provides canonical Knowledge ingestion from an already
  registered `EnterpriseDocument.id`;
- RFC-065 consumes prepared Knowledge fields and deliberately does not
  perform raw-file transformation;
- current canonical Document registration carries Document metadata and
  external source traceability but does not establish canonical Document
  content semantics;
- `DocumentSource.source_reference` remains external traceability and is
  not canonical Document identity, repository alternate identity,
  uniqueness identity or deduplication identity;
- accepted architecture does not authorize silently treating
  `source_reference` as canonical content identity;
- current `document_parser.py`, `semantic_search.py`, `rag_engine.py`
  and `vector_memory.py` remain empty capability seams;
- the current `KnowledgeGraphService` remains an in-memory prototype;
- Document Library behavior, binary storage, upload/download, source
  synchronization, parsing, OCR, extraction, chunking, revision,
  semantic retrieval, embeddings, vector persistence, graph
  persistence, Neo4j, RAG and LLM behavior remain separately deferred;
- authentication, authorization, RBAC, Active Directory and production
  Cybersecurity readiness remain separately gated;
- no accepted lower-level canonical Document-content abstraction was
  identified in the reviewed repository evidence.

### Selection Rationale

PlantMind now possesses canonical Document identity and can derive
canonical Knowledge from an existing Enterprise Document, but the
architecture still lacks an accepted definition of the Document's
content itself.

Introducing parsing, OCR, chunking, semantic search, vector persistence
or RAG before defining canonical Document-content semantics would force
those higher-level capabilities to invent their own answers for content
ownership, association, integrity and retrieval.

Treating `DocumentSource.source_reference` as an implicit file or
content locator would also risk collapsing accepted external
traceability semantics into storage semantics without an explicit
architecture decision.

The minimum dependency-completing next workstream is therefore:

**Canonical Enterprise Document Content Foundation Boundary**

This workstream shall establish the architecture contract needed before
raw Document transformation or Document Library behavior can be safely
promoted.

The selection does not yet decide the detailed content model,
persistence contract or storage technology.

### Objective

Review and define the minimum canonical foundation for Document content
associated with an existing canonical `EnterpriseDocument` while
preserving:

- canonical Enterprise Document identity;
- existing Document source-traceability semantics;
- accepted Document immutability;
- existing Document repository responsibility;
- existing Document Registration responsibility;
- RFC-065 ingestion responsibility;
- canonical Knowledge and lineage semantics;
- six-layer ARCH-001 architecture;
- CORE-002 and CORE-003 dependency rules;
- canonical DatabaseRuntime ownership;
- canonical metadata and Alembic authority;
- default Composition authority;
- Runtime and Bootstrap authority.

### Required Architecture Questions

The architecture contract for this selected workstream shall explicitly
resolve:

1. the canonical name and namespace for Document-content semantics;
2. whether canonical Document content is represented by a new Domain
   concept, a value object, or an explicitly reviewed extension of the
   accepted Document contract;
3. whether Document content has independent canonical identity or is
   identified only through an existing `EnterpriseDocument.id`;
4. whether any content cardinality relationship may be assumed;
5. whether raw binary payload belongs inside a Domain object or behind a
   persistence-neutral content boundary;
6. exact distinction between Document metadata and Document content;
7. exact distinction between external source traceability and canonical
   content location or retrieval semantics;
8. prohibition on silently repurposing
   `DocumentSource.source_reference`;
9. whether media/content type is canonical metadata and, if so, where it
   belongs;
10. whether character encoding belongs in the foundation and under what
    conditions;
11. whether byte length or equivalent size metadata belongs in the
    foundation;
12. whether a cryptographic digest is required for integrity evidence;
13. if a digest exists, whether it is integrity evidence only or whether
    identity/deduplication semantics require a separate future decision;
14. exact immutability semantics for canonical Document content;
15. compatibility with the currently deferred Document revision /
    supersession lifecycle;
16. whether Document existence must be established before content can be
    associated with it;
17. whether a persistence-neutral Document-content repository/store
    contract belongs in this same workstream or must follow as a
    separate foundation;
18. whether content retrieval semantics belong in this foundation or a
    later repository/storage boundary;
19. how a future parser shall consume canonical content without owning
    Document identity or storage semantics;
20. how future binary storage remains infrastructure-owned;
21. how future Document Library behavior remains distinct from the
    canonical content foundation;
22. how trust, approval, authorization and source authenticity remain
    separate from content existence or integrity;
23. whether any schema or Alembic change is actually required;
24. whether default Composition changes are required; none are assumed
    by this selection;
25. exact architecture tests needed to prevent dependency leakage and
    responsibility duplication;
26. exact TDD verification required before any technical implementation
    may be accepted.

### Existing Responsibilities That Shall Be Preserved

Selection of this workstream does not authorize silent redesign of:

- `EnterpriseDocument`;
- `DocumentSource`;
- `DocumentSourceType`;
- `DocumentType`;
- `EnterpriseDocumentRepository`;
- `EnterpriseDocumentRegistrationApplicationService`;
- `KnowledgeRecord`;
- `KnowledgeProvenance`;
- `KnowledgeSubject`;
- `KnowledgeCaptureApplicationService`;
- `DocumentKnowledgeLineage`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeLineageTransactionCoordinator`;
- canonical relational Document persistence;
- canonical relational Knowledge persistence;
- canonical lineage persistence;
- standalone repository lifecycle semantics;
- RFC-064 coordinated transaction semantics;
- canonical `DatabaseRuntime`;
- canonical SQLAlchemy metadata authority;
- canonical Alembic lifecycle;
- `ApplicationFacade`;
- default `CompositionRoot`;
- Runtime;
- Bootstrap;
- ARCH-001;
- CORE-002;
- CORE-003.

If the future content contract requires changing any accepted prior
contract, that change must be identified and reviewed explicitly rather
than being introduced indirectly.

### Explicit Non-Goals

This workstream selection does not authorize:

- production code;
- Document Library implementation;
- file upload;
- file download;
- file-server synchronization;
- binary-storage adapter implementation;
- filesystem storage implementation;
- object-storage implementation;
- parser implementation;
- PDF extraction;
- OCR;
- metadata extraction infrastructure;
- chunking;
- Document revision or supersession lifecycle;
- Document mutation or deletion;
- semantic search;
- search indexing;
- embeddings;
- vector persistence;
- graph persistence;
- Neo4j;
- Knowledge Graph redesign;
- RAG;
- LLM invocation;
- AI Agent behavior;
- HTTP transport;
- API endpoints;
- PI System integration;
- DCS integration;
- source authenticity or verification;
- Document approval or trust state;
- content deduplication policy;
- source-reference deduplication;
- default PostgreSQL Composition wiring;
- Runtime lifecycle expansion;
- Bootstrap responsibility expansion;
- authentication;
- authorization;
- RBAC;
- Active Directory integration;
- Cybersecurity approval;
- production-readiness claims.

### Completed Work

- post-RFC-065 Source-of-Truth closure verified;
- next-workstream evidence pack reviewed;
- dependency ordering reviewed;
- higher-level Parser/Search/Vector/RAG candidates rejected as premature;
- monolithic Document Library implementation rejected as premature;
- Canonical Enterprise Document Content Foundation Boundary selected.

### Selection Verification

Selection review: passed.

Selection commit:

`8c67a681ef1b13d83dc15955b177c3cf55f2944d`

Exact local / remote selection identity: verified.

Working tree after selection push: clean.

### Remaining Work

- perform the broad post-RFC-066 architecture and system evidence review;
- verify architecture boundaries, accepted contracts, implementation
  responsibilities, tests, persistence state and deferred capabilities
  remain coherent;
- identify any architecture debt, contradiction, stale Source-of-Truth
  state or required remediation before new work is selected;
- only after that review passes begin evidence-based selection of another
  architecture workstream.

### Dependencies

This selection depends on the accepted foundations established through
the Enterprise Document, Knowledge, lineage, transaction-coordination
and RFC-065 ingestion workstreams.

Those prerequisites are satisfied.

No parser, storage adapter, Document Library, search, vector, graph,
RAG, LLM or production-security capability is considered a prerequisite
for architecture review of this foundation.

### Resume Condition

Satisfied through verified post-closure Source-of-Truth reconciliation.

The evidence-based RFC-066 selection record was reviewed, committed and
pushed.

The RFC-066 / AD-052 contract was accepted, committed, pushed and
verified.

The implementation-entry Git gate was satisfied before TDD RED work.

RFC-066 technical implementation was completed, pushed and verified.

The Post-RFC-066 system and architecture integrity review passed.

Engineering-memory and architecture closure was reviewed, committed,
pushed and verified.

Closure commit:

`1ddc46c00680aac4718e6d3d76127857acbd4532`

Post-closure Source-of-Truth reconciliation was reviewed, committed,
pushed and verified.

Reconciliation commit:

`9dee653e32b8c22fabdf85a719985ed22a9e8459`

Exact local / remote reconciliation identity: verified.

Working tree after reconciliation push: clean.

RFC-066 is fully closed and Source-of-Truth reconciled.

### Next Exact Action

Perform a broad post-RFC-066 architecture and system evidence review
before selecting another architecture workstream.

The review SHALL examine the maintained Source-of-Truth, accepted
architecture contracts, current implementation, tests, dependency
boundaries, persistence state and explicitly deferred capabilities for
cross-system consistency and remaining architecture risk.

No next RFC has been selected or authorized.

Evidence-based selection of another architecture workstream may begin
only after that broad architecture/system review passes.

---

## RFC-066 — Canonical Enterprise Document Content Foundation Boundary

### Status

Fully Closed and Source-of-Truth Reconciled.

RFC-066 / AD-052 architecture-contract review:

**Passed — 52 / 52 Acceptance Requirements**

Combined RFC-066 / AD-052 semantic-consistency review:

**Passed — 52 PASS / 0 REFINE / 0 BLOCKED**

RFC-066 is Accepted.

AD-052 is Accepted.

Implementation-entry Git gate:

**SATISFIED before TDD RED implementation began**

Accepted contract commit:

`fb277fe00a9e606192c795338ab5419f4b9db788`

Technical implementation commit:

`49080b6c1f6f0607e6ba04ba2476f222dea97155`

Remote technical push: verified.

Exact local / remote technical identity: verified.

Working tree after technical push: clean.

Full PlantMind regression: **840 passed**.

Post-RFC-066 system and architecture integrity review:

**PASS — technical implementation conforms to accepted AD-052 and the
existing PlantMind architecture remains sound.**

Final execution verification:

- focused RFC-066 Domain and architecture verification: **65 passed**;
- full PlantMind regression: **840 passed**;
- Python compile verification: passed;
- canonical Alembic head: `0004`;
- `git diff --check`: passed;
- RFC-057 `backend/app/domain/document.py`: unchanged;
- default `CompositionRoot`: unchanged;
- no migration or schema change;
- technical implementation remained limited to the canonical Domain
  module and its tests.

Engineering-memory and architecture closure:

**COMPLETE AND VERIFIED**

Closure commit:

`1ddc46c00680aac4718e6d3d76127857acbd4532`

Closure push: verified.

Exact local / remote closure identity: verified.

Working tree after closure push: clean.

Post-closure Source-of-Truth reconciliation:

**COMPLETE AND VERIFIED**

Reconciliation commit:

`9dee653e32b8c22fabdf85a719985ed22a9e8459`

Reconciliation push: verified.

Exact local / remote reconciliation identity: verified.

Working tree after reconciliation push: clean.

RFC-066 is fully closed and Source-of-Truth reconciled.

### Context

RFC-057 / AD-043 established the canonical immutable
`EnterpriseDocument` with:

- canonical `EntityId`;
- `DocumentType`;
- title;
- `DocumentSource`.

RFC-058 through RFC-060 established:

- persistence-neutral Enterprise Document repository semantics;
- relational Enterprise Document persistence;
- Enterprise Document Registration application responsibility.

RFC-061 through RFC-065 subsequently established:

- canonical Document-to-Knowledge lineage;
- lineage persistence;
- coordinated Knowledge / lineage persistence;
- canonical Document-derived Knowledge ingestion.

The current canonical `EnterpriseDocument` intentionally does not contain:

- raw bytes;
- text payload;
- binary payload;
- storage location;
- content digest;
- media type;
- byte length;
- parser output;
- revision information.

The accepted `DocumentSource.source_reference` remains external
traceability only.

It is not canonical Document identity, storage identity, content
identity, repository alternate identity, uniqueness identity or
deduplication identity.

Current architecture therefore lacks a canonical definition of the
content associated with an Enterprise Document.

Parser, OCR, extraction, chunking, search, vector and RAG capabilities
must not invent their own content identity, payload or storage semantics.

### Objective

Define the minimum persistence-neutral Domain foundation that describes
the canonical content associated with an existing immutable
`EnterpriseDocument`.

RFC-066 shall establish:

- canonical content-description semantics;
- association with canonical Enterprise Document identity;
- media-type semantics;
- exact byte-length semantics;
- SHA-256 integrity-descriptor semantics;
- content immutability semantics;
- current content cardinality semantics;
- strict separation between Document source traceability and content
  storage/access semantics.

RFC-066 shall not implement content persistence, binary storage,
Document Library behavior, parsing or retrieval.

### Required Architecture Questions — Accepted Resolution

The selected workstream recorded 26 required architecture questions.

This draft resolves them as follows.

1. **Canonical name and namespace**

   The canonical Domain module shall be:

   `app.domain.document_content`

   It shall be implemented in:

   `backend/app/domain/document_content.py`

2. **Domain representation**

   RFC-066 shall introduce a new independent Domain concept rather than
   modifying the accepted RFC-057 `EnterpriseDocument` contract.

   The canonical content concept shall be represented by immutable value
   contracts in the new module.

3. **Content identity**

   Document content shall not receive an independent `EntityId`.

   Its canonical association identity shall be the existing:

   `EnterpriseDocument.id`

   RFC-066 shall not introduce `DocumentContentId`.

4. **Cardinality**

   Under the current immutable, revision-neutral Document architecture,
   one canonical Enterprise Document may have zero or one canonical
   content descriptor.

   Absence of content does not invalidate an already registered
   `EnterpriseDocument`.

   Multiple independent content artifacts, attachments or alternate
   renditions for one Document are not established by RFC-066.

5. **Raw binary payload**

   Raw bytes shall not be stored inside the RFC-066 Domain object.

   The Domain foundation shall describe content, not become an in-memory
   binary-storage container.

   Future byte/stream access shall require a separately accepted
   persistence-neutral content-access/store contract.

6. **Document metadata versus Document content**

   `EnterpriseDocument` shall continue to own:

   - Document identity;
   - Document type;
   - title;
   - external source traceability.

   RFC-066 content contracts shall own only canonical content-description
   semantics.

7. **Source traceability versus content location**

   `DocumentSource.source_reference` shall remain external traceability.

   It shall not become a filesystem path contract, URI contract,
   object-store key, binary-store key or canonical content locator.

8. **Source-reference preservation**

   RFC-066 shall not reinterpret, extend or overload
   `DocumentSource.source_reference`.

9. **Media type**

   Canonical content description shall include:

   `DocumentContentMediaType`

   representing a base media type such as:

   `application/pdf`

   or:

   `text/plain`

   The value shall be normalized by trimming and lowercasing.

   It shall contain one non-empty type and one non-empty subtype
   separated by `/`.

   RFC-066 shall not include media-type parameters such as charset.

10. **Character encoding**

    Character encoding shall not be part of the RFC-066 canonical
    content descriptor.

    Encoding detection, declaration or normalization belongs to a future
    parsing/extraction contract.

11. **Byte length**

    Canonical content description shall include:

    `byte_length: int`

    representing the exact number of bytes in the canonical raw payload.

    Boolean values and non-integers shall be rejected.

    Zero shall be valid.

    Negative values shall be rejected.

12. **Cryptographic digest**

    Canonical content description shall require an immutable SHA-256
    digest.

13. **Digest semantics**

    The digest shall provide content-integrity description only.

    It shall not become:

    - Document identity;
    - content identity;
    - repository identity;
    - uniqueness identity;
    - idempotency identity;
    - deduplication identity.

14. **Immutability**

    RFC-066 content value contracts shall be immutable.

    RFC-066 shall introduce no content update, replace or mutation
    operation.

15. **Revision compatibility**

    RFC-066 shall remain revision-neutral.

    It shall not establish Document revision, supersession or replacement
    semantics.

    Any future revision model that requires multiple content states for
    one Document identity shall require explicit review of RFC-066
    cardinality and immutability assumptions.

16. **Enterprise Document existence**

    Canonical persisted association of content with a Document shall
    require an existing `EnterpriseDocument.id`.

    RFC-066 Domain construction itself shall not perform repository
    lookup or cross-aggregate existence validation.

    Future content-registration/persistence application architecture
    shall own that existence check.

17. **Repository/store responsibility**

    A persistence-neutral content repository or content store shall not
    be introduced by RFC-066.

    It shall be the subject of a later explicit architecture workstream.

18. **Content retrieval**

    Retrieval, streaming and byte-reading operations shall not be defined
    by RFC-066.

    They belong to the future content-access/store contract.

19. **Future parser consumption**

    A future parser shall consume bytes only through an accepted
    content-access/store boundary.

    It shall not:

    - open `DocumentSource.source_reference`;
    - perform alternate Document identity lookup;
    - own binary-storage semantics;
    - redefine canonical content metadata.

20. **Binary storage**

    Future binary persistence shall remain Infrastructure responsibility
    behind a persistence-neutral contract.

    RFC-066 shall not select filesystem, database BLOB, object storage,
    network file server or another storage technology.

21. **Document Library**

    Document Library is a broader application capability and remains
    separate from this Domain foundation.

22. **Trust, approval and authorization**

    Content existence, media type, byte length or SHA-256 digest shall
    not imply:

    - source authenticity;
    - Document approval;
    - content correctness;
    - authorization;
    - trust;
    - compliance approval;
    - Cybersecurity approval.

23. **Schema / Alembic**

    RFC-066 requires no relational schema change.

    Canonical Alembic head shall remain:

    `0004`

24. **Composition**

    RFC-066 shall not modify default:

    - `CompositionRoot`;
    - `ServiceContainer`;
    - `PlatformComposition`;
    - Runtime;
    - Bootstrap.

25. **Architecture tests**

    RFC-066 implementation shall include architecture guardrails proving
    that:

    - the new Domain module is persistence-neutral;
    - accepted `app.domain.document` public classes remain unchanged;
    - no repository contract exists in the Domain module;
    - no file I/O exists in the Domain module;
    - no Infrastructure, service, SQLAlchemy, FastAPI or Pydantic
      dependency enters the Domain module;
    - no raw byte payload field enters the canonical descriptor;
    - no content identity generator is introduced;
    - no default Composition wiring is introduced.

26. **TDD verification**

    Technical implementation, if later authorized, shall begin with RED
    tests for the accepted Domain contract and architecture guardrails.

    GREEN implementation may begin only after the accepted contract is
    committed, pushed, exact local / remote contract identity is verified
    and the working tree is clean.

### Existing Responsibilities That SHALL Be Preserved

RFC-066 shall not silently redesign:

- `EntityId`;
- `DomainEntity`;
- `EnterpriseDocument`;
- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocumentRepository`;
- `EnterpriseDocumentRegistrationApplicationService`;
- canonical Enterprise Document relational persistence;
- `KnowledgeRecord`;
- `KnowledgeProvenance`;
- `KnowledgeSubject`;
- `KnowledgeCaptureApplicationService`;
- `DocumentKnowledgeLineage`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeLineageTransactionCoordinator`;
- canonical Knowledge persistence;
- canonical lineage persistence;
- `DatabaseRuntime`;
- canonical SQLAlchemy metadata authority;
- canonical Alembic lifecycle;
- `ApplicationFacade`;
- default `CompositionRoot`;
- Runtime;
- Bootstrap;
- ARCH-001;
- CORE-002;
- CORE-003.

The existing file:

`backend/app/domain/document.py`

shall not be modified by RFC-066 implementation.

The existing RFC-057 architecture rule that the canonical Document
module contains exactly:

- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`

shall remain intact.

### Accepted Architecture Contract

RFC-066 proposes one new persistence-neutral Domain module:

`app.domain.document_content`

implemented at:

`backend/app/domain/document_content.py`

The proposed canonical public Domain surface is exactly:

- `DocumentContentMediaType`;
- `DocumentContentDigest`;
- `DocumentContentDescriptor`.

This draft is not yet accepted.

### Canonical DocumentContentMediaType Contract

`DocumentContentMediaType` shall be an immutable, keyword-only value
object containing exactly:

`value: str`

Construction shall:

1. require a string;
2. trim surrounding whitespace;
3. lowercase the value;
4. reject an empty value;
5. reject media-type parameters containing `;`;
6. require exactly one `/`;
7. require a non-empty type component;
8. require a non-empty subtype component;
9. reject ASCII whitespace inside the normalized media type.

Examples of valid canonical values include:

- `application/pdf`;
- `text/plain`;
- `image/png`;
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.

RFC-066 does not attempt full IANA media-type registry validation.

Unknown but structurally valid media types may remain representable.

### Canonical DocumentContentDigest Contract

`DocumentContentDigest` shall be an immutable, keyword-only value object
containing exactly:

`value: str`

Its algorithm is fixed by RFC-066 to:

`SHA-256`

Construction shall:

1. require a string;
2. trim surrounding whitespace;
3. lowercase the value;
4. require exactly 64 hexadecimal characters;
5. reject all non-hexadecimal values.

The digest shall represent SHA-256 calculated over the exact canonical
raw byte sequence associated with the Document.

No text normalization, parsing, OCR, decompression or semantic
transformation shall alter the byte sequence used for this digest.

Successful construction of `DocumentContentDigest` validates only digest
format.

It does not by itself prove that:

- payload bytes exist;
- payload bytes were persisted;
- the digest was computed correctly;
- a future store has verified the digest against stored bytes.

Payload verification belongs to a future accepted content
persistence/access contract.

### Canonical DocumentContentDescriptor Contract

`DocumentContentDescriptor` shall be an immutable, keyword-only Domain
value object containing exactly:

- `document_id: EntityId`;
- `media_type: DocumentContentMediaType`;
- `byte_length: int`;
- `digest: DocumentContentDigest`.

Construction shall require canonical instances of:

- `EntityId`;
- `DocumentContentMediaType`;
- `DocumentContentDigest`.

`byte_length` shall:

- require an integer;
- explicitly reject `bool`;
- allow zero;
- reject negative values.

`DocumentContentDescriptor` shall not inherit from `DomainEntity`.

It shall not generate an identity.

It shall not contain:

- `content_id`;
- raw `bytes`;
- `bytearray`;
- memory buffer;
- stream;
- file handle;
- filesystem path;
- URI;
- object-store key;
- source reference;
- title;
- Document type;
- character encoding;
- extracted text;
- parser result;
- revision;
- timestamps;
- actor;
- approval state;
- trust state.

### Canonical Identity and Association Boundary

Canonical Enterprise Document identity remains:

`EnterpriseDocument.id`

RFC-066 shall not introduce another identity representing the same
Document-content association.

`DocumentContentDescriptor.document_id` shall reference canonical
Enterprise Document identity.

The digest shall not become identity.

Media type shall not become identity.

Byte length shall not become identity.

Source reference shall not become identity.

Under the current contract, semantic cardinality is:

`EnterpriseDocument.id -> zero-or-one DocumentContentDescriptor`

This is a Domain architecture statement.

RFC-066 does not itself introduce persistence capable of enforcing that
cardinality.

Future repository/store architecture shall explicitly preserve or
review this rule.

### EnterpriseDocument Preservation Boundary

RFC-066 shall not add content fields to `EnterpriseDocument`.

It shall not modify:

- `EnterpriseDocument.__init__` semantics;
- existing Document identity;
- existing Document validation;
- existing Document source semantics;
- existing Document persistence mapping;
- existing Document relational schema.

An Enterprise Document may continue to exist without registered
canonical content.

Document registration shall remain independent from content
registration/persistence.

### Source Reference Boundary

`DocumentSource.source_reference` remains an opaque external traceability
value.

RFC-066 shall not define it as:

- local path;
- mounted path;
- network path;
- file URI;
- HTTP URI;
- storage locator;
- storage key;
- content key;
- content identity;
- digest;
- deduplication key.

Future acquisition architecture may use source-specific adapters to
interpret an external reference, but such interpretation shall not
change the canonical meaning of `DocumentSource.source_reference`.

### Payload Boundary

RFC-066 Domain contracts shall contain no raw payload bytes.

This prevents the Domain foundation from becoming:

- a binary transport API;
- a storage adapter;
- a memory-loading policy;
- a streaming framework;
- a parser input implementation.

Future content access must define separately:

- how bytes are written;
- how bytes are read;
- whether streaming is mandatory;
- size limits;
- resource lifecycle;
- integrity verification;
- storage failure semantics;
- missing-content semantics.

### Document Existence Boundary

RFC-066 shall not import or depend on:

`EnterpriseDocumentRepository`

inside `app.domain.document_content`.

Domain construction shall not perform I/O.

A future application boundary that establishes persisted content shall
verify canonical Enterprise Document existence before treating the
content association as successfully established.

No orphan-content persistence semantics are authorized by RFC-066.

### Repository and Store Boundary

RFC-066 introduces no:

- `DocumentContentRepository`;
- `DocumentContentStore`;
- persistence adapter;
- filesystem adapter;
- object-store adapter;
- database BLOB adapter;
- session lifecycle;
- transaction coordinator.

The exact persistence-neutral content-access contract shall be selected
and reviewed separately after RFC-066 is closed.

### Transaction and Atomicity Boundary

RFC-066 introduces no new transaction.

It shall not change RFC-060 Document Registration transaction semantics.

It shall not change RFC-064 Knowledge / lineage transaction semantics.

It shall not change RFC-065 Document-to-Knowledge ingestion transaction
assumptions.

Atomicity between:

- Enterprise Document registration;
- content descriptor persistence;
- binary payload persistence

is not decided by RFC-066.

That question belongs to the future content persistence/application
architecture.

### Revision and Mutation Boundary

RFC-066 introduces no:

- update;
- replace;
- delete;
- revision number;
- revision identity;
- supersession relationship;
- current/latest pointer;
- mutable content state.

The descriptor is immutable.

The current zero-or-one content association assumes the accepted
revision-neutral Enterprise Document model.

If future architecture introduces revisions, RFC-066 SHALL be explicitly
reviewed before multiple content states are attached to one canonical
Document identity.

### Parsing and Extraction Boundary

RFC-066 shall not implement:

- parser;
- PDF parser;
- OCR;
- DOCX extraction;
- spreadsheet extraction;
- text extraction;
- metadata extraction;
- chunking;
- character-encoding detection;
- content normalization.

Future parsing shall operate only after a content-access contract exists.

A parser shall not call:

`open(document.source.source_reference)`

or equivalent logic that converts source traceability into canonical
content access.

### Document Library Boundary

RFC-066 is not the Document Library.

It shall not establish:

- upload;
- download;
- browse;
- folder hierarchy;
- source synchronization;
- user file management;
- content registration workflow;
- permissions;
- approval workflow;
- retention policy;
- revision history.

Those capabilities require separate contracts.

### Search, Vector, Graph and AI Boundary

RFC-066 shall not establish:

- keyword search;
- full-text indexing;
- semantic search;
- embeddings;
- vector persistence;
- Qdrant integration;
- graph persistence;
- Neo4j integration;
- RAG;
- LLM invocation;
- AI Agent behavior;
- engineering reasoning.

A canonical content descriptor does not imply that content is parsed,
indexed, searchable or available to AI.

### Security and Trust Boundary

RFC-066 shall not establish:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- LDAP;
- MFA;
- actor identity;
- actor audit;
- Document permissions;
- source verification;
- malware scanning;
- content approval;
- Document approval;
- trust classification;
- compliance approval;
- Cybersecurity approval;
- production-security readiness.

The SHA-256 digest is an integrity descriptor.

It does not establish trust.

### DatabaseRuntime, Schema and Alembic Boundary

RFC-066 shall not create or own:

- database engine;
- SQLAlchemy session;
- session factory;
- `DATABASE_URL`;
- metadata root;
- migration lifecycle.

RFC-066 requires:

- no new table;
- no new column;
- no new index;
- no new constraint;
- no foreign key;
- no new Alembic revision.

Canonical Alembic head remains:

`0004`

If implementation review discovers a genuine persistence requirement,
implementation shall stop and the contract shall be reviewed before any
schema work is authorized.

### Composition, Runtime and Bootstrap Boundary

RFC-066 shall not modify default:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`.

RFC-066 shall not modify:

- Runtime lifecycle;
- Bootstrap;
- readiness semantics;
- health semantics;
- request admission;
- mandatory capability policy.

Existence of Domain content contracts does not make content persistence
a mandatory runtime capability.

### Architectural Layer and Dependency Boundary

RFC-066 introduces no new ARCH-001 layer.

The new module is a Domain contract within the accepted architecture.

It shall depend only on:

- Python standard library;
- accepted shared Domain primitives from `app.domain.base`.

It shall not depend on:

- `app.domain.document`;
- `app.document.repository`;
- `app.services`;
- `app.infrastructure`;
- SQLAlchemy;
- FastAPI;
- Pydantic;
- filesystem APIs;
- network clients.

The descriptor references an `EntityId`, not an
`EnterpriseDocument` object.

This preserves Domain separation and avoids circular aggregate
dependency.

### Core Boundary

RFC-066 does not create a Core Service.

Core Services shall not gain Document-content responsibility through
this RFC.

CORE-002 remains authoritative.

### Explicitly Deferred

RFC-066 shall not establish:

- independent Document Content identity;
- content repository;
- content store;
- binary persistence;
- filesystem persistence;
- object storage;
- database BLOB persistence;
- upload;
- download;
- acquisition;
- source synchronization;
- content retrieval API;
- streaming API;
- parser;
- OCR;
- extraction;
- chunking;
- character encoding;
- revision;
- supersession;
- mutation;
- deletion;
- attachments;
- alternate renditions;
- multi-artifact Document semantics;
- digest-based deduplication;
- source-reference deduplication;
- idempotency;
- content registration application service;
- cross-store transaction coordination;
- distributed transaction;
- outbox;
- retry policy;
- search;
- embeddings;
- vector persistence;
- graph persistence;
- Neo4j;
- RAG;
- LLM;
- AI Agent behavior;
- HTTP/API;
- PI System integration;
- DCS integration;
- authentication;
- authorization;
- RBAC;
- Active Directory;
- trust;
- approval;
- malware scanning;
- retention;
- production composition;
- Cybersecurity approval;
- production-readiness claims.

### Acceptance Requirements

Before RFC-066 / AD-052 may become Accepted, architecture review SHALL
confirm:

1. RFC-066 introduces no new ARCH-001 layer;
2. RFC-057 `EnterpriseDocument` remains unchanged;
3. `backend/app/domain/document.py` remains unchanged;
4. the RFC-057 exact Document-class surface remains unchanged;
5. the new canonical module is `app.domain.document_content`;
6. the proposed public surface contains exactly
   `DocumentContentMediaType`, `DocumentContentDigest` and
   `DocumentContentDescriptor`;
7. all three contracts are immutable;
8. no `DocumentContentId` is introduced;
9. `DocumentContentDescriptor` does not inherit from `DomainEntity`;
10. canonical association uses existing `EnterpriseDocument.id`;
11. the descriptor contains exactly document identity, media type, byte
    length and SHA-256 digest;
12. raw bytes do not enter the Domain descriptor;
13. paths, URIs, handles and storage keys do not enter the Domain
    descriptor;
14. `DocumentSource.source_reference` remains external traceability only;
15. source reference is not used as content identity or locator;
16. media type is normalized and structurally validated;
17. media-type parameters and charset remain outside RFC-066;
18. byte length rejects bool, non-integer and negative values;
19. zero byte length remains valid;
20. digest is fixed to SHA-256;
21. SHA-256 digest is normalized to lowercase 64-character hexadecimal;
22. digest is integrity description only;
23. digest does not establish identity, uniqueness, idempotency or
    deduplication;
24. digest construction does not falsely claim payload verification;
25. current cardinality is zero-or-one content descriptor per canonical
    Document identity;
26. RFC-066 introduces no persistence mechanism to enforce cardinality;
27. Domain construction performs no Document repository lookup;
28. future persisted association must require existing canonical Document
    identity;
29. no content repository/store contract is introduced;
30. no content retrieval/streaming contract is introduced;
31. no binary-storage technology is selected;
32. no content registration application service is introduced;
33. no transaction or atomicity expansion is introduced;
34. RFC-060, RFC-064 and RFC-065 transaction responsibilities remain
    unchanged;
35. revision, supersession, mutation and deletion remain deferred;
36. parser/OCR/extraction/chunking remain deferred;
37. future parser access cannot reinterpret `source_reference` as storage;
38. Document Library remains separately deferred;
39. search/vector/graph/RAG/LLM remain separately deferred;
40. trust, approval and authorization remain outside content semantics;
41. no schema or Alembic change is introduced;
42. canonical Alembic head remains `0004`;
43. default Composition remains unchanged;
44. Runtime and Bootstrap remain unchanged;
45. the new Domain module performs no file I/O;
46. the new Domain module introduces no repository contract;
47. the new Domain module has no Infrastructure or application-service
    dependency;
48. the new Domain module has no SQLAlchemy, FastAPI or Pydantic
    dependency;
49. dependency direction remains explicit and acyclic;
50. implementation architecture tests preserve the accepted RFC-057
    Document module contract;
51. implementation begins with RED tests only after the accepted contract
    Git gate is satisfied;
52. no production-readiness or Cybersecurity claim is introduced.

### Contract Acceptance Gate

Status:

**Passed — RFC-066 / AD-052 Accepted**

Formal architecture-contract review:

- Gate 1 — Domain Identity & RFC-057 Preservation: PASS;
- Gate 2 — Content Semantics & Integrity: PASS;
- Gate 3 — Repository / Storage / Transaction / Parser Boundaries: PASS;
- Gate 4 — Layering / Dependency / Security / Prior-Contract Preservation: PASS;
- Final Static Contract Review: PASS;
- Semantic Contradiction Scan: PASS;
- Acceptance Requirements: 52 PASS / 0 REFINE / 0 BLOCKED.

Combined RFC-066 / AD-052 semantic-consistency review:

**PASS**

The 52 Acceptance Requirements in RFC-066 and AD-052 are
byte-for-byte equivalent.

The combined review confirmed preservation of:

- canonical Enterprise Document identity;
- RFC-057 Document Domain contract;
- zero-or-one Document-content cardinality;
- SHA-256 integrity-only semantics;
- source-reference traceability semantics;
- repository/store/persistence boundaries;
- transaction and atomicity boundaries;
- revision neutrality;
- parser, Document Library, search, vector, graph and AI deferrals;
- security and trust separation;
- DatabaseRuntime and Alembic authority;
- default Composition;
- Runtime and Bootstrap;
- ARCH-001;
- CORE-002;
- CORE-003;
- all accepted prior architecture responsibilities.

RFC-066 is Accepted.

AD-052 is Accepted.

The accepted-contract Git gate was subsequently satisfied before
RFC-066 TDD RED implementation began.

### Implementation Authorization

Status:

**Satisfied — Technical implementation completed and verified.**

Accepted architecture contract commit:

`fb277fe00a9e606192c795338ab5419f4b9db788`

Verified technical implementation commit:

`49080b6c1f6f0607e6ba04ba2476f222dea97155`

The implementation-entry Git gate was satisfied before RFC-066 TDD RED
implementation began.

Technical verification evidence:

- canonical Domain module:
  `backend/app/domain/document_content.py`;
- canonical public surface remains exactly
  `DocumentContentMediaType`, `DocumentContentDigest` and
  `DocumentContentDescriptor`;
- focused RFC-066 Domain and architecture verification: **65 passed**;
- full PlantMind regression: **840 passed**;
- `git diff --check`: passed;
- RFC-057 `backend/app/domain/document.py` remained byte-for-byte
  unchanged during implementation;
- no schema or migration file was introduced;
- no persistence, repository, content-store or file-I/O responsibility
  was introduced;
- default Composition, Runtime and Bootstrap were not modified;
- remote technical push: verified;
- exact local / remote technical identity: verified;
- working tree after technical push: clean.

RFC-066 technical implementation is accepted as implemented within the
AD-052 boundary.

Engineering-memory and architecture closure is complete and verified.

Closure commit:

`1ddc46c00680aac4718e6d3d76127857acbd4532`

Closure push and exact local / remote identity were verified, and the
working tree after closure push was clean.

Post-closure Source-of-Truth reconciliation commit:

`9dee653e32b8c22fabdf85a719985ed22a9e8459`

Reconciliation push and exact local / remote identity were verified.

Working tree after reconciliation push was clean.

RFC-066 is fully closed and Source-of-Truth reconciled.

### Next Exact Action

Perform the broad post-RFC-066 architecture and system evidence review.

The review SHALL determine whether the current repository, accepted
architecture contracts, engineering-memory documents, tests,
dependencies, persistence boundaries and deferred work remain coherent
before another architecture workstream is selected.

No next RFC has been selected or authorized.

Only after the broad architecture/system review passes may PlantMind
begin evidence-based selection of the next architecture workstream.

---

## RFC-065 — Canonical Document-to-Knowledge Ingestion Application Boundary

### Status

Complete.

RFC-065 / AD-051 Contract Acceptance Review: passed.

Implementation-entry Git gate: satisfied.

Technical implementation: complete and verified.

Engineering-memory and architecture closure: complete.

Post-closure Source-of-Truth reconciliation: complete and verified.

Post-RFC-064 evidence-based architecture selection: complete.

Selection baseline:

`56ff5f7a54ea9d5105ae7a9d9cedd86597ef8fdf`

Architecture decision:

`AD-051 — Canonical Document-to-Knowledge Ingestion Application Boundary`

AD-051 status:

Accepted.

### Selection Evidence

The post-RFC-064 architecture and dependency review confirmed:

- RFC-064 is fully closed;
- RFC-064 engineering-memory closure and post-closure reconciliation are complete;
- exact local / remote repository identity is verified at `56ff5f7a54ea9d5105ae7a9d9cedd86597ef8fdf`;
- working tree is clean;
- RFC-064 targeted verification: 37 passed;
- full PlantMind regression: 754 passed;
- Python compileall: passed;
- canonical Alembic head remains `0004`;
- canonical Enterprise Document identity, repository, relational persistence and Registration application boundary are implemented;
- canonical Knowledge identity, repository, relational persistence and `KnowledgeCaptureApplicationService` are implemented;
- canonical `DocumentKnowledgeLineage` identity semantics are implemented;
- canonical lineage repository and relational persistence are implemented;
- RFC-064 established the accepted persistence-neutral `KnowledgeLineageTransactionCoordinator`;
- RFC-064 established one coordinated transaction scope for Knowledge persistence and lineage persistence;
- transaction-scoped Knowledge and lineage repositories share one SQLAlchemy session;
- coordinated participant writes flush without independently committing, rolling back or closing;
- final commit, rollback and session-close authority belong to the coordinator;
- standalone Knowledge and lineage relational repository behavior remains preserved;
- canonical `DatabaseRuntime` remains engine and session-factory lifecycle owner;
- default `CompositionRoot`, Runtime and Bootstrap authority remain unchanged;
- no new relational schema was required by RFC-064;
- accepted architecture explicitly deferred Document-to-Knowledge ingestion until canonical lineage and coordinated Knowledge / lineage persistence semantics existed;
- those prerequisite foundations now exist;
- no additional lower-level foundation has been identified that must precede architecture review of the ingestion application boundary.

Project-level evidence also confirms that PlantMind Phase 1 requires an AI Knowledge Engine and Document capability, and its success criteria include automatic linking of documents to enterprise knowledge.

### Selection Rationale

Earlier Document Knowledge ingestion proposals were correctly deferred because the platform did not yet possess all required canonical foundations.

Before RFC-061, propagating only external Document source metadata into Knowledge would have lost canonical `EnterpriseDocument.id` and reduced ingestion to a thin translation wrapper over Knowledge Capture.

RFC-061 through RFC-063 established:

1. canonical Document-to-Knowledge lineage identity;
2. persistence-neutral lineage repository semantics;
3. relational lineage persistence.

Ingestion still could not safely proceed because Knowledge persistence and lineage persistence independently owned transaction lifecycles.

RFC-064 then established the missing narrow Knowledge-and-lineage transaction-coordination foundation.

The architecture now has the minimum prerequisite chain required to review a specialized application use case that:

1. begins from an existing canonical Enterprise Document identity;
2. creates one canonical `KnowledgeRecord` through accepted Knowledge Capture semantics;
3. creates the corresponding canonical `DocumentKnowledgeLineage`;
4. persists Knowledge and lineage atomically through the accepted RFC-064 coordination boundary;
5. preserves Document identity independently from external source-reference provenance.

The minimum dependency-completing next architecture workstream is therefore a specialized Document-to-Knowledge ingestion application boundary.

This selection does not yet decide the detailed ingestion contract.

### Objective

Define the minimum canonical application boundary for creating Knowledge derived from an existing canonical Enterprise Document while preserving:

- canonical Document identity;
- canonical Knowledge identity;
- accepted Knowledge Capture responsibility;
- canonical Document-to-Knowledge lineage;
- accepted Knowledge provenance semantics;
- accepted Knowledge subject semantics;
- coordinated atomic persistence of Knowledge and lineage;
- current Domain, repository, database, Runtime, Bootstrap and Composition boundaries.

The capability SHALL remain specialized to Document-derived Knowledge ingestion.

It SHALL NOT become a generic workflow framework, generic Unit of Work, Document Library, parser, search engine or AI orchestration subsystem.

### Required Architecture Questions

RFC-065 / AD-051 contract review SHALL explicitly resolve:

1. the canonical application-service name and namespace;
2. the canonical ingestion operation name;
3. immutable request shape;
4. canonical result shape;
5. whether caller input SHALL provide only canonical `document_id` or another accepted Document reference form;
6. whether the ingestion boundary SHALL depend directly on `EnterpriseDocumentRepository`;
7. whether canonical Document existence SHALL be verified before Knowledge capture begins;
8. exact not-found semantics if the canonical Document identity does not exist;
9. whether Document lookup SHALL occur before entering the RFC-064 coordinated transaction;
10. whether accepted Document immutability and absence of delete semantics are sufficient to keep Document lookup outside the Knowledge-and-lineage transaction;
11. prevention of `DocumentSource.source_reference` becoming canonical Document identity;
12. prevention of canonical Document identity being hidden inside `KnowledgeProvenance.source_reference`;
13. how Knowledge provenance `source_type` and `source_reference` SHALL relate to the canonical `EnterpriseDocument.source`;
14. whether provenance source metadata SHALL be derived from the loaded canonical Document rather than duplicated from caller input;
15. preservation of `KnowledgeSubject` as an independent primary contextual reference rather than automatically replacing it with Document identity;
16. exact Knowledge fields that ingestion caller input may provide, including kind, title, content and optional subject;
17. reuse of `KnowledgeCaptureApplicationService` without changing its accepted public behavior or responsibility;
18. construction or injection strategy required to use `KnowledgeCaptureApplicationService` with the transaction-scoped `KnowledgeRecordRepository`;
19. preservation of canonical Knowledge identity and capture-time generation semantics;
20. exact use of `KnowledgeLineageTransactionCoordinator.execute(...)`;
21. creation of exactly one canonical `DocumentKnowledgeLineage` from the existing Document identity and newly created Knowledge identity;
22. lineage repository `add(...)` invocation semantics inside the coordinated transaction;
23. ordering between Knowledge capture and lineage persistence inside one coordinated operation;
24. success semantics: no ingestion success result before the coordinated transaction commits;
25. failure semantics when Knowledge capture fails;
26. failure semantics when lineage persistence fails after Knowledge has flushed;
27. propagation of canonical duplicate errors without retry or synthetic success;
28. propagation of unrelated persistence failures;
29. treatment of `KnowledgeLineageTransactionPostCommitCleanupError`;
30. preservation of the RFC-064 rule that transaction atomicity covers participating relational writes but does not imply broader application or external-system atomicity;
31. prohibition on silently extending the coordinator to Enterprise Document registration;
32. prohibition on a transaction spanning Document registration, Knowledge capture and lineage persistence unless separately accepted architecture later requires it;
33. preservation of standalone Knowledge, Document and lineage repository behavior outside this ingestion use case;
34. whether RFC-065 requires any schema change; current evidence indicates that no schema or Alembic revision should be assumed;
35. whether default Composition wiring is required; current selection does not authorize it;
36. preservation of Runtime and Bootstrap authority;
37. prevention of parser, OCR, Library, search, vector, graph, RAG or LLM responsibilities entering this application boundary;
38. prevention of source authenticity, approval, trust or authorization semantics being inferred merely from successful ingestion;
39. exact architecture tests required to prevent dependency leakage or competing application responsibilities;
40. exact TDD verification required before technical implementation may be accepted.

### Existing Responsibilities That SHALL Be Preserved

The selection assumes no redesign of:

- `EnterpriseDocument`;
- `DocumentSource`;
- `DocumentSourceType`;
- `DocumentType`;
- `KnowledgeRecord`;
- `KnowledgeProvenance`;
- `KnowledgeSubject`;
- `DocumentKnowledgeLineage`;
- `EnterpriseDocumentRepository`;
- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`;
- `EnterpriseDocumentRegistrationApplicationService`;
- `KnowledgeCaptureApplicationService`;
- `KnowledgeLineageTransactionCoordinator`;
- standalone relational Document repository behavior;
- standalone relational Knowledge repository behavior;
- standalone relational lineage repository behavior;
- RFC-064 transaction-scoped Knowledge repository behavior;
- RFC-064 transaction-scoped lineage repository behavior;
- canonical Document identity semantics;
- Document source traceability semantics;
- canonical Knowledge provenance semantics;
- canonical Knowledge subject semantics;
- directed Document-to-Knowledge lineage identity;
- exact duplicate semantics;
- canonical `DatabaseRuntime` engine and session-factory ownership;
- canonical SQLAlchemy metadata authority;
- canonical Alembic schema lifecycle;
- default Composition authority;
- Runtime lifecycle authority;
- Bootstrap authority;
- six-layer ARCH-001 architecture.

### Explicit Non-Goals

RFC-065 selection does NOT authorize:

- Document registration redesign;
- creation of a Document during ingestion;
- a transaction spanning Document registration, Knowledge capture and lineage persistence;
- Document Library behavior;
- binary document storage;
- file upload;
- file-server synchronization;
- parsing;
- PDF parsing;
- OCR;
- chunking;
- text extraction infrastructure;
- metadata extraction infrastructure;
- Document revision or supersession lifecycle;
- source reconciliation;
- source-reference uniqueness;
- source-reference deduplication identity;
- source authenticity;
- Document approval or trust state;
- semantic search;
- search indexing;
- vector persistence;
- embeddings;
- graph persistence;
- Neo4j;
- Knowledge Graph redesign;
- RAG;
- LLM invocation;
- AI Agent behavior;
- HTTP transport;
- API endpoint creation;
- industrial integration;
- PI System integration;
- DCS integration;
- one-sided lineage retrieval;
- reverse lineage traversal;
- lineage business cardinality policy;
- corroboration semantics;
- primary-source semantics;
- multi-source derivation semantics;
- generic platform-wide Unit of Work;
- unrelated cross-subsystem transactions;
- nested coordinated transactions;
- savepoints;
- distributed transactions;
- two-phase commit;
- transactional event publication;
- outbox semantics;
- asynchronous coordination;
- automatic retry policy;
- idempotency policy;
- default PostgreSQL Composition wiring;
- mandatory database Runtime capability;
- authentication expansion;
- authorization expansion;
- RBAC;
- Active Directory integration;
- actor audit;
- Cybersecurity approval;
- production-security readiness;
- production-readiness claims;
- a new architectural layer;
- a new relational schema or Alembic revision as an assumed requirement.

### Dependency Baseline

RFC-065 contract drafting SHALL be reviewed against, at minimum:

- ARCH-001;
- CORE-002;
- CORE-003;
- AD-027 application-boundary semantics;
- RFC-053 / AD-039 — canonical Knowledge foundation;
- RFC-054 / AD-040 — canonical database runtime and schema lifecycle;
- RFC-055 / AD-041 — Knowledge relational persistence;
- RFC-056 / AD-042 — Knowledge Capture application boundary;
- RFC-057 / AD-043 — canonical Enterprise Document foundation;
- RFC-058 / AD-044 — Enterprise Document repository;
- RFC-059 / AD-045 — Enterprise Document relational persistence;
- RFC-060 / AD-046 — Enterprise Document Registration application boundary;
- RFC-061 / AD-047 — canonical Document-to-Knowledge lineage;
- RFC-062 / AD-048 — lineage repository;
- RFC-063 / AD-049 — lineage relational persistence;
- RFC-064 / AD-050 — Knowledge-and-lineage transaction coordination;
- current `EnterpriseDocumentRepository`;
- current `KnowledgeCaptureApplicationService`;
- current `KnowledgeLineageTransactionCoordinator`;
- current canonical relational mappings and metadata authority;
- current default Composition;
- current Runtime and Bootstrap authority;
- PM-001 Phase 1 foundation objectives and success criteria.

### Draft Architecture Contract

The RFC-065 / AD-051 draft establishes one specialized internal
application use case:

`DocumentKnowledgeIngestionApplicationService`

under:

`app.services.document_knowledge_ingestion_application_service`

The canonical operation is proposed as:

`ingest(request: DocumentKnowledgeIngestionRequest) -> DocumentKnowledgeIngestionResult`

This draft is not yet accepted.

### Canonical Public Application Surface

The proposed module shall expose:

- `DocumentKnowledgeIngestionRequest`;
- `DocumentKnowledgeIngestionResult`;
- `DocumentKnowledgeIngestionDocumentNotFoundError`;
- `DocumentKnowledgeIngestionApplicationService`.

The service shall remain a specialized application use-case boundary.

It shall not become:

- a new ARCH-001 architectural layer;
- an external application entry point;
- an AI Agent;
- an Intelligence Engine;
- a Core Service;
- a generic orchestration framework;
- a generic Unit of Work;
- a Document Library;
- a parser or extraction engine.

### Construction and Dependency Contract

`DocumentKnowledgeIngestionApplicationService` shall receive exactly
these application-level constructor dependencies:

- `document_repository: EnterpriseDocumentRepository`;
- `transaction_coordinator: KnowledgeLineageTransactionCoordinator`;
- optional `knowledge_capture_factory`.

The optional factory contract shall be equivalent to:

`Callable[[KnowledgeRecordRepository], KnowledgeCaptureApplicationService]`

When no factory is supplied, the ingestion service shall use a local
default factory that constructs:

`KnowledgeCaptureApplicationService(repository=scoped_knowledge_repository)`

without overriding the identity-source or capture-time defaults already
accepted for Knowledge Capture.

For each ingestion invocation that resolves an existing canonical
Document, exactly one Knowledge Capture service shall be constructed
inside the RFC-064 coordinated operation after the transaction-scoped
repositories have been supplied.

The factory shall receive the exact transaction-scoped
`KnowledgeRecordRepository` supplied by RFC-064.

The ingestion-service constructor shall not accept a preconstructed
`KnowledgeCaptureApplicationService`.

A preconstructed Capture service would bind its repository before the
RFC-064 transaction scope exists and could therefore bypass the required
atomic Knowledge / lineage persistence boundary.

The optional factory exists solely as a narrow deterministic
verification seam.

It shall not:

- perform persistence;
- own transaction lifecycle;
- perform external I/O;
- resolve dependencies globally;
- register services;
- become a provider registry;
- become a Core Service;
- become a dependency-injection framework.

### Application Input

`DocumentKnowledgeIngestionRequest` is proposed as an immutable,
keyword-only application input containing:

- `document_id: EntityId`;
- `kind: str`;
- `title: str`;
- `content: str`;
- `subject: KnowledgeCaptureSubject | None = None`.

Caller input shall not provide:

- canonical Knowledge identity;
- Knowledge capture timestamp;
- Document source type;
- Document source reference;
- preconstructed `KnowledgeRecord`;
- preconstructed `DocumentKnowledgeLineage`.

Document source provenance shall be obtained from the canonical
Enterprise Document rather than duplicated from caller input.

### Canonical Result

`DocumentKnowledgeIngestionResult` is proposed as an immutable,
keyword-only result containing exactly:

- `knowledge_record: KnowledgeRecord`;
- `lineage: DocumentKnowledgeLineage`.

The result shall be returned only after the RFC-064 coordinator reports
successful transaction completion.

The result does not establish:

- Document approval;
- source authenticity;
- trust;
- authorization;
- parsing completeness;
- semantic-search availability;
- AI readiness.

### Existing Document Requirement

RFC-065 shall ingest Knowledge only from an already registered canonical
`EnterpriseDocument`.

The ingestion boundary shall not create, register or modify a Document.

`EnterpriseDocumentRepository` shall therefore be injected explicitly.

Before entering the RFC-064 coordinated transaction, the application
boundary shall call:

`EnterpriseDocumentRepository.get(request.document_id)`

exactly once.

The lookup shall use canonical `EntityId` only.

The application boundary shall not perform source-reference lookup,
source-reference deduplication or alternate-key lookup.

### Document Not-Found Semantics

If the canonical Document lookup returns `None`, the ingestion operation
shall raise:

`DocumentKnowledgeIngestionDocumentNotFoundError`

before coordinated Knowledge / lineage persistence begins.

For this path:

- the RFC-064 coordinator shall not be invoked;
- Knowledge Capture shall not be invoked;
- no Knowledge identity shall be generated;
- no capture timestamp shall be generated;
- no Knowledge repository write shall occur;
- no lineage repository write shall occur.

Unexpected Document repository failures shall propagate.

They shall not be converted to not-found, retry or synthetic success.

### Document Lookup Transaction Boundary

The canonical Document lookup shall occur before the RFC-064 coordinated
Knowledge / lineage transaction.

This is permitted because the currently accepted Enterprise Document
contract is immutable and establishes no update, delete or mutable
revision lifecycle.

RFC-065 shall not extend the RFC-064 coordinator to include
`EnterpriseDocumentRepository`.

RFC-065 shall not establish a transaction spanning:

1. Document registration;
2. Knowledge capture;
3. lineage persistence.

If future accepted architecture introduces Document mutation, deletion,
revision replacement or lifecycle state that can invalidate this
assumption, RFC-065 transaction semantics shall require explicit
architecture review before relying on that new behavior.

### Document Identity Boundary

Canonical Document derivation identity is:

`EnterpriseDocument.id`

The application boundary shall create lineage from this canonical
identity.

`DocumentSource.source_reference` shall remain external source
traceability only.

It shall not become:

- canonical Document identity;
- lineage identity;
- repository alternate identity;
- uniqueness identity;
- deduplication identity.

Canonical Document identity shall not be encoded into
`KnowledgeProvenance.source_reference`.

### Knowledge Provenance Derivation

The ingestion boundary shall derive Knowledge provenance source input
from the loaded canonical `EnterpriseDocument.source`.

Specifically:

- Knowledge `source_type` shall be derived from
  `document.source.source_type.value`;
- Knowledge `source_reference` shall be derived from
  `document.source.source_reference`.

The caller shall not independently supply these two provenance fields.

`KnowledgeCaptureApplicationService` shall remain responsible for:

- constructing canonical `KnowledgeSourceType`;
- constructing canonical `KnowledgeProvenance`;
- generating canonical `captured_at`;
- canonical Knowledge validation.

RFC-065 shall not redefine Knowledge provenance semantics.

Document lineage and external-source provenance remain distinct
concepts.

### Knowledge Subject Boundary

Document derivation shall not automatically replace the Knowledge
record's primary contextual subject.

The ingestion request may provide the existing accepted:

`KnowledgeCaptureSubject`

or no subject.

RFC-065 shall pass that subject through accepted Knowledge Capture
semantics.

RFC-065 shall not:

- infer a subject from Document identity;
- verify subject existence;
- verify subject accessibility;
- introduce an Asset resolver;
- introduce subject cardinality semantics.

### Knowledge Capture Reuse

RFC-065 shall consume:

`KnowledgeCaptureApplicationService`

It shall not bypass that boundary by constructing `KnowledgeRecord`
directly or calling `KnowledgeRecordRepository.add(...)` directly as
application logic.

Inside the RFC-064 coordinated operation, Knowledge Capture shall be
bound to the exact transaction-scoped `KnowledgeRecordRepository`
provided by the coordinator.

RFC-065 shall use the Construction and Dependency Contract defined
above.

The capture-service factory shall be invoked exactly once inside the
coordinated operation and shall receive the exact transaction-scoped
Knowledge repository supplied by RFC-064.

RFC-065 shall not accept or reuse a preconstructed
`KnowledgeCaptureApplicationService`.

The default factory shall preserve the accepted Knowledge Capture
identity and UTC capture-time generation semantics.

### Coordinated Transaction Boundary

For an existing canonical Document, the ingestion application boundary
shall invoke:

`KnowledgeLineageTransactionCoordinator.execute(...)`

exactly once.

The supplied operation shall use exactly the transaction-scoped:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`

provided by RFC-064.

RFC-065 shall not construct or own:

- SQLAlchemy `Session`;
- database engine;
- `DatabaseRuntime`;
- commit;
- rollback;
- session close;
- transaction primitives.

Those responsibilities remain governed by RFC-064 / AD-050 and the
canonical database runtime.

### Persistence Ordering

Within the coordinated operation:

1. construct the `KnowledgeCaptureRequest`;
2. invoke `KnowledgeCaptureApplicationService.capture(...)` exactly once;
3. obtain the newly created canonical `KnowledgeRecord`;
4. construct exactly one `DocumentKnowledgeLineage` using:
   - the loaded canonical `EnterpriseDocument.id`;
   - the returned canonical `KnowledgeRecord.id`;
5. invoke transaction-scoped
   `DocumentKnowledgeLineageRepository.add(...)` exactly once;
6. return the immutable ingestion result to the coordinator.

Knowledge Capture necessarily precedes lineage construction because the
canonical Knowledge identity is created by Knowledge Capture.

This application ordering shall not transfer transaction ownership away
from RFC-064.

### Lineage Boundary

The application boundary shall construct exactly one canonical:

`DocumentKnowledgeLineage`

per successful ingestion invocation.

The relationship shall be:

`document.id -> knowledge_record.id`

RFC-065 shall not introduce:

- lineage surrogate identity;
- lineage timestamp;
- lineage type;
- relational foreign keys;
- global one-to-one cardinality;
- global one-to-many cardinality;
- global many-to-many policy;
- primary-source semantics;
- corroboration;
- merge semantics;
- multi-source derivation semantics.

### Success Semantics

An ingestion invocation shall be successful only when the RFC-064
coordinator completes successfully.

The application boundary shall not report successful ingestion merely
because:

- Knowledge construction succeeded;
- Knowledge `flush()` succeeded;
- lineage construction succeeded;
- lineage `flush()` succeeded.

Successful return requires successful coordinated commit according to
RFC-064.

### Knowledge Failure Semantics

If Knowledge Capture fails before lineage persistence:

- the exception shall propagate;
- lineage `add(...)` shall not be invoked;
- no synthetic success shall be returned;
- RFC-065 shall not retry;
- coordinator-owned rollback semantics remain authoritative where a
  transaction is active.

Canonical Knowledge duplicate errors shall propagate unchanged.

### Lineage Failure Semantics

If lineage persistence fails after Knowledge has been added or flushed
inside the coordinated operation:

- the exception shall propagate;
- RFC-065 shall not report partial success;
- RFC-065 shall not compensate manually;
- RFC-065 shall not issue commit or rollback directly;
- RFC-064 coordinator rollback behavior remains authoritative.

Canonical lineage duplicate errors shall propagate unchanged.

### Unexpected Failure Semantics

Unexpected Domain, repository, factory or persistence failures shall
propagate unless a narrower accepted contract explicitly defines another
semantic.

RFC-065 shall not:

- translate unrelated integrity failures into duplicate errors;
- regenerate Knowledge identity automatically;
- retry automatically;
- overwrite canonical state;
- fabricate successful results.

### Post-Commit Cleanup Semantics

`KnowledgeLineageTransactionPostCommitCleanupError` shall preserve its
accepted RFC-064 meaning.

RFC-065 shall not convert it into an error that falsely implies the
transaction rolled back.

If this exception propagates, participating relational writes may
already be committed.

RFC-065 shall not automatically retry after this outcome.

### Duplicate and Idempotency Boundary

RFC-065 shall preserve existing exact duplicate semantics.

It shall not introduce a new ingestion-level duplicate or idempotency
key.

Repeated ingestion requests for the same Document are not automatically
duplicates because accepted lineage architecture does not establish a
global one-knowledge-record-per-document rule.

Source-reference equality shall not establish duplicate ingestion.

Future idempotency or content-deduplication semantics require a separate
explicit contract.

### Repository Preservation

RFC-065 shall not modify the public contracts of:

- `EnterpriseDocumentRepository`;
- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`.

Standalone relational repository lifecycle behavior shall remain
unchanged.

RFC-064 transaction-scoped repository behavior shall remain unchanged.

No repository shall gain ingestion-specific methods merely for RFC-065.

### ApplicationFacade Boundary

`ApplicationFacade` remains the canonical production operational
workload entry boundary established by AD-027.

`DocumentKnowledgeIngestionApplicationService` is an internal
specialized application use-case boundary.

It shall not compete with `ApplicationFacade`.

RFC-065 shall not:

- add an external endpoint;
- expose ingestion directly to an external production interface;
- modify `ApplicationFacade`;
- modify `IntegrationGateway`;
- modify `OrchestrationService`;
- modify `WorkflowExecutor`.

Any future production external exposure shall require separately
accepted transport, composition and security architecture consistent
with AD-027.

### Architectural Layer Boundary

The term `application` in RFC-065 describes use-case responsibility.

It does not create an Application Layer.

The six-layer ARCH-001 architecture remains unchanged.

AD-051 narrowly governs dependencies required by this specialized
application use case.

RFC-065 shall not establish a general exception allowing arbitrary
cross-layer dependencies elsewhere in PlantMind.

The implementation shall depend on persistence-neutral contracts and
accepted application boundaries, not SQLAlchemy or external systems.

### Core Boundary

RFC-065 shall not modify Core Services.

Core Services shall not depend on RFC-065.

RFC-065 shall not move ingestion workflow responsibility into Core.

CORE-002 remains authoritative.

### DatabaseRuntime Boundary

RFC-065 shall not create or own:

- SQLAlchemy engine;
- session factory;
- database configuration;
- `DATABASE_URL`;
- metadata root;
- database lifecycle.

Canonical `DatabaseRuntime` ownership remains unchanged.

### Relational Schema and Alembic Boundary

Current architecture evidence requires no new relational schema for
RFC-065.

RFC-065 draft therefore assumes:

- no new table;
- no new column;
- no new constraint;
- no new foreign key;
- no new index;
- no new Alembic revision.

Canonical Alembic head remains:

`0004`

If implementation review discovers a genuine schema requirement,
technical implementation shall stop and the architecture contract shall
be reviewed before migration authorization.

### Composition Boundary

RFC-065 shall not automatically modify default:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`.

Existence of the ingestion application boundary does not make
PostgreSQL, Document persistence or coordinated Knowledge persistence a
mandatory default platform capability.

Production composition remains separately governed.

### Runtime and Bootstrap Boundary

RFC-065 shall not modify:

- Runtime lifecycle authority;
- Bootstrap authority;
- readiness semantics;
- Health semantics;
- request-admission semantics;
- operational-transition authority;
- mandatory-capability policy.

Successful ingestion shall not itself change Runtime lifecycle state.

### Parsing and Document Library Boundary

RFC-065 is Knowledge ingestion from an already registered canonical
Document.

It is not raw-file ingestion.

The caller provides prepared Knowledge fields:

- kind;
- title;
- content;
- optional subject.

RFC-065 shall not implement:

- Document Library;
- file upload;
- file download;
- binary storage;
- File Server synchronization;
- PDF parsing;
- OCR;
- text extraction;
- chunking;
- metadata extraction;
- revision tracking.

Future parser, extraction or chunking capabilities may consume RFC-065
after their own contracts are accepted.

### Search and AI Boundary

RFC-065 shall not establish:

- keyword search;
- full-text search;
- semantic search;
- embeddings;
- vector persistence;
- graph persistence;
- Neo4j;
- Knowledge Graph redesign;
- RAG;
- LLM invocation;
- AI Agent behavior;
- engineering reasoning.

Successful ingestion means canonical Knowledge and canonical lineage
were persisted according to accepted contracts.

It does not mean that Knowledge is searchable, indexed, embedded,
retrievable by RAG or available to an LLM.

### Security and Trust Boundary

RFC-065 shall not establish or claim:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- LDAP;
- MFA;
- actor identity;
- actor audit;
- Document permissions;
- source authenticity;
- source correctness;
- Document approval;
- Knowledge approval;
- compliance approval;
- Cybersecurity approval;
- production-security readiness.

Canonical provenance records traceable origin.

Canonical lineage records derivation identity.

Neither establishes trust or authorization.

### Explicitly Deferred

RFC-065 shall not establish:

- Document registration during ingestion;
- Document mutation or deletion;
- Document revision / supersession lifecycle;
- Document Library;
- binary storage;
- upload / download;
- source synchronization;
- parsing;
- OCR;
- chunking;
- semantic search;
- embeddings;
- vector persistence;
- graph persistence;
- Neo4j;
- RAG;
- LLM invocation;
- AI Agent behavior;
- HTTP transport;
- industrial integration;
- PI System integration;
- DCS integration;
- source verification;
- approval lifecycle;
- lineage traversal APIs;
- lineage business cardinality;
- corroboration;
- primary-source rules;
- multi-source derivation;
- ingestion-level deduplication;
- ingestion-level idempotency;
- retry policy;
- savepoints;
- nested coordinated transactions;
- distributed transactions;
- two-phase commit;
- outbox behavior;
- external-system transaction coordination;
- default production composition;
- authentication / authorization expansion;
- production-readiness claims.

### Draft Acceptance Requirements

Before RFC-065 / AD-051 may become Accepted, review shall confirm:

1. no new ARCH-001 architectural layer is introduced;
2. `ApplicationFacade` remains the canonical production workload entry
   boundary;
3. ingestion remains a specialized internal application use case;
4. ingestion begins from an existing canonical `EnterpriseDocument.id`;
5. `EnterpriseDocumentRepository.get(...)` is the canonical existence
   lookup;
6. Document lookup occurs exactly once before transaction coordination;
7. Document not-found prevents coordinator invocation and all writes;
8. no source-reference lookup or identity semantics are introduced;
9. provenance source fields come from the loaded canonical Document;
10. canonical Document identity is not hidden inside provenance;
11. Knowledge subject remains independent from Document lineage;
12. `KnowledgeCaptureApplicationService` is reused rather than bypassed;
13. Knowledge Capture public behavior remains unchanged;
14. Knowledge identity remains owned by Knowledge Capture;
15. capture timestamp remains owned by Knowledge Capture;
16. exactly one Knowledge Capture service is constructed inside the
    coordinated operation through the narrow factory using the exact
    RFC-064 transaction-scoped Knowledge repository, and no preconstructed
    Knowledge Capture service is accepted;
17. `KnowledgeLineageTransactionCoordinator.execute(...)` is invoked
    exactly once for an existing Document;
18. Knowledge Capture occurs exactly once inside that coordinated
    operation;
19. lineage `add(...)` occurs exactly once after Knowledge identity is
    available;
20. lineage uses exact canonical Document and Knowledge identities;
21. no Knowledge or lineage pre-read duplicate check is introduced;
22. no partial-success result is returned;
23. success occurs only after coordinated commit;
24. Knowledge failure prevents lineage success;
25. lineage failure after Knowledge flush enters coordinator-owned
    rollback semantics;
26. canonical duplicate errors remain unchanged;
27. unrelated failures are not heuristically reclassified;
28. post-commit cleanup uncertainty preserves RFC-064 semantics;
29. no automatic retry is introduced;
30. no ingestion-level idempotency or deduplication semantics are
    introduced;
31. repository public contracts remain unchanged;
32. standalone repository behavior remains unchanged;
33. RFC-064 transaction-scoped repository behavior remains unchanged;
34. `DatabaseRuntime` ownership remains unchanged;
35. no schema or Alembic change is required;
36. canonical Alembic head remains `0004`;
37. default Composition remains unchanged;
38. Runtime and Bootstrap authority remain unchanged;
39. no Document Registration transaction is added;
40. no Library, parsing, OCR, chunking, search, vector, graph, RAG or LLM
    responsibility enters RFC-065;
41. no authentication, authorization, trust or production-readiness
    claim is introduced;
42. dependency direction remains explicit, acyclic and compliant with
    ARCH-001 / CORE-002 / CORE-003 plus narrowly accepted ADR authority.

### Contract Acceptance Gate

Status:

**Passed — 42 / 42 Acceptance Requirements**

RFC-065 / AD-051 Contract Acceptance Review is complete.

Review outcome:

- Gate 1 — Dependency & Application-Boundary Compatibility: PASS;
- Gate 2 — Canonical Document Identity & Existence Semantics: PASS;
- Gate 3 — Provenance & Knowledge Subject Preservation: PASS;
- Gate 4 — Transaction, Atomicity & Failure Semantics: PASS;
- Gate 5 — Schema, Composition, Runtime, Bootstrap & Security Preservation: PASS;
- Final Static Contract Review: PASS;
- Acceptance Requirements: 42 PASS / 0 REFINE / 0 BLOCKED.

AD-051 was accepted subject to the implementation-entry Git gate.

That gate was subsequently satisfied before RFC-065 technical
implementation began.

Technical implementation is now complete and verified at:

`c1ab20b693ac90782592961d91dafda8e0782fa1`

### Implementation Authorization

Status:

**Satisfied — Technical implementation completed and verified.**

RFC-065 / AD-051 architecture contract was accepted and committed at:

`3db01142802d98f82a565808b3137a3db64158ac`

The implementation-entry Git gate was satisfied:

1. the accepted contract was committed;
2. the accepted contract was pushed to `origin/feature/engineering-platform`;
3. exact local / remote contract commit identity was verified;
4. the working tree was clean.

RFC-065 technical implementation was completed and committed at:

`c1ab20b693ac90782592961d91dafda8e0782fa1`

Exact local / remote technical commit identity was verified after push.

### Technical Verification Evidence

RFC-065 technical verification completed successfully with:

- RFC-065 targeted verification: **25 passed**;
- preservation verification against accepted Knowledge Capture, Document Registration and RFC-064 boundaries: **66 passed**;
- full PlantMind regression: **779 passed**;
- Python compileall: passed;
- `git diff --check`: passed;
- canonical Alembic head remains `0004`;
- no schema or migration change was introduced;
- no accepted tracked implementation was modified by RFC-065;
- default `CompositionRoot` remains independent of RFC-065;
- Runtime and Bootstrap authority remain unchanged;
- `ApplicationFacade` remains the canonical production workload-entry authority;
- `KnowledgeCaptureApplicationService` remains the canonical Knowledge construction boundary;
- `KnowledgeLineageTransactionCoordinator` remains the transaction lifecycle authority;
- Document lookup occurs before coordinated persistence;
- canonical Document identity is preserved through lineage rather than hidden in provenance;
- Knowledge subject remains independent from Document lineage;
- exact Knowledge and lineage duplicate exceptions propagate unchanged;
- no automatic retry, ingestion-level idempotency or deduplication was introduced;
- no Document Library, parsing, OCR, search, vector, graph, RAG, LLM, security or production-readiness capability was introduced.

### Post-RFC-065 System and Architecture Integrity Review

Outcome:

**PASS — technical implementation conforms to accepted RFC-065 / AD-051.**

The review confirms:

- no new ARCH-001 architectural layer was introduced;
- RFC-065 remains a specialized internal application use case;
- `ApplicationFacade` remains the production workload-entry authority;
- canonical Enterprise Document, Knowledge and lineage identities remain unchanged;
- canonical repository ports remain unchanged and persistence-neutral;
- Knowledge Capture public behavior remains unchanged;
- RFC-064 transaction coordination and failure semantics remain authoritative;
- standalone repository lifecycle behavior remains preserved;
- canonical `DatabaseRuntime` ownership remains unchanged;
- canonical Alembic head remains `0004`;
- default Composition, Runtime and Bootstrap remain unchanged;
- no Document Registration transaction was introduced;
- no production-code architecture redesign is required.

Still explicitly deferred:

- Document Library and binary storage;
- parsing, OCR, extraction and chunking;
- Document revision / supersession lifecycle;
- semantic search and retrieval;
- vector persistence and embeddings;
- graph persistence and Neo4j;
- RAG and LLM capability;
- AI Agent behavior;
- HTTP transport and external production exposure;
- PI System and DCS integration;
- authentication, authorization, RBAC and Active Directory integration;
- trust, approval and production-readiness claims;
- ingestion-level idempotency and deduplication;
- retries, savepoints and nested transactions;
- distributed transactions and outbox behavior;
- external-system transaction coordination.

### Engineering Closure State

RFC-065 engineering-memory and architecture closure was committed and
pushed at:

`cc99e2d0358f1ea7263789aac66747322a62d1f2`

Exact local / remote closure identity was verified.

Working tree after closure push was clean.

RFC-065 is fully closed.

Contract commit:

`3db01142802d98f82a565808b3137a3db64158ac`

Technical implementation commit:

`c1ab20b693ac90782592961d91dafda8e0782fa1`

Engineering-memory closure commit:

`cc99e2d0358f1ea7263789aac66747322a62d1f2`

Verified technical evidence:

- RFC-065 targeted verification: **25 passed**;
- preservation verification: **66 passed**;
- full PlantMind regression: **779 passed**;
- canonical Alembic head: `0004`;
- post-RFC-065 architecture review: **PASS**.

### Next Exact Action

RFC-065 post-closure Source-of-Truth reconciliation is complete and
verified at:

`fe0d8bb82b4e3d22d1ad4e6191205fa05919d30b`

Exact local / remote reconciliation identity was verified.

Working tree after reconciliation push was clean.

RFC-065 is fully closed and Source-of-Truth reconciled.

Evidence-based selection of the next architecture workstream is now
authorized from the current repository, project charter, accepted
architecture and remaining dependency gaps.

No RFC-066 content is assumed or preselected by RFC-065 closure.

No new RFC implementation is authorized until the selected workstream
has its own reviewed and accepted architecture contract, committed,
pushed and verified through its implementation-entry Git gate.

## RFC-064 — Canonical Knowledge-and-Lineage Transaction Coordination Foundation Boundary

### Status

Complete.

Post-RFC-063 evidence-based architecture selection: complete.

Selection baseline:

`f8b63af07dcb7796da5f204ba954b44f5901c7c5`

Proposed architecture decision:

`AD-050 — Canonical Knowledge-and-Lineage Transaction Coordination Foundation Boundary`

AD-050 status:

Accepted.

Formal RFC-064 / AD-050 Contract Acceptance Review:

**PASS.**

Contract draft baseline:

`f0fca291a24393222de660febdd8fd1dc8d4dcb5`

### Selection Evidence

The post-RFC-063 foundation audit confirmed:

- RFC-063 is fully closed;
- exact local/remote repository identity is verified;
- working tree is clean;
- targeted Document + Knowledge + lineage foundation regression: 158 passed;
- full PlantMind regression: 717 passed;
- Python compileall: passed;
- canonical Alembic head: `0004`;
- migration lineage remains linear: `0001 → 0002 → 0003 → 0004`;
- canonical `DatabaseRuntime` owns the SQLAlchemy engine and session factory;
- canonical Knowledge, Enterprise Document and Document-to-Knowledge lineage relational repositories are implemented;
- each current relational repository independently acquires its own session and owns its own commit / rollback / close lifecycle;
- no accepted shared Unit of Work, cross-repository transaction coordinator or equivalent atomic persistence boundary currently exists;
- coordinated Document-to-Knowledge ingestion remains intentionally deferred because Knowledge persistence and lineage persistence do not yet have accepted shared atomicity and failure semantics.

### Selection Rationale

The canonical Document, Knowledge and Document-to-Knowledge lineage foundations are now individually complete through relational persistence.

A future Document-derived Knowledge ingestion capability must be able to persist:

1. one canonical `KnowledgeRecord`; and
2. its canonical `DocumentKnowledgeLineage`

without allowing a partial state in which one succeeds and the other fails.

Introducing ingestion before defining this coordination boundary would force transaction ownership, rollback behavior, partial-failure semantics or compensation behavior implicitly into an application service.

Document-derived Knowledge ingestion SHALL NOT be selected ahead of this unresolved persistence-coordination dependency.

Document Library, parsing, OCR, chunking, semantic search, vector persistence, graph persistence, RAG and LLM capabilities remain separate future workstreams. Their selection SHALL remain evidence-based and SHALL NOT bypass or implicitly redefine the transaction-coordination contract established here.

The minimum dependency-completing next architecture workstream is therefore a narrow Knowledge-and-lineage transaction coordination foundation.

### Objective

Define the minimum canonical transaction-coordination boundary required to allow Knowledge persistence and Document-to-Knowledge lineage persistence to participate in one atomic application-level persistence operation when a later accepted capability requires it.

The workstream SHALL preserve existing canonical Domain identities, repository ports and application responsibilities unless an explicit contract review proves that a narrowly scoped extension is required.

### Required Architecture Questions

RFC-064 / AD-050 contract review SHALL explicitly resolve:

1. transaction ownership;
2. shared SQLAlchemy session ownership;
3. commit authority;
4. rollback authority;
5. repository participation in an externally coordinated transaction;
6. success semantics when both Knowledge and lineage persistence succeed;
7. failure semantics when either persistence step fails;
8. prevention of either partial state within the coordinated operation: Knowledge persisted without its lineage, or lineage persisted without its corresponding Knowledge record;
9. persistence ordering and whether ordering is an application contract or only an infrastructure implementation detail;
10. SQLAlchemy flush authority and the point at which database constraint failures must be materialized before final transaction commit;
11. duplicate and integrity-error classification ownership when individual repositories no longer own the coordinated commit;
12. preservation of exact constraint-aware duplicate semantics in both standalone and coordinated persistence paths;
13. session close ownership;
14. preservation of standalone repository behavior outside coordinated operations;
15. preservation of persistence-neutral repository ports;
16. interaction with `KnowledgeCaptureApplicationService`;
17. whether any existing implementation must be extended or whether transaction-scoped adapters are required;
18. whether compensation is unnecessary when both writes share one canonical PostgreSQL transaction;
19. preservation of canonical `DatabaseRuntime` engine and session-factory ownership without making it a transaction coordinator implicitly;
20. prevention of SQLAlchemy `Session` or transaction primitives leaking into Domain or persistence-neutral repository ports;
21. containment of the capability so it does not become a generic platform-wide Unit of Work without separate evidence.

### Existing Responsibilities That SHALL Be Preserved

The selection assumes no redesign of:

- `EnterpriseDocument`;
- `KnowledgeRecord`;
- `DocumentKnowledgeLineage`;
- `EnterpriseDocumentRepository`;
- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`;
- `EnterpriseDocumentRegistrationApplicationService`;
- `KnowledgeCaptureApplicationService`;
- canonical `DatabaseRuntime` engine and session-factory ownership;
- standalone relational repository behavior outside explicitly coordinated operations;
- canonical Knowledge provenance semantics;
- canonical Knowledge subject semantics;
- Document source traceability semantics;
- directed Document-to-Knowledge lineage identity;
- existing relational identity constraints;
- canonical SQLAlchemy metadata authority;
- canonical Alembic schema lifecycle;
- Runtime lifecycle authority;
- Bootstrap authority.

### Explicit Non-Goals

RFC-064 selection does NOT authorize:

- Document-to-Knowledge ingestion;
- Document registration redesign;
- Document Library behavior;
- binary document storage;
- file upload;
- parser implementation;
- OCR;
- chunking;
- Document revision lifecycle;
- semantic search;
- vector persistence;
- graph persistence;
- Neo4j;
- RAG;
- LLM invocation;
- HTTP transport;
- industrial integration;
- one-sided lineage traversal;
- reverse lineage traversal;
- lineage business cardinality policy;
- corroboration semantics;
- primary-source semantics;
- multi-source derivation semantics;
- default `CompositionRoot` database wiring;
- mandatory database Runtime capability;
- authentication or authorization expansion;
- RBAC;
- Cybersecurity approval;
- production-readiness claims;
- a generic transaction framework for unrelated PlantMind subsystems;
- a new relational schema or Alembic revision as an assumed requirement.

### Dependency Baseline

RFC-064 contract drafting SHALL be reviewed against, at minimum:

- RFC-053 / canonical Knowledge foundation;
- RFC-054 / canonical database runtime and schema lifecycle;
- RFC-055 / Knowledge relational persistence;
- RFC-056 / Knowledge Capture application boundary;
- RFC-057 / canonical Enterprise Document foundation;
- RFC-058 / Enterprise Document repository;
- RFC-059 / Enterprise Document relational persistence;
- RFC-060 / Enterprise Document Registration application boundary;
- RFC-061 / canonical Document-to-Knowledge lineage;
- RFC-062 / lineage repository;
- RFC-063 / lineage relational persistence;
- accepted architecture dependency, Composition, Runtime and Bootstrap rules.

### Draft Architecture Contract

#### Contract Intent

RFC-064 SHALL establish the minimum persistence-neutral and infrastructure-backed coordination boundary required for canonical Knowledge persistence and canonical Document-to-Knowledge lineage persistence to participate in one atomic relational transaction.

The contract exists solely to provide an atomic persistence foundation for future accepted application capabilities that require both repositories together.

RFC-064 SHALL NOT itself implement Document-to-Knowledge ingestion.

#### Canonical Atomicity Invariant

For one coordinated operation, the persistence outcome SHALL be atomic with respect to all Knowledge and lineage writes actually submitted through the transaction-scoped repositories during that operation.

If the supplied application operation performs both:

- a canonical Knowledge write; and
- its corresponding canonical lineage write;

those participating writes SHALL commit together or neither SHALL be successfully committed by that transaction.

All successful participating writes within one coordinated operation SHALL commit together.

Any failure before successful commit SHALL cause the coordinated transaction to enter the accepted rollback path as one unit.

RFC-064 SHALL NOT claim that the transaction coordinator itself:

- requires both repositories to be written;
- infers whether a lineage write is required;
- infers correspondence between arbitrary Knowledge and lineage values;
- enforces Knowledge-to-lineage business completeness;
- enforces business cardinality.

A future accepted application capability that requires one Knowledge record and one lineage relation SHALL own the obligation to invoke both required persistence operations before returning successful use-case completion.

The coordinator guarantees atomicity of participating relational writes.

It does not guarantee application-use-case completeness.

This invariant applies only to writes participating in the same RFC-064 transaction scope.

It does not define global Knowledge-to-lineage business cardinality.

#### Persistence-Neutral Coordination Port

RFC-064 SHALL introduce a narrowly scoped persistence-neutral coordination contract under:

`app.knowledge_lineage_transaction`

Expected package:

- `backend/app/knowledge_lineage_transaction/__init__.py`;
- `backend/app/knowledge_lineage_transaction/coordinator.py`.

The package initializer SHALL remain empty unless a separately reviewed public API becomes necessary.

The persistence-neutral contract SHALL define:

`KnowledgeLineageTransactionCoordinator`

with one coordinated execution operation equivalent in responsibility to:

`execute(operation) -> T`

The operation SHALL receive access only to:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`.

The coordination contract SHALL NOT expose:

- SQLAlchemy `Session`;
- SQLAlchemy transaction objects;
- engine objects;
- connection objects;
- commit primitives;
- rollback primitives;
- flush primitives;
- savepoints;
- database-specific exceptions as transaction-control mechanisms.

Application code SHALL therefore remain persistence-neutral.

#### Application-Level and Dependency Ownership

`KnowledgeLineageTransactionCoordinator` SHALL be an application-level persistence-coordination port.

The term `application-level` describes responsibility and use-case position only.

RFC-064 SHALL NOT introduce a seventh architectural layer and SHALL NOT modify the six-layer model defined by ARCH-001.

The coordinator SHALL NOT be:

- an architectural layer;
- a Domain service;
- a Core platform service;
- an intelligence engine;
- an AI agent;
- an application workload entry point;
- a replacement or competitor for `ApplicationFacade`;
- a transport-facing use case by itself.

It is a narrowly scoped supporting application-level persistence contract for future accepted Knowledge application capabilities.

The persistence-neutral coordination package MAY depend only on:

- accepted persistence-neutral Knowledge repository contracts;
- accepted persistence-neutral lineage repository contracts;
- Python standard-library typing / callable abstractions required to express the contract.

It SHALL NOT depend on:

- `app.infrastructure`;
- SQLAlchemy;
- Psycopg;
- `DatabaseRuntime`;
- Composition;
- Runtime;
- Bootstrap;
- API transport;
- agents;
- intelligence engines.

Application capabilities MAY depend on the persistence-neutral coordinator port.

The SQLAlchemy implementation MAY depend only on the persistence-neutral coordinator contract and its coordination-specific errors as required to implement that accepted contract.

AD-050 SHALL constitute the explicit narrow architecture authorization for that implementation dependency.

This authorization SHALL NOT permit Infrastructure to depend on:

- application services;
- `ApplicationFacade`;
- orchestration services;
- business workflows;
- agents;
- intelligence engines.

Canonical Domain and repository packages SHALL NOT depend outward on the coordinator implementation.

No new general Infrastructure-to-Application dependency rule is established by RFC-064.

#### Synchronous Execution Model

RFC-064 establishes synchronous transaction coordination consistent with the accepted synchronous SQLAlchemy database runtime.

One coordinated operation SHALL execute synchronously.

RFC-064 SHALL NOT establish:

- `AsyncSession`;
- asynchronous transaction coordination;
- concurrent use of one shared SQLAlchemy session by multiple threads or tasks;
- cross-thread transaction-scoped repository use.

A coordinator instance MAY support multiple independent sequential or concurrent callers only if each `execute(...)` invocation owns completely independent session and transaction state.

The coordinator SHALL NOT store one active session as reusable instance state.

#### Coordinated Operation Boundary

One `execute(...)` invocation SHALL represent one independent Knowledge-and-lineage transaction scope.

The coordinator SHALL invoke the supplied operation exactly once.

The supplied operation MAY use only the transaction-scoped:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`

provided for that invocation.

RFC-064 SHALL NOT introduce unrelated repositories into this coordination boundary.

No Enterprise Document repository participation is authorized by RFC-064.

No cross-repository Document existence validation is authorized.

#### Transaction-Scoped Repository Participation

The SQLAlchemy implementation SHALL provide transaction-scoped implementations of the existing:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`.

These participants SHALL preserve the existing persistence-neutral repository contracts.

They SHALL use the same canonical Domain-to-relational mappings already established by accepted persistence architecture.

They SHALL NOT:

- generate Domain identity;
- construct canonical Knowledge on behalf of the application;
- construct canonical lineage on behalf of the application;
- create a database engine;
- create an independent session;
- commit;
- rollback;
- close the shared session;
- alter canonical Domain semantics;
- alter repository public operations.

Transaction-scoped participants SHALL receive one already-owned shared SQLAlchemy session from the coordinator implementation.

#### Standalone Repository Preservation

RFC-064 SHALL NOT replace or redefine the existing standalone:

- `SQLAlchemyKnowledgeRecordRepository`;
- `SQLAlchemyDocumentKnowledgeLineageRepository`.

Existing standalone repository behavior SHALL remain valid:

- each standalone repository may continue to acquire its own session;
- each standalone repository continues to own its standalone commit / rollback / close lifecycle;
- existing duplicate translation remains preserved;
- existing repository runtime tests remain valid.

RFC-064 adds a distinct coordinated transaction path rather than creating ambiguous dual transaction ownership inside the existing standalone repository classes.

#### Shared Session Invariant

For one coordinated `execute(...)` invocation:

- exactly one SQLAlchemy session SHALL be acquired;
- both transaction-scoped repository participants SHALL use that exact same session;
- no participant SHALL acquire a second session;
- no participant SHALL substitute another session;
- the coordinator SHALL NOT retain that session for reuse by a later independent execution.

A new independent execution SHALL receive a new transaction scope.

#### Session Acquisition and Transaction Start

For one coordinated `execute(...)` invocation:

1. the injected session factory SHALL be invoked exactly once;
2. one session SHALL be acquired;
3. the coordinator SHALL establish exactly one transaction scope before invoking the supplied operation;
4. transaction-scoped repository participants SHALL then be created for that scope;
5. only after successful transaction establishment may the supplied operation be invoked.

If session acquisition itself fails:

- the failure SHALL propagate;
- the supplied operation SHALL NOT be invoked;
- no rollback SHALL be attempted because no owned session exists;
- no session close SHALL be attempted for a session that was never acquired.

If transaction establishment fails after a session has been acquired:

- the supplied operation SHALL NOT be invoked;
- no commit SHALL occur;
- the acquired session SHALL still be closed exactly once;
- rollback SHALL be attempted only when an active transaction was actually established.

RFC-064 SHALL NOT depend on an implicit nested transaction or savepoint to establish this scope.

#### DatabaseRuntime Ownership

Canonical `DatabaseRuntime` SHALL remain the owner of:

- SQLAlchemy engine creation;
- canonical session-factory creation;
- engine disposal.

The SQLAlchemy transaction coordinator SHALL receive an injected synchronous session factory.

It SHALL NOT:

- create its own engine;
- construct a second `DatabaseRuntime`;
- read `DATABASE_URL` directly;
- dispose the canonical engine;
- redefine database configuration validation;
- redefine database lifecycle authority.

RFC-064 therefore coordinates a session obtained from canonical infrastructure without taking ownership of database-runtime lifecycle.

#### Transaction Lifecycle Authority

For one coordinated operation, the SQLAlchemy coordinator SHALL own:

1. acquisition of one session;
2. the single transaction scope for that session;
3. creation of transaction-scoped repository participants using that session;
4. invocation of the supplied operation exactly once;
5. final commit authority;
6. rollback authority on failure;
7. session close authority.

Transaction-scoped repositories SHALL own none of those lifecycle responsibilities except persistence operations and required flush behavior described below.

#### Commit Semantics

If the supplied coordinated operation completes successfully:

1. all participant persistence work SHALL already have been submitted to the shared transaction;
2. required participant constraint validation SHALL have been materialized through flush behavior;
3. the coordinator SHALL perform exactly one final commit;
4. only after successful commit may the operation result be considered successfully committed.

No transaction-scoped repository SHALL commit independently.

RFC-064 SHALL NOT introduce multiple success commits for one coordinated operation.

#### Final Commit Failure and Outcome Certainty

If final `commit` raises:

- the coordinated operation SHALL NOT be reported as successfully completed;
- the operation result SHALL NOT be returned as a successful result;
- the coordinator SHALL attempt the accepted rollback failure path;
- no automatic retry SHALL occur.

RFC-064 SHALL distinguish database atomicity from caller-visible outcome certainty.

PostgreSQL transaction atomicity means participating Knowledge and lineage writes are committed together or not committed together at the database transaction level.

However, a client-side or connection failure during final commit MAY leave the caller unable to prove whether the database accepted the commit before the failure became observable.

Therefore:

- a final commit exception SHALL NOT be interpreted automatically as proof that nothing was committed;
- rollback after a commit exception SHALL NOT be documented as proof that a previously completed server-side commit was reversed;
- the coordinator SHALL NOT automatically retry a commit-failed operation;
- future application retry or reconciliation policy requires separate architecture.

This contract prevents a commit communication failure from being converted into an unsafe duplicate application attempt.

#### Rollback Semantics

If any failure occurs before successful commit, including:

- Knowledge persistence failure;
- lineage persistence failure;
- translated duplicate conflict;
- unrelated integrity failure;
- operation failure;
- flush failure;
- final commit failure;

the coordinator SHALL attempt exactly one rollback of the shared transaction.

If rollback succeeds, the original failure SHALL propagate unchanged except where an accepted repository duplicate translation has already occurred.

If rollback itself fails, the rollback failure SHALL NOT be suppressed.

The rollback failure SHALL preserve causal linkage to the failure that triggered rollback.

No participant SHALL independently rollback the shared session.

#### Session Close Semantics

The coordinator SHALL attempt to close the shared session exactly once for every coordinated execution.

Session close SHALL occur after the success or failure transaction path has completed.

During session cleanup, the coordinator SHALL NOT explicitly invoke:

- a second commit; or
- a second rollback.

Session close SHALL NOT be used by PlantMind as a second transaction-decision mechanism.

SQLAlchemy, the database driver or connection-pool implementation MAY perform internal resource cleanup required by their own lifecycle semantics.

RFC-064 SHALL NOT represent such implementation-level cleanup as a new PlantMind transaction decision.

Session cleanup SHALL NOT redefine the already established caller-visible transaction outcome.

A session-close failure is an infrastructure cleanup failure and SHALL NOT be classified as a Domain validation failure or repository duplicate.

RFC-064 SHALL NOT claim that a post-commit cleanup failure reverses an already committed database transaction.

Automatic retry behavior for such failures remains outside RFC-064.

#### Post-Commit Cleanup Outcome

RFC-064 SHALL introduce the persistence-neutral coordination error:

`KnowledgeLineageTransactionPostCommitCleanupError`

This error SHALL be used only when:

1. final database commit has already completed successfully; and
2. subsequent coordinator-owned session cleanup fails.

The error SHALL preserve causal linkage to the underlying cleanup failure.

Its meaning SHALL be explicit:

**the coordinated database transaction committed successfully; cleanup failed afterward.**

A caller SHALL NOT interpret this error as evidence that the Knowledge-and-lineage transaction rolled back.

A caller SHALL NOT automatically retry the coordinated persistence operation solely because this post-commit cleanup error occurred.

If a transaction or rollback failure already exists and session cleanup also fails:

- the transaction / rollback failure SHALL remain the primary transaction outcome;
- the cleanup failure SHALL NOT replace or misrepresent that prior outcome;
- diagnostic causal information about the cleanup failure SHALL be preserved where technically possible.

This prevents a cleanup failure from creating an ambiguous persistence result.

#### Flush Authority

Transaction-scoped repository participants SHALL own flush of their own pending relational write.

For transaction-scoped `add(...)`:

1. the canonical value SHALL be mapped using the existing accepted mapper;
2. the mapped row SHALL be added to the shared session;
3. the participant SHALL flush the shared session;
4. the participant SHALL perform no commit;
5. the participant SHALL perform no rollback;
6. the participant SHALL perform no close.

The purpose of participant-owned flush is to materialize repository-owned database constraint failures at the repository boundary before final coordinated commit.

This preserves repository-level duplicate classification even though final commit ownership moves to the coordinator.

#### Duplicate Classification

Knowledge duplicate classification SHALL preserve the accepted canonical semantics for:

`pk_knowledge_records`

and PostgreSQL unique-violation SQLSTATE:

`23505`

Lineage duplicate classification SHALL preserve the accepted canonical semantics for:

`pk_document_knowledge_lineages`

and PostgreSQL unique-violation SQLSTATE:

`23505`

A transaction-scoped repository SHALL translate only the exact database failure belonging to its accepted canonical identity constraint.

Knowledge identity conflict SHALL translate to:

`KnowledgeRecordAlreadyExistsError`

Lineage identity conflict SHALL translate to:

`DocumentKnowledgeLineageAlreadyExistsError`

Unrelated integrity failures SHALL remain unrelated integrity failures.

Message-text-only duplicate classification SHALL remain prohibited.

The coordinator itself SHALL NOT guess repository ownership of an arbitrary integrity error.

#### Canonical Duplicate-Classification Reuse

RFC-064 SHALL NOT create divergent duplicate-classification algorithms for the same canonical repository identity.

For Knowledge persistence, standalone and transaction-scoped paths SHALL use one canonical infrastructure-owned classification rule for:

- SQLSTATE `23505`;
- constraint `pk_knowledge_records`.

For lineage persistence, standalone and transaction-scoped paths SHALL use one canonical infrastructure-owned classification rule for:

- SQLSTATE `23505`;
- constraint `pk_document_knowledge_lineages`.

Technical implementation MAY refactor existing implementation-private duplicate classifiers into shared infrastructure-private helpers when required.

Such a refactor SHALL NOT change:

- repository public APIs;
- accepted duplicate semantics;
- exception types;
- constraint identities;
- SQLSTATE requirements;
- standalone repository transaction ownership.

Copying two independently maintained classification implementations for the same constraint SHALL NOT be accepted when a single internal classifier can preserve one source of truth.

#### Commit-Time Failure Classification

Participant-owned constraints SHALL be materialized through participant flush whenever technically possible.

A failure appearing only at final commit SHALL NOT be heuristically reclassified by the coordinator as a Knowledge or lineage duplicate.

Commit-time failures SHALL be rolled back and propagated unless a future separately accepted contract establishes safe classification.

This prevents duplicate semantics from silently moving out of repository ownership.

#### Transaction-Scoped Read Semantics

Transaction-scoped implementations SHALL preserve the accepted repository `get(...)` behavior.

For transaction-scoped `get(...)`:

- the exact shared coordinator-owned session SHALL be used;
- no independent session SHALL be acquired;
- no commit SHALL occur;
- no rollback SHALL occur;
- no session close SHALL occur;
- canonical row-to-Domain mapping SHALL remain unchanged;
- an absent identity SHALL return `None` exactly as accepted by the existing repository contract.

A transaction-scoped read SHALL NOT take transaction-lifecycle ownership from the coordinator.

#### Persistence Ordering

RFC-064 SHALL NOT impose a business-level ordering rule between Knowledge and lineage persistence.

The future application operation determines the order in which it invokes the transaction-scoped repositories.

Infrastructure atomicity SHALL remain valid regardless of which participant is called first.

A future Document-derived Knowledge application capability may naturally need Knowledge identity before constructing lineage, but that is an application-use-case concern rather than a database transaction rule.

#### KnowledgeCaptureApplicationService Compatibility

RFC-064 SHALL NOT modify the accepted responsibilities or public behavior of:

`KnowledgeCaptureApplicationService`

The service SHALL remain dependent on the persistence-neutral:

`KnowledgeRecordRepository`

A future accepted application capability MAY use `KnowledgeCaptureApplicationService` inside an RFC-064 coordinated operation by supplying the transaction-scoped `KnowledgeRecordRepository`.

RFC-064 SHALL NOT make the transaction coordinator:

- generate Knowledge identity;
- generate Knowledge capture timestamps;
- construct Knowledge provenance;
- construct Knowledge subject;
- call `KnowledgeCaptureApplicationService` automatically;
- become a Knowledge factory.

Knowledge construction and capture semantics remain owned by the accepted Knowledge Capture application boundary.

#### EnterpriseDocumentRegistrationApplicationService Preservation

RFC-064 SHALL NOT modify:

`EnterpriseDocumentRegistrationApplicationService`

Document registration remains a separate application use case.

RFC-064 does not establish a transaction spanning:

- Enterprise Document registration;
- Knowledge capture;
- lineage persistence.

Any such future cross-use-case transaction would require separate architecture evidence and acceptance.

#### Domain Preservation

RFC-064 SHALL NOT modify:

- `EnterpriseDocument`;
- `KnowledgeRecord`;
- `KnowledgeProvenance`;
- `KnowledgeSubject`;
- `DocumentKnowledgeLineage`;
- canonical `EntityId` semantics;
- Document source traceability semantics;
- directed Document-to-Knowledge lineage semantics.

No transaction state SHALL enter canonical Domain entities or value objects.

#### Repository Port Preservation

RFC-064 SHALL NOT change the accepted public operations of:

`KnowledgeRecordRepository`

or:

`DocumentKnowledgeLineageRepository`

The existing `add(...)` and `get(...)` contracts remain authoritative.

No SQLAlchemy types SHALL enter either persistence-neutral repository port.

No commit, rollback, flush, session or transaction method SHALL be added to those repository ports.

#### Transaction-Scope Lifetime

Transaction-scoped repository participants are valid only during the active coordinated execution that created them.

They SHALL NOT become platform singletons.

They SHALL NOT be registered as durable default services.

They SHALL NOT own reusable session state.

They SHALL NOT be reused across independent coordinated operations.

The implementation SHALL avoid exposing transaction-scoped participants as a new general-purpose persistence API.

#### Reentrancy and Nested Transaction Boundary

RFC-064 SHALL NOT establish:

- nested coordinated transactions;
- savepoint semantics;
- recursive transaction scopes;
- transaction suspension;
- distributed transactions;
- two-phase commit.

No nested transaction guarantee is authorized.

Any future need for nested or distributed transaction semantics requires separate evidence and architecture acceptance.

#### Isolation and Concurrency Boundary

RFC-064 SHALL NOT redefine:

- database isolation level;
- engine pool configuration;
- connection pool lifecycle;
- lock policy;
- deadlock retry;
- statement retry;
- transaction timeout;
- optimistic concurrency policy.

The coordinated transaction SHALL inherit the canonical database configuration of the supplied session factory.

#### Retry and Idempotency Boundary

RFC-064 SHALL NOT automatically retry:

- duplicate failures;
- integrity failures;
- operational database failures;
- deadlocks;
- commit failures;
- rollback failures;
- session cleanup failures.

Application retry and idempotency semantics remain separately governed.

No hidden retry loop SHALL be introduced.

#### External Side-Effect Boundary

RFC-064 atomicity applies only to relational work participating in the same canonical PostgreSQL transaction.

It SHALL NOT claim atomicity for:

- file-system writes;
- binary document storage;
- network calls;
- PI / DCS / OPC UA interactions;
- external databases;
- message publication;
- event delivery;
- email;
- HTTP calls;
- parser execution;
- OCR execution;
- vector persistence;
- graph persistence;
- LLM invocation;
- any other non-participating external system.

The coordinated operation MAY perform pure in-memory canonical construction required to prepare Knowledge and lineage values.

Long-running or non-transactional external work SHALL NOT be treated as rollback-protected merely because it occurs inside the callback.

RFC-064 SHALL NOT introduce an outbox, distributed transaction or external compensation mechanism.

Future application capabilities that combine relational persistence with external side effects require separately accepted coordination semantics.

#### Compensation Boundary

Because Knowledge and lineage relational persistence currently reside within the same canonical PostgreSQL transaction capability, RFC-064 SHALL prefer database atomic rollback over application compensation.

RFC-064 SHALL NOT introduce compensation as a substitute for atomic rollback.

Cross-system compensation remains outside scope.

#### Relational Schema Boundary

RFC-064 SHALL NOT require a new relational table.

RFC-064 SHALL NOT change canonical columns or constraints for:

- `knowledge_records`;
- `document_knowledge_lineages`;
- `enterprise_documents`.

RFC-064 SHALL NOT introduce relational foreign keys.

RFC-064 SHALL NOT introduce a new metadata root.

Canonical SQLAlchemy metadata authority remains unchanged.

#### Alembic Boundary

RFC-064 SHALL NOT assume a new Alembic revision.

Canonical Alembic head SHALL remain:

`0004`

unless contract review discovers a separately justified schema requirement.

Any newly discovered schema requirement SHALL stop implementation and require explicit architecture review before a migration is authorized.

#### SQLAlchemy Infrastructure Namespace

The expected SQLAlchemy implementation namespace is:

`app.infrastructure.knowledge_lineage_transaction`

Expected minimum production surface:

- `backend/app/infrastructure/knowledge_lineage_transaction/__init__.py`;
- `backend/app/infrastructure/knowledge_lineage_transaction/coordinator.py`;
- transaction-scoped repository participant implementation contained within that infrastructure boundary.

The infrastructure package initializer SHALL remain empty unless a separately reviewed public API is necessary.

The implementation SHALL reuse accepted Knowledge and lineage relational mappings and canonical SQLAlchemy metadata.

It SHALL NOT introduce alternate relational models for the same canonical entities.

#### Default Composition Boundary

RFC-064 SHALL NOT automatically wire the SQLAlchemy transaction coordinator into default:

`CompositionRoot`

The existence of a transaction coordinator implementation does not itself make database availability a mandatory default platform capability.

Production composition requires a separately accepted application capability that needs coordinated persistence.

#### Runtime and Bootstrap Boundary

RFC-064 SHALL NOT modify:

- Runtime lifecycle authority;
- Bootstrap authority;
- Operational Transition authority;
- mandatory capability readiness semantics;
- availability semantics;
- database mandatory-capability policy.

No database startup dependency is introduced merely by implementing this foundation.

#### Security Boundary

RFC-064 does not establish or claim:

- authentication;
- authorization;
- RBAC;
- Active Directory integration;
- Data Permission Layer;
- AI response filtering;
- cybersecurity approval;
- production security readiness.

Transaction atomicity is not a security authorization mechanism.

#### Explicitly Deferred

RFC-064 SHALL NOT establish:

- Document-to-Knowledge ingestion;
- Document Library;
- binary document storage;
- file upload;
- parsing;
- OCR;
- chunking;
- Document revision lifecycle;
- source-document verification;
- document approval state;
- document trust state;
- semantic search;
- vector persistence;
- graph persistence;
- Neo4j;
- RAG;
- LLM invocation;
- HTTP transport;
- industrial integration;
- one-sided lineage retrieval;
- reverse lineage traversal;
- lineage business cardinality;
- corroboration;
- primary-source semantics;
- multi-source derivation;
- a generic platform-wide Unit of Work;
- transactions spanning unrelated PlantMind subsystems;
- distributed transaction coordination;
- compensation across external systems;
- automatic retry policy;
- asynchronous transaction coordination;
- `AsyncSession`;
- cross-thread shared-session use;
- transactional event publication;
- outbox semantics;
- production-readiness claims.

#### Expected TDD Verification

RFC-064 technical implementation, if later authorized, SHALL verify at minimum:

1. the persistence-neutral coordinator contract contains no SQLAlchemy dependency;
2. existing Knowledge and lineage repository ports remain unchanged;
3. existing Domain contracts remain unchanged;
4. one coordinated execution acquires exactly one session;
5. Knowledge and lineage transaction-scoped repositories use the exact same session;
6. transaction-scoped repositories acquire no independent session;
7. transaction-scoped Knowledge `add(...)` flushes but does not commit;
8. transaction-scoped lineage `add(...)` flushes but does not commit;
9. transaction-scoped repositories do not rollback;
10. transaction-scoped repositories do not close the shared session;
11. successful coordinated execution commits exactly once;
12. successful coordinated execution closes the session exactly once;
13. operation failure causes one rollback;
14. Knowledge flush failure causes one rollback;
15. lineage flush failure causes one rollback;
16. final commit failure causes one rollback attempt;
17. rollback failure is not swallowed and preserves causal linkage;
18. Knowledge duplicate classification remains exact and constraint-aware;
19. lineage duplicate classification remains exact and constraint-aware;
20. unrelated integrity failures are not misclassified;
21. coordinator does not heuristically classify commit-time integrity failures;
22. no partial success is reported when either participant fails before commit;
23. the operation result is returned only after successful final commit;
24. transaction-scoped participants do not escape into default platform composition;
25. independent executions do not reuse session state;
26. existing standalone Knowledge repository behavior remains unchanged;
27. existing standalone lineage repository behavior remains unchanged;
28. `KnowledgeCaptureApplicationService` remains unchanged;
29. `EnterpriseDocumentRegistrationApplicationService` remains unchanged;
30. canonical `DatabaseRuntime` remains engine/session-factory lifecycle owner;
31. no second metadata authority is introduced;
32. no schema migration is introduced;
33. canonical Alembic head remains `0004`;
34. default `CompositionRoot` remains unchanged;
35. Runtime and Bootstrap authority remain unchanged;
36. Python compileall passes;
37. architecture / forbidden-coupling guards pass;
38. full PlantMind regression remains green;
39. the coordinator port is application-level and persistence-neutral;
40. no Domain or Core package depends on transaction infrastructure;
41. session-factory acquisition failure does not invoke the operation;
42. session-factory acquisition failure attempts neither rollback nor close on a nonexistent session;
43. transaction-start failure does not invoke the operation;
44. an acquired session is closed when transaction establishment fails;
45. the transaction is established before the supplied operation is invoked;
46. transaction-scoped `get(...)` uses the shared session without commit / rollback / close;
47. standalone and coordinated Knowledge duplicate paths use one canonical classification rule;
48. standalone and coordinated lineage duplicate paths use one canonical classification rule;
49. final commit failure is never reported as successful completion;
50. final commit failure triggers no automatic retry;
51. post-commit close failure is distinguishable from transaction rollback through `KnowledgeLineageTransactionPostCommitCleanupError`;
52. post-commit cleanup failure does not imply that committed data was rolled back;
53. cleanup failure does not mask an already-existing transaction or rollback failure;
54. one coordinator instance retains no active session between independent executions;
55. no asynchronous or cross-thread shared-session behavior is introduced;
56. no external-system atomicity claim enters the implementation;
57. RFC-064 introduces no new ARCH-001 architectural layer;
58. the coordinator is not an application workload entry point or `ApplicationFacade` competitor;
59. transaction atomicity is not falsely represented as application-use-case completeness;
60. session cleanup performs no second explicit PlantMind commit or rollback decision.

#### Contract Acceptance Gate

RFC-064 / AD-050 SHALL NOT become Accepted merely because this draft exists.

Before acceptance, a dedicated architecture review SHALL verify:

1. the coordination boundary is the minimum dependency-completing solution;
2. the design does not become a generic Unit of Work;
3. Domain contracts remain unchanged;
4. repository ports remain persistence-neutral and unchanged;
5. existing standalone repositories retain clear transaction ownership;
6. transaction-scoped participants have unambiguous non-owning lifecycle semantics;
7. one shared session is sufficient for atomicity;
8. final commit authority exists in exactly one place;
9. rollback authority exists in exactly one place;
10. flush ownership preserves repository duplicate classification;
11. no duplicate-classification semantics are weakened;
12. `KnowledgeCaptureApplicationService` remains reusable without redesign;
13. `DatabaseRuntime` lifecycle ownership is preserved;
14. no schema or migration change is required;
15. default Composition does not acquire a database dependency;
16. Runtime and Bootstrap authority remain unchanged;
17. deferred ingestion, Library, AI, search and security work remains outside scope;
18. the coordinator port has explicit application-level responsibility without creating a new ARCH-001 layer;
19. session acquisition and transaction-start failure paths are unambiguous;
20. the supplied operation cannot execute before transaction establishment succeeds;
21. commit failure is not falsely documented as proof of rollback;
22. post-commit cleanup failure has an explicit committed-outcome semantic;
23. transaction failure cannot be masked by a later cleanup failure;
24. standalone and coordinated duplicate classification cannot drift into separate rules;
25. transaction-scoped reads preserve repository semantics without acquiring lifecycle ownership;
26. synchronous shared-session usage is explicit and async / cross-thread behavior remains outside scope;
27. PostgreSQL transaction atomicity is not extended falsely to external side effects;
28. the coordinator does not compete with `ApplicationFacade` or become a production workload entry boundary;
29. AD-050 explicitly governs the narrow Infrastructure dependency on the persistence-neutral coordinator contract without establishing a general reverse-layer dependency rule;
30. transaction atomicity is explicitly distinguished from application-use-case completeness;
31. session-close semantics make no unverifiable guarantee about SQLAlchemy, driver or pool internal cleanup while prohibiting any second explicit PlantMind transaction decision.

Outcome:

**PASS — RFC-064 / AD-050 architecture contract accepted.**

The formal review confirmed that all acceptance requirements are satisfied.

The accepted contract preserves:

- the six-layer ARCH-001 model without creating another architectural layer;
- application-level responsibility without competing with `ApplicationFacade`;
- persistence-neutral Domain and repository contracts;
- one narrow Knowledge-and-lineage coordination responsibility;
- one shared relational transaction scope per coordinated execution;
- coordinator-owned commit, rollback and session-close authority;
- transaction-scoped repository flush without independent transaction ownership;
- exact constraint-aware Knowledge and lineage duplicate semantics;
- standalone repository behavior outside coordinated execution;
- canonical `DatabaseRuntime` lifecycle ownership;
- `KnowledgeCaptureApplicationService` responsibility;
- `EnterpriseDocumentRegistrationApplicationService` responsibility;
- default Composition independence;
- Runtime and Bootstrap authority;
- canonical Alembic head `0004`;
- explicit separation between transaction atomicity and application-use-case completeness;
- explicit exclusion of external-system atomicity, retry, ingestion, Library, search, AI, security and production-readiness claims.

### Implementation Authorization

Status:

**Satisfied — Technical implementation completed and verified.**

The RFC-064 / AD-050 architecture contract was accepted and committed at:

`7f63e0262a1dc9c3f22466ae64d4c2235b74855c`

The implementation-entry Git gate was subsequently satisfied:

1. the accepted contract was committed;
2. the accepted contract was pushed to `origin/feature/engineering-platform`;
3. exact local / remote contract commit identity was verified;
4. the working tree was clean.

RFC-064 technical implementation was then completed and committed at:

`f62179a621f1289b47833b6057661a631e5357be`

Exact local / remote technical commit identity was verified after push.

### Technical Verification Evidence

RFC-064 technical verification completed successfully with:

- RFC-064 targeted verification: **37 passed**;
- full PlantMind regression: **754 passed**;
- Python compileall: passed;
- `git diff --check`: passed;
- canonical Alembic head remains `0004`;
- no new schema migration was introduced;
- default `CompositionRoot` remains independent of RFC-064 transaction coordination;
- Runtime and Bootstrap authority remain unchanged;
- canonical `DatabaseRuntime` lifecycle ownership remains unchanged;
- Knowledge and lineage standalone repository behavior remains preserved;
- coordinated Knowledge and lineage participants use one shared SQLAlchemy session;
- transaction-scoped participants flush without independent commit / rollback / close authority;
- coordinator-owned final commit, rollback and session-close behavior is verified;
- exact constraint-aware duplicate classification is shared between standalone and coordinated persistence paths;
- commit-time integrity failures are not heuristically reclassified;
- post-commit cleanup failure has explicit committed-outcome semantics;
- failure of the second participant after the first participant has flushed produces no partial-success result and enters one coordinated rollback path;
- no new ARCH-001 architectural layer was introduced;
- no Domain or Core dependency on transaction infrastructure was introduced;
- no Document-to-Knowledge ingestion, Library, search, AI, external-system atomicity, security or production-readiness capability was introduced.

RFC-064 technical implementation is therefore accepted as implemented.

### Engineering Closure Verification

RFC-064 engineering-memory and architecture closure was committed and pushed at:

`43563a416a24fea7cad4a370a2a4599936c87380`

Exact local / remote closure identity was verified.

Working tree after closure push was clean.

RFC-064 is fully closed.

### Next Exact Action

Perform evidence-based selection of the next architecture workstream from the current repository, project charter, accepted architecture and remaining dependency gaps.

No RFC-065 content is assumed or preselected by RFC-064 closure.

No new RFC implementation is authorized until the selected workstream has an architecture contract that is reviewed, accepted, committed, pushed and passes its implementation-entry Git gate.


---

## RFC-063 — Canonical Document-to-Knowledge Lineage Relational Persistence Adapter Boundary

### Status

Complete.

Post-RFC-062 evidence-based architecture selection: complete.

Selection baseline:

`6261f598a9ccfb9e16075ba14d4847c94ef05503`

Proposed architecture decision:

`AD-049 — Canonical Document-to-Knowledge Lineage Relational Persistence Adapter Boundary`

AD-049 status:

Accepted.

### Selection Rationale

Current accepted architecture now provides:

- canonical immutable `DocumentKnowledgeLineage`;
- persistence-neutral `DocumentKnowledgeLineageRepository`;
- exact directed-pair repository identity;
- canonical relational database runtime and metadata authority;
- canonical relational Knowledge persistence;
- canonical relational Enterprise Document persistence;
- linear Alembic history through revision `0003`.

RFC-062 explicitly deferred relational lineage persistence to a separate future accepted contract.

Document Knowledge ingestion is not selected because coordinated Knowledge and lineage persistence requires explicit atomicity, failure and transaction semantics not yet accepted.

Document Library, parsing, OCR, search, vector, graph, RAG and LLM capabilities remain later application/platform work and SHALL NOT bypass the canonical persistence foundations.

The minimum dependency-completing next step is therefore a relational adapter for the already accepted lineage repository port.

### Objective

Establish the minimum canonical relational persistence adapter for:

`DocumentKnowledgeLineageRepository`

without changing canonical Domain semantics, repository semantics, application boundaries, Runtime authority or default Composition.

### Infrastructure Namespace

RFC-063 SHALL introduce:

`app.infrastructure.document_knowledge_lineage`

The expected production surface is:

- `backend/app/infrastructure/document_knowledge_lineage/__init__.py`;
- `backend/app/infrastructure/document_knowledge_lineage/models.py`;
- `backend/app/infrastructure/document_knowledge_lineage/mapping.py`;
- `backend/app/infrastructure/document_knowledge_lineage/repository.py`.

The package initializer SHALL remain empty unless a separately reviewed public infrastructure API becomes necessary.

### Relational Representation

RFC-063 SHALL introduce:

`DocumentKnowledgeLineageRow`

as the infrastructure-owned relational representation of one canonical lineage pair.

It SHALL contain exactly:

- `document_id`;
- `knowledge_record_id`.

Both columns SHALL use exactly:

`postgresql.UUID(as_uuid=True)`

and SHALL be non-nullable.

This preserves the canonical relational identity representation already used by accepted Knowledge and Enterprise Document persistence.

The row SHALL NOT introduce:

- a separate lineage identifier;
- generated identity;
- timestamp;
- provenance duplication;
- source reference;
- subject fields;
- status;
- approval state;
- trust state;
- revision;
- business cardinality metadata.

### Relational Identity

The canonical relational identity SHALL remain the exact directed pair:

`(document_id, knowledge_record_id)`

The table SHALL use a composite primary key over that exact pair.

Expected primary-key constraint name:

`pk_document_knowledge_lineages`

Neither `document_id` alone nor `knowledge_record_id` alone SHALL be unique.

Distinct rows sharing only one side SHALL remain representable at storage level.

This does not establish Business or Application cardinality policy.

### Table

RFC-063 SHALL introduce the canonical table:

`document_knowledge_lineages`

with exactly the canonical identity columns required by the accepted lineage repository contract.

RFC-063 SHALL NOT introduce an independent surrogate key.

### Foreign-Key Boundary

RFC-063 SHALL NOT introduce relational foreign keys from lineage to:

- `enterprise_documents`;
- `knowledge_records`.

Canonical identity references SHALL be persisted exactly, but cross-domain relational referential-integrity policy remains separately governed.

RFC-063 SHALL NOT perform cross-repository existence validation.

### Mapping Boundary

RFC-063 SHALL introduce explicit mapping between:

`DocumentKnowledgeLineage`

and:

`DocumentKnowledgeLineageRow`

Expected mapper operations:

`lineage_to_row(lineage: DocumentKnowledgeLineage) -> DocumentKnowledgeLineageRow`

and:

`row_to_lineage(row: DocumentKnowledgeLineageRow) -> DocumentKnowledgeLineage`

Mapping SHALL preserve both canonical `EntityId` values exactly.

Mapping SHALL NOT:

- generate identity;
- resolve Documents;
- resolve Knowledge records;
- call repositories;
- infer provenance;
- infer cardinality;
- enrich the Domain value.

### Repository Adapter

RFC-063 SHALL introduce:

`SQLAlchemyDocumentKnowledgeLineageRepository`

implementing the existing:

`DocumentKnowledgeLineageRepository`

The adapter SHALL preserve exactly:

`add(lineage: DocumentKnowledgeLineage) -> None`

and:

`get(document_id: EntityId, knowledge_record_id: EntityId) -> DocumentKnowledgeLineage | None`

No additional public repository operations are authorized.

### Session Ownership

The relational adapter SHALL receive an injected synchronous SQLAlchemy session factory consistent with the accepted canonical database runtime.

For one `add(...)` operation it SHALL:

1. acquire one session;
2. map the canonical lineage value;
3. add the relational row;
4. commit once on success;
5. rollback on write failure;
6. close the session.

For `get(...)` it SHALL:

1. acquire one session;
2. perform exact composite-identity lookup;
3. return canonical lineage when found;
4. return `None` when absent;
5. close the session;
6. perform no commit.

RFC-063 SHALL NOT own engine creation or `DatabaseRuntime`.

### Duplicate Classification

The relational adapter SHALL translate only the database failure corresponding to violation of:

`pk_document_knowledge_lineages`

into:

`DocumentKnowledgeLineageAlreadyExistsError`

For PostgreSQL, duplicate classification SHALL require the accepted unique-violation SQLSTATE together with the exact canonical constraint identity.

Unrelated integrity or database failures SHALL propagate and SHALL NOT be misclassified as lineage duplicates.

### Metadata Authority

`DocumentKnowledgeLineageRow` SHALL participate in the existing canonical SQLAlchemy metadata authority.

RFC-063 SHALL NOT create a second metadata root.

### Alembic Migration

RFC-063 SHALL introduce append-only Alembic revision:

`0004`

with:

`down_revision = "0003"`

Expected migration file:

`backend/migrations/versions/0004_document_knowledge_lineages.py`

RFC-063 technical implementation SHALL also modify:

`backend/migrations/env.py`

only as required to explicitly load `DocumentKnowledgeLineageRow` into the existing canonical SQLAlchemy metadata authority.

Revision `0004` SHALL create only the schema required for canonical lineage relational persistence.

Alembic metadata registration SHALL explicitly ensure `DocumentKnowledgeLineageRow` participates in canonical metadata.

Downgrade SHALL remove only schema introduced by revision `0004`.

### Application Boundary

RFC-063 SHALL NOT introduce or modify:

- `KnowledgeCaptureApplicationService`;
- `EnterpriseDocumentRegistrationApplicationService`;
- Document Knowledge ingestion;
- application transaction orchestration;
- shared Unit of Work;
- compensation behavior;
- retry policy.

### Composition and Runtime Boundary

RFC-063 SHALL NOT make lineage persistence part of default `CompositionRoot`.

It SHALL NOT modify:

- Runtime lifecycle authority;
- Bootstrap authority;
- mandatory capability readiness;
- database availability policy.

Production composition requires a separately accepted application capability when needed.

### Explicitly Deferred

RFC-063 SHALL NOT establish:

- Document Knowledge ingestion;
- cross-repository atomicity;
- shared transaction orchestration;
- compensation across Knowledge and lineage repositories;
- partial-failure recovery;
- one-sided lineage query;
- reverse traversal;
- list/search/filter/pagination;
- Business/Application cardinality;
- corroboration;
- primary-source semantics;
- multi-source derivation;
- Document Library;
- binary storage;
- parsing;
- OCR;
- chunking;
- revision lifecycle;
- semantic search;
- vector persistence;
- graph persistence;
- Neo4j;
- RAG;
- LLM invocation;
- HTTP transport;
- authentication;
- authorization;
- RBAC;
- Cybersecurity approval;
- production-readiness claims.

### Expected TDD Verification

RFC-063 technical implementation, if later authorized, SHALL verify at minimum:

- canonical lineage maps to relational row exactly;
- relational row maps back to canonical lineage exactly;
- composite identity is preserved;
- no surrogate lineage identity exists;
- same exact pair conflicts;
- distinct pairs sharing one side remain permitted at persistence level;
- exact pair `get(...)` returns canonical lineage;
- absent pair returns `None`;
- unrelated integrity failures are not classified as duplicate lineage;
- one successful add commits exactly once;
- failed add rolls back;
- sessions close correctly;
- read path performs no commit;
- no Document repository lookup occurs;
- no Knowledge repository lookup occurs;
- no Domain or application persistence leakage occurs;
- canonical metadata includes lineage row;
- Alembic history becomes `0001 → 0002 → 0003 → 0004`;
- default Composition remains unchanged;
- Runtime and Bootstrap remain unchanged;
- full regression remains green.

### Contract Acceptance Review

Outcome:

**PASS — RFC-063 / AD-049 architecture contract accepted.**

The review confirmed:

- canonical `DocumentKnowledgeLineage` Domain ownership remains unchanged;
- `DocumentKnowledgeLineageRepository` remains unchanged;
- relational identity is exactly `(document_id, knowledge_record_id)`;
- both identity columns use `postgresql.UUID(as_uuid=True)` and are non-nullable;
- no surrogate lineage identity is introduced;
- neither identity side alone becomes unique;
- no relational foreign keys are introduced;
- duplicate translation requires PostgreSQL SQLSTATE `23505` and exact constraint `pk_document_knowledge_lineages`;
- canonical SQLAlchemy metadata authority remains singular;
- `backend/migrations/env.py` may change only for explicit lineage-model registration;
- Alembic revision `0004` must extend `0003`;
- no Document or Knowledge repository lookup enters the adapter;
- no Document Knowledge ingestion enters scope;
- no cross-repository atomicity or transaction orchestration is implied;
- default Composition, Runtime and Bootstrap authority remain unchanged;
- Document Library, parsing, OCR, search, vector, graph, RAG, LLM and production security remain deferred.

### Technical Completion

Contract commit:

`dccc1987d1ade0308156bc11e22fc5a659bbfc8f`

Technical implementation commit:

`49fb300aa77cef82bcbb3c92b40b6deeb4333c51`

Implementation-entry Git gate: satisfied.

Remote technical push: verified.

Exact local/remote technical commit identity: verified.

Working tree after technical push: clean.

Implemented canonical relational persistence surface:

- `DocumentKnowledgeLineageRow`;
- explicit `lineage_to_row(...)` and `row_to_lineage(...)`;
- `SQLAlchemyDocumentKnowledgeLineageRepository`;
- canonical table `document_knowledge_lineages`;
- exact composite primary key `(document_id, knowledge_record_id)`;
- exact constraint `pk_document_knowledge_lineages`;
- canonical Alembic revision `0004`;
- canonical metadata registration in `backend/migrations/env.py`.

Verified technical baseline:

- RFC-063 focused regression: 35 passed;
- RFC-063 architecture / lineage guard verification: 35 passed;
- impacted Document + Knowledge + lineage persistence regression: 103 passed;
- persistence migration regression: 18 passed;
- full PlantMind regression: 717 passed;
- Python compileall: passed;
- `git diff --check`: passed;
- canonical Alembic head: `0004`;
- migration lineage: `0001 → 0002 → 0003 → 0004`;
- forbidden-coupling check: clean;
- default Composition remains unchanged;
- Runtime and Bootstrap authority remain unchanged.

### Post-RFC-063 System and Architecture Integrity Review

Outcome:

**PASS — architecture remains sound and development may continue.**

The review confirmed:

- RFC-063 implementation matches accepted AD-049;
- canonical `DocumentKnowledgeLineage` Domain ownership remains unchanged;
- canonical `DocumentKnowledgeLineageRepository` remains unchanged;
- relational identity remains exactly the directed pair `(document_id, knowledge_record_id)`;
- no surrogate lineage identity was introduced;
- neither identity side alone became unique;
- no relational foreign keys were introduced;
- no Document or Knowledge repository lookup entered the adapter;
- duplicate translation is restricted to PostgreSQL SQLSTATE `23505` plus exact constraint `pk_document_knowledge_lineages`;
- canonical SQLAlchemy metadata authority remains singular;
- Alembic history remains linear with one canonical head at `0004`;
- `KnowledgeCaptureApplicationService` remains unchanged;
- `EnterpriseDocumentRegistrationApplicationService` remains unchanged;
- no Document Knowledge ingestion application boundary was introduced;
- no cross-repository atomicity or shared transaction orchestration was introduced;
- default `CompositionRoot` remains free of lineage relational persistence;
- Runtime and Bootstrap authority remain unchanged;
- no production security, Cybersecurity approval or production-readiness claim is implied;
- no production-code architecture redesign is required.

Still explicitly deferred:

- coordinated Document-to-Knowledge ingestion;
- cross-repository atomicity;
- shared transaction orchestration;
- rollback or compensation across repositories;
- retry and partial-failure recovery;
- one-sided lineage retrieval and reverse traversal;
- Business/Application lineage cardinality policy;
- corroboration and primary-source semantics;
- multi-source derivation policy;
- Document Library;
- binary storage;
- parsing, OCR and chunking;
- Document revision lifecycle;
- semantic search;
- vector persistence;
- graph persistence and Neo4j;
- RAG and LLM capability;
- HTTP transport;
- production authentication, authorization and RBAC;
- Cybersecurity approval and production-readiness claims.

RFC-063 engineering-memory closure is complete.

Closure commit:

`30c494ec790db5e38d1f579de3b131664925e58a`

Exact local/remote closure identity: verified.

Working tree after closure push: clean.

RFC-063 is fully closed.

### Contract State

RFC-063: Complete.

AD-049: Accepted.

Engineering-memory closure:

complete, committed and pushed at `30c494ec790db5e38d1f579de3b131664925e58a`.

Exact local/remote closure identity: verified.

Working tree after closure push: clean.

### Next Exact Action

Perform evidence-based selection of the next architecture workstream from current repository, project-charter and architecture evidence.

Do not assume RFC-064 content before that selection review.

No new RFC implementation is authorized until its architecture contract is reviewed, accepted, committed, pushed and its implementation-entry Git gate is satisfied.

---

## RFC-062 — Canonical Document-to-Knowledge Lineage Repository Foundation Boundary

### Status

Complete.

RFC-062 / AD-048 Contract Acceptance Review: passed.

Implementation-entry Git gate: satisfied.

Technical implementation:

complete and verified at `859f9e2fd05404ad566e6f87d3d9cd1dddd2003a`.

Post-RFC-062 system and architecture integrity review:

complete — PASS.

Engineering-memory closure:

complete, committed and pushed at `713fac8d307eb97dd07d8bbb8eaa4f0c0aca51d0`.

Exact local/remote closure identity: verified.

Working tree after closure push: clean.

Post-RFC-061 evidence-based architecture selection: complete.

Selection baseline:

`1fc8dda3adde6b78b46029df0767534ef24c9636`

Proposed architecture decision:

`AD-048 — Canonical Document-to-Knowledge Lineage Repository Foundation Boundary`

AD-048 status:

Accepted.

### Objective

Establish the minimum persistence-neutral repository contract for canonical `DocumentKnowledgeLineage` values without introducing relational persistence, application ingestion, query expansion or hidden business cardinality semantics.

### Architecture Evidence

Current accepted architecture establishes:

- canonical `EnterpriseDocumentRepository` as a persistence-neutral Document repository port;
- canonical `KnowledgeRecordRepository` as a persistence-neutral Knowledge repository port;
- repository conflicts as repository-level exceptions rather than Domain validation errors;
- `DocumentKnowledgeLineage` as an immutable directed canonical identity relation;
- no accepted lineage repository or persistence contract;
- no accepted lineage relational schema or migration;
- no accepted Document Knowledge ingestion boundary.

RFC-061 explicitly deferred lineage repository, persistence, uniqueness and duplicate semantics to future explicit architecture.

### Proposed Repository Namespace

RFC-062 SHALL introduce:

`app.document_knowledge_lineage.repository`

The package initializer:

`app.document_knowledge_lineage.__init__`

SHALL remain empty.

RFC-062 SHALL NOT introduce a generic lineage framework or repository shared by unrelated future relationship types.

### Proposed Repository Contract

RFC-062 SHALL introduce:

`DocumentKnowledgeLineageAlreadyExistsError`

and:

`DocumentKnowledgeLineageRepository`

The repository SHALL be persistence-neutral.

It SHALL expose exactly:

`add(lineage: DocumentKnowledgeLineage) -> None`

and:

`get(document_id: EntityId, knowledge_record_id: EntityId) -> DocumentKnowledgeLineage | None`

### Duplicate Identity Semantics

Repository duplicate classification SHALL use the exact directed canonical identity pair:

`(document_id, knowledge_record_id)`

Re-adding the same directed pair SHALL raise:

`DocumentKnowledgeLineageAlreadyExistsError`

The repository SHALL NOT silently overwrite an existing canonical lineage relation.

Neither `document_id` alone nor `knowledge_record_id` alone SHALL become repository duplicate identity under RFC-062.

Therefore, at repository-storage level, distinct lineage pairs sharing one side are not duplicates and MAY coexist.

This storage capability does not establish that such relationships are valid, authorized or meaningful at Business or Application level.

RFC-062 does not establish:

- business one-to-many policy;
- business many-to-one policy;
- corroboration semantics;
- primary-source semantics;
- merge semantics;
- multi-source derivation authorization.

Those higher-level semantics remain separately governed and require explicit future architecture.

### Exact Retrieval Semantics

`get(...)` SHALL perform exact-pair retrieval only.

For an existing exact pair, it SHALL return the canonical `DocumentKnowledgeLineage`.

For an absent exact pair, it SHALL return `None`.

RFC-062 SHALL NOT introduce:

- retrieval by Document alone;
- retrieval by Knowledge alone;
- reverse traversal;
- list;
- find;
- search;
- filter;
- query;
- pagination;
- ranking.

### Domain Ownership Boundary

RFC-062 SHALL reuse:

- `EntityId`;
- `DocumentKnowledgeLineage`.

The repository SHALL NOT:

- generate identity;
- construct Documents;
- construct Knowledge records;
- modify lineage values;
- duplicate lineage Domain validation;
- resolve referenced Document identity;
- resolve referenced Knowledge identity;
- call Document repositories;
- call Knowledge repositories.

Referenced-entity existence validation is not repository-port ownership under RFC-062.

### Dependency Boundary

The canonical repository port SHALL depend only on the minimum canonical contracts required to express its interface.

It SHALL NOT depend on:

- SQLAlchemy;
- Psycopg;
- infrastructure;
- application services;
- Runtime;
- Bootstrap;
- Composition;
- FastAPI;
- parser;
- OCR;
- search;
- vector;
- graph;
- RAG;
- LLM.

### Persistence Boundary

RFC-062 SHALL introduce no:

- SQLAlchemy lineage row;
- relational lineage table;
- foreign key;
- unique database constraint;
- index;
- Alembic migration;
- Session ownership;
- transaction;
- commit;
- rollback;
- database-runtime composition.

Canonical Alembic head SHALL remain:

`0003`

Relational lineage persistence requires a separate future accepted contract.

### Application and Ingestion Boundary

RFC-062 SHALL NOT introduce or modify:

- `KnowledgeCaptureApplicationService`;
- `EnterpriseDocumentRegistrationApplicationService`;
- Document Knowledge ingestion;
- application transaction orchestration;
- compensation behavior.

A future ingestion contract SHALL preserve canonical Document identity, Knowledge identity and lineage responsibilities without bypassing accepted boundaries.

### Deferred Capabilities

RFC-062 SHALL NOT introduce:

- Document Library;
- binary/file storage;
- parsing;
- OCR;
- chunking;
- revision lifecycle;
- semantic search;
- vector persistence;
- graph persistence;
- Neo4j;
- RAG;
- LLM invocation;
- HTTP transport;
- industrial integration;
- authentication;
- authorization;
- RBAC;
- Cybersecurity approval;
- production-readiness claims.

### Expected Technical Surface

If the RFC-062 contract is later accepted and its implementation-entry Git gate is satisfied, the expected production surface is:

- `backend/app/document_knowledge_lineage/__init__.py`;
- `backend/app/document_knowledge_lineage/repository.py`.

Expected verification surface:

- repository contract tests;
- architecture guardrails for dependency and operation containment.

No existing production implementation is expected to require modification.

No migration is expected.

### TDD Acceptance Requirements

Technical implementation SHALL demonstrate at minimum:

- repository port is abstract;
- exact abstract operation set is `add` and `get`;
- repository conflict exception is not a `DomainException`;
- canonical lineage value is preserved exactly;
- absent exact pair returns `None`;
- duplicate exact directed pair raises repository conflict;
- duplicate add does not silently overwrite;
- neither side alone is treated as repository duplicate identity;
- no entity identity is generated;
- no referenced entity repository lookup occurs;
- no persistence technology enters the repository port;
- no search or CRUD expansion appears;
- default Composition remains unchanged;
- Runtime and Bootstrap remain unchanged;
- canonical Alembic head remains `0003`.

### Contract Acceptance

RFC-062 / AD-048 Contract Acceptance Review: passed.

No production implementation is authorized by contract acceptance alone.

### Technical Completion

Contract commit:

`89576ccc41cc84d462841d55728663813ad7f230`

Technical implementation commit:

`859f9e2fd05404ad566e6f87d3d9cd1dddd2003a`

Implementation-entry Git gate: satisfied.

Remote technical push: verified.

Exact local/remote technical identity: verified.

Working tree after technical push: clean.

Verified technical baseline:

- canonical `DocumentKnowledgeLineageRepository`;
- repository-level `DocumentKnowledgeLineageAlreadyExistsError`;
- exactly `add(...)` and `get(...)`;
- exact directed-pair duplicate identity;
- distinct pairs sharing one side remain non-duplicate at repository-storage level;
- focused RFC-062 verification: 18 passed;
- full PlantMind regression: 682 passed;
- canonical Alembic head: `0003`;
- persistence / migration lineage leak check: clean;
- default Composition lineage check: clean;
- `git diff --check`: passed.

### Post-RFC-062 System and Architecture Integrity Review

Outcome:

**PASS — architecture remains sound and development may continue.**

The review confirmed:

- RFC-062 implementation matches accepted AD-048;
- the repository port remains persistence-neutral;
- canonical lineage Domain ownership remains unchanged;
- no SQLAlchemy, Psycopg or database ownership entered the repository port;
- no lineage relational persistence or migration was introduced;
- no cross-repository Document or Knowledge existence lookup was introduced;
- no Document Knowledge ingestion capability was introduced;
- Knowledge Capture and Document Registration responsibilities remain unchanged;
- default CompositionRoot remains free of the lineage repository;
- Runtime and Bootstrap authority remain unchanged;
- canonical Alembic head remains `0003`;
- storage-level duplicate semantics remain separate from Business/Application cardinality policy;
- atomicity, transaction orchestration and partial-failure recovery remain intentionally deferred;
- no production security, Cybersecurity approval or production-readiness claim is implied;
- no production-code architecture redesign is required.

RFC-062 engineering-memory closure is complete.

Closure commit:

`713fac8d307eb97dd07d8bbb8eaa4f0c0aca51d0`

Exact local/remote closure identity: verified.

Working tree after closure push: clean.

RFC-062 is fully closed.

### Contract State

RFC-062: Complete.

AD-048: Accepted.

### Next Exact Action

Perform evidence-based selection of the next architecture workstream from current repository, project-charter and architecture evidence.

Do not assume RFC-063 content before that selection review.

No new RFC implementation is authorized until its architecture contract is reviewed, accepted, committed, pushed and its implementation-entry Git gate is satisfied.


## RFC-061 — Canonical Document-to-Knowledge Lineage Foundation Boundary

### Status

Complete.

Post-RFC-060 evidence-based architecture selection: complete.

RFC-060 engineering-memory closure baseline:

`7fff8ab3b350417ce25a1afd0308f2b570629afc`

Architecture decision:

`AD-047 — Canonical Document-to-Knowledge Lineage Foundation Boundary`

AD-047 status: Accepted.

RFC-061 / AD-047 Contract Acceptance Review: passed.

Contract commit:

`7881668908226bf42815236b7e080e27b46c41bd`

Technical implementation:

complete and verified at `903382f121198091ac7ad31e2928d3769c04cb32`.

Implementation-entry Git gate: satisfied.

Post-RFC-061 system and architecture integrity review:
complete — PASS.

Engineering-memory closure:

complete, committed and pushed at `0b268950558ab46a6cf6f3dedf9ee83fa6a33ef1`.

Exact local/remote closure identity: verified.

Working tree after closure push: clean.

### Objective

Establish the minimum canonical domain contract that can preserve the identity relationship between one canonical `EnterpriseDocument` and one canonical `KnowledgeRecord` derived from that Document.

RFC-061 exists because external Document source references are traceability values rather than canonical PlantMind identity and MAY be shared by distinct canonical Documents.

Document-derived Knowledge SHALL therefore not rely on `source_reference` alone when future architecture requires canonical Document-to-Knowledge lineage.

### Architecture Evidence

Accepted architecture establishes:

- `EnterpriseDocument.id` as canonical Document identity;
- `KnowledgeRecord.id` as canonical Knowledge identity;
- `DocumentSource.source_reference` as external traceability rather than identity;
- `KnowledgeProvenance` as origin metadata consisting of source type, source reference and capture time;
- `KnowledgeSubject` as the optional primary contextual reference of Knowledge;
- cross-record derivation and provenance relationships as a separately governed future contract.

The previously considered Document Knowledge Ingestion boundary was rejected before commit because merely copying Document source metadata into `KnowledgeCaptureRequest` would lose canonical Document identity and collapse into a thin translation wrapper.

### Canonical Domain Contract

RFC-061 SHALL introduce:

`DocumentKnowledgeLineage`

under:

`app.domain.document_knowledge_lineage`

The canonical type SHALL be an immutable domain value representing one directed relationship:

`EnterpriseDocument -> KnowledgeRecord`

It SHALL contain exactly:

- `document_id: EntityId`;
- `knowledge_record_id: EntityId`.

The relationship means:

the identified canonical Knowledge record is derived from the identified canonical Enterprise Document.

### Identity Boundary

`document_id` SHALL contain the existing canonical `EnterpriseDocument.id`.

`knowledge_record_id` SHALL contain the existing canonical `KnowledgeRecord.id`.

RFC-061 SHALL use the shared canonical `EntityId`.

RFC-061 SHALL NOT introduce:

- `DocumentId`;
- `KnowledgeId`;
- `LineageId`;
- a new identity generator;
- a global identity service;
- a database-generated identity.

The lineage relation itself SHALL NOT receive a separate entity identity under RFC-061.

### Domain Ownership Boundary

`DocumentKnowledgeLineage` SHALL reference canonical identity without taking ownership of either Document or Knowledge.

RFC-061 SHALL NOT:

- construct an `EnterpriseDocument`;
- construct a `KnowledgeRecord`;
- modify either canonical entity;
- duplicate Document validation;
- duplicate Knowledge validation;
- resolve either identity from a repository.

The contract SHALL validate only that both supplied identifiers are canonical `EntityId` values.

Invalid identifier types SHALL fail through existing `DomainException` semantics.

### Dependency Boundary

The production domain module SHALL depend only on the minimum shared domain primitives required to express the relation.

It SHALL NOT depend on:

- Document repository contracts;
- Knowledge repository contracts;
- application services;
- infrastructure;
- SQLAlchemy;
- Psycopg;
- Runtime;
- Bootstrap;
- Composition;
- API;
- parser;
- search;
- vector;
- graph;
- RAG;
- LLM.

The lineage domain contract SHALL NOT require repository or database access for validation.

### Direction Semantics

RFC-061 defines one explicit direction:

`document_id -> knowledge_record_id`

The source side is the canonical Document.

The derived side is the canonical Knowledge record.

RFC-061 SHALL NOT automatically define a reverse ownership relationship.

A caller MAY navigate or index the relation differently in a future repository or graph boundary, but those persistence and query semantics are not part of RFC-061.

### Provenance Separation

RFC-061 SHALL NOT modify:

`KnowledgeProvenance`

Existing Knowledge provenance remains:

- source type;
- source reference;
- capture timestamp.

Document-to-Knowledge lineage is a canonical identity relationship and SHALL remain distinct from external-source provenance.

RFC-061 SHALL NOT:

- replace Knowledge provenance;
- encode `document_id` into `source_reference`;
- reinterpret `source_reference` as Document identity;
- add Document identity to `KnowledgeProvenance`;
- modify capture-time semantics.

A future ingestion boundary MAY use both canonical lineage and existing provenance under its own accepted contract.

### Knowledge Subject Separation

RFC-061 SHALL NOT modify:

`KnowledgeSubject`

The Knowledge subject remains the optional primary contextual reference of the Knowledge record.

A Document that produced Knowledge SHALL NOT automatically become the Knowledge subject merely because lineage exists.

For example, Knowledge derived from a procedure Document MAY still have equipment as its primary Knowledge subject.

Document lineage and Knowledge subject are separate semantics.

### Source Reference Boundary

`DocumentSource.source_reference` remains external/source-system traceability only.

RFC-061 SHALL NOT interpret it as:

- canonical Document identity;
- canonical Knowledge identity;
- lineage identity;
- global uniqueness;
- a repository alternate key;
- a deduplication key;
- proof of source authenticity;
- proof of document approval.

Equal source references MAY continue to exist on different canonical Document identities.

Canonical lineage SHALL use canonical entity identity rather than external source-reference equality.

### Cardinality Boundary

One `DocumentKnowledgeLineage` value represents one Document-to-Knowledge identity pair.

RFC-061 SHALL NOT decide global cardinality.

It SHALL NOT establish whether:

- one Document may derive many Knowledge records;
- one Knowledge record may derive from multiple Documents;
- duplicate lineage pairs are allowed in persistence;
- one source is primary;
- multiple sources are corroborating;
- multiple derivations must be merged.

Those semantics require future explicit architecture.

RFC-053 restrictions on inferred multi-source provenance remain authoritative.

### Equality and Uniqueness Boundary

In-memory immutable value semantics SHALL NOT be interpreted as database uniqueness.

RFC-061 SHALL NOT introduce:

- unique constraints;
- composite database keys;
- duplicate exceptions;
- deduplication behavior;
- repository prechecks.

Future repository and persistence contracts SHALL explicitly define duplicate and uniqueness semantics.

### Persistence Boundary

RFC-061 is domain-foundation only.

It SHALL NOT introduce:

- `DocumentKnowledgeLineageRepository`;
- SQLAlchemy lineage models;
- relational tables;
- foreign keys;
- indexes;
- database constraints;
- migrations;
- Session ownership;
- transactions;
- commit or rollback behavior.

Canonical Alembic head SHALL remain:

`0003`

A future persistence-neutral lineage repository requires a separate accepted contract.

### Knowledge Capture Boundary

RFC-061 SHALL NOT modify:

`KnowledgeCaptureApplicationService`

or:

`KnowledgeCaptureRequest`

RFC-061 SHALL NOT yet call Knowledge Capture.

RFC-061 SHALL NOT:

- construct Knowledge records;
- generate Knowledge identity;
- establish capture time;
- persist Knowledge;
- perform Document-to-Knowledge ingestion.

The accepted Knowledge Capture boundary remains unchanged.

### Document Registration Boundary

RFC-061 SHALL NOT modify or call:

`EnterpriseDocumentRegistrationApplicationService`

Document registration remains separately owned by RFC-060 / AD-046.

RFC-061 does not create, register or persist Documents.

### Ingestion Boundary

RFC-061 SHALL NOT introduce:

`DocumentKnowledgeIngestionApplicationService`

Document Knowledge ingestion remains deferred until canonical lineage foundations necessary to preserve Document identity are accepted and implemented.

A future ingestion contract SHALL consume:

- accepted canonical Document identity;
- accepted Knowledge Capture boundary;
- accepted Document-to-Knowledge lineage contracts;

without bypassing their responsibilities.

### Parsing and Extraction Boundary

RFC-061 SHALL NOT introduce:

- PDF parsing;
- Word parsing;
- spreadsheet parsing;
- OCR;
- text extraction;
- table extraction;
- section detection;
- chunking;
- automatic metadata extraction;
- automatic classification.

Existing empty parser seams remain unpromoted.

### Document Library Boundary

RFC-061 is not a Document Library.

It SHALL NOT introduce:

- upload;
- download;
- binary storage;
- blobs;
- filesystem storage;
- object storage;
- catalogue;
- browse;
- retrieval API;
- permissions;
- ownership;
- retention;
- archival;
- synchronization.

### Revision Boundary

RFC-061 remains revision-neutral.

It SHALL NOT establish:

- Document revision identity;
- version numbers;
- revision numbers;
- current revision;
- supersession;
- replacement;
- revision history.

Future revision semantics SHALL determine how lineage interacts with document revisions if and when revision architecture is accepted.

### Search, Graph and AI Boundary

RFC-061 SHALL NOT introduce:

- keyword search;
- full-text search;
- semantic search;
- ranking;
- embeddings;
- vector persistence;
- Qdrant;
- graph persistence;
- Neo4j;
- graph traversal;
- RAG;
- prompts;
- LLM invocation;
- summarization;
- autonomous agents.

The existence of a canonical lineage value does not establish Knowledge Graph capability.

### Trust Boundary

Document-to-Knowledge lineage means only that PlantMind records a derivation relationship between canonical identities.

It does not establish:

- source authenticity;
- correctness;
- trust;
- document approval;
- knowledge approval;
- compliance approval;
- safety approval;
- authorization.

Knowledge provenance remains separate from operational trust.

### Composition and Runtime Boundary

RFC-061 SHALL NOT modify:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`;
- Runtime;
- Bootstrap;
- Health;
- readiness;
- request admission;
- mandatory-capability policy.

The domain value requires no default composition.

### Transport and Integration Boundary

RFC-061 SHALL introduce no:

- FastAPI routes;
- HTTP endpoints;
- transport DTOs;
- message bus;
- event publication;
- PI integration;
- DCS integration;
- OPC UA integration;
- CMMS integration;
- SAP integration;
- File Server integration;
- SharePoint integration;
- document-control integration.

AD-009 source-neutral architecture remains authoritative.

### Security Boundary

RFC-061 establishes no:

- authentication;
- authorization;
- RBAC;
- principal identity;
- actor audit;
- Active Directory;
- LDAP;
- MFA;
- Cybersecurity approval.

No production-readiness claim is implied.

### Expected Technical Surface

If implementation is later authorized, the expected production surface is exactly:

- `backend/app/domain/document_knowledge_lineage.py`.

Expected verification surface:

- `tests/domain/test_document_knowledge_lineage.py`;
- minimum architecture guardrails required to verify domain dependency direction.

No existing production file is expected to change.

No migration is expected.

Any additional production file requires explicit evidence and review.

### TDD Acceptance Requirements

Technical implementation SHALL be test-driven.

Tests SHALL demonstrate at minimum:

- `DocumentKnowledgeLineage` is immutable;
- valid canonical Document and Knowledge `EntityId` values are preserved exactly;
- non-`EntityId` Document identity is rejected with `DomainException`;
- non-`EntityId` Knowledge identity is rejected with `DomainException`;
- no identity is generated by the lineage value;
- no repository access occurs;
- no database access occurs;
- no Document or Knowledge entity reconstruction occurs;
- the production module introduces no application-service dependency;
- the production module introduces no repository dependency;
- the production module introduces no SQLAlchemy or Psycopg dependency;
- the production module does not alter `KnowledgeProvenance`;
- the production module does not alter `KnowledgeSubject`;
- the production module does not use Document source reference as canonical lineage identity;
- default Composition and Runtime behavior remain unchanged;
- canonical Alembic head remains `0003`.

### Contract Acceptance Gate

RFC-061 / AD-047 Contract Acceptance Review: passed.

The review confirmed absence of:

- source-reference-as-identity semantics;
- Knowledge provenance redesign;
- forced Document identity as Knowledge subject;
- competing entity identity types;
- generated lineage identity;
- repository ownership;
- persistence ownership;
- migration ownership;
- ingestion ownership;
- parser/OCR ownership;
- revision ownership;
- Document Library ownership;
- search/vector/graph/RAG/LLM ownership;
- default-composition coupling;
- Runtime-authority expansion;
- unsupported security or production-readiness claims.

### Current Contract State

RFC-061: Technically Complete.

AD-047: Accepted.

Contract commit:

`7881668908226bf42815236b7e080e27b46c41bd`

Technical implementation commit:

`903382f121198091ac7ad31e2928d3769c04cb32`

Implementation-entry Git gate: satisfied.

Post-RFC-061 system and architecture integrity review:
PASS.

Focused RFC-061 verification: 11 passed.

Domain regression: 131 passed.

Document + Knowledge impacted regression: 233 passed.

Full PlantMind regression: 664 passed.

Python compilation: passed.

Canonical Alembic head: `0003`.

Exact local/remote technical commit identity: verified.

Technical working tree before documentation closure: clean.

Engineering-memory documentation closure is complete.

Closure commit:

`0b268950558ab46a6cf6f3dedf9ee83fa6a33ef1`

Exact local/remote closure identity: verified.

Working tree after closure push: clean.

RFC-061 is fully closed.

### Next Exact Action

Perform evidence-based selection of the next architecture workstream from current repository, project-charter and architecture evidence.

No new RFC implementation is authorized until its architecture contract is reviewed, accepted, committed, pushed and implementation-entry Git verification succeeds.


---

## RFC-060 — Canonical Enterprise Document Registration Application Boundary

### Status

Technically Complete.

Post-RFC-059 system and architecture integrity review: complete — PASS.

Evidence-based RFC-060 workstream selection: complete.

Architecture decision:

`AD-046 — Canonical Enterprise Document Registration Application Boundary`

AD-046 status: Accepted.

RFC-060 / AD-046 Contract Acceptance Review: passed.

Technical implementation: complete and verified at `c3ffb25849d6ae7b3fe26264cdf326ae5b3f86c7`.

Implementation-entry Git gate: satisfied.

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

RFC-060: Technically Complete.

AD-046: Accepted.

Contract acceptance: passed.

Contract commit:

`cda5e57eeabfa3699f960586982899cdf0ff9757`

Implementation-entry Git gate: satisfied.

Technical implementation commit:

`c3ffb25849d6ae7b3fe26264cdf326ae5b3f86c7`

Technical verification:

- RFC-060 focused verification: 16 passed;
- Document + Knowledge boundary verification: 77 passed;
- full PlantMind regression: 653 passed;
- Python compilation: passed;
- canonical Alembic head: `0003`;
- remote technical push: verified;
- exact local/remote technical identity: verified;
- working tree after technical push: clean.

Post-RFC-060 system and architecture integrity review:

PASS.

### Next Exact Action

Complete and commit the RFC-060 engineering-memory and post-implementation architecture-review closure.

After documentation closure is pushed and local/remote identity is verified, perform evidence-based selection of the next architecture workstream.

Do not preselect, draft or implement RFC-061 before that selection review.
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


---

## RFC-068 Final Source-of-Truth Reconciliation Verification

### Status

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Engineering-memory closure commit:

`bcf2fc8b20c866584db8596341c8abdb965358ea`

Post-closure Source-of-Truth reconciliation commit:

`074e534e0d97a927b6434341ad5d1c8671bfa381`

Final reconciliation Git verification:

- reconciliation commit parent: `bcf2fc8b20c866584db8596341c8abdb965358ea`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**.

Verified technical baseline remains:

- full PlantMind regression: **866 passed**;
- canonical Alembic head: `0004`.

AD-054 remains the latest Accepted Architecture Decision.

No AD-055 is created by this verification record.

No successor RFC or architecture workstream is selected or preselected.

### Successor Governance

No successor RFC or architecture workstream is selected or preselected by
this final verification record.

Before separate evidence-based successor-workstream selection begins, the
Final Verification record SHALL pass its external Git gate:

1. complete five-document review;
2. preserve committed Engineering Journal history;
3. preserve committed Architecture Decision history;
4. confirm documentation-only scope;
5. pass `git diff --check`;
6. commit the reviewed five-document record;
7. push the commit;
8. verify exact local / tracking / remote identity;
9. verify a clean working tree.

This external Git gate does not require another RFC-068 Source-of-Truth
reconciliation or final-verification commit.

After that gate passes, evidence-based successor-workstream selection may
begin only as a separate governed activity.

No production-readiness, production-security or Cybersecurity-approval
claim is introduced.

---

## RFC-069 Architecture Contract Accepted State

**Canonical Document Content Relational Persistence Adapter Boundary**

Verified workstream-selection commit:

`5d7794352029576e0b62c2ac8cbfa248fe11961d`

Current phase:

**ARCHITECTURE CONTRACT ACCEPTED — ACCEPTED-CONTRACT GIT GATE PENDING; IMPLEMENTATION NOT AUTHORIZED**

Architecture Decision:

**AD-055 — ACCEPTED**

Final refined contract review:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

### Contract Objective

Introduce only the minimum canonical relational Infrastructure adapter required
to implement the accepted descriptor-only `DocumentContentRepository`.

The existing Domain and persistence-neutral repository contracts remain
authoritative and unchanged.

### Accepted Canonical Infrastructure Ownership

`app.infrastructure.document_content`

Accepted production surface after separate implementation authorization:

- `backend/app/infrastructure/document_content/__init__.py`
- `backend/app/infrastructure/document_content/duplicate_classification.py`
- `backend/app/infrastructure/document_content/mapping.py`
- `backend/app/infrastructure/document_content/models.py`
- `backend/app/infrastructure/document_content/repository.py`

The package initializer remains empty.

### Accepted Relational Contract

Row:

`DocumentContentDescriptorRow`

Table:

`document_content_descriptors`

Exact descriptor columns:

1. `document_id`
   - PostgreSQL UUID with `as_uuid=True`;
   - non-null;
   - sole primary-key identity.

2. `media_type`
   - SQLAlchemy `String`;
   - non-null.

3. `byte_length`
   - SQLAlchemy `BigInteger`;
   - non-null.

4. `digest`
   - SQLAlchemy `String`;
   - non-null.

Primary-key constraint:

`pk_document_content_descriptors`

The accepted contract introduces no surrogate `id`, no `DocumentContentId`,
no digest identity or uniqueness, no additional unique constraint, no
Enterprise Document foreign key, no cascade rule, no database-generated
identity, no revision/version column and no binary/storage-location column.

The absence of an Enterprise Document foreign key is intentional. RFC-069 does
not decide cross-boundary existence, lifecycle or transaction-coordination
semantics.

### Accepted Mapping Contract

Explicit mapping SHALL reconstruct and preserve the canonical:

- `EntityId`;
- `DocumentContentMediaType`;
- `DocumentContentDigest`;
- `DocumentContentDescriptor`.

The relational representation SHALL NOT replace Domain validation.

### Accepted Repository Adapter Contract

Concrete adapter:

`SQLAlchemyDocumentContentRepository`

Implements:

`DocumentContentRepository`

Session dependency:

`Callable[[], Session]`

`add(descriptor)` SHALL create one session, map and add one row, commit once on
success, perform no pre-read duplicate check and perform no Enterprise Document
repository lookup.

On persistence failure, the adapter SHALL attempt rollback and SHALL close the
session on all paths.

Failure precedence SHALL match accepted relational-adapter precedent:

- if persistence fails and rollback succeeds, the original persistence failure
  remains authoritative unless session close itself fails;
- if rollback fails, the rollback failure SHALL be raised from the original
  persistence failure;
- if session close fails while an earlier failure is active, the close failure
  SHALL propagate with that earlier failure preserved in exception context.

RFC-069 SHALL NOT silently replace, swallow or text-classify unrelated database
failures.

Only the exact combination of SQLSTATE `23505` and constraint
`pk_document_content_descriptors` SHALL translate to
`DocumentContentAlreadyExistsError`.

Other integrity/database failures remain unclassified and propagate.
Human-readable database messages SHALL NOT be used for duplicate
classification.

`get(document_id)` SHALL create one session, use exact `document_id` identity,
perform no commit, return `None` when missing, reconstruct the canonical
descriptor when present and close the session on all paths.

### Database and Alembic Contract

The existing `DatabaseBase.metadata` remains the sole relational metadata
authority.

`DatabaseRuntime` remains unchanged.

Current canonical Alembic head:

`0004`

After accepted-contract Git verification and separate implementation
authorization, accepted migration:

`backend/migrations/versions/0005_document_content_descriptors.py`

with revision `0005`, down revision `0004`, one linear canonical head, only the
accepted descriptor table, no foreign key, no BLOB/binary field and no
unrelated schema change.

Alembic `env.py` SHALL import/register `DocumentContentDescriptorRow` before
`target_metadata = DatabaseBase.metadata` is bound so the canonical table is
present in Alembic metadata discovery.

This registration is metadata visibility only and SHALL NOT expand
`DatabaseRuntime` ownership or runtime lifecycle responsibility.

### Explicitly Deferred

RFC-069 does not authorize raw bytes, BLOB/filesystem/object/network storage,
byte stream/open/read/download APIs, `DocumentContentStore`, Document Content
establishment application service, cross-repository transaction coordination,
Enterprise Document + descriptor + future payload atomicity, Document Library,
parser, OCR, chunking, Search, Vector, Graph, RAG, LLM, Composition, Runtime,
Bootstrap or production-security/Cybersecurity claims.

### Future Technical Verification Requirements

After separate implementation authorization, RFC-069 SHALL require focused
contracts for Infrastructure boundaries, exact model/table/constraint shape,
Domain/row round trip, duplicate classification, repository lifecycle,
Alembic lineage/metadata registration, absence of FK/binary fields, unchanged
Domain/repository contracts, impacted regression, full regression, Python
compilation, `git diff --check` and one canonical Alembic head.

### Current Next Exact Action

Review the complete five-document RFC-069 / AD-055 acceptance-propagation diff.

Do not stage or commit until that review passes.

After the accepted-contract commit is pushed and exact local / tracking /
remote identity plus a clean working tree are verified, open a separate
implementation-entry Git gate before TDD RED or any production/schema/migration
change.

---

## RFC-069 Technical Completion and Engineering-Memory Closure Pending

### Current Governance State

RFC-069 technical implementation commit:

`4572b40cedecc263577453b95ca63ecab6e61428`

Technical push and exact local / tracking / remote identity:

**PASS**

Working tree after technical push:

**clean**

Full regression baseline:

**912 passed**

Canonical Alembic head:

`0005`

Architecture Decision:

**AD-055 — ACCEPTED**

Engineering-memory closure:

**PENDING — DRAFT / REVIEW GATE**

Post-closure Source-of-Truth reconciliation:

**NOT STARTED**

Successor RFC / architecture workstream:

**NONE SELECTED OR PRESELECTED**

### Next Gate

Review the five-document engineering-memory closure diff.

No staging or commit is authorized until that review passes.

No successor selection is authorized until RFC-069 closure and separate
Source-of-Truth reconciliation are complete, pushed and verified.

---

## RFC-069 Post-Closure Source-of-Truth Reconciliation

### Verified Closure State

Engineering-memory closure commit:

`63790de5312c69c709e2249b56e91995a00426b6`

Closure push and exact local / tracking / remote identity:

**PASS**

Working tree after closure push:

**clean**

Engineering-memory closure:

**COMPLETE — COMMITTED, PUSHED AND VERIFIED**

### Reconciliation State

Post-closure Source-of-Truth reconciliation:

**PENDING — DRAFT / REVIEW GATE**

Reconciliation commit:

**NOT YET CREATED**

RFC-069 is not yet fully closed and Source-of-Truth reconciled.

No successor RFC or architecture workstream is selected or preselected.

### Current Next Gate

Review the complete five-document reconciliation diff.

No staging or commit is authorized until that review passes.

After reconciliation is committed, pushed and exact identity is verified,
a separate final reconciliation verification record remains required before
successor-workstream selection.

---

## RFC-069 Final Verified Closure and Source-of-Truth Reconciliation Record

RFC-069 is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Verified engineering-memory closure commit:

`63790de5312c69c709e2249b56e91995a00426b6`

Verified post-closure Source-of-Truth reconciliation commit:

`231e0cc66862c797e299fdb71ff20da8a39e8ae2`

Reconciliation push:

**PASS**

Exact local / tracking / remote reconciliation identity:

**PASS**

Working tree after reconciliation push:

**clean**

The reconciliation changed exactly the five maintained Source-of-Truth
documents and introduced no backend or test-file change.

AD-055 remains Accepted.

Full regression baseline remains **912 passed**.

Canonical Alembic head remains `0005`.

No successor RFC or architecture workstream is selected or preselected by
this record.

Successor selection is a separate evidence-based governed activity.

This record does not contain or predict its own future Git commit identity and
does not require a recursive RFC-069 verification record.

---

## Selected Successor Architecture Workstream — RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary

### Status

**CHIEF ARCHITECT SELECTED — SELECTION REVIEW PASS / STAGING PENDING**

Selection baseline:

`3a57f02167e9b69aafee7261b5901b64fe894446`

Last fully closed RFC:

**RFC-070 — Canonical Binary Document Content Store / Access Foundation**

### Selection Evidence

RFC-070 completed the persistence-neutral binary content port but deliberately
introduced no concrete Infrastructure storage adapter.

Current repository evidence shows:

- `DocumentContentStore` exists;
- descriptor persistence exists;
- binary adapter implementation does not exist;
- concrete behavioral conformance remains blocked by adapter absence.

The selected minimum next dependency is therefore:

**RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary**

### Dependency Ordering

1. **Now:** concrete binary Document Content Infrastructure adapter boundary.
2. **Later:** descriptor/payload coordination and establishment semantics.
3. **Later:** application-level Document Content workflows.
4. **Downstream:** Document Library and parser/OCR/chunking.
5. **Higher-level:** Search/Vector/Graph/RAG/LLM.

### Architecture Contract Required

Selection does not choose the physical storage technology.

The RFC-071 architecture contract must decide the concrete adapter technology,
namespace, physical addressing, publication atomicity, failure contract,
durability, configuration, migration implications and verification model.

### Prohibited Before Selection Git Gate

- AD-057 authoring;
- implementation;
- Infrastructure storage files;
- schema/migration changes;
- application coordination;
- Document Library/parser work;
- Runtime/Composition wiring.

### Next Exact Action

Stage exactly the five Source-of-Truth documents for a staging-only review.

Do not commit or push until that staging review passes.

---

## Active Architecture Workstream — RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary

### Current Status

**ARCHITECTURE CONTRACT ACCEPTED — ACCEPTANCE-STATE REVIEW / GIT GATE PENDING**

Verified selection commit:

`92fc4196f24c84d49846ee9825aba9eeb1b03d8b`

Accepted Architecture Decision:

**AD-057 — Canonical Filesystem-Backed Binary Document Content Infrastructure Adapter Boundary**

### Accepted Concrete Boundary

Adapter:

`FilesystemDocumentContentStore`

Module:

`app.infrastructure.document_content.filesystem_store`

Technology:

**filesystem-backed persistence through an injected absolute storage root**

### Dependency Shape

`DocumentContentStore`
→
`FilesystemDocumentContentStore`
→
Python standard-library filesystem primitives
→
injected filesystem root.

No Domain or Application layer receives a filesystem path.

### Publication Invariant

Same-directory temporary write followed by atomic hard-link
create-if-absent publication.

This preserves:

- one payload per `document_id`;
- no overwrite;
- no partial final publication;
- race-safe duplicate establishment.

### Refined Infrastructure Ownership

The configured root remains deployment-owned and pre-existing.

The adapter owns only deterministic shard directories beneath that root.

Only final hard-link destination conflict maps to canonical duplicate identity.

Root unavailability remains operational failure.

Confirmed absence is evaluated only beneath a healthy configured root.

### Explicit Deferrals

No:

- PostgreSQL BLOB/large object;
- object storage;
- S3/MinIO;
- direct File Server protocol;
- NFS/SMB-specific adapter;
- descriptor/payload coordination;
- content-establishment service;
- Document Library/parser/OCR;
- Search/Vector/Graph/RAG/LLM;
- default production composition;
- production-security claim.

### Migration / Runtime

Alembic head remains:

`0005`

`DatabaseRuntime` unchanged.

Default `CompositionRoot` unwired.

### Architecture Acceptance Gate

Final refined architecture review:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

AD-057:

**ACCEPTED — ACCEPTED-CONTRACT GIT GATE PENDING**

Implementation:

**NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document architecture acceptance state.

Do not stage before that review passes.

Do not implement before accepted-contract commit/push/exact-identity
verification and the separate implementation-entry gate.

---

## RFC-071 Engineering Closure Gate

### Workstream

**RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary**

Architecture:

**AD-057 — ACCEPTED / GIT DURABLE**

Selection commit:

`92fc4196f24c84d49846ee9825aba9eeb1b03d8b`

Accepted-contract commit:

`14b2b56e9395b680da7aaca1a98515eea3a71b01`

Technical commit:

`9b556850adc011afca41cd6740a0265be03a2aa8`

### Technical Outcome

Implemented:

`FilesystemDocumentContentStore`

Verified full regression:

**956 passed**

Alembic:

`0005`

No database-schema, Runtime/Composition or provider-SDK expansion.

### Current Gate

Technical implementation durability:

**COMPLETE**

Closure documentation:

**AUTHORED — REVIEW PENDING**

Terminal RFC closure:

**NOT YET CLAIMED**

Post-closure Source-of-Truth reconciliation:

**PENDING**

Successor selection:

**NOT STARTED**

### Next Exact Action

Review RFC-071 closure documentation.

No staging, commit, push or successor selection until the closure review gate
passes.

---

## RFC-071 Post-Closure Source-of-Truth Reconciliation Gate

### Workstream

**RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary**

Architecture Decision:

**AD-057 — ACCEPTED**

Engineering closure commit:

`c725163808d88d5b89e034b608eb51829efd0f4b`

Post-closure reconciliation commit:

`a6ad9bac7745a8c7e4583b9373acb3cbe889df75`

### Durable Reconciliation Result

Reconciliation parent:

`c725163808d88d5b89e034b608eb51829efd0f4b`

Reconciliation push:

**PASS**

Exact local / tracking / remote reconciliation identity:

**PASS**

Working tree:

**CLEAN**

Reconciliation surface:

**EXACTLY FIVE SOURCE-OF-TRUTH DOCUMENTS**

Full verified regression:

**956 passed**

Alembic:

`0005`

### Governed State

RFC-071:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Active RFC:

**NONE**

Selected successor:

**NONE**

Successor-workstream selection has not started.

Any successor must be selected separately through evidence-based governance.

The final verification record is intentionally non-self-referential and records
only reconciliation commit `a6ad9bac7745a8c7e4583b9373acb3cbe889df75`.

---

## RFC-071 Final Source-of-Truth Reconciliation Verification

### Status

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Selected workstream:

RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary

Architecture Decision:

**AD-057 — ACCEPTED**

Verified commit chain:

- selection: `92fc4196f24c84d49846ee9825aba9eeb1b03d8b`;
- accepted contract: `14b2b56e9395b680da7aaca1a98515eea3a71b01`;
- technical implementation: `9b556850adc011afca41cd6740a0265be03a2aa8`;
- engineering closure: `c725163808d88d5b89e034b608eb51829efd0f4b`;
- post-closure reconciliation: `a6ad9bac7745a8c7e4583b9373acb3cbe889df75`.

### Final Reconciliation Git Verification

- reconciliation parent: `c725163808d88d5b89e034b608eb51829efd0f4b`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- exact five Source-of-Truth document surface: **PASS**;
- production-code changes: none;
- test-file changes: none.

### Verified Technical Baseline

- full PlantMind regression: **956 passed**;
- canonical Alembic head: **0005**;
- concrete Infrastructure adapter:
  `app.infrastructure.document_content.filesystem_store.FilesystemDocumentContentStore`;
- canonical persistence-neutral binary store port remains unchanged.

Production deployment conformance remains separately governed.

### Governed State After RFC-071

There is no active RFC or selected successor workstream.

Successor-workstream selection has not started.

Any successor must be selected separately through evidence-based governance.

This state is intentionally non-self-referential and records only already
verified commits through reconciliation commit `a6ad9bac7745a8c7e4583b9373acb3cbe889df75`.

---

## Selected Successor Architecture Workstream — RFC-072 — Canonical Document Content Establishment Application Coordination Boundary

### Selection Result

**SELECTED**

Successor:

**RFC-072 — Canonical Document Content Establishment Application Coordination Boundary**

Selection baseline:

`0363365989786c51d6757fb09662622dc54d5b44`

RFC-071 state:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Full regression:

**956 passed**

Alembic head:

`0005`

### Why RFC-072 Is Next

RFC-071 completed the concrete Infrastructure implementation of the canonical
binary `DocumentContentStore`.

The repository contains no Application-layer consumer of that store.

The next dependency-completing gap is therefore the narrow
Document Content establishment Application coordination boundary.

This selection deliberately does not expand the existing
Document-to-Knowledge ingestion service or Knowledge/Lineage transaction
coordinator.

### Architecture Work Required Before Implementation

RFC-072 must determine:

1. exact use-case ownership;
2. accepted port dependencies;
3. Document existence requirements;
4. descriptor/payload ordering;
5. cross-boundary consistency and partial-success semantics;
6. duplicate behavior;
7. failure classification;
8. compensation legality;
9. retry/idempotency behavior;
10. whether a narrow coordinator abstraction is required;
11. preservation of binary-store immutability and storage neutrality.

### Deferred / Rejected At This Gate

Not selected:

- filesystem deployment-conformance work;
- Runtime/Composition wiring;
- Document Library;
- parser/OCR/chunking;
- Search/Vector/Graph/RAG/LLM;
- production-security/Cybersecurity work.

These remain separately evidence-governed.

### Gate

Architecture drafting may begin only after this successor-selection record is:

1. reviewed;
2. staged and verified;
3. committed;
4. pushed;
5. confirmed exact on Local / Tracking / Remote.

No implementation is authorized by this selection.

---

## RFC-072 Architecture Contract Accepted — Canonical Document Content Establishment Application Coordination Boundary

Accepted Architecture Decision:

**AD-058 — Accepted / Accepted-Contract Git Gate Pending**

### Status

**ACCEPTED — ACCEPTED-CONTRACT GIT GATE PENDING**

The RFC-072 / AD-058 Architecture Contract is Accepted.

Its accepted-contract commit, push and exact Git durability gate remain
pending.

Implementation remains:

**NOT AUTHORIZED**

### Related Workstream

**RFC-072 — Canonical Document Content Establishment Application Coordination Boundary**

Verified successor-selection commit:

`0c9a8cba53221f547d340fa499f1ac7d07d1e7d3`

Selection Git durability:

**PASS — LOCAL / TRACKING / REMOTE IDENTITY VERIFIED**

Last fully closed workstream:

**RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary**

Full regression baseline:

**956 passed**

Canonical Alembic head:

`0005`

### Context

PlantMind now has the complete prerequisite Document Content foundation:

- canonical immutable `DocumentContentDescriptor` Domain semantics;
- canonical persistence-neutral `DocumentContentRepository`;
- relational descriptor persistence;
- canonical persistence-neutral `DocumentContentStore`;
- concrete `FilesystemDocumentContentStore`.

The remaining dependency gap is the Application-layer use case that establishes
one coherent canonical Document Content association without collapsing
descriptor persistence and binary storage into one responsibility.

### Architectural Decision

RFC-072 SHALL introduce one narrow Application service:

`DocumentContentEstablishmentApplicationService`

under:

`app.services.document_content_establishment_application_service`

implemented at:

`backend/app/services/document_content_establishment_application_service.py`

RFC-072 SHALL NOT introduce a new ARCH-001 layer.

The service SHALL coordinate existing persistence-neutral contracts.

It SHALL NOT become a persistence adapter or transaction manager.

### Canonical Public Surface

The new module SHALL expose exactly these RFC-072 public classes:

- `DocumentContentEstablishmentRequest`;
- `DocumentContentEstablishmentDocumentNotFoundError`;
- `DocumentContentEstablishmentConflictError`;
- `DocumentContentEstablishmentIntegrityError`;
- `DocumentContentEstablishmentApplicationService`.

No package-level re-export is required.

Existing package initializers SHALL remain unchanged unless separately reviewed.

### Canonical Request

`DocumentContentEstablishmentRequest`

SHALL be an immutable keyword-only dataclass containing exactly:

`document_id: EntityId`

`media_type: str`

`source: BinaryIO`

The request SHALL NOT require callers to supply:

- byte length;
- SHA-256 digest;
- filesystem path;
- URI;
- storage key;
- Infrastructure adapter;
- SQLAlchemy session.

Byte length and digest SHALL be derived from the exact canonical byte sequence
processed by the Application use case.

### Canonical Service Dependencies

`DocumentContentEstablishmentApplicationService.__init__`

SHALL receive exactly these persistence-neutral dependencies:

- `document_repository: EnterpriseDocumentRepository`;
- `content_repository: DocumentContentRepository`;
- `content_store: DocumentContentStore`.

The service SHALL NOT depend on:

- `FilesystemDocumentContentStore`;
- SQLAlchemy;
- `DatabaseRuntime`;
- filesystem paths;
- storage roots;
- provider SDKs;
- `KnowledgeLineageTransactionCoordinator`;
- concrete Infrastructure repositories.

### Canonical Operation

The canonical Application operation SHALL be:

`establish(request: DocumentContentEstablishmentRequest) -> DocumentContentDescriptor`

Normal return SHALL mean that the Application service has verified one coherent
canonical content state for the requested `document_id`.

### Enterprise Document Existence

Before reading caller payload bytes or creating new descriptor/payload state,
the service SHALL verify:

`document_repository.get(request.document_id)`

returns an existing canonical `EnterpriseDocument`.

If the Document is absent, the service SHALL raise:

`DocumentContentEstablishmentDocumentNotFoundError`

No descriptor or payload persistence SHALL occur for an absent Document.

RFC-072 SHALL NOT combine Enterprise Document registration with content
establishment.

`EnterpriseDocumentRegistrationApplicationService` remains unchanged.

### Source Reference Boundary

The Application service SHALL receive canonical payload bytes explicitly through:

`request.source`

It SHALL NOT open, interpret or convert:

`EnterpriseDocument.source.source_reference`

into canonical content access.

`source_reference` remains external provenance / traceability only.

### Media-Type Boundary

`request.media_type`

SHALL be converted through the existing canonical:

`DocumentContentMediaType`

before content establishment is reported successful.

RFC-072 SHALL NOT duplicate media-type normalization or validation rules.

### Exact Byte Measurement

RFC-072 SHALL own Application-level derivation of:

- exact byte length;
- SHA-256 digest

for the canonical raw byte sequence.

Measurement SHALL use the exact bytes from the caller source's current position
through EOF.

It SHALL perform no:

- text normalization;
- parsing;
- OCR;
- decompression;
- character conversion;
- semantic transformation.

The resulting descriptor SHALL use existing:

`DocumentContentDigest`

and:

`DocumentContentDescriptor`

Domain contracts.

SHA-256 remains integrity metadata.

It SHALL NOT become canonical identity, deduplication identity or storage
identity.

### Caller Source Lifecycle

The Application service SHALL preserve RFC-070 caller-source semantics:

- source ownership remains with the caller;
- source is consumed from current position through EOF;
- non-seekable sources are supported;
- successful `seek()` is not required;
- successful `tell()` is not required;
- `fileno()` is not required;
- the Application service SHALL NOT close the caller-owned source;
- no rewind or position-restoration guarantee exists after failure.

RFC-072 SHALL NOT require complete payload materialization in memory.

### Single-Pass Fresh-Payload Measurement Boundary

For fresh payload establishment, the Application service MAY use an
Application-private read-through measuring wrapper around the caller-owned
source.

That wrapper SHALL:

- forward bytes incrementally to `DocumentContentStore.add()`;
- count only bytes actually yielded through the wrapper;
- update SHA-256 only from those exact yielded bytes;
- preserve byte order and value;
- require no `seek()`;
- require no `tell()`;
- require no caller `fileno()`;
- never close the caller-owned source;
- not read ahead merely to complete validation;
- not require full payload buffering in memory;
- not introduce Application-owned filesystem or temporary-file persistence.

Measurement from a fresh write SHALL be considered complete and usable for
descriptor construction only when `DocumentContentStore.add()` returns
normally.

If `add()` fails, partial measurement state SHALL NOT be used to construct or
persist a new descriptor.

This preserves exact single-pass measurement without creating a replay or
temporary-storage responsibility in the Application layer.

### Existing-Payload Read Lifecycle

When RFC-072 must verify an already-established payload, it SHALL use:

`DocumentContentStore.open(document_id)`

through the accepted context-manager lifecycle.

The service SHALL:

- consume the opened payload from byte zero;
- calculate exact SHA-256 and byte length;
- close the store-owned resource through the context manager;
- treat `None` only as confirmed absence;
- allow operational storage failures to propagate.

### Canonical Establishment State Model

RFC-072 recognizes four observable combinations for an existing canonical
Document identity:

1. descriptor absent / payload absent;
2. descriptor present / payload absent;
3. descriptor absent / payload present;
4. descriptor present / payload present.

RFC-072 SHALL NOT add a persisted workflow-state field or status table for these
combinations.

The state is derived only by observing the accepted repository/store contracts.

Observation of descriptor state and payload state SHALL NOT be represented as
one atomic cross-store snapshot.

RFC-072 claims no cross-store linearizable read.

Concurrent establishment may therefore cause an invocation to fail
conservatively with conflict or integrity classification even when a later
observation would show a converged state.

A later explicit invocation may re-observe the current canonical state.

No result may claim success unless the success invariants of this contract have
actually been verified.

### Fresh Establishment Ordering

For:

**descriptor absent / payload absent**

RFC-072 SHALL establish the binary payload first.

The service SHALL stream the caller source through measurement logic into:

`DocumentContentStore.add(document_id, source)`

Only after successful payload establishment may the service construct and add
the canonical descriptor.

The descriptor SHALL be derived from the exact bytes consumed by the successful
payload operation.

RFC-072 deliberately selects:

**payload publication before descriptor publication**

for new content.

This prevents RFC-072 itself from exposing a newly persisted descriptor before
the corresponding new payload has been established.

### Fresh Descriptor Persistence

After successful new payload establishment, the service SHALL construct:

`DocumentContentDescriptor`

using:

- the requested canonical `document_id`;
- normalized `DocumentContentMediaType`;
- measured exact byte length;
- measured SHA-256 digest.

It SHALL then call:

`DocumentContentRepository.add(descriptor)`

Normal return SHALL occur only after the descriptor is successfully accepted
according to the existing repository contract or an exact concurrent descriptor
result is safely reconciled as defined below.

RFC-072 SHALL NOT add a stronger physical-durability guarantee to the abstract
repository contract than that contract already provides.

### Descriptor-Present / Payload-Absent Integrity State

When a canonical descriptor already exists but the binary payload is confirmed
absent, RFC-072 SHALL classify the observed state as:

`DocumentContentEstablishmentIntegrityError`

RFC-072 SHALL NOT automatically heal this state.

For this state, the invocation SHALL:

- not consume the caller-owned source;
- not call `DocumentContentStore.add()`;
- not add or replace a descriptor;
- not overwrite any canonical state;
- not introduce temporary buffering or replay storage.

This restriction is intentional.

The existing binary store exposes immutable create-if-absent publication and no
conditional pre-publication digest predicate.

The caller source is allowed to be non-seekable and RFC-072 introduces no
replay-buffer persistence contract.

Therefore RFC-072 cannot both:

1. fully validate an arbitrary non-seekable caller stream against the existing
   descriptor before publication; and
2. subsequently publish those same bytes through the unchanged store

without adding buffering/replay or changing the accepted store contract.

Neither expansion is authorized by RFC-072.

Descriptor-present / payload-absent state is not a state produced by the normal
RFC-072 payload-first flow.

If encountered, remediation requires separately governed operational or
architecture action.

A later invocation may observe a different state if another authorized actor
has independently restored the payload.

### Payload-Present / Descriptor-Absent Recovery

When the payload already exists but the descriptor is absent:

1. the existing payload SHALL be measured through `DocumentContentStore.open`;
2. the caller source SHALL be consumed and measured;
3. caller source byte length and SHA-256 SHALL match the existing payload;
4. the requested media type SHALL be normalized through the Domain contract;
5. the descriptor SHALL be constructed from the already-established payload's
   measured bytes;
6. the descriptor may then be persisted through `DocumentContentRepository`.

If caller source bytes do not match the already-established payload, the
operation SHALL raise:

`DocumentContentEstablishmentConflictError`

and SHALL NOT create a descriptor.

### Descriptor-Present / Payload-Present Verification

When descriptor and payload both already exist:

1. requested media type SHALL match the canonical descriptor;
2. persisted payload byte length and SHA-256 SHALL match the canonical
   descriptor;
3. caller source SHALL be consumed and measured;
4. caller source bytes SHALL match the canonical persisted content;
5. only then may an explicit repeated establishment request return successfully.

Successful exact repeat SHALL return the existing canonical descriptor.

This is Application-level idempotent convergence.

It SHALL NOT change the underlying repository/store duplicate contracts into
idempotent-success contracts.

### Canonical Integrity Failure

`DocumentContentEstablishmentIntegrityError`

SHALL represent canonical persisted-state inconsistency.

It SHALL be raised when:

- a canonical descriptor is present while the payload is confirmed absent; or
- an already-persisted descriptor and already-persisted payload disagree on
  byte length; or
- an already-persisted descriptor and already-persisted payload disagree on
  SHA-256 digest.

It SHALL NOT:

- overwrite either side;
- delete either side;
- reinterpret the mismatch as absence;
- silently repair using caller bytes.

Such a mismatch is an observed canonical integrity violation requiring separate
operational investigation.

### Canonical Request Conflict

`DocumentContentEstablishmentConflictError`

SHALL represent a request that cannot converge with already-established
canonical state.

Examples include:

- requested media type differs from an existing canonical descriptor;
- caller bytes differ from an already-established canonical payload;
- a concurrent binary-store duplicate occurs after this invocation already
  attempted a new write and exact equivalence cannot safely be proven from the
  possibly-consumed caller source.

Conflict SHALL NOT authorize overwrite or replacement.

### Duplicate and Concurrency Semantics

RFC-072 SHALL preserve the accepted duplicate contracts of both underlying
ports.

`DocumentContentPayloadAlreadyExistsError`

from a racing new `DocumentContentStore.add()` SHALL NOT automatically become
idempotent success in the same invocation.

RFC-070 permits a failed `add()` to leave caller-source position unspecified.

Therefore RFC-072 SHALL NOT assume it can safely replay or revalidate that
source after a racing store duplicate.

That invocation SHALL raise:

`DocumentContentEstablishmentConflictError`

The RFC-072 Application service SHALL map that racing
`DocumentContentPayloadAlreadyExistsError` to the Application conflict
classification.

It SHALL NOT treat the duplicate as same-invocation idempotent success because
the caller source may already be partially or fully consumed and exact
equivalence cannot safely be proven by replay.

The original store duplicate MAY be retained as causal exception context.

A later explicit invocation using a fresh source may re-observe the now-existing
canonical state and converge through the applicable state rules.

### Descriptor Duplicate Reconciliation

If the payload has already been successfully established or verified and
`DocumentContentRepository.add()` encounters
`DocumentContentAlreadyExistsError` due to a concurrent descriptor writer,
RFC-072 MAY re-read the canonical descriptor.

If the observed descriptor is exactly equal to the descriptor this invocation
has already derived and the payload state is known valid, the operation MAY
return that canonical descriptor successfully.

If the descriptor differs, the service SHALL raise:

`DocumentContentEstablishmentConflictError`

No overwrite is allowed.

### Success Contract

Normal return from `establish()` SHALL mean:

- the canonical Enterprise Document exists;
- exactly one canonical descriptor is present for the Document;
- one canonical binary payload is present for the Document;
- descriptor `document_id` equals the canonical Document identity;
- descriptor media type is canonical;
- descriptor byte length describes the exact persisted payload;
- descriptor SHA-256 describes the exact persisted payload;
- the supplied caller source for this invocation has been established or
  verified against that canonical state;
- no overwrite, replacement or deletion occurred.

### Atomicity Decision

RFC-072 SHALL NOT claim distributed or all-or-nothing transaction atomicity
across:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`.

The current descriptor repository uses independently committed persistence.

The binary store publishes immutable payloads through a separately owned
storage boundary with no delete/rollback operation.

A generic transaction coordinator cannot truthfully provide rollback across
those accepted contracts without redesigning them.

RFC-072 therefore selects:

**monotonic recoverable Application coordination**

rather than false distributed atomicity.

### New Coordinator Decision

RFC-072 SHALL NOT introduce a new descriptor/payload transaction coordinator.

It SHALL NOT extend:

`KnowledgeLineageTransactionCoordinator`

That coordinator remains exclusively responsible for its accepted Knowledge and
lineage transaction scope.

Application orchestration is sufficient for RFC-072 because the selected model
is explicit state observation, monotonic establishment and retry recovery—not a
shared transactional resource boundary.

### Partial-Failure Contract

RFC-072 SHALL distinguish success from recoverable partial state.

If binary payload establishment fails before canonical publication, no new
descriptor SHALL be added by RFC-072.

If the store raises an operational failure after canonical publication may
already have occurred, RFC-072 SHALL propagate the failure and SHALL NOT add a
new descriptor in that invocation.

This may leave:

**payload present / descriptor absent**

A later explicit retry may recover that state.

If descriptor persistence raises a non-duplicate operational failure after
payload establishment, the failure SHALL propagate.

The canonical state may then be:

- payload-only; or
- already complete if the descriptor persistence boundary committed before a
  later cleanup failure.

A later retry SHALL re-observe actual state rather than infer outcome from the
prior exception.

### No Automatic Rollback

RFC-072 SHALL NOT automatically delete a published binary payload.

RFC-072 SHALL NOT add delete, replace or rollback operations to:

- `DocumentContentStore`;
- `DocumentContentRepository`.

RFC-072 SHALL NOT attempt compensating filesystem deletion.

Accepted RFC-070/RFC-071 immutability remains authoritative.

### Retry / Idempotency Decision

RFC-072 introduces no automatic retry loop.

Retry is an explicit new Application invocation.

An explicit retry MAY return idempotent success only after re-observing and
verifying exact canonical state according to this contract.

RFC-072 SHALL NOT use as standalone idempotency identity:

- SHA-256 digest;
- media type;
- byte length;
- source reference;
- filesystem path.

Canonical association identity remains:

`document_id`

Idempotent convergence is a verified Application outcome, not a new persistence
identity.

### Operational Failure Propagation

Operational failures from:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- caller source reads;
- opened payload reads

SHALL remain operational failures unless this contract explicitly classifies
them as one of the RFC-072 Application errors.

RFC-072 SHALL NOT introduce a generic catch-all storage or repository error
hierarchy.

### Existing Responsibility Preservation

RFC-072 SHALL NOT modify or absorb the responsibilities of:

- `EnterpriseDocumentRegistrationApplicationService`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeCaptureApplicationService`;
- `KnowledgeLineageTransactionCoordinator`;
- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- `FilesystemDocumentContentStore`;
- `DocumentContentDescriptor`;
- `EnterpriseDocument`.

Document registration remains independent.

Document-to-Knowledge ingestion remains independent.

Knowledge/Lineage transactional coordination remains independent.

### Persistence and Database Boundary

RFC-072 requires no new:

- SQLAlchemy model;
- database table;
- column;
- foreign key;
- index;
- uniqueness constraint;
- BLOB;
- large-object persistence;
- Alembic revision.

Canonical Alembic head SHALL remain:

`0005`

`DatabaseRuntime` remains unchanged.

### Infrastructure Boundary

Application code SHALL NOT import:

`app.infrastructure`

It SHALL depend only on accepted persistence-neutral ports and Domain contracts.

RFC-072 SHALL NOT expose:

- storage root;
- shard layout;
- path;
- hard link;
- temporary filename;
- filesystem implementation detail.

The same Application service SHALL remain compatible with a future alternative
`DocumentContentStore` implementation conforming to the accepted port.

### Runtime / Composition Boundary

RFC-072 SHALL NOT modify or expand:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`;
- Runtime;
- Bootstrap;
- readiness;
- Health;
- request admission;
- mandatory-capability policy.

No default `FilesystemDocumentContentStore` wiring is authorized.

### Document Library / Parser Boundary

RFC-072 is not the Document Library.

It SHALL NOT introduce:

- upload API/UI;
- download API/UI;
- browse/catalogue behavior;
- folder hierarchy;
- parser integration;
- PDF extraction;
- OCR;
- DOCX extraction;
- spreadsheet extraction;
- text extraction;
- metadata extraction;
- chunking.

Future parser behavior SHALL consume canonical bytes through an accepted
Application/access path and SHALL NOT reinterpret `source_reference`.

### Search / Vector / Graph / AI Boundary

RFC-072 SHALL NOT introduce:

- keyword search;
- semantic search;
- embeddings;
- vector persistence;
- Qdrant integration;
- graph persistence;
- Neo4j production integration;
- RAG;
- LLM invocation;
- AI Agent behavior.

### Security and Deployment Boundary

RFC-072 SHALL NOT claim or implement production:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- malware scanning;
- Document approval;
- retention enforcement;
- compliance approval;
- Cybersecurity approval.

RFC-071 filesystem deployment conformance remains separately governed.

### Expected Technical Surface After Separate Implementation Entry Gate

Only if this RFC-072 / AD-058 contract is later:

1. reviewed;
2. refined if required;
3. accepted;
4. committed;
5. pushed;
6. verified exact on local / tracking / remote;
7. followed by a separate implementation-entry PASS

may implementation introduce:

`backend/app/services/document_content_establishment_application_service.py`

and focused tests:

`tests/services/test_document_content_establishment_application_service.py`

`tests/services/test_document_content_establishment_architecture.py`

No other production file is pre-authorized.

If implementation reveals that a historical architecture test contains an
assumption superseded specifically by accepted RFC-072 scope, the failure SHALL
be classified before any test change.

No historical test SHALL be mechanically weakened.

### Acceptance Requirements

Before RFC-072 / AD-058 may become Accepted, review SHALL confirm:

1. RFC-072 introduces no new ARCH-001 layer;
2. canonical module ownership is
   `app.services.document_content_establishment_application_service`;
3. the public RFC-072 class surface is exactly the five classes defined here;
4. `DocumentContentEstablishmentRequest` is immutable and keyword-only;
5. request fields are exactly `document_id`, `media_type` and `source`;
6. caller does not supply canonical byte length;
7. caller does not supply canonical SHA-256 digest;
8. byte length and digest are derived from exact raw bytes;
9. SHA-256 remains integrity metadata only;
10. service constructor depends exactly on the three persistence-neutral ports;
11. Application code imports no concrete Infrastructure adapter;
12. `establish()` returns `DocumentContentDescriptor`;
13. canonical Enterprise Document existence is checked before source
    consumption or content mutation;
14. absent Document raises the RFC-072 Document-not-found error;
15. absent Document causes no descriptor/payload persistence;
16. Document registration remains independent;
17. `source_reference` is never opened as canonical content;
18. media type uses existing Domain validation;
19. source is consumed from current position through EOF;
20. non-seekable sources remain supported;
21. caller source is never closed by the service;
22. no seek/tell/fileno dependency is introduced;
23. zero-byte payload remains valid;
24. fresh payload measurement is single-pass and requires neither full-payload
    memory materialization nor Application-owned temporary/replay storage;
25. existing payload verification uses the context-managed store contract;
26. confirmed store absence remains distinct from operational failure;
27. the four descriptor/payload observable state combinations are recognized,
    without claiming an atomic or linearizable cross-store snapshot;
28. no persisted workflow-state table or field is introduced;
29. fresh establishment publishes payload before descriptor;
30. fresh descriptor values derive from bytes consumed by successful payload
    establishment;
31. RFC-072 fresh flow does not create descriptor-before-payload state;
32. descriptor-present / payload-absent is classified as an integrity state and
    is not automatically healed by RFC-072;
33. descriptor-present / payload-absent raises the RFC-072 integrity error
    without consuming caller source or publishing a payload;
34. payload-only recovery verifies persisted payload and caller source;
35. payload-only recovery creates descriptor only for matching bytes;
36. complete existing state verifies persisted descriptor/payload integrity;
37. complete exact repeated requests may converge idempotently;
38. persisted descriptor/payload mismatch raises the RFC-072 integrity error;
39. caller content conflicting with canonical state raises the RFC-072 conflict
    error;
40. no overwrite, replace, update or delete is introduced;
41. a racing `DocumentContentPayloadAlreadyExistsError` during fresh
    establishment is mapped to
    `DocumentContentEstablishmentConflictError` and is not translated to
    same-invocation idempotent success;
42. failed store writes preserve RFC-070 source-position semantics;
43. later explicit retry may re-observe and recover partial state;
44. descriptor duplicate after verified payload may reconcile only when exact
    descriptor equality is observed;
45. different concurrent descriptor state becomes conflict;
46. normal return requires Document + descriptor + payload consistency;
47. RFC-072 claims no distributed transaction atomicity;
48. no new descriptor/payload transaction coordinator is introduced;
49. `KnowledgeLineageTransactionCoordinator` remains unchanged;
50. monotonic recoverable coordination is explicit;
51. no automatic payload rollback or deletion is introduced;
52. store post-publication operational failure is propagated;
53. descriptor persistence operational failure is propagated;
54. no automatic retry loop is introduced;
55. retry is an explicit Application invocation;
56. digest/media type/byte length/source reference do not become idempotency
    identities;
57. underlying repository/store duplicate semantics remain unchanged;
58. existing Document-to-Knowledge ingestion remains unchanged;
59. existing Document Registration remains unchanged;
60. existing Domain content contracts remain unchanged;
61. existing relational descriptor adapter remains unchanged;
62. existing filesystem store remains unchanged;
63. no SQLAlchemy or Alembic expansion occurs;
64. canonical Alembic head remains `0005`;
65. `DatabaseRuntime` remains unchanged;
66. default Composition/Runtime/Bootstrap remain unchanged;
67. no Document Library/parser/OCR/chunking capability is promoted;
68. no Search/Vector/Graph/RAG/LLM capability is promoted;
69. no production-security or Cybersecurity completion claim is introduced;
70. implementation begins only after accepted-contract Git durability and a
    separate implementation-entry gate.

These are Architecture Contract acceptance requirements.

They SHALL NOT require RFC-072 production implementation to exist before
AD-058 acceptance.

### Future Implementation / Technical Gate Requirements

The following requirements belong to the later RFC-072 technical implementation
gate, not to AD-058 architecture acceptance.

Only after:

1. AD-058 is Accepted;
2. the accepted-contract commit is created;
3. the accepted-contract commit is pushed;
4. exact Local / Tracking / Remote identity is verified; and
5. a separate implementation-entry PASS authorizes code changes

shall the RFC-072 technical gate require:

1. focused RFC-072 service behavior tests pass;
2. RFC-072 architecture/dependency tests pass;
3. relevant RFC-066/RFC-068/RFC-069/RFC-070/RFC-071 regressions remain
   passing;
4. full PlantMind regression remains passing;
5. Python compilation passes;
6. `git diff --check` passes.

These future technical checks SHALL NOT be used as prerequisites for AD-058
architecture acceptance.

They SHALL NOT be used to bypass the separate implementation-entry gate.

### Alternatives Considered

#### Distributed Transaction / Two-Phase Commit

Rejected.

Current descriptor persistence and immutable filesystem publication do not share
one rollback-capable transactional resource.

Claiming atomic rollback would be architecturally false.

#### Extend KnowledgeLineageTransactionCoordinator

Rejected.

Its accepted scope is Knowledge + lineage persistence only.

RFC-072 SHALL NOT turn it into a generic Unit of Work.

#### Descriptor-First Fresh Establishment

Rejected.

RFC-072 would then intentionally create a newly visible descriptor before the
new payload exists.

Payload-first ordering better preserves the meaning of canonical descriptor
visibility under the accepted immutable store model.

#### Automatic Payload Deletion Compensation

Rejected.

It conflicts with accepted no-delete/no-overwrite binary-store semantics.

#### Require Caller-Supplied Digest and Byte Length

Rejected.

RFC-072 can derive canonical integrity metadata directly from the exact bytes
processed by the use case and avoids shifting canonical byte-accounting
responsibility into ungoverned callers.

#### Pre-Buffer Entire Payload

Rejected as a canonical requirement.

It would weaken non-seekable/streaming behavior and could introduce unbounded
memory or hidden temporary-storage policy into the Application layer.

RFC-072 therefore does not attempt automatic repair of a
descriptor-present / payload-absent integrity state.

Such repair would require a separately accepted replay/buffering contract,
a changed store contract, or another explicitly governed remediation boundary.

### Architecture Contract Acceptance

Final refined architecture review:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

Gate-separation review:

**PASS — CIRCULAR ACCEPTANCE / IMPLEMENTATION GATE REMOVED**

AD-058:

**ACCEPTED — ACCEPTED-CONTRACT GIT GATE PENDING**

Implementation:

**NOT AUTHORIZED**

Acceptance-state staging / commit / push:

**NONE**

The accepted contract remains local Source-of-Truth content until its dedicated
Git durability gate completes.

### Next Exact Action

Review the complete five-document RFC-072 / AD-058 architecture acceptance
state.

Do not stage before that review passes.

Do not begin implementation before accepted-contract commit/push/exact-identity
verification and the separate implementation-entry gate.

---

## RFC-072 Engineering Closure Gate

### Workstream

**RFC-072 — Canonical Document Content Establishment Application Coordination Boundary**

Architecture:

**AD-058 — ACCEPTED / GIT DURABLE**

Selection commit:

`0c9a8cba53221f547d340fa499f1ac7d07d1e7d3`

Accepted-contract commit:

`aa444f1f339c6aa00d37a9b3f0f564f3b5b6c06e`

Technical commit:

`81a137d117df65c5beebd1fb935ca5b48e014733`

### Technical Outcome

Implemented:

`DocumentContentEstablishmentApplicationService`

Canonical module:

`app.services.document_content_establishment_application_service`

Focused RFC-072 verification:

**39 passed**

Relevant prior-boundary regression:

**175 passed**

Verified full regression:

**995 passed**

Alembic:

`0005`

Technical diff SHA-256:

`66ea75b2fbdccd1e423f123590261900f59e05679d7c708874600880dc3e0100`

No database-schema, Alembic, Runtime/Composition/Bootstrap, Document Library,
parser/OCR/chunking, Search/Vector/Graph/RAG/LLM or production-security
expansion occurred.

### Current Gate

Technical implementation durability:

**COMPLETE**

Closure documentation:

**AUTHORED — REVIEW PENDING**

Terminal RFC closure:

**NOT YET CLAIMED**

Post-closure Source-of-Truth reconciliation:

**PENDING**

Successor selection:

**NOT STARTED**

### Next Exact Action

Review RFC-072 closure documentation.

No staging, commit, push or successor selection until the closure review gate
passes.

---

## RFC-072 Post-Closure Source-of-Truth Reconciliation Gate

### Workstream

**RFC-072 — Canonical Document Content Establishment Application Coordination Boundary**

Architecture Decision:

**AD-058 — ACCEPTED**

Engineering closure commit:

`99066acafd76205ba41d7997eba7486d2f572fc7`

Closure Git durability:

**COMPLETE**

Full verified regression:

**995 passed**

Alembic:

`0005`

### Current Gate

Engineering closure:

**COMPLETE / PUSHED / EXACT IDENTITY VERIFIED**

Post-closure Source-of-Truth reconciliation:

**AUTHORED — REVIEW PENDING**

Reconciliation staging:

**NOT PERFORMED**

Reconciliation commit:

**NOT YET CREATED**

Reconciliation push / exact identity verification:

**NOT YET PERFORMED**

Final reconciliation verification record:

**NOT YET CREATED**

RFC-072 terminal closure:

**NOT YET CLAIMED**

Successor selection:

**NOT AUTHORIZED**

### Next Exact Action

Review RFC-072 post-closure Source-of-Truth reconciliation.

No staging, commit, push, final-verification record or successor selection
until the reconciliation review gate passes.

---

## RFC-072 Final Source-of-Truth Reconciliation Verification

### Status

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Selected workstream:

RFC-072 — Canonical Document Content Establishment Application Coordination Boundary

Architecture Decision:

**AD-058 — ACCEPTED**

### Verified Commit Chain

- selection: `0c9a8cba53221f547d340fa499f1ac7d07d1e7d3`;
- accepted contract: `aa444f1f339c6aa00d37a9b3f0f564f3b5b6c06e`;
- technical implementation: `81a137d117df65c5beebd1fb935ca5b48e014733`;
- engineering closure: `99066acafd76205ba41d7997eba7486d2f572fc7`;
- post-closure reconciliation: `3fab31e046c47c90a0b3a10467570af646273011`.

### Final Reconciliation Git Verification

Reconciliation parent:

`99066acafd76205ba41d7997eba7486d2f572fc7`

Reconciliation push:

**PASS**

Exact Local / Tracking / Remote reconciliation identity:

**PASS**

Working tree:

**CLEAN**

Reconciliation surface:

**EXACTLY FIVE SOURCE-OF-TRUTH DOCUMENTS**

Full verified regression:

**995 passed**

Alembic:

`0005`

### Governed State

RFC-072:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Active RFC:

**NONE**

Selected successor:

**NONE**

Successor-workstream selection has not started.

Any successor must be selected separately through evidence-based governance.

The final verification record is intentionally non-self-referential and
records only already durable commits through reconciliation commit:

`3fab31e046c47c90a0b3a10467570af646273011`

Its own Git durability is verified externally and does not require another
RFC-072 Source-of-Truth record.

---

## Post-RFC-072 Successor Workstream Selection Draft — RFC-073

### Candidate Workstream

**RFC-073 — Canonical Document Content Access Application Boundary**

Selection baseline:

`60ede75cb850101afbcf08f6cac18cce3a04ef43`

RFC-072 terminal state:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Latest Accepted Architecture Decision:

**AD-058**

Full verified regression:

**995 passed**

Alembic:

`0005`

### Dependency Rationale

RFC-072 completed canonical content establishment.

The next narrow dependency is an accepted Application access path for
canonical binary Document Content.

This boundary is required before a downstream parser can consume canonical
bytes without bypassing the Application layer or treating `source_reference`
as storage.

### Not Promoted

The following remain downstream:

- Document Library;
- parser / PDF / DOCX / spreadsheet / text extraction;
- OCR;
- metadata extraction;
- chunking;
- Search / Vector / Graph;
- RAG / LLM / AI Agents;
- Runtime / Composition / Bootstrap expansion;
- production security / RBAC / Active Directory;
- production deployment conformance.

### Current Gate

RFC-073 successor selection:

**AUTHORED — REVIEW PENDING**

Active RFC:

**NONE**

Architecture Decision:

**NOT CREATED**

Architecture contract:

**NOT AUTHORED**

Implementation:

**NOT AUTHORIZED**

Staging:

**NONE**

Commit:

**NONE**

Push:

**NONE**

### Next Exact Action

Review the RFC-073 successor-selection documentation.

No staging is authorized until that review passes.
