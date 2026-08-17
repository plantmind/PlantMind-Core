# PlantMind Architecture Decisions

## Document Control

| Property | Value |
|---|---|
| Project | PlantMind Core |
| Project ID | PM-001 |
| Status | Active |
| Purpose | Consolidated record of major architectural decisions |

---

# Decision Format

Each decision records:

- Context
- Decision
- Rationale
- Consequences
- Future Impact

---

# AD-001 — Enterprise On-Premise Deployment

## Context

PlantMind is intended for industrial and petrochemical environments where operational data, engineering documents and production knowledge are sensitive.

## Decision

Production deployment SHALL be on-premise inside the company environment.

GitHub remains a development repository only.

## Rationale

- Protect industrial and operational data.
- Support company Cybersecurity requirements.
- Avoid mandatory dependence on public cloud infrastructure.
- Enable Active Directory and internal-network integration.
- Support locally hosted AI models.

## Consequences

- Infrastructure must support internal deployment.
- External cloud dependencies must not be mandatory.
- Security, RBAC and auditability remain first-class concerns.

## Future Impact

All connectors, AI services, data stores and deployment designs must support this position.

---

# AD-002 — Architecture Before Features

## Context

Rapid feature development without architectural review creates duplication, hidden coupling and expensive rework.

## Decision

No feature may be implemented before reviewing:

- Existing components
- Responsibility boundaries
- Dependencies
- Interfaces
- Tests
- Documentation impact

## Rationale

PlantMind is a long-lived enterprise platform, not a short-lived prototype.

## Consequences

Some features may be delayed while shared foundations are built.

## Future Impact

Every RFC must begin with an existing-code and architecture review.

---

# AD-003 — Reuse Before Rebuild

## Context

The project contains existing runtime, service, registry, connector and orchestration capabilities.

## Decision

Existing components SHALL be reviewed before creating a replacement or parallel implementation.

## Rationale

This prevents duplicate responsibility and architectural fragmentation.

## Consequences

New RFC proposals may be changed or cancelled when suitable infrastructure already exists.

## Future Impact

Search and dependency review are mandatory before new platform foundations are introduced.

---

# AD-004 — Preserve Before Delete

## Context

Deleting files too early can break hidden dependencies and discard useful implementation history.

## Decision

The preferred change order is:

1. Keep
2. Rename
3. Move
4. Merge
5. Compatibility wrapper
6. Deprecate
7. Delete after dependency and impact verification

## Rationale

This protects backward compatibility and reduces uncontrolled change.

## Consequences

Legacy wrappers may remain temporarily.

## Future Impact

No deletion is allowed without reference search, tests and confirmed replacement.

---

# AD-005 — Generic Registry Framework

## Context

PlantMind requires registration and resolution for readers, plugins, connectors, agents, engines and future extensions.

## Decision

A generic typed `Registry[T]` is the shared registration foundation.

## Rationale

- Avoid repeated factory logic.
- Provide consistent duplicate protection.
- Provide consistent resolution behavior.
- Improve typing and testability.

## Consequences

Specialized registries should build on the generic registry rather than reimplementing registration logic.

## Future Impact

Future factories and registries should use the generic framework unless their lifecycle requirements clearly differ.

---

# AD-006 — Distinct Registry Responsibilities

## Context

PlantMind currently contains:

- Generic Registry
- Plugin Registry
- Service Registry

These components appear similar but manage different concepts.

## Decision

Their responsibilities SHALL remain distinct.

| Component | Responsibility |
|---|---|
| `Registry[T]` | Factory registration and resolution |
| `PluginRegistry` | Plugin creation and registration |
| `ServiceRegistry` | Runtime service instances and lifecycle |

## Rationale

The Service Registry stores active service instances, while the generic registry stores factories.

## Consequences

The existing Service Registry must not be replaced merely to unify naming.

## Future Impact

Any consolidation requires a dedicated lifecycle and dependency review.

---

# AD-007 — Plugin Framework as an Extension Foundation

## Context

PlantMind will eventually support connectors, agents, engines, knowledge providers and enterprise modules.

## Decision

The Plugin Framework is accepted as the first reusable extension mechanism.

## Rationale

It provides:

- A common plugin contract
- Registration
- Creation
- Future activation and deactivation lifecycle

## Consequences

RFC-025 remains the accepted foundation.

## Future Impact

A future Enterprise Extension Framework may extend the Plugin Framework but must not discard it without migration analysis.

---

# AD-008 — Mock Before Production Integration

## Context

Real PI Web API integration introduces authentication, certificates, networking and production-system dependencies.

## Decision

Internal architecture SHALL first be developed and tested using contracts and mock implementations.

## Rationale

- Enables independent development.
- Reduces external-system coupling.
- Improves testability.
- Delays infrastructure complexity until internal design is stable.

## Consequences

Mock PI readers are intentional, not temporary shortcuts.

## Future Impact

Real connectors must implement the established contracts without forcing changes into higher layers.

---

# AD-009 — PI Is One Knowledge Source

## Context

PlantMind must understand more than historian data.

## Decision

PI System is treated as one source among many.

The platform must also support:

- P&ID and engineering drawings
- Operating procedures
- Vendor manuals
- CMMS and SAP history
- Incident and RCA reports
- Shift handovers
- Expert knowledge

## Rationale

Operational intelligence requires live data, engineering context, procedures and historical evidence together.

## Consequences

Higher layers must not depend directly on PI-specific models where a source-neutral contract is more appropriate.

## Future Impact

Knowledge-source abstraction and document ingestion remain core roadmap items.

---

# AD-010 — Source of Truth Order

## Context

Information may appear in code, tests, architecture documents, roadmaps and conversations.

## Decision

When information conflicts, use this order:

1. Current committed code and tests
2. Accepted ADR, ARCH, CORE and RFC documents
3. Active Work Register
4. Project Context
5. Session Handoff
6. Engineering Journal
7. Conversation history

## Rationale

Conversation history can be incomplete, slow or unavailable.

## Consequences

Important decisions must be moved into repository documentation.

## Future Impact

New sessions must read the project-memory documents before proposing changes.

---

# AD-011 — Authoritative Development Environment

## Context

Two virtual environments existed:

- `PlantMind-Core/.venv`
- `PlantMind-Core/backend/.venv`

They contained different packages and produced misleading test failures.

## Decision

The authoritative development environment is:

```text
PlantMind-Core/.venv
```

The approved test command is:

```bash
PYTHONPATH=backend ./.venv/bin/python -m pytest -q
```

## Rationale

This environment reproduced the verified regression baseline.

## Consequences

The alternate environment must not be treated as authoritative.

## Future Impact

Environment consolidation and dependency reproducibility should be handled in a dedicated future task.

---

# AD-012 — Mandatory RFC Completion Gate

## Context

Passing a focused test alone does not prove platform safety.

## Decision

An RFC is complete only after:

1. Architecture review
2. Dependency review
3. Implementation
4. Compilation
5. Focused tests
6. Full regression
7. Git status review
8. Commit
9. Push
10. Clean working tree
11. Documentation update when required

## Rationale

This prevents unfinished or unverified work from entering the platform history.

## Consequences

All RFCs use the same completion discipline.

## Future Impact

Automation may later enforce these gates.

---

# AD-013 — The Platform Must Understand Itself

## Context

PlantMind is intended to become a long-lived platform with many RFCs, components and dependencies.

## Decision

The platform should eventually track:

- Implemented capabilities
- Incomplete work
- Dependencies
- Technical debt
- Release readiness
- Governance status

## Rationale

Engineering continuity must not depend on individual memory.

## Consequences

Project-memory and governance documents are now part of the engineering system.

## Future Impact

An Engineering Governance Engine may later automate this capability.

---

# AD-014 — Project Memory Is a Maintained Asset

## Context

Long conversations became difficult to load and transfer between sessions.

## Decision

The following documents form the permanent project-memory layer:

- `PROJECT-CONTEXT.md`
- `SESSION-HANDOFF.md`
- `ENGINEERING-JOURNAL.md`
- `ARCHITECTURE-DECISIONS.md`
- `ROADMAP-004-Active-Work-Register.md`

## Rationale

These files preserve context independently of any chat session.

## Consequences

Relevant documents must be updated when an RFC changes project state or architecture.

## Future Impact

Any new engineer or AI session should be able to resume work by reading these files and the latest Git state.
---

# AD-015 — Composition Root Owns Plugin Infrastructure Composition

## Context

RFC-027 integrated plugin lifecycle behavior into Bootstrap, and RFC-028 introduced the dedicated `PluginLifecycleManager`.

RFC-029 established an authoritative production composition path for plugin infrastructure.

Without a single composition owner, multiple consumers could construct independent plugin registries or lifecycle managers and create inconsistent runtime object graphs.

## Decision

The Composition Root SHALL own construction and wiring of the production plugin infrastructure.

The composed platform SHALL create one `PluginRegistry` and one `PluginLifecycleManager` for each platform composition.

Those same instances SHALL be:

- Injected into `BootstrapManager`
- Registered in `ServiceContainer`
- Exposed through `PlatformComposition`

`PluginRegistry`, `PluginLifecycleManager`, `BootstrapManager`, `ServiceRegistry`, and `CompositionRoot` SHALL retain distinct responsibilities.

## Rationale

- Maintains one authoritative production object graph.
- Prevents duplicate plugin registries and lifecycle managers.
- Preserves Dependency Injection.
- Keeps lifecycle ownership inside `PluginLifecycleManager`.
- Keeps startup and shutdown orchestration inside `BootstrapManager`.
- Keeps dependency construction and wiring inside `CompositionRoot`.

## Consequences

The Composition Root is the authoritative production assembly point for plugin infrastructure.

Existing backward-compatible fallback construction may remain where already established, but the composed production path SHALL use explicitly injected dependencies.

No parallel plugin infrastructure should be introduced without dedicated architecture and dependency review.

## Future Impact

Plugin discovery, enterprise extensions, connectors, agents, engines, and future plugin capabilities must integrate with the composed plugin infrastructure instead of creating independent registries or lifecycle managers.


---

# AD-016 — Plugin Registration Enters Through the Composition Boundary

## Context

RFC-030 introduced a controlled registration boundary for supplying plugins to the production platform composition.

Before RFC-030, the Composition Root owned plugin infrastructure construction but had no explicit production boundary for supplying plugin registrations.

Adding a separate registrar, automatic discovery mechanism, or parallel registry would duplicate existing responsibilities and weaken the authoritative plugin object graph established by RFC-029.

## Decision

Plugin registrations SHALL enter the production platform explicitly through the Composition Root.

Registrations SHALL be represented by immutable `PluginRegistration` declarations containing a plugin name and factory.

The Composition Root SHALL apply those registrations to the existing composed `PluginRegistry`.

`PluginRegistry` SHALL remain the owner of registration and duplicate-registration semantics.

`PluginLifecycleManager` SHALL remain the owner of plugin creation, activation and deactivation.

`BootstrapManager` SHALL remain the owner of startup and shutdown orchestration.

Plugin factories SHALL remain lazy during composition and SHALL NOT be instantiated merely because they are registered.

The no-registration composition path SHALL remain backward compatible.

RFC-030 SHALL NOT introduce automatic filesystem discovery, dynamic module scanning, package loading, or a second registrar, registry, lifecycle manager, or plugin object graph.

## Rationale

- Preserves one authoritative plugin infrastructure.
- Preserves existing registry semantics.
- Prevents duplicated registration responsibility.
- Maintains lazy plugin creation.
- Maintains Dependency Injection and Composition Root ownership.
- Keeps lifecycle and bootstrap responsibilities separated.
- Provides a controlled extension point for future enterprise plugin capabilities.

## Consequences

Production plugin registrations must be supplied through the established composition boundary.

Future plugin sources may prepare `PluginRegistration` declarations, but they must integrate with the existing `PluginRegistry` rather than bypassing or replacing it.

Automatic discovery, security approval policy, metadata, version compatibility and package loading require separate architecture review before introduction.

## Future Impact

Future enterprise extension catalogs, connector plugins, agents, engines and approved discovery mechanisms should feed the controlled registration boundary while preserving the authoritative composed plugin infrastructure.


---

# AD-017 — Plugin Runtime Identity Must Match Registry Identity

## Context

RFC-031 identified a possible divergence between the identity used to register a plugin and the identity reported by the created plugin instance through `Plugin.name`.

The `PluginRegistry` resolves factories by registration name, while runtime lifecycle reporting uses the identity exposed by the plugin instance.

Without an explicit consistency rule, one plugin could be known by different identities across registration and runtime lifecycle boundaries.

## Decision

The plugin registration name SHALL be the authoritative plugin identity.

Every plugin instance created for registration name `X` SHALL report `plugin.name == X`.

Identity validation SHALL occur at the existing `PluginRegistry.create()` boundary after lazy factory resolution and before the plugin instance is returned to lifecycle orchestration.

An identity mismatch SHALL raise the plugin-specific `PluginIdentityMismatchError`.

A mismatched plugin SHALL NOT proceed to activation.

Plugin identity errors SHALL remain separate from the Generic Registry error hierarchy.

`PluginLifecycleManager` SHALL retain plugin activation and deactivation responsibility.

`BootstrapManager` SHALL retain startup and shutdown orchestration responsibility.

Composition SHALL remain lazy and SHALL NOT instantiate plugins merely to validate identity.

## Rationale

- Establishes one authoritative plugin identity across registration and runtime.
- Prevents registry and lifecycle identity divergence.
- Detects invalid plugin factories before activation.
- Preserves lazy plugin creation.
- Keeps identity validation within the plugin-specific registry boundary.
- Preserves Generic Registry independence.
- Preserves existing lifecycle, Bootstrap and Composition Root responsibilities.

## Consequences

Plugin factories must produce instances whose `Plugin.name` matches the registration name used by `PluginRegistry`.

Existing duplicate-registration, registration-not-found and ordering semantics remain unchanged.

Future plugin metadata, discovery, package loading, version compatibility and security approval mechanisms must preserve this identity invariant.

## Future Impact

Any future enterprise extension framework, plugin catalog, discovery mechanism or security approval layer must use the authoritative registry identity consistently and must not introduce an alternate runtime plugin identity.

---

# AD-018 — Plugin Metadata Extends the Existing Registration Contract

## Context

RFC-032 introduced metadata for registered plugins after RFC-031 established the plugin registration name as the authoritative plugin identity.

Plugin metadata must provide explicit version information without creating a second identity, registry, lifecycle path, discovery mechanism, or compatibility engine.

The metadata model must also preserve lazy plugin creation and the controlled registration boundary established by RFC-030.

## Decision

Plugin metadata SHALL be represented by immutable `PluginMetadata`.

`PluginMetadata` SHALL require an explicit `plugin_version`.

The metadata contract SHALL expose immutable contract version `1.0`.

`PluginRegistration.name` SHALL remain the authoritative plugin identity and plugin metadata SHALL NOT introduce another plugin name.

`PluginRegistration` MAY contain optional `PluginMetadata`.

Existing `PluginRegistration(name, factory)` construction SHALL remain backward compatible.

Plugin metadata SHALL be associated with the same registration inside the existing `PluginRegistry`.

Metadata lookup SHALL NOT instantiate the registered plugin factory.

`CompositionRoot` SHALL forward supplied plugin metadata through the existing controlled registration boundary into the same composed `PluginRegistry`.

Clearing `PluginRegistry` SHALL also clear its associated plugin metadata.

Existing duplicate-registration, registration-not-found, registry ordering and RFC-031 identity-validation semantics SHALL remain unchanged.

`PluginLifecycleManager` SHALL retain activation and deactivation responsibility.

`BootstrapManager` SHALL retain startup and shutdown orchestration responsibility.

PlantMind `APP_VERSION` SHALL NOT be used as an implicit plugin version.

## Rationale

- Provides explicit plugin-version metadata without coupling plugins to the PlantMind application version.
- Preserves one authoritative plugin identity.
- Preserves the existing composed plugin infrastructure.
- Maintains lazy plugin creation.
- Preserves backward compatibility for existing plugin registrations.
- Prevents metadata from creating a parallel registry or lifecycle responsibility.
- Establishes a minimal contract that future plugin capabilities can extend through dedicated architecture decisions.

## Consequences

Plugin metadata is optional for existing registrations but, when supplied, is stored alongside the authoritative registration in the existing `PluginRegistry`.

Metadata can be inspected independently of plugin instantiation.

Metadata lifecycle follows registration lifecycle and is removed when the Plugin Registry is cleared.

RFC-032 does not evaluate semantic-version compatibility and does not define plugin discovery, filesystem scanning, package loading, capability catalogs or security approval policy.

## Future Impact

Future plugin compatibility, discovery, catalog, package-loading or security-approval mechanisms must build on this metadata contract while preserving the authoritative registration identity, lazy creation, controlled registration boundary and existing lifecycle responsibilities.

Any expansion of plugin metadata semantics requires dedicated architecture review before implementation.

---

# AD-019 — Plugin Version Format Is Validated at Metadata Construction

## Context

RFC-032 introduced explicit plugin version metadata but did not constrain the format of `plugin_version`.

Future compatibility, catalog or governance mechanisms require plugin versions to have a stable canonical representation before they can safely depend on version information.

Version-format validation must not create new Registry, Composition, Lifecycle or Bootstrap responsibilities.

## Decision

`PluginMetadata.plugin_version` SHALL use canonical `MAJOR.MINOR.PATCH` format.

`MAJOR`, `MINOR` and `PATCH` SHALL each be non-negative decimal integers.

Numeric components SHALL NOT contain leading zeros except for the value `0`.

Missing components, additional components, `v` prefixes, surrounding whitespace, pre-release suffixes, build suffixes and invalid separators SHALL be rejected.

Validation SHALL occur when immutable `PluginMetadata` is constructed.

Invalid plugin versions SHALL raise the plugin-specific `InvalidPluginVersionError`.

`InvalidPluginVersionError` SHALL preserve `ValueError` semantics.

`PluginMetadata.contract_version` semantics SHALL remain unchanged.

Valid RFC-032 plugin metadata behavior SHALL remain unchanged.

Version validation SHALL NOT be moved into `PluginRegistry`, `PluginRegistration`, `CompositionRoot`, `PluginLifecycleManager` or `BootstrapManager`.

RFC-033 SHALL NOT introduce an external version-parsing dependency.

## Rationale

- Establishes a deterministic canonical plugin version representation.
- Fails invalid metadata at its natural contract boundary.
- Keeps validation responsibility with the immutable metadata model.
- Preserves existing Registry, Composition Root, Lifecycle and Bootstrap responsibilities.
- Avoids unnecessary dependency expansion.
- Creates a stable foundation for future version-aware architecture without implementing compatibility policy prematurely.

## Consequences

Plugin metadata containing a non-canonical version cannot be constructed.

Existing registrations without metadata remain backward compatible.

Valid RFC-032 metadata continues to behave as before.

Plugin version format is now enforced independently from PlantMind `APP_VERSION`.

RFC-033 does not define version comparison, semantic-version compatibility evaluation, plugin discovery, filesystem scanning, package loading, capability catalogs or security approval policy.

## Future Impact

Any future plugin compatibility, catalog, discovery, package-loading or governance mechanism must build on this canonical version-format invariant.

Version comparison or compatibility policy requires a dedicated architecture review and must not be inferred from RFC-033 alone.

---

# AD-020 — Bootstrap Startup Failure Is Atomic

## Context

BOOT-002 requires Bootstrap to stop startup immediately when a critical dependency fails and prohibits partial startup unless explicitly supported.

Before RFC-034, service validation and initialization were interleaved, successfully initialized services were not rolled back after later startup failures, and successful plugin activations could remain active after a later plugin failed.

RUNTIME-001 defines `FAILED` as the runtime state for a critical failure preventing safe operation.

## Decision

Bootstrap startup SHALL behave atomically with respect to components successfully started during the current startup attempt.

All registered services SHALL complete validation before any registered service is initialized.

A service validation failure SHALL stop startup before service initialization or plugin activation begins.

A service initialization failure SHALL stop further initialization.

Only services whose `initialize()` operation completed successfully during the current startup attempt SHALL participate in startup rollback.

Successfully initialized services SHALL be shut down in reverse initialization order when a later startup stage fails.

A plugin activation failure SHALL stop further activation.

Successfully activated plugins SHALL be rolled back through the existing `PluginLifecycleManager`.

Plugin rollback SHALL occur before initialized-service rollback and SHALL preserve reverse activation order.

Runtime SHALL own the public transition into `FAILED`.

A critical startup failure SHALL request the Runtime `FAILED` transition and Runtime readiness SHALL remain false.

Runtime SHALL NOT transition to READY unless all mandatory startup stages complete successfully.

When compensating cleanup succeeds, the original startup exception SHALL remain the primary propagated failure.

## Rationale

- Enforces the existing BOOT-002 prohibition on partial startup.
- Keeps Bootstrap as the startup and shutdown orchestration authority.
- Keeps Runtime as the owner of Runtime state.
- Reuses existing Plugin Lifecycle ownership instead of creating a parallel rollback mechanism.
- Ensures failed startup cannot intentionally leave previously started components running.
- Preserves deterministic reverse-order cleanup.
- Preserves successful startup and shutdown behavior.

## Consequences

Service validation is completed as a distinct phase before service initialization begins.

Bootstrap tracks successfully initialized services for the duration of the startup attempt.

Critical startup failures transition Runtime to `FAILED` through its public interface.

Successful plugin activations are deactivated before initialized services are shut down when plugin activation fails.

RFC-034 does not define retry logic, automatic startup recovery, dependency graphs, parallel initialization, plugin discovery, ServiceState redesign, logging architecture redesign or version compatibility policy.

Secondary failures that occur during compensating cleanup require separate architecture review.

## Future Impact

Future startup stages and infrastructure integrations must preserve atomic failure semantics and must not introduce intentional partial startup without dedicated architecture approval.

Startup recovery, retry policy, rollback-failure aggregation and dependency-aware initialization remain separate future architecture concerns.

---

# AD-021 — Runtime Enters STOPPING Before Managed Shutdown

## Context

BOOT-002 defines the official shutdown pipeline as:

1. Request Admission Disabled
2. Runtime Transition to STOPPING
3. Service Shutdown
4. Infrastructure Shutdown
5. Runtime Transition to STOPPED

Before RFC-035, `BootstrapManager.shutdown()` performed managed shutdown work without first transitioning Runtime to `STOPPING`.

Runtime exposed `STOPPED` through existing behavior but did not expose a public transition operation for `STOPPING`.

RFC-035 aligns the implementation with BOOT-002 and RUNTIME-001 without changing established lifecycle ownership.

## Decision

Runtime SHALL expose a public transition operation for `STOPPING`.

The Runtime-owned `STOPPING` transition SHALL set readiness to false.

Bootstrap SHALL request Runtime transition to `STOPPING` before managed plugin or service shutdown begins.

Runtime state SHALL continue to be modified only through Runtime public interfaces.

Plugin deactivation SHALL remain owned by `PluginLifecycleManager`.

Registered services SHALL continue to shut down in deterministic reverse registry enumeration order.

Bootstrap SHALL request transition to `STOPPED` only after required shutdown operations complete successfully.

Existing `Runtime.mark_not_ready()` behavior SHALL remain backward compatible.

RFC-034 startup failure atomicity semantics SHALL remain unchanged.

## Rationale

- Aligns implementation with the accepted BOOT-002 shutdown pipeline.
- Makes shutdown state observable before managed components begin stopping.
- Keeps Runtime as the exclusive owner of Runtime state transitions.
- Keeps Bootstrap as the lifecycle orchestration authority.
- Preserves Plugin Lifecycle ownership.
- Avoids unnecessary changes to `ServiceRegistry` ordering semantics.
- Preserves existing startup and successful shutdown behavior.

## Consequences

Runtime now exposes an explicit public `STOPPING` transition.

Runtime is not ready throughout managed shutdown.

Bootstrap enters `STOPPING` before plugin deactivation and service shutdown.

Service shutdown order remains based on reverse `ServiceRegistry.registered_services()` enumeration.

Runtime reaches `STOPPED` only after required shutdown work completes successfully.

RFC-035 does not define shutdown retry logic, cleanup-failure aggregation, automatic recovery, dependency graphs, parallel shutdown, ServiceState redesign, request-admission implementation, plugin discovery or logging architecture redesign.

## Future Impact

Any future shutdown stage must preserve the Runtime `STOPPING` boundary and established ownership responsibilities.

Shutdown failure semantics, cleanup-failure aggregation, recovery policy and request-admission behavior require separate architecture review.

---

# AD-022 — Managed Shutdown Failures Are Contained and Aggregated

## Context

RFC-035 aligned graceful shutdown with the accepted Runtime lifecycle by entering `STOPPING` before managed component shutdown and reaching `STOPPED` only after successful completion.

Before RFC-036, an exception raised during plugin deactivation or service shutdown immediately interrupted the remaining shutdown sequence.

This could leave later plugins or services unattempted and leave Runtime in `STOPPING` without a complete representation of the shutdown failure.

RUNTIME-001 defines `FAILED` as the state for a critical failure preventing safe operation.

## Decision

Managed shutdown SHALL use deterministic best-effort failure containment.

Runtime SHALL enter `STOPPING` before managed shutdown attempts begin.

`PluginLifecycleManager` SHALL attempt all active plugin deactivations in reverse activation order even when individual deactivations fail.

Successfully deactivated plugins SHALL be removed from the active set.

Plugins whose deactivation fails SHALL remain tracked as active because their final lifecycle state is unresolved.

Plugin deactivation ownership SHALL remain exclusively in `PluginLifecycleManager`.

Bootstrap SHALL continue to registered-service shutdown when plugin deactivation reports failure.

Bootstrap SHALL attempt all registered service shutdown operations in deterministic reverse registry enumeration order even when individual service shutdown operations fail.

If all required managed shutdown operations succeed, Runtime MAY complete the existing transition to `STOPPED`.

If any managed shutdown operation fails, Bootstrap SHALL request the Runtime-owned transition to `FAILED` and Runtime readiness SHALL remain false.

A single managed shutdown failure SHALL remain the directly propagated original exception.

Multiple managed shutdown failures SHALL be propagated through `ExceptionGroup`.

Aggregated failures SHALL preserve deterministic shutdown encounter order.

## Rationale

- Prevents one failing component from blocking cleanup of unrelated managed components.
- Preserves deterministic shutdown ordering.
- Avoids falsely reporting `STOPPED` after incomplete or failed shutdown.
- Keeps Runtime state ownership inside Runtime.
- Keeps plugin lifecycle ownership inside `PluginLifecycleManager`.
- Preserves original exception identity for single-failure cases.
- Provides complete failure visibility for multi-failure shutdown without introducing a parallel error framework.

## Consequences

Managed shutdown becomes best-effort rather than fail-fast.

Failed plugin deactivations remain visible through the active plugin set.

Successful plugin deactivations are removed even when other plugin deactivations fail.

Service shutdown continues after individual service failures.

Runtime transitions to `FAILED` when any managed shutdown operation fails.

Multiple failures may be exposed as `ExceptionGroup` and consumers of the Bootstrap boundary must be prepared for that Python 3.11 behavior.

RFC-036 does not define automatic retry, automatic recovery, dependency-aware shutdown, parallel shutdown, ServiceState redesign, request-admission implementation, logging architecture redesign, structured shutdown telemetry or process termination policy.

## Future Impact

Future shutdown stages must participate in the same deterministic best-effort containment model unless a dedicated architecture decision replaces it.

Retry policy, recovery strategy, dependency-aware shutdown, structured failure telemetry and process termination remain separate architecture concerns.
---

# AD-023 — Runtime Owns Request Admission State

## Context

BOOT-002 defines Request Admission Enabled only after Runtime reaches `READY` and Request Admission Disabled before Runtime enters `STOPPING`.

RUNTIME-001 assigns Request Admission State ownership to Runtime and assigns request-admission enforcement to the API hosting layer.

Before RFC-037, Runtime exposed readiness but no explicit request-admission state. Bootstrap reached `READY` without explicitly enabling admission and entered `STOPPING` without explicitly disabling admission first.

## Decision

Runtime SHALL exclusively own request-admission state.

Request admission SHALL be disabled when Runtime is created.

Runtime SHALL expose public operations to enable and disable request admission and a public read interface for admission state.

Bootstrap SHALL enable request admission only after all mandatory startup stages succeed and Runtime has reached `READY`.

Failed startup SHALL never leave request admission enabled.

Bootstrap SHALL disable request admission before requesting Runtime transition to `STOPPING`.

Runtime transitions to `STOPPING` and `FAILED` SHALL not permit request admission to remain enabled.

Request admission SHALL remain disabled throughout managed shutdown.

Failed managed shutdown SHALL leave request admission disabled while Runtime is `FAILED`.

The API hosting layer SHALL remain responsible for enforcing request admission according to Runtime state.

## Rationale

- Separates lifecycle readiness from workload admission.
- Keeps Runtime as the authoritative owner of platform lifecycle and admission state.
- Keeps Bootstrap focused on lifecycle orchestration.
- Prevents workload admission before mandatory startup completes.
- Prevents new workload admission after managed shutdown begins.
- Preserves existing startup atomicity and shutdown failure-containment behavior.
- Avoids creating a second admission controller outside Runtime.

## Consequences

Runtime now exposes explicit request-admission state independently from readiness.

Successful Bootstrap startup transitions Runtime to `READY` before enabling request admission.

Bootstrap disables request admission before requesting `STOPPING`.

Critical startup and managed shutdown failures leave request admission disabled.

Existing RFC-034, RFC-035 and RFC-036 lifecycle contracts remain compatible.

RFC-037 does not implement API middleware, request rejection responses, authentication, authorization, health verification, OPERATIONAL transition, DEGRADED transition, traffic draining, retry or recovery.

## Future Impact

Future API hosting components must enforce admission according to the Runtime-owned request-admission state.

Health verification, API admission enforcement, request rejection policy, traffic draining, OPERATIONAL and DEGRADED transitions require separate architecture review.

---

# AD-024 — Runtime Owns Readiness Verification

## Context

RUNTIME-001 defines readiness as a Runtime decision.

Bootstrap may request readiness but SHALL NOT directly own or manipulate Runtime lifecycle state.

BOOT-002 requires health verification before Runtime transitions to `READY`.

Before RFC-038, Bootstrap directly called `Runtime.mark_ready()` after service and plugin startup without an explicit Runtime-owned verification contract.

`ConfigurationProvider` already owns mandatory configuration validation.

`HealthCapability` is read-only observation and derives part of its status from Runtime readiness. Using it as the pre-READY decision owner would create a circular readiness dependency.

`ServiceRegistry` owns service inventory and SHALL remain independent of lifecycle decisions.

## Decision

Runtime SHALL remain the exclusive owner of the readiness decision.

Runtime readiness verification SHALL consume immutable `ReadinessEvidence`.

Readiness evidence SHALL represent completion of mandatory startup requirements without transferring lifecycle ownership to Bootstrap.

Runtime SHALL deterministically accept or reject a readiness request based on the supplied evidence.

Runtime SHALL NOT enter `READY` when any mandatory readiness evidence is unsatisfied.

Rejected readiness SHALL leave Runtime not ready and request admission disabled.

Bootstrap SHALL invoke mandatory configuration validation before service validation, initialization or plugin activation.

Configuration validation SHALL remain owned by `ConfigurationProvider`.

Bootstrap SHALL construct readiness evidence only after mandatory startup stages complete successfully.

Bootstrap SHALL request Runtime readiness before enabling request admission.

Readiness rejection SHALL participate in RFC-034 startup rollback semantics.

`HealthCapability` SHALL remain read-only observation and SHALL NOT become a readiness decision component.

`ServiceRegistry` SHALL remain independent of lifecycle decisions.

Composition Root SHALL inject the composed `ConfigurationProvider` and `HealthCapability` instances into Bootstrap.

Existing `Runtime.mark_ready()` compatibility SHALL remain available until a separate compatibility review authorizes removal.

## Rationale

- Preserves Runtime ownership of lifecycle decisions.
- Makes readiness deterministic and explicitly verifiable.
- Separates readiness evidence from lifecycle state mutation.
- Prevents Bootstrap from becoming the readiness authority.
- Preserves ConfigurationProvider ownership of configuration validation.
- Avoids circular dependency between Runtime readiness and HealthCapability observation.
- Preserves ServiceRegistry independence from lifecycle decisions.
- Preserves RFC-037 ordering between `READY` and request admission.
- Keeps Composition Root as the dependency-construction authority.

## Consequences

Production Bootstrap now uses the validated Runtime readiness path instead of directly publishing `READY`.

Incomplete readiness evidence prevents Runtime from entering `READY`.

Configuration validation now participates in mandatory Bootstrap startup sequencing.

Readiness rejection participates in startup rollback and leaves request admission disabled.

HealthCapability remains observation-only.

Existing RFC-034, RFC-035, RFC-036 and RFC-037 lifecycle behavior remains compatible.

RFC-038 does not define OPERATIONAL or DEGRADED transitions, API admission enforcement, request rejection policy, traffic draining, retry, recovery, dependency-aware startup, parallel startup or health-report redesign.

## Future Impact

Future lifecycle work must preserve Runtime ownership of readiness decisions and immutable readiness evidence unless replaced by a dedicated architecture decision.

OPERATIONAL and DEGRADED transitions, API request-admission enforcement, traffic draining, retry and recovery require separate architecture review.

---

# AD-025 — API Hosting Enforces Runtime Request Admission

## Context

RFC-037 established Runtime as the exclusive owner of request-admission state.

RUNTIME-001 requires the API hosting layer to enforce request admission according to Runtime.

Before RFC-039, the FastAPI hosting layer did not enforce the Runtime-owned admission state.

RFC-038 requires Runtime to reach `READY` before Bootstrap enables request admission.

Platform status and health observation must remain available even when operational request admission is disabled.

## Decision

Runtime SHALL remain the exclusive owner of request-admission state.

The API hosting layer SHALL enforce Runtime-owned request admission for operational requests.

API enforcement SHALL read Runtime admission state only through the approved public Runtime interface.

API enforcement SHALL NOT modify Runtime lifecycle state or request-admission state.

Operational requests received while admission is disabled SHALL be rejected with HTTP `503 Service Unavailable`.

The rejection response SHALL use a deterministic platform-owned response contract.

The platform-status endpoint `/` SHALL remain explicitly available while request admission is disabled.

The platform-health endpoint `/health` SHALL remain explicitly available while request admission is disabled.

Observation exemptions SHALL be explicit and SHALL NOT use unrestricted health-path matching.

The API hosting layer SHALL use the same composed Runtime instance used by Bootstrap and the platform lifecycle.

`HealthCapability` SHALL remain read-only observation and SHALL NOT participate in admission decisions.

Request admission SHALL be evaluated when a new request enters the API hosting boundary.

RFC-039 SHALL NOT define draining or cancellation semantics for requests already executing.

## Rationale

- Preserves Runtime as the single source of truth for request admission.
- Places enforcement at the boundary where operational requests enter the platform.
- Prevents API hosting from becoming a second lifecycle authority.
- Keeps lifecycle observation available during startup, shutdown and failure.
- Prevents accidental exemption of arbitrary health-like paths.
- Preserves RFC-038 readiness-before-admission ordering.
- Uses the Composition Root dependency graph rather than an independent Runtime instance.

## Consequences

Operational requests are now rejected deterministically when Runtime admission is disabled.

Platform status and health observation remain available independently of operational admission.

The production FastAPI application uses the composed Runtime instance for admission enforcement.

API enforcement remains stateless with respect to lifecycle ownership.

Existing RFC-037 and RFC-038 lifecycle behavior remains compatible.

RFC-039 does not define OPERATIONAL or DEGRADED transitions, authentication, authorization, rate limiting, retry, recovery, traffic draining, request cancellation or business workflow behavior.

## Future Impact

Future production operational API routes must remain behind the Runtime-owned admission boundary unless explicitly classified as approved observation interfaces.

Any new observation exemption must be explicit and architecture-reviewed.

OPERATIONAL and DEGRADED transitions, traffic draining, authentication, authorization, retry and recovery remain separate architecture concerns.

---

# AD-026 — Platform Operational Semantics Alignment

## Context

PlantMind defines `READY` and `OPERATIONAL` as distinct Runtime lifecycle states.

RFC-037 established Runtime-owned request admission.

RFC-038 established Runtime-owned readiness verification.

RFC-039 established API-hosting enforcement of Runtime-owned request admission.

Architecture review for RFC-040 identified terminology that could be interpreted inconsistently across Bootstrap, Health Capability and Core Service lifecycle documentation.

Successful Bootstrap startup currently terminates at Runtime `READY` and subsequently enables request admission.

No approved Runtime operation currently performs a transition from `READY` to `OPERATIONAL`.

The implemented Core Service state model does not currently contain `ServiceState.OPERATIONAL`.

## Decision

`READY`, request admission and `OPERATIONAL` SHALL remain distinct platform concepts.

### READY

`READY` means mandatory startup and readiness requirements have completed successfully.

Runtime in `READY` is eligible for request admission.

`READY` SHALL NOT itself mean that Runtime is `OPERATIONAL`.

### Request Admission

Request admission remains an independent Runtime-owned control.

Enabling request admission SHALL permit eligible new operational requests to enter the API hosting boundary.

Enabling request admission SHALL NOT itself transition Runtime to `OPERATIONAL`.

### OPERATIONAL

`OPERATIONAL` remains a distinct Runtime lifecycle state.

Runtime SHALL NOT enter `OPERATIONAL` merely because:

- Bootstrap completed successfully;
- Runtime entered `READY`;
- request admission was enabled;
- API hosting admitted a request.

A future transition from `READY` to `OPERATIONAL` requires a separately approved architecture contract defining the operational workload execution boundary and authorized Runtime transition.

### Runtime

Runtime remains the sole authoritative owner of platform lifecycle state.

Only an approved Runtime public operation may perform a future `OPERATIONAL` transition.

RFC-040 does not introduce that operation.

### Bootstrap

Bootstrap remains responsible for startup and shutdown coordination.

Successful Bootstrap startup terminates at Runtime `READY`, followed by request-admission enablement.

Bootstrap SHALL NOT transition Runtime to `OPERATIONAL` under RFC-040.

### Health Capability

Health Capability remains a read-only observation and reporting capability.

Health Capability SHALL NOT:

- determine Runtime readiness;
- enable or disable request admission;
- initiate or authorize an `OPERATIONAL` transition;
- maintain an independent platform lifecycle state;
- interpret enabled request admission as proof that Runtime is `OPERATIONAL`.

### API Hosting

API request-admission enforcement remains read-only with respect to Runtime lifecycle ownership.

Admitting an operational request SHALL NOT itself produce a Runtime lifecycle transition.

### Core Service Lifecycle

The `Operational` stage documented in CORE-002 represents target architectural lifecycle intent.

It SHALL NOT be interpreted as currently implemented `ServiceState` behavior.

RFC-040 SHALL NOT introduce `ServiceState.OPERATIONAL`.

Service lifecycle semantics remain separate from platform Runtime lifecycle semantics.

Any future service-level `OPERATIONAL` state requires dedicated architecture review.

### DEGRADED

`DEGRADED` remains deferred.

RFC-040 does not define degraded-state detection, transition, recovery or operational semantics.

## Rationale

This decision prevents three independent concepts from being collapsed into one implicit state transition.

It preserves Runtime as the single lifecycle authority.

It prevents Bootstrap, Health Capability and API hosting from becoming competing lifecycle decision owners.

It preserves current committed behavior while establishing an explicit architecture boundary for future operational workload execution.

It prevents documentation-only lifecycle intent from being mistaken for implemented service behavior.

## Consequences

Successful startup continues to terminate at Runtime `READY`.

Request admission may continue to be enabled after `READY`.

API hosting may continue to admit operational requests according to Runtime-owned admission state without changing lifecycle state.

Health Capability remains observation-only.

No production Python implementation changes are introduced by RFC-040.

No `ServiceState.OPERATIONAL` is introduced.

A future `READY` to `OPERATIONAL` implementation requires a dedicated RFC.

## Documentation Alignment

RFC-040 aligns:

- `BOOT-001 — Platform Bootstrap Lifecycle`
- `CAP-002 — Health Capability`
- `CORE-002 — Core Services Architecture`

`RUNTIME-001` remains authoritative for platform lifecycle state semantics.

## Future Impact

A future operational-transition RFC must define:

- the approved operational workload execution boundary;
- the authorized Runtime transition operation;
- exact `READY` to `OPERATIONAL` transition conditions;
- lifecycle observability requirements;
- interaction with request admission;
- failure semantics;
- shutdown interaction.

`DEGRADED`, traffic draining, retry, recovery, authentication and authorization remain separate architecture concerns.

---

# AD-027 — Operational Workload Entry Boundary

## Context

RFC-040 established that `READY`, request admission and `OPERATIONAL` are distinct platform concepts.

A future Runtime transition from `READY` to `OPERATIONAL` requires an approved operational workload execution boundary before lifecycle transition semantics can be defined.

PlantMind already contains an application workload path consisting of:

- `ApplicationFacade`
- `IntegrationGateway`
- `OrchestrationService`
- `WorkflowExecutor`

Before RFC-041, these components could construct downstream dependencies independently and were not part of the production `CompositionRoot` dependency graph.

The existing `ApplicationFacade` contract identifies it as the stable application-level entry point and directs external interfaces away from internal orchestration and reasoning services.

## Decision

The canonical PlantMind operational workload path SHALL be:

External Interface

↓

`ApplicationFacade`

↓

`IntegrationGateway`

↓

`OrchestrationService`

↓

`WorkflowExecutor`

↓

Approved reasoning and presentation capabilities

### ApplicationFacade

`ApplicationFacade` SHALL be the canonical application-level operational workload entry boundary.

Production external interfaces SHALL enter application workload execution through the composed `ApplicationFacade`.

External production interfaces SHALL NOT bypass `ApplicationFacade` by directly depending on internal orchestration or reasoning services unless separately architecture-approved.

### IntegrationGateway

`IntegrationGateway` SHALL remain the integration-isolation boundary.

It SHALL isolate external-facing integration concerns from internal application architecture.

It SHALL NOT compete with `ApplicationFacade` as the canonical application workload entry authority.

### OrchestrationService

`OrchestrationService` SHALL remain responsible for workflow coordination.

It SHALL NOT become the external production application entry authority.

### WorkflowExecutor

`WorkflowExecutor` SHALL remain responsible for concrete workflow execution.

It SHALL execute approved workflow stages without owning platform Runtime lifecycle state.

### Enterprise Engines

Enterprise Engines SHALL NOT own workflow orchestration or platform workload-entry responsibilities.

Cross-engine coordination SHALL continue through approved orchestration components.

### Composition Root

`CompositionRoot` SHALL own production construction of the operational workload dependency chain.

Production composition SHALL explicitly construct:

- `WorkflowExecutor`
- `OrchestrationService`
- `IntegrationGateway`
- `ApplicationFacade`

The same composed instances SHALL be registered in `ServiceContainer` and exposed through `PlatformComposition`.

Production composition SHALL NOT rely on independent implicit construction of parallel workload dependency chains.

Backward-compatible standalone constructors MAY remain where required by existing compatibility contracts and tests.

## Lifecycle Boundary

RFC-041 establishes the operational workload entry boundary but does not implement a Runtime transition to `OPERATIONAL`.

The following events SHALL NOT automatically modify Runtime lifecycle state under RFC-041:

- request admission;
- invocation of `ApplicationFacade`;
- invocation of `IntegrationGateway`;
- workflow execution;
- workflow completion.

Runtime remains the sole authoritative owner of platform lifecycle state.

A future operational-transition RFC MAY use execution through the RFC-041 workload boundary as lifecycle evidence only after defining:

- exact transition conditions;
- transition authority;
- failure semantics;
- lifecycle observation requirements;
- interaction with request admission;
- shutdown behavior.

## Rationale

This decision establishes one production workload entry path without introducing another application or orchestration layer.

It preserves existing component responsibilities and prevents external interfaces from coupling directly to internal workflow implementation.

It brings the workload path under Composition Root dependency ownership and prevents parallel production dependency graphs.

It establishes the prerequisite boundary required for future `READY` to `OPERATIONAL` lifecycle design without prematurely introducing that transition.

## Consequences

`ApplicationFacade` is now the canonical production workload entry boundary.

The workload dependency chain is explicitly composed by `CompositionRoot`.

The same workload instances are available through `ServiceContainer` and `PlatformComposition`.

Existing standalone construction remains backward compatible.

Runtime lifecycle behavior is unchanged.

Request-admission behavior is unchanged.

No `OPERATIONAL` or `DEGRADED` lifecycle transition is introduced.

No `ServiceState.OPERATIONAL` is introduced.

## Future Impact

A future Runtime operational-transition RFC must build on this workload boundary rather than creating a competing execution boundary.

Any new production external interface must consume the approved composed application boundary unless a separate architecture decision explicitly authorizes another path.

Authentication, authorization, traffic draining, retry, recovery and degraded-state behavior remain separate architecture concerns.

---

# AD-028 — Operational Transition Evidence and Lifecycle Authority

## Context

RFC-040 established that `READY`, request admission and `OPERATIONAL` are distinct platform concepts.

RFC-041 established `ApplicationFacade` as the canonical production operational workload entry boundary without changing Runtime lifecycle state.

RFC-042 reviewed the evidence required before PlantMind may safely implement a future `READY` to `OPERATIONAL` transition.

The current platform has authoritative Runtime-owned readiness and request-admission state, and it has an approved operational workload path.

However, the committed platform does not currently provide a trustworthy live observation contract proving that mandatory capabilities remain available during operational workload execution.

## Decision

Runtime SHALL remain the sole authoritative owner of platform lifecycle state.

Operational-transition eligibility SHALL be evaluated from two distinct classes of information:

### Runtime-Owned Preconditions

Runtime SHALL evaluate its own state directly.

A future operational transition SHALL require Runtime to verify:

- lifecycle state is `READY`;
- request admission is enabled.

These facts SHALL NOT be duplicated as externally supplied evidence.

External components SHALL NOT attest Runtime-owned state on Runtime behalf.

### External Operational Evidence

Operational-transition evidence SHALL represent independently observable facts that Runtime does not own directly.

The required evidence categories are:

- canonical operational workload entry through the composed `ApplicationFacade`;
- concrete workflow execution start through the composed `WorkflowExecutor`;
- trustworthy live availability of mandatory capabilities required for operational execution.

Evidence SHALL be immutable when passed across architecture boundaries.

Evidence SHALL NOT itself cause a lifecycle transition.

## Evidence Ownership

`ApplicationFacade` MAY provide evidence that the canonical operational workload boundary was entered.

`WorkflowExecutor` MAY provide evidence that concrete workflow execution started.

Neither component SHALL become a lifecycle decision authority.

Mandatory-capability availability SHALL be provided only through an approved read-only availability observation contract.

`ServiceRegistry` registration SHALL NOT be interpreted as availability.

Startup-time service validation SHALL NOT be interpreted as continuing availability.

Startup readiness evidence SHALL NOT be interpreted as continuing operational availability.

Current `HealthCapability` reporting SHALL NOT be treated as a substitute for a dedicated live capability-availability contract.

## Current Architecture Gap

No trustworthy mandatory-capability availability producer currently exists in the committed platform.

This gap SHALL block implementation of the Runtime `READY` to `OPERATIONAL` transition.

PlantMind SHALL NOT satisfy the gap by:

- hard-coded availability values;
- fabricated evidence;
- registration counts;
- startup-only validation results;
- assumptions derived from request admission;
- assumptions derived from workload completion.

## Lifecycle Authority

A future Runtime operational-transition operation SHALL evaluate:

- Runtime-owned lifecycle preconditions;
- trusted canonical workload-entry evidence;
- trusted workflow-execution-start evidence;
- trusted mandatory-capability availability evidence.

Only Runtime SHALL decide whether those conditions permit transition to `OPERATIONAL`.

`ApplicationFacade`, `IntegrationGateway`, `OrchestrationService`, `WorkflowExecutor`, API hosting and `HealthCapability` SHALL NOT transition Runtime lifecycle state.

## Consequences

RFC-042 introduces no production transition behavior.

No `mark_operational()`, `request_operational()` or equivalent Runtime operation is approved by this decision.

No `ServiceState.OPERATIONAL` is introduced.

No `DEGRADED` behavior is introduced.

The next architecture-controlled prerequisite is a trustworthy read-only capability-availability observation contract.

## Future Impact

A future RFC SHALL define the capability-availability observation boundary before any Runtime operational-transition implementation is approved.

That capability SHALL provide evidence only and SHALL remain separate from lifecycle decision authority.

A later Runtime operational-transition RFC may consume that evidence together with RFC-041 workload evidence and Runtime-owned preconditions.

---

# AD-029 — Mandatory Capability Availability Observation Boundary

## Context

RFC-042 established that a future Runtime `READY` to `OPERATIONAL` transition requires trustworthy live evidence that mandatory capabilities remain available during operational execution.

The existing platform did not provide a trusted live capability-availability observation contract.

`ServiceRegistry` provides registration and lookup semantics but does not prove current capability availability.

Startup validation and readiness evidence establish startup conditions but do not prove continuing availability.

`HealthCapability` is the authoritative read-only health reporting interface but is not the owner of capability-specific probes or lifecycle decisions.

RFC-043 establishes the missing availability observation boundary.

## Decision

PlantMind SHALL use a dedicated read-only capability-availability observation architecture.

The approved dependency direction is:

Capability-Specific Availability Sources

↓

`CapabilityAvailabilityObserver`

↓

Immutable `CapabilityAvailabilityObservation`

↓

Approved Consumers

`HealthCapability` MAY report approved availability observations in a future integration.

A future Runtime operational-transition contract MAY consume trusted availability evidence derived from this boundary.

Neither consumer becomes the owner of capability-specific observation.

## Availability State

Capability availability SHALL use:

`CapabilityAvailabilityState`

with exactly:

- `AVAILABLE`
- `UNAVAILABLE`
- `UNKNOWN`

`AVAILABLE` means a trusted source successfully established current availability.

`UNAVAILABLE` means a trusted source successfully established current unavailability.

`UNKNOWN` means trustworthy current availability could not be established.

Observation failure SHALL produce `UNKNOWN`.

`UNKNOWN` SHALL NOT be interpreted as `AVAILABLE`.

## Immutable Observation

`CapabilityAvailabilityObservation` SHALL be immutable and SHALL contain:

- `capability_name`;
- availability state;
- `observed_at`;
- `source_name`.

Capability and source identities SHALL be non-empty.

Observation timestamps SHALL be timezone-aware and normalized to UTC.

Naive timestamps SHALL be rejected.

The observation contains evidence only and carries no lifecycle-transition authority.

## Trusted Source Boundary

`CapabilityAvailabilitySource` SHALL define the abstract source contract for one explicitly identified capability.

A source SHALL expose:

- `capability_name`;
- `source_name`;
- `observe()`.

A source SHALL NOT:

- declare mandatory-capability policy;
- change Runtime lifecycle state;
- change request-admission state;
- fabricate availability evidence.

Production sources SHALL represent real approved observation mechanisms.

Test doubles MAY be used to verify contract behavior but SHALL NOT be treated as production sources.

## Observer Boundary

`CapabilityAvailabilityObserver` SHALL coordinate explicitly supplied trusted sources.

Observation order SHALL preserve explicit composition order and remain deterministic.

Failure of one source SHALL:

- produce `UNKNOWN` for that source capability;
- preserve the declared capability identity;
- preserve the declared source identity;
- not prevent observation of remaining sources.

An observer with no sources SHALL return no availability evidence.

The observer SHALL NOT:

- perform automatic discovery;
- scan packages;
- introduce a second service registry;
- infer mandatory-capability membership;
- convert `UNKNOWN` to `AVAILABLE`;
- modify Runtime lifecycle or request admission.

## Mandatory Capability Policy

Capability availability observation and mandatory-capability policy are separate responsibilities.

A capability source SHALL NOT declare itself mandatory.

Observer membership SHALL NOT imply mandatory status.

Mandatory-capability membership remains a future platform composition or configuration policy concern.

## HealthCapability Boundary

`HealthCapability` remains the authoritative read-only platform health reporting interface.

It MAY consume availability observations in a separately approved reporting integration.

It SHALL NOT become:

- the capability-specific probe owner;
- the operational-eligibility decision authority;
- the Runtime lifecycle transition authority.

## Runtime Boundary

Runtime remains the sole authoritative owner of platform lifecycle state.

Runtime SHALL NOT perform capability-specific availability probes.

RFC-043 introduces no Runtime `READY` to `OPERATIONAL` transition behavior.

A future operational-transition contract MAY consume trusted immutable availability evidence produced through this architecture.

## Composition Ownership

`CompositionRoot` SHALL own production construction and wiring of the single `CapabilityAvailabilityObserver`.

The same composed observer SHALL be registered in `ServiceContainer` and exposed through `PlatformComposition`.

No competing production availability-observation graph SHALL be independently constructed.

RFC-043 introduces no fabricated production capability sources.

The currently composed observer therefore has no production sources and produces no false availability evidence.

## Consequences

PlantMind now has a deterministic fail-closed availability observation foundation.

Availability evidence is attributable to explicit trusted sources.

Unknown availability remains distinguishable from confirmed unavailability.

One failing source cannot prevent observation of other capabilities.

Capability observation remains separate from lifecycle authority, health reporting and mandatory-capability policy.

No `OPERATIONAL`, `DEGRADED` or `ServiceState.OPERATIONAL` behavior is introduced.

## Verification

RFC-043 verification completed with:

- Contract commit: `0d30cfb`
- Technical commit: `ed807f0`
- Focused TDD suite: 15 passed
- Impacted regression: 40 passed
- Full regression: 278 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified

---

# AD-030 — Mandatory Capability Policy Boundary

## Context

RFC-042 established that a future Runtime `READY` to `OPERATIONAL` transition requires trusted operational evidence.

RFC-043 established the read-only capability-availability observation boundary but intentionally separated availability observation from mandatory-capability policy.

PlantMind therefore required an explicit policy contract defining which capabilities are mandatory without assigning that responsibility to configuration access, availability observation, health reporting or Runtime lifecycle ownership.

RFC-044 establishes that policy boundary.

## Decision

PlantMind SHALL use an explicit immutable:

`MandatoryCapabilityPolicy`

with an explicit:

`MandatoryCapabilityPolicyState`

The policy states SHALL be exactly:

- `UNCONFIGURED`
- `CONFIGURED`

Mandatory-capability policy SHALL remain a distinct responsibility from:

- `ConfigurationProvider`;
- `CapabilityAvailabilityObserver`;
- `HealthCapability`;
- `ServiceRegistry`;
- Runtime lifecycle state.

## Policy State Semantics

`UNCONFIGURED` means no approved mandatory-capability requirements have been established for the current platform composition or deployment.

An `UNCONFIGURED` policy SHALL contain no required capabilities.

`UNCONFIGURED` SHALL NOT represent successful operational eligibility.

`CONFIGURED` means explicit approved mandatory-capability requirements have been established.

A `CONFIGURED` policy SHALL contain at least one required capability.

A configured empty policy SHALL be invalid.

This distinction prevents future availability evaluation from treating an empty requirement collection as vacuously satisfied.

## Immutable Policy

`MandatoryCapabilityPolicy` SHALL be immutable.

It SHALL contain:

- `state`;
- `required_capabilities`.

Required capability identifiers SHALL:

- be strings;
- be non-empty;
- contain no leading or trailing whitespace;
- be unique.

Explicit requirement ordering SHALL be preserved.

Duplicate identifiers SHALL be rejected rather than silently collapsed.

## Policy Ownership

`MandatoryCapabilityPolicy` owns:

- mandatory-capability membership representation;
- policy-state invariants;
- capability-identifier validation;
- deterministic requirement ordering.

`ConfigurationProvider` remains responsible for configuration access and validation.

`ConfigurationProvider` SHALL NOT become the semantic owner of mandatory-capability policy.

A future configuration-backed integration MAY provide raw configured capability identifiers to policy construction while policy invariants remain owned by `MandatoryCapabilityPolicy`.

## Availability Boundary

`MandatoryCapabilityPolicy` defines what capabilities are required.

`CapabilityAvailabilityObserver` reports what trusted capability availability evidence currently exists.

Observer source membership SHALL NOT imply mandatory-policy membership.

Availability state SHALL NOT modify mandatory-policy membership.

Mandatory-policy membership SHALL NOT fabricate availability evidence.

## Runtime Boundary

Runtime remains the sole authoritative owner of platform lifecycle state.

Runtime SHALL NOT define mandatory-capability membership.

RFC-044 introduces no Runtime `READY` to `OPERATIONAL` transition behavior.

A future operational-eligibility contract MAY consume the mandatory policy together with trusted availability observations.

## HealthCapability Boundary

`HealthCapability` remains the authoritative read-only platform health reporting interface.

It SHALL NOT:

- define mandatory-capability membership;
- decide mandatory-policy satisfaction;
- decide operational eligibility;
- modify Runtime lifecycle state.

## Composition Ownership

`CompositionRoot` SHALL own construction of the production `MandatoryCapabilityPolicy`.

The same composed policy SHALL be:

- registered in `ServiceContainer`;
- exposed through `PlatformComposition`.

Production code SHALL NOT independently construct competing mandatory-capability policies.

Until real mandatory requirements are approved, production composition SHALL use one explicit `UNCONFIGURED` policy with no fabricated capability names.

## Consequences

PlantMind now distinguishes explicitly between:

- absence of approved mandatory requirements;
- configured mandatory requirements.

The platform does not infer mandatory status from availability sources or service registration.

The production policy remains explicitly unconfigured until real requirements are approved.

No availability coverage evaluator is introduced.

No `OPERATIONAL`, `DEGRADED` or `ServiceState.OPERATIONAL` behavior is introduced.

## Verification

RFC-044 verification completed with:

- Contract commit: `91c6090`
- Technical commit: `a709c0d`
- Focused TDD suite: 15 passed
- Impacted regression: 55 passed
- Full regression: 293 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified

---

# AD-031 — Mandatory Capability Coverage Evaluation Boundary

## Context

RFC-043 established trusted capability-availability observation.

RFC-044 established explicit immutable mandatory-capability policy.

PlantMind therefore required a deterministic boundary that compares mandatory requirements with supplied trusted availability observations without introducing lifecycle-transition authority.

RFC-045 establishes that coverage-evaluation boundary.

## Decision

PlantMind SHALL use:

`MandatoryCapabilityCoverageEvaluator`

to evaluate one explicit `MandatoryCapabilityPolicy` against supplied immutable `CapabilityAvailabilityObservation` evidence.

The evaluator SHALL remain deterministic, read-only and fail closed.

## Coverage State

Coverage SHALL use:

`MandatoryCapabilityCoverageState`

with exactly:

- `SATISFIED`
- `UNSATISFIED`

`SATISFIED` means every required capability in a configured policy is proven by exactly one matching `AVAILABLE` observation.

`UNSATISFIED` means mandatory capability coverage cannot be proven.

Coverage state SHALL NOT represent Runtime lifecycle state.

## Immutable Coverage Result

`MandatoryCapabilityCoverageResult` SHALL be immutable.

It SHALL report:

- overall coverage state;
- required capabilities;
- satisfied capabilities;
- missing capabilities;
- unavailable capabilities;
- unknown capabilities;
- ambiguous capabilities.

Diagnostic ordering SHALL preserve mandatory-policy requirement order.

Each required capability in a configured policy SHALL receive exactly one diagnostic classification.

The result SHALL contain evidence only and SHALL NOT carry lifecycle-transition authority.

## Unconfigured Policy Semantics

An `UNCONFIGURED` mandatory-capability policy SHALL always produce `UNSATISFIED`.

It SHALL NOT succeed because the requirement collection is empty.

Supplied availability evidence SHALL NOT convert an unconfigured policy into satisfied coverage.

## Configured Policy Semantics

For each required capability:

No matching observation SHALL classify the capability as missing.

Exactly one `AVAILABLE` observation SHALL classify the capability as satisfied.

Exactly one `UNAVAILABLE` observation SHALL classify the capability as unavailable.

Exactly one `UNKNOWN` observation SHALL classify the capability as unknown.

More than one matching observation SHALL classify the capability as ambiguous.

Any missing, unavailable, unknown or ambiguous required capability SHALL produce overall `UNSATISFIED`.

## Ambiguity Boundary

RFC-045 SHALL NOT perform multi-source aggregation.

When multiple observations match one required capability, the evaluator SHALL NOT:

- select the newest observation;
- select the oldest observation;
- prefer `AVAILABLE`;
- prefer `UNAVAILABLE`;
- assign source priority;
- merge source states.

Multiple matching observations SHALL fail closed as ambiguous.

## Freshness Boundary

RFC-045 SHALL NOT define observation freshness.

The evaluator SHALL NOT introduce:

- TTL;
- maximum observation age;
- staleness thresholds;
- current-time comparisons.

Timestamp freshness requires a separately approved architecture contract.

## Non-Required Evidence

Observations for capabilities not present in the mandatory policy SHALL NOT affect mandatory coverage.

Availability evidence SHALL NOT create mandatory-policy membership.

## Availability Boundary

`CapabilityAvailabilityObserver` remains responsible for collecting trusted availability observations.

`MandatoryCapabilityCoverageEvaluator` evaluates supplied observations against mandatory policy.

The evaluator SHALL NOT perform capability-specific probes or modify availability observation infrastructure.

## Policy Boundary

`MandatoryCapabilityPolicy` remains the owner of mandatory-capability membership.

The evaluator SHALL consume the supplied policy and SHALL NOT construct or modify an independent policy.

## Runtime Boundary

Runtime remains the sole authoritative owner of platform lifecycle state.

A `SATISFIED` coverage result is evidence only.

Coverage evaluation SHALL NOT:

- modify Runtime lifecycle state;
- modify request-admission state;
- transition Runtime to `OPERATIONAL`.

RFC-045 introduces no Runtime operational-transition behavior.

## Composition Ownership

`CompositionRoot` SHALL own production construction of the single `MandatoryCapabilityCoverageEvaluator`.

The evaluator SHALL receive the exact composed `MandatoryCapabilityPolicy` instance.

The same evaluator SHALL be registered in `ServiceContainer` and exposed through `PlatformComposition`.

Production code SHALL NOT construct competing coverage evaluators backed by independent mandatory policies.

## Consequences

PlantMind now has an explicit fail-closed bridge between mandatory-capability policy and trusted availability evidence.

The architecture distinguishes:

- what capabilities are required;
- what capability availability is observed;
- whether mandatory requirements are covered;
- whether Runtime should transition lifecycle state.

These remain separate responsibilities.

No multi-source aggregation, freshness policy, `OPERATIONAL`, `DEGRADED` or `ServiceState.OPERATIONAL` behavior is introduced.

## Verification

RFC-045 verification completed with:

- Contract commit: `9abde19`
- Technical commit: `0b410ce`
- Focused TDD suite: 16 passed
- Impacted regression: 71 passed
- Full regression: 309 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified

---

# AD-032 — Operational Workload Evidence Boundary

## Context

RFC-042 established that trustworthy operational-transition evidence requires proof that a workload:

- entered through the canonical `ApplicationFacade`;
- reached concrete execution start through `WorkflowExecutor`.

RFC-045 separately established mandatory-capability coverage evidence.

PlantMind therefore required a correlated workload-evidence boundary without introducing operational-eligibility decisions or Runtime lifecycle-transition authority.

RFC-046 establishes that boundary.

## Decision

PlantMind SHALL represent trusted canonical workload provenance through immutable correlated operational-workload evidence.

Each canonical `ApplicationFacade.analyze()` invocation SHALL originate exactly one workload identity.

The same workload identity SHALL propagate unchanged through:

`ApplicationFacade`
→ `IntegrationGateway`
→ `OrchestrationService`
→ `WorkflowExecutor`

## Workload Identity

Canonical workload identity SHALL use `UUID`.

`ApplicationFacade` SHALL generate the identity once for each canonical invocation.

Intermediate layers SHALL NOT replace or regenerate that identity.

Separate canonical facade invocations SHALL use distinct workload identities.

## Facade Entry Evidence

`ApplicationFacadeEntryEvidence` SHALL represent proof that a workload entered through the canonical application facade.

It SHALL be immutable and contain:

`workload_id: UUID`

`ApplicationFacade` owns production creation of this evidence.

## Execution Start Evidence

`WorkflowExecutionStartEvidence` SHALL represent proof that the correlated workload reached concrete workflow execution start.

It SHALL be immutable and contain:

`workload_id: UUID`

`WorkflowExecutor` SHALL create this evidence only when canonical facade-entry evidence has been propagated to it.

The execution-start workload identity SHALL match the propagated facade-entry workload identity.

## Correlated Evidence

`OperationalWorkloadEvidence` SHALL contain:

- `facade_entry: ApplicationFacadeEntryEvidence`
- `execution_start: WorkflowExecutionStartEvidence`

It SHALL be immutable.

Construction SHALL fail when the two evidence objects contain different workload identities.

Matching workload identity establishes correlation between canonical facade entry and concrete workflow execution start.

## Propagation Boundary

`IntegrationGateway` and `OrchestrationService` SHALL forward supplied facade-entry evidence unchanged.

They SHALL NOT:

- originate canonical facade-entry evidence;
- replace workload identity;
- regenerate workload identity;
- create lifecycle-transition decisions.

## Workflow Execution Exposure

`WorkflowExecution` SHALL optionally expose:

`operational_workload_evidence: OperationalWorkloadEvidence | None`

Existing result, stage and completion semantics SHALL remain unchanged.

Canonical facade execution SHALL return correlated operational-workload evidence when workflow execution completes successfully.

Direct internal execution without canonical facade-entry evidence SHALL NOT fabricate operational-workload evidence.

## Direct Internal Invocation

Direct invocation of:

- `IntegrationGateway.execute()`;
- `OrchestrationService.run()`;
- `WorkflowExecutor.execute()`;

without facade-entry evidence remains supported.

Such execution SHALL produce no canonical operational-workload evidence.

Internal workflow execution alone is insufficient proof of canonical application-facade entry.

## Failure Boundary

RFC-046 SHALL NOT introduce a persistent or global evidence recorder.

If workflow execution raises before a `WorkflowExecution` result is returned, completed correlated workload evidence SHALL NOT be fabricated for the caller.

Historical tracing, partial in-flight evidence persistence and failure-event recording remain separate concerns.

## Trust Boundary

RFC-046 establishes trusted in-process architectural provenance through canonical ownership and propagation boundaries.

It does not establish:

- cryptographic attestation;
- cross-process signing;
- distributed trace authentication;
- external identity verification.

## Capability Coverage Boundary

Operational workload evidence remains independent from:

- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityPolicy`;
- `MandatoryCapabilityCoverageEvaluator`;
- `MandatoryCapabilityCoverageResult`.

RFC-046 SHALL NOT combine workload evidence and mandatory-capability coverage into operational eligibility.

## Runtime Boundary

Runtime remains the sole authoritative owner of platform lifecycle state.

Operational workload evidence is evidence only.

RFC-046 SHALL NOT:

- modify Runtime lifecycle state;
- modify request admission;
- add `Runtime.mark_operational()`;
- add `Runtime.request_operational()`;
- transition Runtime from `READY` to `OPERATIONAL`;
- introduce `DEGRADED` behavior.

## Composition Boundary

RFC-046 preserves the canonical production chain owned by `CompositionRoot`.

It SHALL NOT introduce duplicate facade, gateway, orchestration-service or workflow-executor authorities.

No global mutable workload-evidence registry is introduced.

## Consequences

PlantMind now possesses trustworthy correlated evidence proving that the same canonical workload:

- entered through `ApplicationFacade`;
- reached concrete execution start through `WorkflowExecutor`.

This closes the workload-provenance evidence gap identified by RFC-042 while preserving separation between evidence and lifecycle authority.

Operational eligibility and Runtime transition remain outside RFC-046.

## Verification

RFC-046 verification completed with:

- Contract commit: `2365b68`
- Technical commit: `6aca0a1`
- Focused TDD suite: 18 passed
- Impacted regression: 32 passed
- Full regression: 327 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified

---

# AD-033 — Operational Transition Evidence Aggregation Boundary

## Context

AD-028 established that future Runtime operational-transition evaluation must distinguish Runtime-owned preconditions from externally supplied operational evidence.

RFC-045 established mandatory-capability coverage evidence.

RFC-046 established correlated operational-workload evidence.

PlantMind therefore required one immutable fail-closed aggregate for approved external operational-transition evidence without duplicating Runtime-owned state or introducing lifecycle-transition authority.

RFC-047 establishes that boundary.

## Decision

PlantMind SHALL represent externally supplied operational-transition evidence through immutable:

`OperationalTransitionEvidence`

containing:

- `operational_workload: OperationalWorkloadEvidence | None`
- `mandatory_capability_coverage: MandatoryCapabilityCoverageResult | None`

The aggregate SHALL use immutable value semantics.

## External Evidence Completeness

`OperationalTransitionEvidence` SHALL expose derived:

`is_complete: bool`

External evidence is complete only when:

- operational-workload evidence is present;
- mandatory-capability coverage evidence is present;
- mandatory-capability coverage state is `SATISFIED`.

Every incomplete or unsatisfied combination SHALL fail closed.

`is_complete` represents external evidence completeness only.

It SHALL NOT represent final Runtime operational eligibility.

## Runtime-Owned Preconditions

The aggregate SHALL NOT contain or duplicate:

- Runtime lifecycle state;
- Runtime readiness;
- request-admission state;
- external readiness attestations;
- external request-admission attestations.

Runtime remains responsible for evaluating its own lifecycle state and request-admission state directly.

## Workload Evidence Boundary

RFC-047 consumes existing validated `OperationalWorkloadEvidence`.

It SHALL NOT:

- recreate canonical facade-entry evidence;
- recreate workflow-execution-start evidence;
- generate workload identity;
- replace workload identity;
- repeat workload-correlation validation;
- fabricate canonical workload provenance.

Operational-workload correlation remains owned by RFC-046.

## Mandatory Capability Coverage Boundary

RFC-047 consumes existing `MandatoryCapabilityCoverageResult`.

It SHALL NOT:

- collect availability observations;
- construct mandatory-capability policy;
- perform mandatory-capability coverage evaluation;
- reclassify missing, unavailable, unknown or ambiguous capabilities.

Mandatory-capability coverage semantics remain owned by RFC-045.

Only `SATISFIED` coverage satisfies the capability portion of external transition evidence.

## Evidence Identity

The aggregate SHALL preserve the exact evidence objects supplied to it.

It SHALL NOT copy, normalize, replace or mutate either evidence category.

This preserves explicit provenance and evidence identity.

## Determinism

For the same supplied evidence objects, external evidence completeness SHALL remain deterministic.

RFC-047 introduces no:

- current-time checks;
- freshness policy;
- TTL;
- retry;
- probing;
- source priority;
- external I/O;
- mutable internal state.

## Evidence Ownership

RFC-047 SHALL NOT introduce a global mutable evidence collector, recorder or persistent aggregate.

`OperationalTransitionEvidence` is per-evaluation evidence constructed explicitly from already produced evidence objects.

`CompositionRoot` SHALL NOT maintain a global operational-transition evidence instance.

## Lifecycle Authority

Runtime remains the sole authoritative owner of platform lifecycle state.

A complete `OperationalTransitionEvidence` aggregate remains evidence only.

RFC-047 SHALL NOT:

- transition Runtime;
- modify Runtime;
- modify request admission;
- add `Runtime.mark_operational()`;
- add `Runtime.request_operational()`;
- introduce `DEGRADED`;
- introduce `ServiceState.OPERATIONAL`.

## Future Runtime Transition Boundary

A future separately approved RFC may allow Runtime to consume:

- `OperationalTransitionEvidence`;
- Runtime-owned lifecycle state;
- Runtime-owned request-admission state.

Runtime SHALL independently validate its own preconditions under that future contract.

RFC-047 does not implement that transition.

## Consequences

PlantMind now possesses a single immutable fail-closed aggregate for approved external operational-transition evidence.

The architecture now separates:

- Runtime-owned lifecycle preconditions;
- correlated operational-workload evidence;
- mandatory-capability coverage evidence;
- external evidence completeness;
- final Runtime lifecycle-transition authority.

No final operational-eligibility decision or `READY` to `OPERATIONAL` transition is introduced.

## Verification

RFC-047 verification completed with:

- Contract commit: `35004dc`
- Technical commit: `ebc4769`
- Focused TDD suite: 17 passed
- Impacted regression: 56 passed
- Full regression: 344 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified

# AD-034 — Runtime Operational Transition Authority Boundary

## Status

Accepted.

## Context

AD-028 established Runtime as the sole authoritative lifecycle owner.

RFC-047 established immutable `OperationalTransitionEvidence` as the aggregate of approved external operational-transition evidence.

The remaining architectural gap was the authoritative decision boundary for entering `RuntimeState.OPERATIONAL`.

Runtime already owned:

- lifecycle state;
- readiness state;
- request admission.

External transition evidence already represented:

- correlated canonical operational-workload evidence;
- mandatory-capability coverage evidence;
- deterministic external evidence completeness.

A second eligibility service or lifecycle authority would duplicate Runtime responsibility and weaken lifecycle ownership.

## Decision

Runtime SHALL remain the sole authority capable of deciding and executing the `READY` to `OPERATIONAL` lifecycle transition.

The guarded transition operation is:

`Runtime.request_operational(evidence: OperationalTransitionEvidence) -> None`

Runtime SHALL transition to `RuntimeState.OPERATIONAL` only when:

- current lifecycle state is exactly `RuntimeState.READY`;
- request admission is enabled;
- supplied `OperationalTransitionEvidence.is_complete` is `True`.

Runtime SHALL evaluate lifecycle state and request admission directly.

External evidence SHALL NOT duplicate Runtime-owned lifecycle or admission state.

No public `mark_operational()` bypass SHALL exist.

## Failure Semantics

Operational-transition rejection is fail-closed and atomic.

If any required precondition is not satisfied:

- `RuntimeError` is raised;
- lifecycle state remains unchanged;
- readiness remains unchanged;
- request admission remains unchanged;
- supplied evidence remains unchanged.

Incomplete external evidence SHALL NOT automatically cause `FAILED`, `STOPPED` or `DEGRADED`.

Rejected transition SHALL NOT automatically disable request admission.

## Successful Transition Semantics

A successful transition performs only:

`READY` → `OPERATIONAL`

After success:

- `Runtime.state` is `RuntimeState.OPERATIONAL`;
- Runtime remains ready;
- request admission remains enabled.

No separate operational boolean or duplicate operational lifecycle state is introduced.

## Authority Boundaries

Bootstrap SHALL NOT automatically transition Runtime to `OPERATIONAL`.

`ApplicationFacade`, `IntegrationGateway`, `OrchestrationService` and `WorkflowExecutor` SHALL NOT own or invoke lifecycle-transition authority as part of RFC-048.

`HealthCapability` remains read-only reporting.

`CompositionRoot` SHALL NOT introduce an operational-transition manager, independent operational-eligibility evaluator or competing lifecycle controller.

Existing workload-evidence, capability-availability, capability-policy, capability-coverage and transition-evidence responsibilities remain unchanged.

## Consequences

PlantMind now has an explicit authoritative path from startup readiness into operational lifecycle state.

The operational transition is guarded by both Runtime-owned preconditions and approved external evidence while maintaining strict separation of responsibility.

Repeated transition requests after Runtime has already entered `OPERATIONAL` are rejected because the transition is valid only from exactly `READY`.

RFC-048 does not introduce:

- automatic operational transition;
- operational recovery;
- `DEGRADED` transition behavior;
- evidence freshness or TTL;
- traffic draining;
- retry behavior;
- `ServiceState.OPERATIONAL`.

## Verification

- RFC-048 contract commit: `ac1c625`
- RFC-048 technical commit: `b714ceb`
- Focused TDD suite: 18 passed
- Impacted regression: 93 passed
- Full regression: 362 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified

# AD-035 — Mandatory Capability Composition Boundary

## Status

Accepted.

## Context

RFC-043 established the capability availability observation boundary.

RFC-044 established immutable mandatory-capability policy.

RFC-045 established deterministic fail-closed mandatory-capability coverage evaluation.

RFC-048 established Runtime as the sole authoritative operational-transition authority.

Before RFC-049, canonical production composition always created:

- `CapabilityAvailabilityObserver(sources=())`;
- an `UNCONFIGURED` empty `MandatoryCapabilityPolicy`.

This preserved safe fail-closed behavior but provided no canonical composition-time path for deployment-approved availability sources or mandatory-capability policy.

## Decision

`CompositionRoot` SHALL provide the canonical composition-time injection boundary for:

- capability availability sources;
- mandatory-capability policy.

The existing architecture types remain authoritative:

- `CapabilityAvailabilitySource`;
- `MandatoryCapabilityPolicy`;
- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityCoverageEvaluator`.

No duplicate capability configuration model is introduced.

## Fail-Closed Default

When no capability availability sources are supplied, the observer SHALL contain no sources.

When no mandatory-capability policy is supplied, composition SHALL create the existing canonical policy:

- state `MandatoryCapabilityPolicyState.UNCONFIGURED`;
- empty `required_capabilities`.

Default mandatory-capability coverage therefore remains `UNSATISFIED`.

RFC-049 does not weaken default fail-closed behavior.

## Policy Identity

When a `MandatoryCapabilityPolicy` is explicitly supplied:

- the exact supplied instance is exposed through `PlatformComposition`;
- the exact supplied instance is registered in `ServiceContainer`;
- the exact supplied instance is consumed by `MandatoryCapabilityCoverageEvaluator`.

CompositionRoot SHALL NOT copy, reconstruct, normalize or reinterpret the supplied policy.

Policy validation remains owned by `MandatoryCapabilityPolicy`.

## Availability Source Identity

Explicitly supplied availability sources SHALL be forwarded to the existing `CapabilityAvailabilityObserver`.

Composition SHALL preserve:

- source ordering;
- source object identity.

CompositionRoot SHALL NOT:

- invoke sources during composition;
- merge sources;
- deduplicate sources;
- prioritize sources;
- reinterpret source observations.

Observation behavior remains owned by `CapabilityAvailabilityObserver`.

## Missing and Duplicate Source Semantics

A configured mandatory-capability policy does not require matching sources at composition time.

Missing observations remain coverage diagnostics owned by `MandatoryCapabilityCoverageEvaluator`.

Multiple sources for the same capability SHALL remain preserved.

Existing ambiguous-capability coverage semantics remain authoritative.

CompositionRoot SHALL NOT introduce source-selection policy.

## Configuration Ownership

`ConfigurationProvider` does not own mandatory-capability policy.

Core composition remains capability-name agnostic.

Deployment-specific capability identifiers SHALL NOT be invented or hard-coded by CompositionRoot.

Deployment-approved policy and source construction occur outside core composition decision logic and are supplied explicitly through the composition boundary.

## Runtime Boundary

Capability composition SHALL NOT modify Runtime lifecycle behavior.

CompositionRoot SHALL NOT call:

`Runtime.request_operational(...)`

Composition of availability sources or mandatory-capability policy does not automatically cause an operational transition.

Runtime remains the sole lifecycle-transition authority.

## Operational Transition Evidence Boundary

RFC-049 does not construct `OperationalTransitionEvidence`.

RFC-049 does not combine operational-workload evidence with mandatory-capability coverage.

Operational-transition coordination remains a separate future architecture concern.

## Compatibility

`build_platform_composition(...)` SHALL remain a backward-compatible composition factory.

It SHALL forward RFC-049 capability inputs to `CompositionRoot.build(...)`.

Existing callers using no arguments or only plugin registrations remain supported.

## Consequences

PlantMind now has a canonical deployment-neutral path for supplying real mandatory-capability dependencies without weakening core fail-closed behavior.

The platform can now compose deployment-approved capability sources and policy while keeping:

- observation ownership separate;
- coverage ownership separate;
- configuration ownership separate;
- Runtime lifecycle authority separate.

RFC-049 introduces no concrete production capability sources and no deployment-specific mandatory capability names.

## Verification

- RFC-049 contract commit: `ca5ccbf`
- RFC-049 technical commit: `496fe42`
- Focused TDD suite: 15 passed
- Impacted regression: 101 passed
- Full regression: 377 passed
- Compilation: passed
- `git diff --cached --check`: passed
- Remote technical push: verified

# AD-036 — Operational Transition Coordination Boundary

## Status

Accepted.

## Context

RFC-043 established the capability availability observation boundary.

RFC-045 established deterministic fail-closed mandatory-capability coverage evaluation.

RFC-046 established canonical operational-workload evidence.

RFC-047 established immutable operational-transition evidence aggregation.

RFC-048 established Runtime as the sole authoritative operational-transition authority.

RFC-049 established the canonical composition boundary for deployment-approved capability availability sources and mandatory-capability policy.

Before RFC-050, PlantMind had all required evidence components and Runtime authority, but no canonical boundary responsible for coordinating those components into an explicit operational-transition request.

## Decision

PlantMind SHALL provide an `OperationalTransitionCoordinator` as the canonical operational-transition coordination boundary.

The coordinator SHALL:

- accept approved `OperationalWorkloadEvidence` or `None`;
- obtain live capability observations through `CapabilityAvailabilityObserver`;
- evaluate mandatory-capability coverage through `MandatoryCapabilityCoverageEvaluator`;
- construct one immutable `OperationalTransitionEvidence`;
- delegate the authoritative lifecycle decision to `Runtime.request_operational(...)`.

The coordinator coordinates evidence.

Runtime remains the sole lifecycle-transition authority.

## Dependency Boundary

`OperationalTransitionCoordinator` SHALL depend on the exact canonical instances of:

- `Runtime`;
- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityCoverageEvaluator`.

It SHALL NOT own:

- Runtime lifecycle state;
- request admission;
- mandatory-capability policy;
- capability source definitions;
- workload execution;
- workload evidence generation.

## Workload Evidence Boundary

The public coordination operation SHALL accept:

`OperationalWorkloadEvidence | None`

A `WorkflowExecution` is not an approved coordinator input.

The coordinator SHALL NOT:

- create workload identifiers;
- reconstruct workload evidence;
- inspect workflow stages;
- extract evidence from `WorkflowExecution`;
- revalidate workload UUID semantics.

`None` remains valid incomplete external evidence and fails closed through existing transition semantics.

## Availability Observation Boundary

Each operational-transition request SHALL invoke:

`CapabilityAvailabilityObserver.observe_all()`

exactly once.

The exact observation tuple returned by the observer SHALL be supplied unchanged to `MandatoryCapabilityCoverageEvaluator`.

The coordinator SHALL NOT:

- invoke capability sources directly;
- retry source observations;
- cache observations;
- merge observations;
- reorder observations;
- apply source priority;
- introduce freshness or TTL policy.

Source failures remain owned and contained by `CapabilityAvailabilityObserver` according to existing `UNKNOWN` semantics.

## Coverage Evaluation Boundary

Each coordination request SHALL invoke mandatory-capability coverage evaluation exactly once.

The coordinator SHALL preserve the exact coverage result returned by `MandatoryCapabilityCoverageEvaluator`.

It SHALL NOT:

- inspect mandatory-capability policy;
- independently classify capability observations;
- modify coverage diagnostics;
- fabricate capability coverage.

Coverage semantics remain owned exclusively by `MandatoryCapabilityCoverageEvaluator`.

## Operational Transition Evidence

The coordinator SHALL construct exactly one `OperationalTransitionEvidence` after observation and coverage evaluation.

The evidence SHALL preserve by identity:

- the supplied workload evidence;
- the evaluator-produced mandatory-capability coverage result.

The coordinator SHALL NOT copy, normalize, reconstruct or reinterpret either component.

## Runtime Authority

The exact constructed `OperationalTransitionEvidence` SHALL be passed to:

`Runtime.request_operational(...)`

exactly once.

The coordinator SHALL NOT inspect Runtime lifecycle state, readiness or request-admission state before delegation.

Runtime SHALL independently evaluate all Runtime-owned transition prerequisites.

The coordinator SHALL NOT:

- call an unguarded operational transition;
- mutate Runtime state directly;
- enable or disable request admission;
- retry a rejected transition;
- reinterpret Runtime rejection.

On success, the coordinator SHALL return the exact evidence object supplied to Runtime.

## Failure Semantics

Runtime rejection SHALL propagate to the caller without retry.

Unexpected observer or evaluator failures SHALL propagate before Runtime is called.

Coordinator failure SHALL NOT independently transition Runtime to:

- `FAILED`;
- `DEGRADED`;
- `STOPPED`;
- any other lifecycle state.

The coordinator introduces no independent recovery or lifecycle policy.

## Composition Boundary

`CompositionRoot` SHALL construct exactly one `OperationalTransitionCoordinator` from the existing canonical Runtime, observer and evaluator instances.

The exact coordinator instance SHALL be:

- exposed through `PlatformComposition`;
- registered in `ServiceContainer`.

Composition SHALL preserve dependency identity.

`CompositionRoot.build(...)` SHALL NOT execute an operational-transition request.

## Automatic Transition Boundary

RFC-050 introduces no automatic operational transition.

The following SHALL NOT implicitly invoke the coordinator:

- `BootstrapManager.startup()`;
- `ApplicationFacade.analyze(...)`;
- `IntegrationGateway`;
- `OrchestrationService`;
- `WorkflowExecutor`;
- `HealthCapability`;
- `CompositionRoot.build(...)`.

Operational-transition coordination remains an explicit operation.

## State and Persistence Boundary

`OperationalTransitionCoordinator` SHALL remain stateless between requests.

It SHALL NOT maintain:

- last transition evidence;
- evidence history;
- transition history;
- queues;
- global coordination state.

RFC-050 introduces no evidence persistence.

## Consequences

PlantMind now has a canonical explicit path:

External operational-workload evidence
→ live capability observation
→ mandatory-capability coverage evaluation
→ operational-transition evidence
→ Runtime authority.

This closes the coordination gap between RFC-043 through RFC-049 without weakening lifecycle ownership or fail-closed behavior.

Runtime remains the sole authority that decides whether the platform may enter `OPERATIONAL`.

## Verification

- RFC-050 contract commit: `0001bf0`
- RFC-050 technical commit: `995a73b`
- Focused RFC-050 suite: 21 passed
- Impacted core regression: 261 passed
- Full regression: 398 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

# AD-037 — Explicit Operational Transition Application Boundary

## Status

Accepted.

## Context

RFC-041 established `ApplicationFacade` as the canonical application-level operational workload entry boundary.

RFC-046 established trusted correlated `OperationalWorkloadEvidence` produced by the canonical workload execution path.

RFC-048 established Runtime as the sole authoritative `READY` to `OPERATIONAL` lifecycle-transition authority.

RFC-050 established `OperationalTransitionCoordinator` as the canonical operational-transition evidence coordination boundary.

Before RFC-051, PlantMind had no canonical application-level use-case boundary connecting workload execution through `ApplicationFacade` with an explicit operational-transition request through `OperationalTransitionCoordinator`.

Placing that coordination directly in FastAPI would move application orchestration and workload-evidence trust into the transport layer.

## Decision

PlantMind SHALL provide an:

`OperationalTransitionApplicationService`

as the canonical application-level boundary for the explicit combined workload-and-operational-transition use case.

The approved operation is:

`request_operational(observations: tuple[Observation, ...]) -> OperationalTransitionApplicationResult`

The service SHALL remain an application coordinator.

It SHALL NOT become a lifecycle authority.

## Dependency Boundary

`OperationalTransitionApplicationService` SHALL depend on the exact canonical instances of:

- `ApplicationFacade`;
- `OperationalTransitionCoordinator`.

It SHALL NOT directly depend on:

- `Runtime`;
- `IntegrationGateway`;
- `OrchestrationService`;
- `WorkflowExecutor`;
- reasoning services;
- presentation services.

## Observation Boundary

The service SHALL consume existing immutable:

`Observation`

domain objects.

Observation validation remains owned by `Observation`.

RFC-051 introduces no duplicate observation model and no transport-specific deserialization responsibility.

## Workload Execution Boundary

Each explicit request SHALL invoke:

`ApplicationFacade.analyze(...)`

exactly once.

The exact observation tuple supplied to the application service SHALL be forwarded unchanged to `ApplicationFacade`.

`ApplicationFacade` remains the canonical operational workload-entry boundary.

The application service SHALL NOT construct an alternate workload execution path.

## Workload Evidence Trust Boundary

The application service SHALL obtain workload evidence only from:

`WorkflowExecution.operational_workload_evidence`

returned by the canonical `ApplicationFacade` execution path.

It SHALL NOT:

- create workload identifiers;
- create workload-entry evidence;
- create workflow-execution-start evidence;
- construct `OperationalWorkloadEvidence`;
- reconstruct workload evidence;
- accept workload evidence from an external client;
- validate workload UUID correlation independently;
- infer workload evidence from workflow stages.

The exact workload-evidence value, including `None`, SHALL be forwarded unchanged to `OperationalTransitionCoordinator`.

## Transition Coordination Boundary

The application service SHALL invoke:

`OperationalTransitionCoordinator.request_operational(...)`

exactly once after successful workload execution.

It SHALL NOT:

- construct `OperationalTransitionEvidence`;
- observe mandatory capabilities;
- evaluate mandatory-capability coverage;
- inspect mandatory-capability policy;
- inspect Runtime state;
- inspect Runtime readiness;
- inspect request admission;
- call `Runtime.request_operational(...)` directly.

Runtime remains the sole authoritative lifecycle-transition authority.

## Application Result

RFC-051 introduces immutable:

`OperationalTransitionApplicationResult`

containing:

- the exact `WorkflowExecution` returned by `ApplicationFacade`;
- the exact `OperationalTransitionEvidence` returned by `OperationalTransitionCoordinator`.

The result preserves object identity.

It is not lifecycle state, transition authority, eligibility state or persistent transition history.

## Failure Semantics

If `ApplicationFacade.analyze(...)` fails:

- the exception propagates;
- the coordinator is not invoked;
- workload execution is not retried;
- no synthetic workload evidence is created;
- no operational-transition request is attempted.

If `OperationalTransitionCoordinator.request_operational(...)` fails:

- the exception propagates;
- the coordinator is not retried;
- workload execution is not repeated;
- Runtime state is not independently modified;
- request admission is not independently modified.

Existing Runtime and coordinator failure semantics remain authoritative.

## No Automatic Lifecycle Side Effects

Normal calls to:

`ApplicationFacade.analyze(...)`

remain workload-only operations.

RFC-051 SHALL NOT automatically request an operational transition after ordinary workload execution.

The combined use case occurs only through an explicit invocation of `OperationalTransitionApplicationService`.

## Composition Boundary

`CompositionRoot` SHALL compose exactly one `OperationalTransitionApplicationService`.

The exact service instance SHALL be:

- exposed through `PlatformComposition`;
- registered in `ServiceContainer`.

Its dependencies SHALL be the exact composed:

- `ApplicationFacade`;
- `OperationalTransitionCoordinator`.

CompositionRoot SHALL NOT execute the service during build.

## Bootstrap and Health Boundaries

Bootstrap SHALL NOT invoke the application service.

Health SHALL NOT invoke the application service.

RFC-051 introduces no startup-triggered or health-triggered operational transition.

## API Boundary

RFC-051 introduces no HTTP endpoint and no FastAPI routing changes.

The API hosting layer SHALL NOT construct workload evidence or directly coordinate internal workload and Runtime-transition components.

A future external-interface contract MAY expose this approved application service through HTTP or another transport.

Any such operational interface remains subject to Runtime-owned request-admission enforcement unless separately architecture-approved.

## State and Persistence Boundary

`OperationalTransitionApplicationService` SHALL remain stateless between requests.

It SHALL NOT maintain:

- last workflow execution;
- last workload evidence;
- last transition evidence;
- transition history;
- retry queues;
- lifecycle state;
- operational eligibility state.

## Consequences

PlantMind now has a canonical application-level path:

External Interface
→ `OperationalTransitionApplicationService`
→ `ApplicationFacade`
→ trusted `WorkflowExecution`
→ trusted operational-workload evidence
→ `OperationalTransitionCoordinator`
→ Runtime authority.

This keeps workload evidence generated inside the approved application path, prevents the transport layer from becoming an application orchestrator, and preserves Runtime as the sole lifecycle-transition authority.

## Verification

- RFC-051 contract commit: `ccdd80d`
- RFC-051 technical commit: `866f786`
- Focused RFC-051 suite: 18 passed
- Impacted services/core regression: 348 passed
- Full regression: 416 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified


---

# AD-038 — Explicit Operational Transition API Boundary

## Status

Accepted.

## Context

RFC-051 established `OperationalTransitionApplicationService` as the canonical application-level boundary for the explicit combined workload-and-operational-transition use case.

RFC-051 intentionally introduced no HTTP endpoint and reserved transport-specific request schemas for a future external-interface contract.

PlantMind therefore required a canonical HTTP transport boundary that could expose the approved application use case without moving workload orchestration, workload-evidence trust, mandatory-capability evaluation, or Runtime lifecycle authority into FastAPI.

## Decision

PlantMind SHALL expose the explicit operational-transition use case through:

`POST /operational-transition`

The endpoint SHALL delegate to the exact canonical:

`OperationalTransitionApplicationService`

composed by `CompositionRoot`.

A successful request SHALL return:

`204 No Content`

The response SHALL NOT expose internal workflow execution, workload evidence, transition evidence, mandatory-capability observations, or Runtime-internal evidence.

## Transport Observation Boundary

RFC-052 introduces transport-only observation request models.

Each accepted transport observation SHALL contain:

- `source`;
- `observation_type`;
- `value`;
- `observed_at`.

The API SHALL map each accepted transport observation into exactly one existing immutable domain `Observation`.

Client-supplied observation order SHALL be preserved.

The resulting domain observation tuple SHALL be supplied unchanged to:

`OperationalTransitionApplicationService.request_operational(...)`

exactly once.

Domain `Observation` remains authoritative for domain invariants and timestamp normalization.

The transport schema SHALL NOT replace or duplicate the domain model.

## Evidence Trust Boundary

The HTTP client SHALL NOT supply trusted internal workload or transition evidence.

The request schema SHALL reject extra fields, including client attempts to provide workload evidence or transition evidence.

The API SHALL NOT construct, reconstruct, validate, or infer:

- workload identifiers;
- workload-entry evidence;
- workflow-execution-start evidence;
- `OperationalWorkloadEvidence`;
- `OperationalTransitionEvidence`;
- mandatory-capability coverage evidence.

Trusted workload evidence continues to originate exclusively from the canonical workload execution path.

## Application Boundary

The API SHALL invoke:

`OperationalTransitionApplicationService.request_operational(...)`

exactly once per accepted request.

The API SHALL NOT directly coordinate:

- `ApplicationFacade`;
- `OperationalTransitionCoordinator`;
- `CapabilityAvailabilityObserver`;
- `MandatoryCapabilityCoverageEvaluator`;
- Runtime lifecycle transition operations.

The API SHALL NOT construct a second application-service instance or an alternate operational workload path.


## Runtime Authority Boundary

The API SHALL NOT call `Runtime.request_operational(...)` directly.

It SHALL NOT inspect Runtime readiness or lifecycle state to reproduce transition eligibility rules.

It SHALL NOT enable or disable request admission, mark Runtime operational, construct transition evidence, or establish independent lifecycle authority.

Runtime remains the sole authoritative lifecycle-transition owner.

## Request Admission Boundary

`POST /operational-transition` SHALL remain subject to the existing `RequestAdmissionMiddleware`.

The endpoint SHALL NOT be added to `DEFAULT_ADMISSION_EXEMPT_PATHS`.

When operational request admission is disabled, middleware SHALL reject the request before the application service executes.

RFC-052 does not modify Runtime-owned request-admission semantics.

## Validation and Failure Semantics

Transport deserialization and structural validation remain API responsibilities.

Domain `Observation` remains responsible for its existing domain invariants.

A domain observation-construction validation failure SHALL produce `422 Unprocessable Entity` without invoking the application service.

Application-service failures SHALL NOT be retried.

The API SHALL NOT repeat workload execution, independently request a Runtime transition, or fabricate a successful response.


## Bootstrap and Health Boundaries

Bootstrap SHALL NOT invoke the operational-transition application service automatically.

Health SHALL remain observational and SHALL NOT initiate an operational transition.

RFC-052 introduces no startup-triggered or health-triggered operational transition.

## PI and External Connectivity Boundary

RFC-052 introduces no PI Web API communication, PI authentication, certificate handling, connectivity probes, connector lifecycle changes, production capability-availability sources, or mandatory-capability deployment policy.

The accepted mock-before-production integration architecture remains unchanged.


## State and Persistence Boundary

The operational-transition API boundary SHALL remain stateless between requests.

It SHALL NOT persist observations, workflow executions, workload evidence, transition evidence, transition eligibility, Runtime lifecycle state, or retry state.

## Consequences

PlantMind now has a canonical external HTTP path:

`POST /operational-transition`
→ transport observation mapping
→ `OperationalTransitionApplicationService`
→ `ApplicationFacade`
→ trusted workload evidence
→ `OperationalTransitionCoordinator`
→ Runtime authority.

The transport layer remains limited to HTTP concerns and domain-object mapping.

Trusted evidence remains internal, Runtime remains the sole lifecycle-transition authority, and request admission remains Runtime-owned.


## Verification

- RFC-052 contract commit: `f9b0816`
- RFC-052 technical commit: `62bb854`
- Focused RFC-052 suite: 16 passed
- API regression: 25 passed
- Impacted API/services/core regression: 373 passed
- Full regression: 432 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

---

# AD-039 — Canonical Enterprise Knowledge Foundation Boundary

## Status

Accepted.

## Context

The post-RFC-052 Source-of-Truth architecture review established that PlantMind has a mature operational runtime and transition foundation but does not yet have a canonical enterprise knowledge foundation.

Existing knowledge-oriented components are either prototype, placeholder or intentionally unimplemented.

The accepted equipment domain already provides canonical equipment identity through `app.domain.equipment.Equipment` and the shared `DomainEntity[EntityId]` model.

The existing reasoning subsystem consumes `Observation` and does not define an accepted enterprise-knowledge input boundary.

`backend/app/database.py` provides concrete SQLAlchemy infrastructure but does not define a persistence-neutral enterprise knowledge repository.

PlantMind therefore requires a canonical knowledge-domain boundary before Document Library, Asset Library, Search Engine, Knowledge Graph, semantic retrieval, vector storage or RAG capabilities are introduced.

## Decision

PlantMind SHALL establish an immutable, traceable and persistence-neutral enterprise knowledge foundation centered on:

- `KnowledgeRecord`;
- `KnowledgeKind`;
- `KnowledgeProvenance`;
- `KnowledgeSourceType`;
- `KnowledgeSubject`;
- `KnowledgeSubjectType`;
- `KnowledgeRecordRepository`.

The canonical knowledge model SHALL remain independent of database, graph, vector, LLM, API and industrial-connectivity technologies.

## Canonical Knowledge Record

`KnowledgeRecord`

SHALL be the canonical domain representation of one addressable enterprise knowledge item.

It SHALL inherit canonical PlantMind identity through:

`DomainEntity[EntityId]`

A knowledge record SHALL contain:

- canonical `EntityId` identity;
- `kind: KnowledgeKind`;
- `title: str`;
- `content: str`;
- `provenance: KnowledgeProvenance`;
- `subject: KnowledgeSubject | None`.

A knowledge record SHALL remain immutable after construction.

It SHALL NOT become a database row model, graph node model, vector point, embedding, prompt, generated answer, operational observation or reasoning result.

## Knowledge Type Value Objects

`KnowledgeKind`, `KnowledgeSourceType` and `KnowledgeSubjectType`

SHALL be open immutable value objects rather than closed enums.

Each SHALL contain one string value.

Normalization SHALL:

- remove leading and trailing whitespace;
- normalize alphabetic characters to lowercase;
- preserve internal whitespace and characters.

The resulting value SHALL be non-empty.

PlantMind SHALL NOT establish a closed global vocabulary or type registry through RFC-053.

## Content Normalization

`KnowledgeRecord.title` and `KnowledgeRecord.content`

SHALL remove leading and trailing whitespace only.

Internal characters, whitespace and line breaks SHALL otherwise be preserved.

Both values SHALL remain non-empty after normalization.

## Domain Validation

Knowledge-domain invariants SHALL be enforced by the canonical domain types.

Validation failures SHALL raise the existing PlantMind:

`DomainException`

or an appropriate domain-specific subtype.

Domain validation SHALL NOT require repository, database, graph, vector, API or application-service access.

Repository conflicts SHALL remain separate from domain validation.

## Provenance Boundary

Each `KnowledgeRecord` SHALL contain exactly one immutable:

`KnowledgeProvenance`

containing:

- `source_type: KnowledgeSourceType`;
- `source_reference: str`;
- `captured_at: datetime`.

`source_reference` SHALL be non-empty after removing leading and trailing whitespace.

`captured_at` SHALL be timezone-aware and SHALL normalize to UTC while preserving the represented instant.

Provenance records origin.

Provenance SHALL NOT by itself establish correctness, authorization, operational trust, reasoning eligibility, safety approval or lifecycle readiness.

Cross-record corroboration, derivation and multi-source provenance relationships require a future explicit contract.

## Knowledge Subject Boundary

`KnowledgeSubject`

SHALL contain:

- `subject_type: KnowledgeSubjectType`;
- `subject_id: EntityId`.

It SHALL represent an optional typed primary contextual reference to an existing PlantMind domain entity.

It SHALL NOT embed the referenced entity.

It SHALL NOT be treated as an exhaustive knowledge relationship model.

Construction of a `KnowledgeSubject` SHALL NOT load, resolve or verify the referenced entity.

RFC-053 SHALL NOT establish referential-integrity verification between `subject_type` and `subject_id`.

Entity existence, accessibility and subject-type correspondence require a future explicit application or integration contract.

## Equipment Ownership Boundary

`app.domain.equipment.Equipment`

remains the canonical equipment entity.

`EquipmentSnapshot`

remains the immutable point-in-time equipment operational view.

Knowledge MAY reference canonical equipment identity through `KnowledgeSubject`.

The knowledge foundation SHALL NOT duplicate equipment state, criticality, alarms or lifecycle responsibility.

`app.models.equipment.Equipment` SHALL NOT become a second canonical equipment domain.

RFC-053 SHALL NOT create a third equipment model.

## Repository Port

PlantMind SHALL introduce a persistence-neutral:

`KnowledgeRecordRepository`

port with the minimum operations:

`add(record: KnowledgeRecord) -> None`

and:

`get(record_id: EntityId) -> KnowledgeRecord | None`

`add(...)` SHALL NOT silently overwrite a record with an existing canonical identity.

Duplicate canonical identity SHALL raise:

`KnowledgeRecordAlreadyExistsError`

`get(...)` SHALL return `None` when the canonical identity is absent.

Repository implementations SHALL NOT mutate supplied immutable records.

Repository reads MAY reconstruct immutable records.

Python object identity SHALL NOT be required across repository operations.

A successful add/get round trip SHALL preserve complete canonical domain-value equivalence.

## Repository Failure Boundary

`KnowledgeRecordAlreadyExistsError`

SHALL remain a repository-boundary conflict and SHALL NOT become an alternate domain-invariant authority.

Unexpected persistence failures SHALL NOT become synthetic success.

RFC-053 introduces no automatic repository retry and no platform-wide exception taxonomy.

## Dependency Direction

The canonical knowledge domain SHALL NOT depend on `KnowledgeRecordRepository`.

`KnowledgeRecordRepository` MAY depend on the canonical knowledge-domain types required by its contract.

Future application services MAY depend on the repository port.

Future infrastructure adapters MAY implement the repository port and depend on approved persistence technologies.

The canonical knowledge domain SHALL NOT depend on:

- SQLAlchemy;
- PostgreSQL;
- Neo4j;
- Qdrant;
- API transport;
- application orchestration;
- `CompositionRoot`;
- `ServiceContainer`.

## Persistence Technology Boundary

RFC-053 introduces no production persistence adapter.

`backend/app/database.py`

remains concrete SQLAlchemy infrastructure and SHALL NOT become the canonical enterprise knowledge repository contract.

A test-only in-memory repository MAY be used to verify repository semantics but SHALL NOT be composed, registered or represented as production infrastructure.

## Search, Graph, Vector and RAG Boundaries

Identity lookup through `KnowledgeRecordRepository.get(...)` is not the PlantMind Search Engine.

RFC-053 introduces no:

- keyword or full-text search;
- semantic or similarity search;
- ranking;
- Knowledge Graph persistence or traversal;
- embeddings;
- vector indexing;
- Qdrant integration;
- RAG behavior;
- LLM invocation.

Future search, graph, vector and RAG capabilities SHALL build on canonical knowledge identity rather than replace it.

## Reasoning Boundary

RFC-053 SHALL NOT modify:

- `ReasoningEngine`;
- `ReasoningPipeline`;
- reasoning builders;
- `Observation`;
- `ReasoningResult`;
- operational workload execution.

The accepted reasoning path remains observation-based.

Knowledge-to-reasoning integration requires a future explicit contract.

## PI and Operational Data Boundary

PI operational data and enterprise knowledge remain distinct architectural concepts.

RFC-053 SHALL NOT introduce PI production connectivity or automatic conversion between PI values, `Observation` and `KnowledgeRecord`.

Any such transformation requires a future accepted boundary.

Stored enterprise knowledge SHALL NOT automatically become trusted operational evidence.

## Application, Composition and API Boundaries

RFC-053 introduces no production knowledge application service.

RFC-053 introduces no production knowledge repository adapter.

RFC-053 SHALL NOT modify production `CompositionRoot`.

RFC-053 SHALL NOT register a production knowledge repository or application service in `ServiceContainer`.

RFC-053 introduces no HTTP endpoint and no transport schema.

Future application, composition and API contracts SHALL consume the canonical knowledge foundation rather than bypass it.

## Prototype and Legacy Containment

Existing prototype, placeholder and empty knowledge-oriented components SHALL NOT be treated as canonical production infrastructure merely because they exist.

RFC-053 does not authorize broad migration, deletion or production promotion of:

- `app.models.equipment.Equipment`;
- `EquipmentService`;
- `KnowledgeGraphService`;
- `KnowledgeGraphEngine`;
- existing empty parser, graph, RAG, semantic-search, knowledge-memory, vector-memory or knowledge-agent modules.

Preserve-before-delete remains authoritative.

## Lifecycle Boundary

The knowledge foundation SHALL NOT modify Runtime state, readiness, request admission, mandatory-capability policy, availability, transition evidence, Bootstrap or Health behavior.

The existence of canonical knowledge-domain contracts SHALL NOT automatically make knowledge a mandatory operational capability.

Runtime remains the sole lifecycle-transition authority.

## Consequences

PlantMind gains one canonical, immutable and traceable enterprise knowledge foundation before higher-level knowledge capabilities are introduced.

Knowledge identity is separated from persistence identifiers.

Knowledge provenance is separated from operational trust.

Knowledge subjects reference existing canonical domain identity without duplicating domain ownership.

Repository semantics are defined independently of persistence technology.

Search, Knowledge Graph, vector retrieval, RAG, application orchestration and external APIs can now evolve as explicit future boundaries without redefining what canonical enterprise knowledge is.

## Verification

- RFC-053 Contract Acceptance Review: passed
- Contract commit: `37112a2`
- Architecture decision: AD-039
- Technical implementation: complete
- Technical commit: `ee18bc8`
- Focused RFC-053 verification: 44 passed
- Full regression: 476 passed
- Compilation: passed
- `git diff --check`: passed
- Remote technical push: verified

---

# AD-040 — Canonical Database Runtime & Schema Lifecycle Foundation

## Status

Accepted.

## Context

RFC-053 established the canonical enterprise knowledge domain and the persistence-neutral `KnowledgeRecordRepository` port.

The required post-RFC-053 Source-of-Truth architecture review established that production Knowledge persistence cannot safely be introduced yet.

The review found that:

- `backend/app/database.py` is preliminary isolated SQLAlchemy infrastructure;
- `app.database` has no current production consumer;
- the authoritative root `.venv` does not currently provide SQLAlchemy;
- backend dependency declarations do not currently establish SQLAlchemy, a PostgreSQL driver or Alembic;
- no canonical ORM schema or metadata ownership boundary exists;
- no database migration lifecycle exists;
- no database-focused test foundation exists;
- `ConfigurationProvider.validate()` participates in Bootstrap startup, but database readiness is not currently a mandatory platform capability.

PlantMind therefore requires an explicit database runtime and schema-lifecycle foundation before any production repository adapter or persistent enterprise knowledge model is introduced.

## Decision

PlantMind SHALL establish one canonical database infrastructure boundary responsible for:

- database dependency ownership;
- explicit database runtime construction;
- SQLAlchemy engine ownership;
- SQLAlchemy session-factory ownership;
- canonical relational schema metadata ownership;
- Alembic migration ownership;
- deterministic database-resource disposal;
- explicit database-specific failure behavior.

This foundation SHALL remain infrastructure.

It SHALL NOT become domain knowledge, application orchestration, Runtime lifecycle authority or a repository implementation.

## Technology Boundary

PostgreSQL remains the approved relational database target for the PlantMind enterprise platform.

SQLAlchemy SHALL be the canonical Python relational database runtime and mapping toolkit.

RFC-054 SHALL use the synchronous SQLAlchemy `Engine` and `Session` model.

RFC-054 SHALL NOT introduce SQLAlchemy `AsyncEngine` or `AsyncSession`.

Any future asynchronous relational-persistence runtime requires a separate accepted architecture contract.

Psycopg 3, distributed through the `psycopg` package, SHALL be the canonical PostgreSQL DBAPI driver.

PostgreSQL SQLAlchemy URLs used by the canonical runtime SHALL identify the approved Psycopg driver explicitly rather than relying on environment-dependent driver selection.

Alembic SHALL be the sole canonical relational schema-migration authority.

The canonical PostgreSQL DBAPI driver SHALL be explicitly declared as a backend dependency.

Database technologies SHALL NOT leak into PlantMind domain contracts.

## Dependency Ownership

All dependencies required by the canonical database foundation SHALL be explicitly declared in the maintained backend dependency manifest.

The implementation SHALL NOT depend on packages that happen to exist only in a developer environment.

The authoritative PlantMind Python environment remains the root:

`.venv`

RFC-054 SHALL NOT establish or depend upon `backend/.venv`.

The database foundation SHALL explicitly declare the dependencies required for:

- SQLAlchemy;
- Alembic;
- PostgreSQL connectivity.

Exact dependency versions SHALL be maintained through the existing backend dependency-management mechanism.

## Canonical Database Runtime

PlantMind SHALL introduce one canonical infrastructure-owned database runtime.

The canonical database runtime SHALL own:

- one SQLAlchemy `Engine` per canonical database-runtime instance;
- the session factory bound to that engine;
- deterministic disposal of engine-owned resources.

The database runtime SHALL be constructed explicitly.

Importing a PlantMind module SHALL NOT create the canonical database engine.

Importing a PlantMind module SHALL NOT open a database connection.

A process-wide hidden database session SHALL NOT be introduced.

A mutable global SQLAlchemy `Session` SHALL NOT be introduced.

Database sessions SHALL be created explicitly from the canonical session factory and SHALL possess deterministic close behavior.

The database runtime SHALL NOT perform engineering reasoning or own enterprise knowledge.

## Configuration Boundary

The canonical database runtime SHALL receive resolved database configuration explicitly.

The infrastructure implementation SHALL NOT read the global `settings` object as a hidden dependency during module import.

Database configuration SHALL remain environment-driven.

Database credentials SHALL NOT be embedded as production secrets in source code.

RFC-054 implementation SHALL retire the committed credential-bearing default value currently associated with `DATABASE_URL`.

The absence of configured database capability MAY be represented by an unset or optional database URL while no accepted production capability requires relational persistence.

Development or test database credentials SHALL be supplied through explicit local environment configuration or test fixtures rather than committed production configuration defaults.

Database credentials SHALL NOT be written to logs or exposed through exception formatting controlled by PlantMind.

RFC-054 SHALL NOT make `DATABASE_URL` a mandatory condition of the existing general `ConfigurationProvider.validate()` contract.

Database-specific configuration SHALL be validated when the database capability is explicitly constructed or invoked.

The absence of database configuration SHALL NOT by itself prevent PlantMind core Bootstrap from operating while no accepted production capability requires the database.

## Engine Boundary

SQLAlchemy engine creation SHALL occur only through the canonical database runtime or its approved construction boundary.

No second module SHALL independently own another canonical engine for the same PlantMind relational persistence responsibility.

Engine construction SHALL NOT itself be treated as proof of database availability.

RFC-054 introduces no production connectivity probe.

RFC-054 introduces no automatic connection retry.

Database connection failures SHALL NOT become synthetic success.

Engine resources SHALL support explicit deterministic disposal.

## Session Boundary

The canonical database runtime SHALL provide one approved session-factory boundary.

Each requested session SHALL be an independent SQLAlchemy session instance.

Sessions SHALL NOT be shared as mutable global state.

Session lifecycle SHALL support deterministic close behavior.

Session creation SHALL NOT imply application or repository transaction ownership.

The canonical database runtime SHALL NOT automatically commit application or repository work.

RFC-054 SHALL NOT define repository-specific transaction semantics or introduce a Unit of Work abstraction.

Future repository and application contracts SHALL define transaction ownership appropriate to their use cases rather than embedding application or domain transaction semantics into the database runtime.

## Canonical Schema Metadata

PlantMind SHALL establish one canonical relational schema metadata authority.

All future production SQLAlchemy persistence models SHALL participate in that approved metadata authority unless a future accepted architecture decision explicitly establishes another database boundary.

PlantMind domain entities SHALL NOT inherit from the SQLAlchemy declarative base.

SQLAlchemy mapped models SHALL remain infrastructure representations.

A database row SHALL NOT replace a canonical PlantMind domain entity.

RFC-054 SHALL NOT introduce a `KnowledgeRecord` ORM model.

## Migration Authority

Alembic SHALL be the sole canonical mechanism for production relational schema evolution.

PlantMind application startup SHALL NOT automatically run schema migrations.

Runtime Bootstrap SHALL NOT automatically upgrade or downgrade the database schema.

`MetaData.create_all()` SHALL NOT become the production schema deployment mechanism.

Production schema changes SHALL be expressed through explicit ordered Alembic revisions.

Applied migration history SHALL be treated as append-only engineering history.

An existing accepted migration revision SHALL NOT be silently rewritten to represent a different schema state.

Breaking or destructive schema evolution requires an explicit future architecture decision and migration review.

The migration graph SHALL maintain one canonical head unless an explicit future architecture decision authorizes branching.

## Migration Configuration

Migration configuration SHALL reference the canonical PlantMind schema metadata authority.

Migration configuration SHALL NOT contain production database credentials.

The database URL required for migration execution SHALL be supplied through an approved environment-driven configuration boundary.

RFC-054 MAY establish an intentionally schema-neutral initial migration revision to create the canonical revision lineage before application persistence tables exist.

RFC-054 SHALL NOT create enterprise knowledge tables.

## Failure Boundary

Invalid database-specific configuration SHALL fail explicitly when the database capability is constructed or invoked.

Missing database dependencies SHALL remain an environment or build defect and SHALL NOT be converted into synthetic database availability.

Unexpected engine, session or migration failures SHALL propagate as explicit infrastructure failures.

RFC-054 introduces no automatic database retry policy.

RFC-054 introduces no platform-wide database exception taxonomy.

Database failures SHALL NOT independently modify PlantMind Runtime lifecycle state.

Any future coupling between database availability and mandatory-capability readiness requires a separate accepted architecture contract.

## Bootstrap and Runtime Boundary

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

## Composition Boundary

RFC-054 establishes infrastructure that future persistence adapters may consume.

RFC-054 SHALL NOT introduce a production Knowledge repository adapter.

RFC-054 SHALL NOT register `KnowledgeRecordRepository` in `ServiceContainer`.

RFC-054 SHALL NOT wire production Knowledge persistence into `CompositionRoot`.

RFC-054 SHALL NOT create a database-backed application service.

A future accepted persistence contract SHALL decide how the canonical database runtime is composed with production repository adapters.

## Legacy Database Module

`backend/app/database.py`

is preliminary isolated infrastructure and SHALL NOT remain a competing owner of canonical engine or session-factory construction after RFC-054 implementation.

Preserve-before-delete remains authoritative.

Before changing or removing that module, implementation SHALL re-verify repository dependencies and compatibility impact.

If no dependency requires the legacy module, its duplicate database-runtime responsibility SHALL be retired.

If a compatibility dependency is discovered, RFC-054 SHALL NOT preserve duplicate engine ownership merely to retain the old implementation.

Any required compatibility path SHALL delegate to the canonical database foundation or be separately documented before implementation proceeds.

## Security Boundary

RFC-054 SHALL preserve the on-premise enterprise deployment model.

RFC-054 SHALL NOT introduce external database services.

Database secrets SHALL remain outside committed source code.

PlantMind-controlled diagnostics SHALL NOT expose database passwords or complete credential-bearing connection URLs.

Authentication, certificate policy, network segmentation and production PostgreSQL hardening remain deployment and Cybersecurity concerns and SHALL NOT be falsely represented as completed merely by introducing the database runtime foundation.

## Knowledge Boundary

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

RFC-054 SHALL NOT create relational persistence tables for canonical enterprise knowledge.

The first production Knowledge persistence adapter requires a future explicit accepted architecture contract.

## Prototype and Advanced Capability Boundary

RFC-054 SHALL NOT promote existing prototype or placeholder knowledge components into production.

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

## Non-Goals

RFC-054 SHALL NOT:

- implement production Knowledge persistence;
- introduce a Knowledge ORM model;
- add a knowledge HTTP API;
- implement document ingestion;
- implement search;
- implement graph persistence;
- implement vector persistence;
- implement RAG;
- modify the reasoning subsystem;
- redesign the equipment domain;
- add automatic database retry;
- add automatic schema migration during application startup;
- make PostgreSQL availability a mandatory Runtime capability;
- perform a broad application-configuration refactor;
- introduce another lifecycle authority.

## TDD Boundary

Before production implementation, focused tests SHALL establish:

- database infrastructure dependencies are explicitly declared;
- the authoritative root `.venv` can import the approved database dependencies after installation;
- canonical database infrastructure can be imported without creating a database connection;
- importing PlantMind core modules does not construct the canonical database engine as a hidden side effect;
- database runtime construction is explicit;
- the database runtime owns its engine and session factory;
- independent session requests return independent session instances;
- sessions support deterministic close behavior;
- database runtime disposal releases engine-owned resources;
- canonical relational metadata has one approved ownership boundary;
- PlantMind domain modules do not depend on SQLAlchemy;
- PlantMind domain entities do not inherit SQLAlchemy mapped classes;
- Alembic configuration uses the canonical metadata authority;
- Alembic configuration contains no committed production credential;
- the migration graph has one canonical head;
- an initial migration lineage can be resolved deterministically;
- application startup does not automatically execute Alembic migrations;
- application startup does not automatically call `MetaData.create_all()`;
- Bootstrap behavior remains unchanged;
- Runtime lifecycle behavior remains unchanged;
- no production Knowledge repository is introduced;
- no production Knowledge persistence is composed or registered;
- `backend/app/database.py` no longer owns a competing canonical engine or session factory after the accepted migration path is applied.

## Verification Boundary

RFC-054 implementation SHALL pass:

- focused database-foundation tests;
- relevant configuration and Bootstrap regression tests;
- architecture dependency tests;
- full PlantMind regression;
- Python compilation checks;
- `git diff --check`;
- Git review;
- remote push verification;
- clean working-tree verification.

A real production PostgreSQL connection is not required merely to accept the RFC-054 architecture contract.

RFC-054 SHALL NOT claim production database connectivity until separately verified against an approved deployment environment.

## Consequences

PlantMind gains one explicit relational database infrastructure foundation before production persistence adapters are introduced.

Database dependency ownership becomes reproducible.

Engine and session ownership become explicit instead of import-time global infrastructure.

Relational schema metadata receives one canonical owner.

Schema evolution becomes versioned and auditable through Alembic.

Application startup remains independent from automatic database migration.

The canonical knowledge domain remains persistence-neutral.

Future Knowledge persistence can depend on this foundation without redefining database lifecycle responsibility.

## Contract Acceptance

RFC-054 Contract Acceptance Review: passed.

Architecture decision: AD-040.

The Canonical Database Runtime & Schema Lifecycle Foundation contract is accepted.

Contract commit: `8659acd`.

Remote contract push: verified.

Local and remote contract commit identity: verified.

Working tree after contract push: clean.

Technical implementation is complete within the accepted AD-040 architecture boundary.

Technical commit: `0e483d5`.

Focused RFC-054 verification: 32 passed.

Full PlantMind regression: 506 passed.

Python compilation: passed.

`git diff --check`: passed.

Alembic canonical migration head: `0001`.

Remote technical push: verified.

Local and remote technical commit identity: verified.

Working tree after technical push: clean.

Production Knowledge persistence remains outside RFC-054 scope.

Production PostgreSQL connectivity and deployment Cybersecurity approval remain intentionally unclaimed.

## Technical Implementation Verification

The completed RFC-054 implementation preserves the accepted AD-040 responsibility boundaries.

The implementation establishes canonical database runtime ownership, schema metadata ownership and Alembic migration lifecycle without introducing production Knowledge persistence, application-startup migration, database readiness as a mandatory Runtime capability, CompositionRoot database composition or additional lifecycle authority.

The legacy `backend/app/database.py` duplicate engine and session-factory responsibility was retired after dependency review confirmed no production consumer required it.

The schema-neutral initial Alembic revision `0001` establishes the canonical migration lineage without introducing application or enterprise Knowledge tables.

## Post-RFC-054 Source-of-Truth Architecture Review

The required post-RFC-054 Source-of-Truth architecture review is complete.

The review confirmed that AD-039 / RFC-053 and AD-040 / RFC-054 remain authoritative and SHALL NOT be redesigned by the next workstream.

The review established that:

- no production relational implementation of `KnowledgeRecordRepository` currently exists;
- no production Knowledge relational mapping or relational table currently exists;
- no production Unit of Work abstraction currently exists;
- `DatabaseRuntime` owns engine and session-factory lifecycle but does not own repository transaction semantics;
- Alembic revision `0001` remains intentionally schema-neutral and SHALL NOT be rewritten;
- future Knowledge schema evolution requires a new append-only migration revision;
- default `CompositionRoot` does not register or expose Knowledge persistence;
- application startup remains independent from database configuration.

The selected engineering direction is:

`Canonical Knowledge Relational Persistence Adapter Boundary`

This is an engineering direction only.

It is not yet an accepted architecture contract and implementation is not authorized.

## Next Exact Action

Draft and review the architecture contract for the Canonical Knowledge Relational Persistence Adapter Boundary before any implementation.

Do not assign production composition responsibility or begin persistence implementation before contract acceptance.

# AD-041 — Canonical Knowledge Relational Persistence Adapter Boundary

## Status

Accepted.

## Context

AD-039 / RFC-053 established the canonical persistence-neutral enterprise Knowledge domain and the `KnowledgeRecordRepository` port.

AD-040 / RFC-054 established the canonical synchronous relational database runtime, SQLAlchemy engine and session-factory ownership, `DatabaseBase.metadata` authority, PostgreSQL Psycopg boundary and Alembic schema lifecycle.

The required post-RFC-054 Source-of-Truth architecture review confirmed that:

- no production relational implementation of `KnowledgeRecordRepository` exists;
- no canonical relational representation of `KnowledgeRecord` exists;
- Alembic revision `0001` remains intentionally schema-neutral;
- `DatabaseRuntime` owns engine and session-factory lifecycle but not repository transaction semantics;
- default `CompositionRoot` does not register or expose Knowledge persistence;
- application startup remains independent from database availability.

PlantMind therefore requires one explicit persistence-adapter boundary before canonical Knowledge can be stored relationally.

## Decision

PlantMind SHALL introduce one canonical infrastructure-owned relational implementation of:

`KnowledgeRecordRepository`

The implementation SHALL reside under:

`app.infrastructure.knowledge`

The canonical domain and persistence-neutral repository contract SHALL remain unchanged.

The adapter SHALL implement only the existing repository operations:

- `add(record: KnowledgeRecord) -> None`;
- `get(record_id: EntityId) -> KnowledgeRecord | None`.

RFC-055 SHALL NOT introduce update, delete, upsert, merge-based overwrite or a Unit of Work abstraction.

## Relational Representation

The canonical relational table SHALL be:

`knowledge_records`

The SQLAlchemy mapped representation SHALL remain distinct from `KnowledgeRecord`.

The relational database SHALL NOT generate or replace canonical Knowledge record identity or canonical provenance capture time.

The relational representation SHALL preserve:

- canonical UUID identity;
- Knowledge kind;
- title;
- content;
- provenance source type;
- provenance source reference;
- timezone-aware provenance timestamp;
- optional Knowledge subject type;
- optional Knowledge subject UUID identity.

The canonical primary-key constraint SHALL be:

`pk_knowledge_records`

The subject-pair constraint SHALL be:

`ck_knowledge_records_subject_pair`

Subject type and subject identity SHALL either both be absent or both be present.

No relational foreign key SHALL incorrectly constrain the polymorphic Knowledge subject reference to one specific aggregate.

## Domain and Infrastructure Boundary

`app.domain` and `app.knowledge` SHALL remain SQLAlchemy-free.

`app.knowledge` SHALL remain the persistence-neutral Knowledge contract boundary.

`app.infrastructure.database` SHALL remain the generic relational runtime, metadata and schema-lifecycle foundation.

The generic database package SHALL NOT become the owner of Knowledge repository semantics.

The Knowledge relational adapter MAY depend upon canonical Knowledge contracts, the repository port, canonical database metadata and session-factory boundaries, and SQLAlchemy.

The generic database infrastructure SHALL NOT acquire a reverse dependency upon the Knowledge adapter.

## Session and Transaction Ownership

The relational Knowledge adapter SHALL receive the canonical session-factory boundary explicitly.

It SHALL NOT construct an independent engine, competing session factory, hidden database configuration dependency or process-global mutable Session.

Each repository operation SHALL use an independent deterministic session lifetime.

`DatabaseRuntime` remains the owner of engine and session-factory lifecycle.

The Knowledge adapter SHALL own repository-operation transaction semantics only.

A successful `add()` SHALL complete one atomic transaction.

A failed `add()` SHALL roll back without partially persisting the record.

`get()` SHALL remain read-only and SHALL NOT perform an application-data commit.

RFC-055 SHALL NOT introduce cross-repository transaction coordination.

Any future multi-repository or application-workflow transaction boundary requires a separate accepted architecture decision.

## Duplicate Identity Boundary

The relational primary-key constraint SHALL remain the concurrency-safe authority for canonical Knowledge identity.

The adapter SHALL NOT use a pre-insert existence query as authoritative duplicate prevention.

Only a failure positively identified through structured database or driver diagnostics as a violation of the canonical Knowledge identity constraint SHALL be translated to:

`KnowledgeRecordAlreadyExistsError`

Human-readable database error-message parsing SHALL NOT be used to classify canonical duplicate identity.

Unrelated integrity, mapping, connection, driver and transaction failures SHALL preserve their infrastructure failure semantics.

A duplicate attempt SHALL NOT overwrite or modify the original canonical record.

## Schema and Migration Boundary

Alembic remains the sole canonical production relational schema-evolution authority.

RFC-055 SHALL introduce one linear append-only migration successor to `0001`:

`0002`

Revision `0001` SHALL NOT be modified, rewritten or repurposed.

Migration `0002` SHALL establish the canonical `knowledge_records` schema.

The mapped relational representation SHALL register with `DatabaseBase.metadata`.

Alembic metadata discovery SHALL load canonical mapped-table registration without creating an engine, Session, database connection or hidden configuration dependency.

The mapped schema and migration `0002` SHALL remain aligned.

The migration graph SHALL retain exactly one canonical head.

Application startup SHALL NOT automatically execute migrations.

`MetaData.create_all()` SHALL NOT become the production schema-deployment mechanism.

Migration `0002` MAY define reversal of schema introduced by `0002`, but destructive downgrade against a data-bearing environment requires separate explicit migration and deployment review.

Runtime and Bootstrap SHALL NOT automatically execute schema downgrade.

## Composition and Runtime Boundary

RFC-055 SHALL NOT automatically:

- construct `DatabaseRuntime` from default `CompositionRoot.build()`;
- register `KnowledgeRecordRepository` in the default `ServiceContainer`;
- expose Knowledge persistence from default `PlatformComposition`;
- require `DATABASE_URL` during default application startup;
- make PostgreSQL a mandatory Runtime capability.

Existing zero-argument `CompositionRoot.build()` behavior SHALL remain compatible.

RFC-055 SHALL NOT modify Runtime lifecycle states, readiness semantics, request admission, operational-transition evidence, mandatory-capability policy, Bootstrap startup or Bootstrap shutdown responsibilities.

A repository operation failure SHALL NOT independently become Runtime transition authority.

Production Knowledge persistence composition remains deferred until an accepted application capability explicitly requires it.

## Application Boundary

RFC-055 establishes persistence infrastructure only.

It SHALL NOT introduce:

- a production Knowledge application service;
- a Knowledge HTTP API;
- semantic search;
- vector persistence;
- Qdrant integration;
- Knowledge Graph persistence;
- Neo4j integration;
- RAG;
- LLM invocation;
- production PI connectivity.

Application, orchestration, reasoning and operational-transition responsibilities remain unchanged.

## Security and Deployment Readiness

RFC-055 preserves the accepted on-premise enterprise deployment model.

Database credentials SHALL remain outside committed source code.

Code-level implementation acceptance SHALL NOT mean production-deployment readiness.

A live production PostgreSQL environment is not required merely to accept the RFC-055 architecture contract or complete code-level implementation verification.

Before relational Knowledge persistence is declared production-deployment ready, a separate approved PostgreSQL integration verification SHALL demonstrate migration, schema alignment, repository behavior, UUID and timestamp semantics, structured duplicate classification, rollback behavior and deterministic session ownership.

Successful RFC-055 unit, architecture, migration-definition and regression testing SHALL NOT be represented as evidence of production PostgreSQL connectivity, deployment configuration or Cybersecurity approval.

Production deployment readiness remains subject to separately verified integration, deployment and Cybersecurity gates.

## Consequences

PlantMind gains its first canonical relational persistence boundary for enterprise Knowledge without making persistence a domain responsibility.

Canonical Knowledge remains immutable and persistence-neutral.

Database engine and session-factory ownership remain centralized under AD-040.

Repository transaction semantics become explicit without prematurely introducing a Unit of Work.

Schema evolution remains ordered, auditable and append-only.

Default application startup remains independent from relational Knowledge persistence and PostgreSQL availability.

Production composition remains deferred until an application capability explicitly requires it.

Existing RFC-053 and RFC-054 architecture guardrails SHALL evolve narrowly where RFC-055 intentionally introduces accepted infrastructure, but SHALL NOT be deleted or weakened merely to make implementation tests pass.

## Contract Acceptance

RFC-055 Contract Acceptance Review: passed.

Architecture decision: AD-041.

The Canonical Knowledge Relational Persistence Adapter Boundary contract is accepted.

Technical implementation is complete within the accepted AD-041 architecture boundary.

RFC-055 technical verification:

- Contract commit: `ea046bd`
- Technical commit: `9fc34c7`
- Focused verification: 137 passed
- Full regression: 543 passed
- Python compilation: passed
- `git diff --check`: passed
- Alembic canonical head: `0002`
- Remote technical push: verified
- Local and remote technical commit identity: verified
- Working tree after technical push: clean

The next required architecture action is the post-RFC-055 Source-of-Truth review before selection or authorization of another architecture workstream.

Production PostgreSQL connectivity, production schema deployment and Cybersecurity approval remain intentionally unclaimed.

# AD-042 — Canonical Knowledge Capture Application Boundary

## Status

Accepted.

## Context

AD-039 / RFC-053 established the canonical immutable enterprise Knowledge domain and persistence-neutral `KnowledgeRecordRepository`.

AD-040 / RFC-054 established the canonical relational database runtime and schema-lifecycle foundation.

AD-041 / RFC-055 established the canonical relational implementation of `KnowledgeRecordRepository` without introducing a production Knowledge application service or default relational Knowledge composition.

The post-RFC-055 Source-of-Truth review initially identified an application-level Knowledge boundary as the next architecture area.

A deeper evidence-based review determined that a generic application service exposing repository-equivalent `add()` and `get()` behavior would introduce an unnecessary delegation layer without owning an independent application responsibility.

PlantMind nevertheless requires an explicit application use case for its chartered company-Knowledge capture objective.

## Decision

PlantMind SHALL introduce one specialized application boundary:

`KnowledgeCaptureApplicationService`

under:

`app.services.knowledge_capture_application_service`

The same module SHALL contain the immutable application input contracts:

- `KnowledgeCaptureRequest`;
- `KnowledgeCaptureSubject`.

The canonical operation SHALL be:

`capture(request: KnowledgeCaptureRequest) -> KnowledgeRecord`

The Capture application boundary SHALL convert approved capture inputs into one canonical immutable `KnowledgeRecord`, persist that record through `KnowledgeRecordRepository.add(...)`, and return the exact captured canonical record only after persistence succeeds.

## Application and Domain Ownership

Canonical Knowledge invariants, normalization and validation remain owned by `app.domain.knowledge`.

The Capture boundary SHALL construct accepted canonical Knowledge domain types and SHALL NOT duplicate domain validation rules.

The Capture boundary SHALL own application-level creation of:

- canonical record `EntityId`;
- canonical provenance `captured_at`.

The default identity source SHALL remain `EntityId.new()`.

The default capture-time source SHALL produce the current timezone-aware UTC time when required by the Capture operation.

Narrow deterministic identity and time callables MAY be injected per service instance for testing.

RFC-056 SHALL NOT create a platform-wide Clock framework, identity service, provider registry or new dependency-injection framework.

## Subject Boundary

Caller-supplied subject input SHALL use `KnowledgeCaptureSubject` containing:

- `subject_type: str`;
- `subject_id: EntityId`.

The Capture boundary SHALL construct the canonical `KnowledgeSubjectType` and `KnowledgeSubject`.

RFC-056 SHALL NOT verify subject existence, accessibility or subject-type correspondence and SHALL NOT introduce an Asset Library or canonical subject resolver.

## Repository and Persistence Boundary

`KnowledgeCaptureApplicationService` SHALL receive the persistence-neutral `KnowledgeRecordRepository` explicitly.

For a Capture invocation that reaches persistence, `KnowledgeRecordRepository.add(...)` SHALL be invoked exactly once.

The Capture boundary SHALL NOT perform repository `get(...)` merely to confirm the write or prevent duplicates.

Repository Session lifetime and transaction semantics remain owned by AD-041 / RFC-055 infrastructure.

The Capture boundary SHALL NOT construct or own:

- SQLAlchemy Session;
- database engine;
- `DatabaseRuntime`;
- database configuration;
- schema migration;
- commit or rollback behavior.

`KnowledgeRecordAlreadyExistsError` remains the repository-boundary duplicate conflict and SHALL propagate without automatic identity regeneration, overwrite or retry.

Unexpected repository failures SHALL propagate and SHALL NOT become synthetic success.

## Composition and Runtime Boundary

AD-042 / RFC-056 SHALL NOT automatically register or expose Knowledge Capture or relational Knowledge persistence through default `CompositionRoot`, `ServiceContainer` or `PlatformComposition`.

Default application startup SHALL remain independent from `DATABASE_URL` and PostgreSQL availability.

Knowledge Capture SHALL NOT become a mandatory Runtime capability merely because the application boundary exists.

Runtime lifecycle, Bootstrap, Health, request-admission and operational-transition responsibilities remain unchanged.

Production Knowledge Capture composition requires a separate accepted architecture boundary.

## ApplicationFacade Boundary

`ApplicationFacade` remains the stable application entry boundary for the existing analysis/orchestration workload.

Knowledge Capture SHALL remain a distinct specialized application use case.

AD-042 SHALL NOT route Capture through the reasoning workflow or modify `ApplicationFacade`.

## Deferred Capability Boundary

AD-042 / RFC-056 SHALL NOT introduce:

- Knowledge HTTP or other external transport exposure;
- Document Library or document ingestion;
- file upload, parsing, OCR or chunking;
- update, delete or upsert Knowledge operations;
- keyword, full-text, semantic or similarity search;
- embeddings or vector persistence;
- Knowledge Graph persistence or traversal;
- RAG;
- LLM invocation;
- production PI, DCS or OPC UA connectivity.

Future transport and ingestion boundaries SHALL consume the accepted Capture application boundary rather than bypass it and call the repository directly.

## Security and Trust Boundary

Knowledge provenance records origin information but does not establish correctness, authentication, authorization, trust, safety or compliance approval.

Because AD-042 / RFC-056 does not establish authentication, capture authorization or actor-audit semantics, it SHALL NOT authorize external or production transport exposure of Knowledge Capture.

Code-level contract or implementation acceptance SHALL NOT be represented as Cybersecurity approval or production deployment readiness.

## Consequences

PlantMind gains its first explicit Knowledge application use case without adding a generic repository-delegation service.

Knowledge Capture receives a stable application boundary that future API and ingestion capabilities can consume.

Canonical Knowledge domain ownership remains unchanged.

Repository and database lifecycle ownership remain unchanged.

Default platform composition remains independent from relational Knowledge persistence.

Identity and capture-time generation become deterministic and testable without introducing platform-wide provider infrastructure.

Future Capture authorization, subject verification, ingestion, retrieval and reasoning capabilities remain explicit separately governed architecture work.

## Contract Acceptance

RFC-056 Contract Acceptance Review: passed.

Architecture decision: AD-042.

The Canonical Knowledge Capture Application Boundary contract is accepted.

Technical implementation is complete within the accepted AD-042 / RFC-056 architecture boundary.

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

The implementation preserves canonical Knowledge domain ownership, repository transaction ownership, default composition independence and Runtime/Bootstrap boundaries defined by AD-039 through AD-041.

Production Knowledge Capture composition, production transport exposure, authentication and authorization, actor-audit semantics, PostgreSQL deployment verification and Cybersecurity approval remain intentionally unclaimed.

## Post-RFC-056 Source-of-Truth Architecture Review Outcome

The required post-RFC-056 Source-of-Truth architecture review is complete.

The review confirmed that the canonical Knowledge foundation, database runtime, relational repository adapter and Capture application boundary established by AD-039 through AD-042 remain authoritative.

Current document ingestion, semantic-search, vector, graph, RAG and Knowledge-memory seams are not production implementations.

The existing `KnowledgeGraphService` remains an in-memory prototype and SHALL NOT become the next production architecture by promotion.

The current `SecurityManager` is not an accepted enterprise authentication or authorization boundary and SHALL NOT be represented as RBAC, Active Directory, LDAP, MFA, principal identity or actor-audit readiness.

Accordingly, external or production Knowledge ingestion remains unauthorized until separately governed security, composition, transport and deployment boundaries are accepted and verified.

The evidence-based next architecture direction is:

`RFC-057 — Canonical Document Knowledge Ingestion Application Boundary`

A future RFC-057 contract SHALL consume `KnowledgeCaptureApplicationService` rather than bypass the accepted Capture application boundary and writing directly through `KnowledgeRecordRepository`.

RFC-057 is a selected architecture direction only.

Its contract is not yet accepted.

AD-043 has not been created.

Implementation is not authorized.

The next required action is to draft and review the RFC-057 architecture contract before any technical implementation.

---

## RFC-057 Direction Refinement

The post-RFC-056 architecture review initially selected a Canonical Document Knowledge Ingestion Application Boundary as the next workstream.

Before contract acceptance, deeper repository review established that PlantMind does not yet contain a canonical enterprise Document identity or Document domain contract.

`app.domain.procedure` is empty.

Existing `app.models.procedure` and `ProcedureService` are prototype-level components and are not canonical enterprise Document architecture.

No canonical `DocumentId`, Document reference contract, Document revision model or Document repository exists.

Introducing Document Knowledge ingestion before the Document foundation would either force application-layer ownership of document identity/lifecycle semantics or produce a thin translation wrapper over the accepted Knowledge Capture application boundary.

The direction is therefore refined before acceptance to:

`RFC-057 — Canonical Enterprise Document Foundation Boundary`

This refinement does not invalidate the future need for Document Knowledge ingestion.

It establishes the prerequisite canonical Document foundation first.

---

# AD-043 — Canonical Enterprise Document Foundation Boundary

## Status

Accepted.

## Context

PlantMind must support enterprise knowledge sources including engineering drawings, operating procedures, vendor manuals, incident/RCA reports and other controlled documents.

AD-009 establishes that PI System is only one source among many and that higher layers should remain source-neutral.

AD-039 / RFC-053 deliberately established the canonical Knowledge foundation before Document Library, document ingestion, Search, Knowledge Graph, vector and RAG capabilities.

RFC-053 explicitly deferred document versioning, document storage, parsing, OCR, chunking and document-to-Knowledge transformation.

Repository review after RFC-056 confirmed that PlantMind still lacks a canonical enterprise Document identity and Document domain contract.

A document-ingestion application boundary should therefore not invent those semantics.

PlantMind requires a minimal canonical Document foundation first.

## Decision

PlantMind SHALL introduce:

`app.domain.document`

containing:

- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`.

`EnterpriseDocument` SHALL use shared PlantMind `EntityId`.

No document-specific identity primitive SHALL be created.

## Enterprise Document Contract

`EnterpriseDocument` SHALL be an immutable canonical domain entity containing:

- `id: EntityId`;
- `document_type: DocumentType`;
- `title: str`;
- `source: DocumentSource`.

The entity SHALL represent one immutable canonical enterprise Document record inside PlantMind.

It SHALL NOT represent a binary file, parsed content, revision object, Knowledge record or search result.

## Document Classification

`DocumentType` SHALL be an immutable open classification.

It SHALL require a string, trim surrounding whitespace, normalize the classification value to lowercase and reject an empty normalized value.

It SHALL remain open rather than encode a closed list of procedures, manuals, P&IDs or other document families.

## Document Source Contract

`DocumentSourceType` SHALL be an immutable open classification of the source system/context.

It SHALL require a string, trim surrounding whitespace, normalize the classification value to lowercase and reject an empty normalized value.

`DocumentSource` SHALL contain:

- `source_type: DocumentSourceType`;
- `source_reference: str`.

The source reference SHALL be trimmed, non-empty and case-preserving.

It SHALL remain opaque to the canonical domain.

The canonical domain SHALL NOT assume it is a path, URL, document number or database key.

## Identity Separation

`EnterpriseDocument.id` is the canonical PlantMind identity.

`DocumentSource.source_reference` is external/source-system traceability.

The source reference SHALL NOT become canonical identity.

AD-043 SHALL NOT establish global source-reference uniqueness, deduplication, aliasing or reconciliation semantics.

## Domain Ownership

Canonical Document validation belongs to:

`app.domain.document`

using existing shared:

- `DomainEntity`;
- `EntityId`;
- `DomainException`.

The Document domain SHALL remain independent from the Knowledge domain.

`EnterpriseDocument` SHALL NOT derive from or wrap `KnowledgeRecord`.

## Procedure Separation

A Document with type `procedure` does not automatically become an operational Procedure aggregate.

The existing empty `app.domain.procedure` remains unpromoted.

Future Procedure execution semantics require their own explicit domain contract.

## Deferred Lifecycle Boundary

`EnterpriseDocument` establishes one immutable canonical Document record and its PlantMind identity.

AD-043 / RFC-057 intentionally remains neutral about whether future revisions retain that identity, receive independent identity, become separate Document records or use a dedicated revision entity/aggregate.

AD-043 / RFC-057 SHALL NOT establish:

- Document revision identity;
- revision number;
- version chain;
- effective dates;
- approval lifecycle;
- supersession;
- retention;
- archival;
- deletion;
- mutable document state.

Those require separate architecture decisions.

## Deferred Persistence Boundary

AD-043 / RFC-057 SHALL NOT introduce:

- Document repository;
- Document database model;
- Document table;
- Alembic migration;
- PostgreSQL persistence;
- document uniqueness indexes.

Future Document persistence SHALL consume the accepted canonical Document domain.

## Deferred Document Library Boundary

AD-043 / RFC-057 SHALL NOT implement:

- production Document Library;
- catalogue;
- binary storage;
- upload;
- retrieval;
- source synchronization;
- document permissions;
- document search;
- revision management.

The accepted Document foundation will become a prerequisite for those capabilities.

## Deferred Ingestion and Parsing Boundary

AD-043 / RFC-057 SHALL NOT introduce:

- document ingestion application service;
- PDF parsing;
- OCR;
- chunking;
- extraction;
- document-to-Knowledge transformation;
- AI-based classification or extraction.

The previously considered `DocumentKnowledgeIngestionApplicationService` is not introduced.

A future ingestion contract SHALL depend on the accepted Document foundation and existing Knowledge Capture boundary.

## Knowledge Boundary

AD-039 through AD-042 remain unchanged.

RFC-057 SHALL NOT modify:

- canonical Knowledge domain;
- `KnowledgeRecordRepository`;
- relational Knowledge persistence;
- `KnowledgeCaptureApplicationService`;
- Knowledge provenance semantics.

Document and Knowledge remain separate canonical concepts until an explicit transformation boundary connects them.

## Source-Neutral Boundary

AD-009 remains authoritative.

The canonical Document domain SHALL NOT depend directly on:

- PI System;
- File Server;
- SAP;
- CMMS;
- SharePoint;
- DCS;
- OPC UA;
- any specific document-management product.

Source-specific connectors SHALL translate their source semantics into future approved application/integration boundaries.

## Composition and Runtime Boundary

AD-043 SHALL NOT modify:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`;
- Runtime states;
- Bootstrap;
- Health;
- mandatory-capability policy.

Canonical Document domain availability SHALL NOT create a new mandatory Runtime capability.

## Security and Trust Boundary

`DocumentSource` provides origin/reference traceability only.

It does not establish:

- authenticity;
- approval;
- integrity;
- authorization;
- user identity;
- RBAC;
- correctness;
- safety;
- compliance.

The current prototype `SecurityManager` SHALL NOT be interpreted as production enterprise security.

AD-043 acceptance SHALL NOT be represented as Cybersecurity approval or production readiness.

## Consequences

PlantMind gains one canonical definition of an immutable enterprise Document record and its PlantMind identity before Document Library or ingestion capabilities are implemented.

Future Document Library, parser, ingestion, search and Knowledge-transformation work can depend on a shared canonical Document model rather than invent competing models.

Shared `EntityId` remains the platform-wide entity identity primitive.

External source references remain distinct from canonical PlantMind identity.

The design avoids prematurely committing to revision, persistence, binary-storage or lifecycle semantics.

Document and Knowledge remain independently governed canonical concepts.

## Contract Acceptance

RFC-057 Contract Acceptance Review: passed.

AD-043 is accepted.

The Canonical Enterprise Document Foundation Boundary contract is accepted.

Contract review found no conflicting ownership, competing identity primitive, premature revision semantics, hidden persistence coupling, premature Document Library or ingestion implementation, default-composition coupling or unsupported production-security claim.

The RFC-057 implementation-entry Git gate has been satisfied.

RFC-057 technical implementation is complete within the accepted AD-043 architecture boundary.

Acceptance requires review against:

- shared domain primitives;
- AD-009;
- AD-039 / RFC-053;
- AD-040 / RFC-054;
- AD-041 / RFC-055;
- AD-042 / RFC-056;
- canonical Knowledge implementation;
- current Domain patterns;
- current Procedure prototypes;
- architecture guardrails;
- regression tests;
- Project Context;
- Session Handoff;
- Engineering Journal;
- Active Work Register.

## Technical Completion

RFC-057 technical implementation is complete.

The implementation established:

- canonical `app.domain.document`;
- immutable `DocumentType`;
- immutable `DocumentSourceType`;
- immutable `DocumentSource`;
- immutable `EnterpriseDocument`;
- shared `EntityId` as canonical PlantMind Document identity;
- source-neutral traceability without persistence or source-system coupling.

Technical verification:

- Contract commit: `63d9119`
- Technical commit: `a134c7a`
- Focused RFC-057 plus Knowledge architecture verification: 70 passed
- Full PlantMind regression: 586 passed
- Python compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Exact local/remote technical commit identity: verified
- Working tree after technical push: clean

The implementation introduces no Document repository, persistence, revision lifecycle, Document Library, parsing, ingestion, search, vector, graph, RAG, LLM, default-composition or production-security capability.

## Post-RFC-057 Source-of-Truth Architecture Review Outcome

The required post-RFC-057 Source-of-Truth architecture review is complete.

The review confirmed that AD-043 / RFC-057 established canonical enterprise Document identity and source traceability while intentionally deferring repository, persistence, revision, Document Library and ingestion responsibilities.

The next missing prerequisite is a persistence-neutral canonical Document repository port.

The evidence-based next architecture direction is:

`RFC-058 — Canonical Enterprise Document Repository Foundation Boundary`

The preliminary repository contract direction is:

- `EnterpriseDocumentRepository`;
- `EnterpriseDocumentAlreadyExistsError`;
- `add(document: EnterpriseDocument) -> None`;
- `get(document_id: EntityId) -> EnterpriseDocument | None`.

Duplicate conflict SHALL concern canonical Document `EntityId` only.

`DocumentSource.source_reference` remains external/source-system traceability and SHALL NOT become canonical identity, globally unique repository key or implicit search contract.

RFC-058 SHALL NOT automatically introduce source-reference lookup, list, search, update, delete, upsert, revision semantics, relational persistence, SQLAlchemy, migrations, Document Library behavior, ingestion or production composition.

The persistence-neutral repository namespace direction is:

`app.document.repository`

RFC-058 / AD-044 Contract Acceptance Review is complete and passed.

AD-044 is accepted.

RFC-058 implementation-entry Git gate was subsequently satisfied.

The accepted contract was committed and pushed, exact local/remote contract commit identity was verified and the working tree was clean before implementation.

RFC-058 technical implementation is now complete within the accepted AD-044 boundary.

---

# AD-044 — Canonical Enterprise Document Repository Foundation Boundary

## Status

Accepted.

RFC-058 Contract Acceptance Review: passed.

RFC-058 implementation-entry Git gate: satisfied.

RFC-058 technical implementation: complete.

## Context

AD-043 / RFC-057 established the canonical immutable enterprise Document domain:

- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`;
- shared canonical `EntityId`.

AD-043 intentionally deferred persistence semantics.

PlantMind therefore has a canonical Document entity but no accepted persistence-neutral Document repository port.

The post-RFC-057 Source-of-Truth architecture review identified this missing repository contract as the next prerequisite before relational persistence, Document Library behavior or document ingestion.

## Problem

Without an accepted persistence-neutral repository contract, future Document capabilities could independently invent:

- competing repository interfaces;
- source-reference identity;
- source-reference uniqueness assumptions;
- implicit CRUD behavior;
- relational coupling;
- lifecycle semantics;
- persistence behavior inside application services.

That would weaken the separation established by AD-043.

## Proposed Decision

If accepted, AD-044 / RFC-058 will introduce the persistence-neutral repository port:

`EnterpriseDocumentRepository`

under:

`app.document.repository`

The package initializer:

`app.document.__init__.py`

will remain empty within RFC-058 and will not establish a new public re-export API.

The repository port will expose exactly two canonical operations:

`add(document: EnterpriseDocument) -> None`

and:

`get(document_id: EntityId) -> EnterpriseDocument | None`

The repository will persist and retrieve canonical Document identity without owning relational technology, search, lifecycle or ingestion behavior.

## Repository Conflict

If `add()` encounters an already-existing canonical Document identity, the repository contract will represent the conflict using:

`EnterpriseDocumentAlreadyExistsError`

The conflict concerns only canonical:

`EnterpriseDocument.id`

using shared:

`EntityId`

The repository must not silently overwrite an existing canonical Document.

## Exception Ownership

`EnterpriseDocumentAlreadyExistsError` is a repository-level persistence conflict.

It will derive from:

`Exception`

and not:

`DomainException`

Canonical Document validation remains owned by `app.domain.document`.

## Identity Lookup

`get()` performs canonical identity lookup only.

If identity exists, it returns the canonical `EnterpriseDocument`.

If identity is absent, it returns:

`None`

No not-found exception is required.

Identity lookup is not Search capability.

## Source Reference Separation

AD-043 remains authoritative.

`DocumentSource.source_reference` is source traceability and is not canonical PlantMind identity.

AD-044 / RFC-058 will not establish source-reference uniqueness.

It will not introduce:

`find_by_source_reference()`

or equivalent source-reference lookup behavior.

Future source reconciliation, aliasing, deduplication or uniqueness semantics require separate explicit architecture.

## Mutation Boundary

AD-044 / RFC-058 will not introduce:

- update;
- delete;
- upsert;
- replace;
- mutable lifecycle state.

The accepted Document entity remains immutable.

## Revision Boundary

AD-044 / RFC-058 remains revision-neutral.

No decision is made about future Document revisions, version identity, supersession or current-revision behavior.

## Persistence Technology Boundary

AD-044 / RFC-058 is persistence-neutral.

It will not introduce:

- SQLAlchemy;
- relational Document models;
- PostgreSQL Document persistence;
- Session ownership;
- transaction ownership;
- Alembic migration;
- Document tables;
- indexes;
- constraints.

A future relational adapter will require separate architecture authorization.

## Document Library Boundary

A persistence-neutral repository port is not a production Document Library.

AD-044 / RFC-058 will not introduce catalogue, browse, upload, retrieval, storage, retention, permissions, revision management or synchronization behavior.

## Ingestion Boundary

AD-044 / RFC-058 will not introduce document ingestion or document-to-Knowledge transformation.

Those remain future application/integration concerns.

AD-044 does not decide whether a future ingestion boundary depends directly on `EnterpriseDocumentRepository`, another accepted application service, or both.

A future ingestion boundary must not invent competing canonical Document persistence semantics.

## Search Boundary

AD-044 / RFC-058 will not introduce list, find, search, filter, query, ranking or semantic retrieval operations.

Search requires separate architecture.

## Knowledge Boundary

AD-039 through AD-042 remain unchanged.

AD-044 / RFC-058 will not modify Knowledge domain, Knowledge repository, relational Knowledge persistence or Knowledge Capture.

## Composition and Runtime Boundary

AD-044 / RFC-058 will not modify:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`;
- Runtime;
- Bootstrap;
- Health;
- mandatory-capability policy.

The repository interface will not automatically become a default production dependency.

## Security Boundary

AD-044 / RFC-058 does not establish authentication, authorization, RBAC, actor audit, source authenticity, Document approval or Cybersecurity approval.

No production-security readiness is implied.

## Source-Neutral Boundary

AD-009 remains authoritative.

The repository contract will not depend directly on PI System, DCS, OPC UA, SAP, CMMS, File Server, SharePoint or any document-management technology.

## Alternatives Rejected

### Direct relational persistence first

Rejected because SQLAlchemy/database ownership should not define the canonical repository contract.

### Document ingestion first

Rejected because ingestion should consume accepted Document persistence/application boundaries rather than invent them.

### Full Document Library first

Rejected because it would prematurely combine repository, storage, lifecycle, search, permissions and ingestion responsibilities.

### Source-reference repository identity

Rejected because AD-043 explicitly separates external source references from canonical PlantMind identity.

### Generic CRUD repository

Rejected because update/delete/upsert/list/search semantics have not been justified by current requirements and would expand the architecture without evidence.

## Consequences

If accepted:

- PlantMind gains one canonical persistence-neutral Document repository port;
- canonical Document identity remains based on shared `EntityId`;
- source references remain traceability rather than identity;
- future relational adapters can implement a stable canonical port;
- future application services can depend on a persistence-neutral abstraction;
- relational persistence, Document Library, revision lifecycle, ingestion and search remain separately governed.

## Contract Review Gate

RFC-058 Contract Acceptance Review passed and AD-044 was accepted before implementation.

The accepted RFC-058 / AD-044 contract was committed and pushed as:

`b0af39f5a1a8df63e15203fa51349233136c9d2d`

Exact local/remote contract commit identity and a clean working tree were verified before technical implementation began.

The implementation-entry Git gate was therefore satisfied.

## Contract Acceptance

RFC-058 Contract Acceptance Review: passed.

The review found no conflicting ownership, source-reference identity leakage, source-reference uniqueness assumption, hidden Search capability, unjustified CRUD expansion, premature revision semantics, relational-infrastructure ownership, Document Library behavior, ingestion ownership, default-composition coupling or unsupported production-security claim.

The two acceptance refinements were incorporated before acceptance:

- `app.document.__init__.py` remains empty and does not establish a new public re-export API;
- future ingestion dependency shape remains undecided and RFC-058 does not force direct repository dependency.

## Technical Completion

RFC-058 technical implementation is complete within the accepted AD-044 boundary.

The implementation introduced:

- empty `app.document.__init__.py`;
- persistence-neutral `app.document.repository`;
- `EnterpriseDocumentAlreadyExistsError`;
- abstract `EnterpriseDocumentRepository`;
- exactly `add()` and `get()` repository operations.

The implementation preserved:

- canonical `EntityId` duplicate semantics only;
- `DocumentSource.source_reference` as traceability rather than identity;
- absence-as-`None` identity lookup;
- no search or CRUD expansion;
- no revision semantics;
- no relational-infrastructure dependency;
- no default composition change.

Technical verification:

- Contract commit: `b0af39f5a1a8df63e15203fa51349233136c9d2d`
- Technical commit: `b0f7ffc67100ce1899f0d30d43c2eabf0d2f7a73`
- Focused RFC-058 verification: 14 passed
- Document + repository guardrails: 47 passed
- Full PlantMind regression: 600 passed
- Python compilation: passed
- `git diff --check`: passed
- Remote technical push: verified
- Exact local/remote technical commit identity: verified
- Working tree after technical push: clean

The implementation introduced no SQLAlchemy Document adapter, Document table, migration, Document Library, revision lifecycle, ingestion, parsing, search, vector/graph/RAG/LLM capability, production composition or production-security claim.

## Current Decision State

AD-044: Accepted.

RFC-058: Technically Complete.

## Post-RFC-058 Source-of-Truth Architecture Review

The required post-RFC-058 Source-of-Truth architecture review is complete.

### Review Evidence

The review confirmed that:

- AD-043 / RFC-057 established canonical `EnterpriseDocument`;
- AD-044 / RFC-058 established the persistence-neutral `EnterpriseDocumentRepository`;
- no relational Document row/model currently exists;
- no relational Document mapper currently exists;
- no SQLAlchemy Document repository adapter currently exists;
- no Document relational schema or Alembic migration currently exists;
- `DatabaseBase.metadata` remains the canonical relational metadata authority;
- Alembic remains the sole schema-migration authority;
- existing Knowledge relational persistence demonstrates the accepted separation between canonical domain, persistence-neutral repository port and infrastructure-owned relational adapter;
- the current migration chain ends with the Knowledge schema introduced after the canonical database foundation;
- Document revision semantics remain undecided;
- Document Library behavior remains separately governed;
- document ingestion remains separately governed;
- document search remains separately governed.

### Architecture Direction Selected

The next evidence-based architecture direction is:

`RFC-059 — Canonical Document Relational Persistence Adapter Boundary`

RFC-059 status:

Direction Selected — Contract Not Drafted.

No architecture decision for RFC-059 has been drafted or accepted by this review.

No implementation gate is open.

### Preliminary Boundary

A future RFC-059 contract may define, subject to Contract Acceptance Review:

- an infrastructure-owned relational representation of `EnterpriseDocument`;
- explicit mapping between canonical `EnterpriseDocument` and its relational representation;
- a SQLAlchemy implementation of the accepted `EnterpriseDocumentRepository`;
- the next canonical Alembic migration required for Document relational persistence;
- explicit registration of the Document relational model with the canonical metadata lifecycle where required.

The preliminary relational shape is limited to canonical RFC-057 state:

- canonical Document identity;
- document type;
- title;
- source type;
- source reference.

The review does not authorize:

- source-reference uniqueness;
- source-reference identity;
- revision/version columns;
- update/delete/upsert;
- list/search/query;
- search indexes;
- document binary or file storage;
- Document Library behavior;
- ingestion;
- parsing or OCR;
- Knowledge transformation;
- vector, graph, RAG or LLM capability;
- default production composition;
- mandatory database startup;
- authentication or authorization expansion;
- Cybersecurity approval or production-readiness claims.

### Review Outcome

Post-RFC-058 Source-of-Truth architecture review: complete.

RFC-059 direction: selected.

RFC-059 contract: not drafted.

RFC-059 architecture decision: not drafted.

RFC-059 technical implementation: not authorized.

## Next Exact Action

Draft the RFC-059 architecture contract and proposed architecture decision.

Perform Contract Acceptance Review before committing an accepted contract or opening any implementation gate.

---

# AD-045 — Canonical Document Relational Persistence Adapter Boundary

## Status

Accepted.

RFC-059 Contract Acceptance Review: passed.

Technical implementation: complete and verified at `c1090919945af826992cfd4940aeec674907df76`.

## Context

AD-043 / RFC-057 established canonical immutable `EnterpriseDocument`.

AD-044 / RFC-058 established `EnterpriseDocumentRepository`.

AD-040 / RFC-054 established canonical relational runtime, session-factory ownership, `DatabaseBase.metadata` and Alembic schema lifecycle.

The post-RFC-058 review confirmed that no relational Document model, mapper, SQLAlchemy repository adapter or Document migration currently exists.

AD-041 / RFC-055 provides the accepted relational persistence precedent.

## Decision

PlantMind SHALL introduce one infrastructure-owned SQLAlchemy implementation of:

`EnterpriseDocumentRepository`

under:

`app.infrastructure.document`

The canonical infrastructure contracts are proposed as:

- `EnterpriseDocumentRow`;
- `document_to_row(...)`;
- `row_to_document(...)`;
- `SQLAlchemyEnterpriseDocumentRepository`.

The canonical domain and persistence-neutral repository SHALL remain unchanged.

The adapter SHALL implement only:

- `add(document: EnterpriseDocument) -> None`;
- `get(document_id: EntityId) -> EnterpriseDocument | None`.

## Relational Representation

The canonical relational table SHALL be:

`enterprise_documents`

It SHALL preserve:

- canonical UUID identity;
- document type;
- title;
- source type;
- source reference.

The primary-key constraint SHALL be:

`pk_enterprise_documents`

`source_reference` SHALL remain non-unique external traceability.

## Domain Boundary

`app.domain.document` and `app.document.repository` SHALL remain SQLAlchemy-free.

Explicit mapping SHALL reconstruct canonical Document objects through approved constructors.

Relational rows SHALL NOT replace canonical domain entities.

## Session and Transaction Boundary

The adapter SHALL receive the canonical session factory explicitly.

It SHALL NOT create an independent engine, competing session factory, hidden configuration dependency or process-global Session.

`DatabaseRuntime` remains engine/session lifecycle owner.

`add()` SHALL commit atomically or roll back.

`get()` SHALL remain read-only.

No Unit of Work or cross-repository transaction coordination is introduced.

## Duplicate Boundary

The relational primary key SHALL remain the concurrency-safe duplicate authority.

Only a structured PostgreSQL failure satisfying both:

- SQLSTATE `23505`;
- diagnostic constraint identity `pk_enterprise_documents`

SHALL translate to:

`EnterpriseDocumentAlreadyExistsError`

Neither SQLSTATE nor constraint identity alone is sufficient.

No human-readable error-message parsing is permitted.

No pre-insert lookup SHALL become authoritative duplicate prevention.

## Migration Boundary

Alembic remains the canonical schema-migration authority.

RFC-059 establishes revision:

`0003`

as the single linear successor to:

`0002`

Revision `0003` SHALL create `enterprise_documents`.

Revisions `0001` and `0002` SHALL remain unchanged.

The migration graph SHALL retain one canonical head.

## Metadata Boundary

The mapped Document table SHALL register with:

`DatabaseBase.metadata`

Alembic SHALL explicitly load `EnterpriseDocumentRow` registration in `backend/migrations/env.py` before using canonical metadata for schema comparison.

The registration SHALL follow the existing Knowledge mapped-model registration pattern.

Metadata registration SHALL create no engine, Session, database connection or migration side effect.

## Composition and Runtime Boundary

RFC-059 SHALL NOT make PostgreSQL mandatory in default platform composition or startup.

Runtime, Bootstrap, readiness, admission and lifecycle authority remain unchanged.

## Deferred Boundaries

RFC-059 SHALL NOT introduce:

- source-reference uniqueness or lookup;
- revision/version semantics;
- update/delete/upsert;
- Document Library;
- file/binary storage;
- ingestion;
- parser/OCR;
- search;
- Knowledge transformation;
- vector/graph/RAG/LLM capability;
- default relational production composition.

## Security and Deployment

Passing architecture or implementation verification SHALL NOT mean production PostgreSQL connectivity, production schema deployment, Cybersecurity approval or production readiness.

Those remain separately gated.

## Contract Acceptance

RFC-059 Contract Acceptance Review: passed.

The review found no competing Document identity, source-reference identity leakage, source-reference uniqueness assumption, hidden search capability, premature revision ownership, Document Library ownership, ingestion ownership, competing engine/session ownership, migration-history rewrite, default-composition coupling, Runtime-authority expansion or unsupported production-readiness claim.

Pre-acceptance refinements fixed:

- canonical infrastructure contract names;
- mandatory Alembic metadata registration for `EnterpriseDocumentRow`;
- strict duplicate classification requiring both SQLSTATE `23505` and `pk_enterprise_documents`.

## Current Decision State

AD-045: Accepted.

RFC-059: Technically Complete.

Contract commit:

`61e69e73a0f2460281c91169020b06ef1b5ad1db`

Technical commit:

`c1090919945af826992cfd4940aeec674907df76`

Verification:

- full PlantMind regression: 637 passed;
- Python compilation: passed;
- canonical Alembic head: `0003`;
- migration lineage: `0001 → 0002 → 0003`;
- remote technical push: verified;
- exact local/remote technical commit identity: verified;
- working tree after technical push: clean.

Post-RFC-059 system and architecture integrity review:

**PASS.**

The review found no Domain dependency leak, persistence leak, default-composition database coupling, competing lifecycle authority or need for architectural redesign.

## Next Exact Action

Commit and push the RFC-059 engineering-memory and post-implementation architecture-review closure.

After documentation closure, select the next architecture workstream from current evidence; RFC-060 is not preselected.

---

# AD-046 — Canonical Enterprise Document Registration Application Boundary

## Status

Accepted.

RFC-060 Contract Acceptance Review: passed.

Technical implementation: complete and verified at `c3ffb25849d6ae7b3fe26264cdf326ae5b3f86c7`.

## Context

AD-043 / RFC-057 established canonical immutable `EnterpriseDocument` identity and Document semantics.

AD-044 / RFC-058 established the persistence-neutral `EnterpriseDocumentRepository`.

AD-045 / RFC-059 established the canonical relational implementation of that repository while explicitly deferring any document registration workflow.

Post-RFC-059 architecture review confirmed that PlantMind remains architecturally sound and that no Document Registration application service currently exists.

A generic application wrapper exposing repository-equivalent `add()` and `get()` behavior would add no independent application responsibility.

PlantMind does, however, require an explicit use case that accepts caller registration inputs, owns creation of canonical Document identity, constructs canonical Document types and submits the resulting Document through the accepted repository port.

## Decision

PlantMind SHALL introduce:

`EnterpriseDocumentRegistrationApplicationService`

under:

`app.services.enterprise_document_registration_application_service`

with immutable application input:

`EnterpriseDocumentRegistrationRequest`

The canonical operation SHALL be:

`register(request: EnterpriseDocumentRegistrationRequest) -> EnterpriseDocument`

The service SHALL construct one canonical immutable `EnterpriseDocument`, persist it through `EnterpriseDocumentRepository.add(...)`, and return the same canonical Document only after persistence succeeds.

## Application Input

`EnterpriseDocumentRegistrationRequest` SHALL contain:

- `document_type: str`;
- `title: str`;
- `source_type: str`;
- `source_reference: str`.

Caller input SHALL NOT provide canonical Document identity or preconstructed canonical Document objects.

## Identity Ownership

The Registration boundary SHALL create canonical Document identity using shared `EntityId`.

Default identity generation SHALL use:

`EntityId.new()`

Narrow deterministic identity injection MAY be supported per service instance for verification.

No `DocumentId`, global identity service, provider registry or new DI framework is introduced.

## Domain Ownership

Canonical normalization and validation remain owned by:

`app.domain.document`

The Registration boundary SHALL construct:

- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`.

It SHALL NOT duplicate canonical Document validation rules.

## Source Reference

`DocumentSource.source_reference` remains source-system traceability only.

It SHALL NOT become canonical identity, global uniqueness, deduplication identity, repository alternate key, authenticity evidence or approval evidence.

Equal source references MAY exist on distinct canonical Document identities.

## Repository Boundary

`EnterpriseDocumentRepository` SHALL be injected explicitly.

For registration reaching persistence:

`add(...)`

SHALL be called exactly once.

Repository `get(...)` SHALL NOT be used for pre-insert duplicate checks, post-write confirmation or source-reference lookup.

`EnterpriseDocumentAlreadyExistsError` and unexpected repository failures SHALL propagate without retry, overwrite, identity regeneration or synthetic success.

## Persistence Ownership

RFC-060 SHALL NOT own SQLAlchemy, Session, engine, `DatabaseRuntime`, transaction, commit, rollback, migration or schema responsibility.

AD-045 / RFC-059 remains authoritative for relational persistence behavior.

## Explicit Deferrals

RFC-060 SHALL NOT introduce:

- update/delete/upsert;
- revision/version lifecycle;
- approval lifecycle;
- Document Library;
- binary/file storage;
- upload/download;
- catalogue browsing;
- source synchronization;
- parsing;
- OCR;
- chunking;
- ingestion;
- Knowledge transformation;
- Knowledge Capture calls;
- search;
- embeddings;
- vector persistence;
- Knowledge Graph persistence;
- RAG;
- LLM invocation;
- HTTP/transport;
- industrial source integration;
- default production composition.

## Composition and Runtime

RFC-060 SHALL NOT automatically modify `CompositionRoot`, `ServiceContainer`, `PlatformComposition` or `ApplicationFacade`.

Default application startup remains independent from PostgreSQL and Document source availability.

Runtime, Bootstrap, readiness, Health, request admission and operational-transition authority remain unchanged.

## Security and Deployment

RFC-060 does not establish authentication, authorization, RBAC, actor identity, actor audit, Active Directory, LDAP, MFA, document permissions, source authenticity, approval, Cybersecurity acceptance or production readiness.

Those remain separately gated.

## Contract Acceptance

RFC-060 / AD-046 Contract Acceptance Review: passed.

The accepted boundary is a specialized Document registration application use case rather than a generic repository wrapper.

It preserves canonical Document identity, domain validation, repository persistence ownership, source-reference semantics, default composition independence and all deferred Document Library, ingestion, AI, security and deployment capabilities.

## Current Decision State

AD-046: Accepted.

RFC-060: Technically Complete.

Contract commit:

`cda5e57eeabfa3699f960586982899cdf0ff9757`

Technical implementation commit:

`c3ffb25849d6ae7b3fe26264cdf326ae5b3f86c7`

Verification:

- RFC-060 focused verification: 16 passed;
- Document + Knowledge boundary verification: 77 passed;
- full PlantMind regression: 653 passed;
- Python compilation: passed;
- Alembic head remains `0003`;
- remote technical push: verified;
- exact local/remote technical identity: verified;
- working tree after technical push: clean.

Post-RFC-060 system and architecture integrity review: PASS.

The implementation preserves canonical Document-domain ownership, repository persistence separation, source-reference semantics, default-composition independence and Runtime/Bootstrap authority.

No Document Library, revision lifecycle, ingestion, Knowledge transformation, search/vector/graph/RAG/LLM, production security or production-readiness capability is established.

## Next Exact Action

Complete and commit the RFC-060 engineering-memory and post-implementation architecture-review closure.

After that closure is pushed and verified, select the next architecture workstream from current evidence.

Do not preselect RFC-061.

---

# AD-047 — Canonical Document-to-Knowledge Lineage Foundation Boundary

## Status

Accepted.

RFC-061 / AD-047 Contract Acceptance Review: passed.

Technical implementation is not authorized until the implementation-entry Git gate is satisfied.

## Context

PlantMind now has canonical Enterprise Document identity and canonical Knowledge identity.

External Document source references remain intentionally distinct from canonical PlantMind identity and MAY be shared by multiple canonical Documents.

Knowledge provenance currently records source type, source reference and capture timestamp.

Knowledge subject is the optional primary contextual reference of a Knowledge record.

RFC-053 explicitly deferred derivation and provenance relationships to a future explicit contract.

A proposed Document Knowledge Ingestion contract was reviewed and rejected before commit because propagating only external Document source metadata into Knowledge would lose the canonical Document identity and create a thin translation wrapper over Knowledge Capture.

## Decision

PlantMind SHALL establish a canonical identity-level relationship:

`DocumentKnowledgeLineage`

under:

`app.domain.document_knowledge_lineage`

containing exactly:

- `document_id: EntityId`;
- `knowledge_record_id: EntityId`.

It represents the directed semantic relationship:

the canonical Knowledge record identified by `knowledge_record_id` is derived from the canonical Enterprise Document identified by `document_id`.

## Identity Decision

The relation reuses canonical entity identities.

No new `DocumentId`, `KnowledgeId` or `LineageId` is introduced.

The lineage value does not generate identity.

It does not own either referenced entity.

## Provenance Decision

AD-047 SHALL NOT modify `KnowledgeProvenance`.

Existing source type, source reference and capture-time semantics remain authoritative.

Canonical Document lineage and external-source provenance are separate concepts.

Document identity SHALL NOT be hidden inside provenance `source_reference`.

## Subject Decision

AD-047 SHALL NOT modify `KnowledgeSubject`.

Document derivation SHALL NOT automatically replace the Knowledge record's primary contextual subject.

Lineage and subject semantics remain separate.

## Source Reference Decision

`DocumentSource.source_reference` remains external traceability only.

It SHALL NOT become lineage identity, canonical identity, uniqueness or deduplication identity.

Canonical lineage therefore references `EnterpriseDocument.id`, not equality of source references.

## Cardinality Decision

AD-047 defines one directed identity pair only.

It does not establish global one-to-one, one-to-many or many-to-many cardinality semantics.

It does not establish corroboration, primary-source, merge or multi-source derivation rules.

Those require future contracts.

## Persistence Decision

AD-047 establishes no repository or persistence contract.

No lineage table, foreign key, unique constraint, index or Alembic migration is introduced.

Persistence-neutral lineage repository semantics remain future architecture work.

## Application Decision

AD-047 does not establish Document Knowledge ingestion.

It does not call Knowledge Capture or Document Registration.

A future ingestion boundary must preserve canonical lineage rather than reducing Document identity to external source-reference metadata.

## Parsing and Library Decision

AD-047 introduces no parsing, OCR, extraction, chunking, Document Library, binary storage, catalogue or source synchronization.

## Revision Decision

AD-047 is revision-neutral.

Document revision and supersession architecture remain separate.

Future revision architecture must explicitly determine lineage interaction with revisions.

## Search and AI Decision

AD-047 establishes no search, vector, graph, RAG or LLM capability.

A domain lineage relation is not equivalent to a Knowledge Graph implementation.

## Trust Decision

Lineage records derivation identity only.

It does not establish authenticity, correctness, trust, authorization, approval, compliance or safety acceptance.

## Composition and Runtime Decision

AD-047 introduces no default composition, Runtime, Bootstrap, Health or request-admission change.

## Security Decision

AD-047 establishes no authentication, authorization, RBAC, actor audit, Active Directory, LDAP, MFA or Cybersecurity readiness.

## Alternatives Rejected

### Extend KnowledgeProvenance with Document identity

Rejected because canonical Knowledge provenance already has accepted origin semantics and relational persistence.

Document-to-Knowledge derivation is an explicit cross-record identity relationship and should not silently redefine provenance.

### Encode Document identity in source_reference

Rejected because source reference is intentionally opaque external traceability and MAY be shared by multiple canonical Documents.

### Force Document identity into KnowledgeSubject

Rejected because subject represents primary contextual reference and may correctly refer to equipment or another domain entity.

### Implement Document Knowledge ingestion immediately

Rejected because ingestion without a canonical identity-level lineage contract would lose canonical Document identity or collapse into a thin Knowledge Capture translation wrapper.

### Introduce lineage persistence immediately

Rejected because the canonical relationship semantics must be accepted independently before repository and relational technology decisions.

### Implement graph lineage directly

Rejected because canonical domain semantics must not be defined by Neo4j or graph technology.

## Consequences

PlantMind gains a minimal canonical Document-to-Knowledge derivation identity contract.

Existing Document, Knowledge, provenance, subject, repository, persistence, Capture and Registration responsibilities remain unchanged.

Future repository, relational persistence and ingestion work can build on the lineage contract without inventing competing identity semantics.

## Contract Acceptance

RFC-061 / AD-047 Contract Acceptance Review: passed.

No production implementation is authorized until the accepted contract is committed, pushed and verified.

## Current Decision State

AD-047: Accepted.

RFC-061: Contract Accepted — Implementation Gate Pending.

## Next Exact Action

Commit and push this accepted contract.

Do not implement RFC-061 before Git implementation-entry verification.

---

# AD-048 — Canonical Document-to-Knowledge Lineage Repository Foundation Boundary

## Status

Accepted.

RFC-062 / AD-048 Contract Acceptance Review: passed.

Technical implementation is not authorized until the implementation-entry Git gate is satisfied.

## Context

PlantMind now has:

- canonical Enterprise Document identity;
- canonical Knowledge Record identity;
- canonical persistence-neutral Document repository semantics;
- canonical persistence-neutral Knowledge repository semantics;
- canonical immutable `DocumentKnowledgeLineage`;
- explicit separation between canonical lineage, Knowledge provenance and Knowledge subject.

RFC-061 / AD-047 established only the directed canonical identity relationship:

`document_id -> knowledge_record_id`

It deliberately introduced no repository, persistence, duplicate, database or application-ingestion behavior.

AD-047 explicitly deferred persistence-neutral lineage repository semantics to future architecture.

The next required architectural step is therefore to establish a minimal persistence-neutral repository port for canonical lineage values before relational persistence or Document Knowledge ingestion is considered.

## Decision

PlantMind SHALL establish:

`DocumentKnowledgeLineageRepository`

under:

`app.document_knowledge_lineage.repository`

The repository SHALL represent persistence-neutral storage and exact retrieval of canonical `DocumentKnowledgeLineage` values.

The package:

`app.document_knowledge_lineage`

SHALL NOT become a generic relationship framework.

Its initializer SHALL remain empty under RFC-062.

## Repository Conflict Decision

PlantMind SHALL establish:

`DocumentKnowledgeLineageAlreadyExistsError`

as a repository-level conflict exception.

It SHALL derive from:

`Exception`

and SHALL NOT derive from `DomainException`.

A repository conflict is not canonical Domain validation failure.

## Repository Operation Decision

`DocumentKnowledgeLineageRepository`

SHALL expose exactly two abstract operations:

`add(lineage: DocumentKnowledgeLineage) -> None`

and:

`get(document_id: EntityId, knowledge_record_id: EntityId) -> DocumentKnowledgeLineage | None`

No generic CRUD contract is authorized.

## Duplicate Identity Decision

Repository duplicate identity SHALL be the exact directed canonical identity pair:

`(document_id, knowledge_record_id)`

Re-adding the same directed pair SHALL raise:

`DocumentKnowledgeLineageAlreadyExistsError`

and SHALL NOT silently overwrite the existing canonical lineage relation.

Neither `document_id` alone nor `knowledge_record_id` alone SHALL define repository duplicate identity.

Therefore, at repository-storage level, distinct canonical lineage pairs sharing one side are not duplicates and MAY coexist.

For example, the repository contract does not classify either of the following as a duplicate solely because one identity is shared:

- `(document_A, knowledge_A)` and `(document_A, knowledge_B)`;
- `(document_A, knowledge_A)` and `(document_B, knowledge_A)`.

This is a storage-level duplicate-classification decision only.

It does not establish that such relationships are valid, authorized or meaningful at Business or Application level.

AD-048 does not establish:

- business one-to-one policy;
- business one-to-many policy;
- business many-to-one policy;
- business many-to-many policy;
- corroboration semantics;
- primary-source semantics;
- merge semantics;
- multi-source derivation authorization.

Those higher-level semantics remain separately governed and require explicit future architecture.

Repository storage capability SHALL NOT be interpreted as Business or Application authorization for any cardinality or derivation policy.

## Exact Retrieval Decision

`get(...)`

SHALL perform exact directed-pair lookup only.

When the exact pair exists, the repository SHALL return the canonical `DocumentKnowledgeLineage`.

When the exact pair does not exist, it SHALL return `None`.

AD-048 SHALL NOT introduce:

- `get_by_document`;
- `get_by_knowledge`;
- reverse traversal;
- list;
- find;
- search;
- filter;
- query;
- pagination;
- ranking.

Future query requirements require separate evidence and architecture review.

## Domain Ownership Decision

The repository SHALL consume existing canonical:

- `EntityId`;
- `DocumentKnowledgeLineage`.

It SHALL NOT:

- generate identity;
- construct `EnterpriseDocument`;
- construct `KnowledgeRecord`;
- reconstruct lineage from unrelated values;
- modify canonical lineage values;
- duplicate canonical lineage Domain validation.

Canonical lineage validation remains owned by:

`app.domain.document_knowledge_lineage`

## Referenced Entity Decision

The lineage repository SHALL NOT validate existence of referenced Document or Knowledge entities.

It SHALL NOT call:

- `EnterpriseDocumentRepository`;
- `KnowledgeRecordRepository`.

It SHALL NOT own cross-repository referential verification.

The repository port records and retrieves accepted canonical lineage values only.

Any future application-level requirement to verify referenced entities requires explicit architecture ownership.

## Dependency Decision

The canonical lineage repository port SHALL remain persistence-neutral.

It SHALL depend only on the minimum canonical contracts necessary to express its interface.

It SHALL NOT depend on:

- SQLAlchemy;
- Psycopg;
- infrastructure adapters;
- application services;
- Runtime;
- Bootstrap;
- Composition;
- FastAPI;
- parser;
- OCR;
- search;
- vector infrastructure;
- graph infrastructure;
- RAG;
- LLM.

## Persistence Decision

AD-048 establishes no relational persistence implementation.

It introduces no:

- SQLAlchemy row;
- lineage table;
- foreign key;
- database uniqueness constraint;
- database index;
- Alembic migration;
- Session ownership;
- transaction ownership;
- commit behavior;
- rollback behavior;
- `DatabaseRuntime` composition.

Canonical Alembic head remains:

`0003`

A relational lineage adapter requires a separate future accepted contract.

## Application Decision

AD-048 establishes no Document Knowledge ingestion application service.

It SHALL NOT modify or call:

- `KnowledgeCaptureApplicationService`;
- `EnterpriseDocumentRegistrationApplicationService`.

It establishes no application transaction or compensation semantics.

A future ingestion boundary must preserve accepted Document identity, Knowledge identity, Knowledge Capture and lineage responsibilities without bypassing them.

## Atomicity Decision

AD-048 does not claim atomicity across Knowledge persistence and lineage persistence.

It does not define:

- shared transaction orchestration;
- rollback across repositories;
- compensation;
- retry;
- partial-failure recovery.

Those concerns must be resolved explicitly before any future ingestion workflow attempts coordinated persistence across these boundaries.

## Parsing, Library and Revision Decision

AD-048 introduces no:

- Document Library;
- binary storage;
- file upload or download;
- parser;
- OCR;
- extraction;
- chunking;
- revision lifecycle;
- supersession behavior.

## Search, Graph and AI Decision

AD-048 introduces no:

- semantic search;
- embeddings;
- vector persistence;
- Qdrant;
- graph persistence;
- Neo4j;
- graph traversal;
- RAG;
- prompts;
- LLM invocation;
- autonomous agents.

A persistence-neutral lineage repository is not a Knowledge Graph implementation.

## Composition and Runtime Decision

AD-048 introduces no default:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`;
- Runtime;
- Bootstrap;
- Health;
- readiness;
- request-admission

change.

## Security Decision

AD-048 establishes no:

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

## Alternatives Rejected

### Implement relational lineage persistence immediately

Rejected because PlantMind architecture separates persistence-neutral repository semantics from relational adapter technology.

### Implement Document Knowledge ingestion immediately

Rejected because ingestion would require coordinated Knowledge and lineage persistence behavior, including explicit failure and atomicity semantics not owned by RFC-062.

### Store lineage directly in Knowledge provenance

Rejected because AD-047 already established canonical lineage and external-source provenance as separate concepts.

### Use Document source reference as repository identity

Rejected because source reference is external traceability and is not canonical PlantMind identity.

### Query lineage by one side immediately

Rejected because current evidence establishes exact identity-pair storage need, not broader traversal or search requirements.

### Implement lineage directly in Neo4j

Rejected because canonical repository semantics SHALL remain technology-neutral.

## Consequences

PlantMind gains a minimal persistence-neutral repository abstraction for canonical Document-to-Knowledge lineage.

Existing:

- Document ownership;
- Knowledge ownership;
- provenance semantics;
- Knowledge subject semantics;
- Knowledge Capture;
- Document Registration;
- relational persistence;
- Runtime;
- Composition

remain unchanged.

A future relational adapter can implement this accepted repository contract without defining canonical repository semantics inside SQLAlchemy or another persistence technology.

Future ingestion architecture can depend on a canonical lineage repository contract rather than inventing persistence behavior inside the ingestion workflow.

## Contract Acceptance

RFC-062 / AD-048 Contract Acceptance Review: passed.

The accepted contract preserves:

- exact directed-pair repository duplicate identity;
- separation of repository-storage capability from Business and Application cardinality policy;
- exact-pair retrieval only;
- persistence neutrality;
- Domain ownership boundaries;
- referenced-entity ownership boundaries;
- relational persistence deferral;
- ingestion and atomicity deferral;
- Runtime and Composition independence.

No production implementation is authorized by contract acceptance alone.

## Contract State

AD-048: Accepted.

RFC-062: Contract Accepted — Implementation Gate Pending.

Technical implementation is not authorized until the implementation-entry Git gate is satisfied.

## Next Exact Action

Commit and push the accepted RFC-062 / AD-048 contract.

After push, verify exact local/remote contract identity and a clean working tree before technical implementation begins.

Do not preselect the workstream after RFC-062.

---

# AD-049 — Canonical Document-to-Knowledge Lineage Relational Persistence Adapter Boundary

## Status

Accepted.

## Context

PlantMind now has an accepted canonical foundation for Document-derived Knowledge lineage.

Accepted architecture provides:

- canonical immutable `DocumentKnowledgeLineage`;
- canonical Document identity through `EnterpriseDocument.id`;
- canonical Knowledge identity through `KnowledgeRecord.id`;
- persistence-neutral `DocumentKnowledgeLineageRepository`;
- exact directed-pair repository identity;
- canonical synchronous relational database runtime;
- canonical SQLAlchemy metadata authority;
- relational Knowledge persistence;
- relational Enterprise Document persistence;
- linear Alembic history through revision `0003`.

AD-047 established canonical lineage identity semantics.

AD-048 established the persistence-neutral lineage repository port and explicitly deferred relational lineage persistence.

The current repository therefore contains a complete canonical lineage Domain and Repository contract but no production relational adapter for that repository.

Document Knowledge ingestion SHALL NOT be introduced at this stage because coordinated Knowledge persistence and lineage persistence requires explicit transaction, failure, atomicity and compensation semantics that are not yet accepted.

The minimum dependency-completing architectural step is therefore relational persistence for the already accepted lineage repository contract.

## Decision

PlantMind SHALL establish a canonical relational persistence adapter for:

`DocumentKnowledgeLineageRepository`

under:

`app.infrastructure.document_knowledge_lineage`

The adapter SHALL preserve the accepted canonical Domain and Repository contracts exactly.

It SHALL NOT expand application behavior, Runtime responsibility, default composition, lineage business semantics or Document Knowledge ingestion capability.

## Canonical Relational Representation

The infrastructure layer SHALL introduce:

`DocumentKnowledgeLineageRow`

representing exactly one canonical directed lineage pair.

The row SHALL contain exactly:

- `document_id`;
- `knowledge_record_id`.

Both SHALL use exactly:

`postgresql.UUID(as_uuid=True)`

with non-nullable relational columns.

This preserves the canonical relational identity representation already established by accepted Knowledge and Enterprise Document persistence.

The relational representation SHALL NOT contain:

- surrogate lineage identity;
- generated identity;
- timestamps;
- duplicated provenance;
- source reference;
- Knowledge subject fields;
- status;
- approval;
- trust;
- revision;
- business cardinality metadata.

## Relational Identity

The relational identity SHALL be the exact directed canonical pair:

`(document_id, knowledge_record_id)`

The canonical table SHALL use a composite primary key over that pair.

The primary-key constraint SHALL be named:

`pk_document_knowledge_lineages`

Neither side alone SHALL be unique.

Distinct lineage pairs sharing one side SHALL remain representable at relational-storage level.

This storage capability SHALL NOT establish Business or Application cardinality semantics.

## Canonical Table

The canonical relational table SHALL be:

`document_knowledge_lineages`

It SHALL contain only the relational columns required to preserve the accepted canonical lineage repository identity.

No surrogate primary key SHALL be introduced.

## Referential-Integrity Boundary

AD-049 SHALL NOT introduce relational foreign keys to:

- `enterprise_documents`;
- `knowledge_records`.

Canonical identities SHALL be persisted exactly as lineage references.

Cross-domain relational referential-integrity policy remains separately governed.

The relational adapter SHALL NOT:

- resolve referenced Documents;
- resolve referenced Knowledge records;
- call `EnterpriseDocumentRepository`;
- call `KnowledgeRecordRepository`;
- verify referenced entity existence.

## Mapping Boundary

Infrastructure SHALL provide explicit mapping between:

`DocumentKnowledgeLineage`

and:

`DocumentKnowledgeLineageRow`

using:

`lineage_to_row(lineage: DocumentKnowledgeLineage) -> DocumentKnowledgeLineageRow`

and:

`row_to_lineage(row: DocumentKnowledgeLineageRow) -> DocumentKnowledgeLineage`

Mapping SHALL preserve both canonical identities exactly.

Mapping SHALL NOT:

- generate identity;
- mutate canonical values;
- construct Documents;
- construct Knowledge records;
- call repositories;
- infer provenance;
- infer cardinality;
- enrich lineage Domain semantics.

## Repository Adapter

Infrastructure SHALL provide:

`SQLAlchemyDocumentKnowledgeLineageRepository`

implementing:

`DocumentKnowledgeLineageRepository`

It SHALL expose no public repository operations beyond the accepted contract:

`add(lineage: DocumentKnowledgeLineage) -> None`

and:

`get(document_id: EntityId, knowledge_record_id: EntityId) -> DocumentKnowledgeLineage | None`

## Session and Transaction Ownership

The relational repository adapter SHALL receive an injected synchronous SQLAlchemy session factory.

It SHALL NOT create or own the canonical database engine or `DatabaseRuntime`.

For successful `add(...)`:

1. one session is acquired;
2. the lineage value is mapped to its relational representation;
3. one row is submitted;
4. one commit occurs;
5. the session closes.

For failed `add(...)`:

1. the failure is observed;
2. the transaction is rolled back;
3. the session closes;
4. the failure is either translated only when canonical duplicate conditions are satisfied or otherwise propagated.

For `get(...)`:

1. one session is acquired;
2. exact composite-identity lookup is performed;
3. canonical lineage is returned when present;
4. `None` is returned when absent;
5. the session closes;
6. no commit occurs.

## Duplicate Classification

Only violation of the canonical relational identity constraint:

`pk_document_knowledge_lineages`

MAY be translated into:

`DocumentKnowledgeLineageAlreadyExistsError`

For PostgreSQL, duplicate classification SHALL require both:

- unique-violation SQLSTATE `23505`;
- exact canonical constraint identity `pk_document_knowledge_lineages`.

Unrelated integrity failures or database failures SHALL propagate unchanged.

The adapter SHALL NOT classify failure merely from exception type or message text.

## Metadata Authority

`DocumentKnowledgeLineageRow` SHALL participate in the existing canonical SQLAlchemy metadata authority.

AD-049 SHALL NOT introduce a second declarative metadata root.

## Schema Lifecycle

AD-049 authorizes one append-only Alembic revision:

`0004`

with:

`down_revision = "0003"`

The revision SHALL create only the canonical lineage relational schema authorized by this decision.

Expected table:

`document_knowledge_lineages`

Expected primary key:

`pk_document_knowledge_lineages`

Alembic metadata loading SHALL explicitly register the lineage relational model with canonical metadata.

`backend/migrations/env.py` SHALL be modified only as required to explicitly load `DocumentKnowledgeLineageRow` into that existing metadata authority.

No second metadata root or alternate schema authority SHALL be introduced.

Downgrade SHALL remove only schema introduced by revision `0004`.

## Application Boundary

AD-049 SHALL NOT introduce or modify:

- `KnowledgeCaptureApplicationService`;
- `EnterpriseDocumentRegistrationApplicationService`;
- Document Knowledge ingestion;
- application transaction orchestration;
- shared Unit of Work;
- cross-repository transaction semantics;
- compensation;
- retry policy.

## Composition Boundary

The relational lineage adapter SHALL NOT be automatically registered in default `CompositionRoot`.

Production composition requires a separately accepted application capability that explicitly needs lineage persistence.

Database availability SHALL NOT become a mandatory Runtime capability solely because this adapter exists.

## Runtime and Bootstrap Boundary

AD-049 SHALL NOT modify:

- Runtime lifecycle authority;
- Bootstrap authority;
- operational transition authority;
- mandatory capability policy;
- readiness semantics;
- database availability policy.

## Explicitly Deferred

The following remain outside AD-049:

- Document Knowledge ingestion;
- cross-repository atomicity;
- shared transaction orchestration;
- compensation across repositories;
- retry and partial-failure recovery;
- one-sided lineage retrieval;
- reverse traversal;
- list/search/filter/query/pagination;
- Business/Application lineage cardinality;
- corroboration;
- primary-source semantics;
- merge semantics;
- multi-source derivation;
- Document Library;
- binary storage;
- parsing;
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
- authentication;
- authorization;
- RBAC;
- Cybersecurity approval;
- production-readiness claims.

## Alternatives Considered

### Implement Document Knowledge ingestion now

Rejected.

The existing architecture does not yet define coordinated Knowledge and lineage persistence atomicity, transaction ownership, compensation or partial-failure semantics.

Introducing ingestion now would force those responsibilities implicitly into an application boundary.

### Introduce foreign keys immediately

Rejected.

Canonical lineage identity references are accepted, but cross-domain relational referential-integrity policy has not been separately established.

Foreign keys would introduce database-level lifecycle and deletion coupling beyond the accepted repository contract.

### Add a surrogate lineage identity

Rejected.

Canonical lineage identity is already the exact directed pair:

`(document_id, knowledge_record_id)`

A new identifier would add an unnecessary identity concept and weaken the accepted canonical model.

### Add one-sided or traversal queries

Rejected.

AD-048 established exact-pair retrieval only.

Search and traversal capability requires separate architecture.

### Compose relational lineage persistence immediately

Rejected.

The existence of an infrastructure adapter does not itself establish an application capability or mandatory Runtime dependency.

## Consequences

Positive consequences:

- canonical lineage becomes persistable using the accepted relational infrastructure;
- canonical pair identity remains consistent across Domain, Repository and relational storage;
- lineage persistence follows established Knowledge and Document persistence patterns;
- migration history remains linear;
- infrastructure remains replaceable behind the persistence-neutral repository port;
- Document Knowledge ingestion may later build on a real persistence foundation rather than a placeholder.

Constraints preserved:

- no application ingestion yet;
- no implicit cross-repository transaction semantics;
- no foreign-key lifecycle coupling;
- no default Composition coupling;
- no Runtime authority expansion;
- no search/traversal expansion;
- no production security or deployment claim.

## Acceptance Requirements

Before AD-049 may become Accepted, architecture review SHALL confirm:

1. canonical Domain ownership remains unchanged;
2. `DocumentKnowledgeLineageRepository` remains unchanged;
3. relational identity exactly matches the accepted directed pair;
4. no surrogate lineage identity is introduced;
5. neither side alone becomes unique;
6. no relational foreign keys are introduced;
7. duplicate translation requires SQLSTATE `23505` and exact canonical constraint identity;
8. canonical metadata authority remains singular;
9. Alembic lineage becomes `0001 → 0002 → 0003 → 0004`;
10. no Document or Knowledge repository lookup enters the adapter;
11. no Document Knowledge ingestion enters scope;
12. no cross-repository atomicity is implied;
13. default Composition remains unchanged;
14. Runtime and Bootstrap authority remain unchanged;
15. deferred Document Library, search, AI and security capabilities remain deferred.

## Contract Acceptance Review

Outcome:

**PASS — AD-049 accepted.**

The review confirmed all acceptance requirements after two pre-acceptance refinements:

1. canonical UUID storage is explicitly `postgresql.UUID(as_uuid=True)` with non-nullable lineage identity columns;
2. `backend/migrations/env.py` is explicitly included only for registration of `DocumentKnowledgeLineageRow` with the existing canonical metadata authority.

The accepted decision preserves:

- canonical Domain and repository ownership;
- exact directed-pair relational identity;
- composite primary-key duplicate semantics;
- no surrogate identity;
- no foreign-key lifecycle coupling;
- no cross-repository existence validation;
- no ingestion or application transaction semantics;
- no default Composition dependency;
- unchanged Runtime and Bootstrap authority;
- all explicitly deferred higher-level capabilities.

## Implementation Authorization

Status:

**Accepted — Implementation Gate Pending**

The architecture contract is accepted.

Technical implementation remains prohibited until this accepted contract is committed, pushed to `origin/feature/engineering-platform`, exact local/remote contract identity is verified, and the working tree is clean.

---

# AD-050 — Canonical Knowledge-and-Lineage Transaction Coordination Foundation Boundary

## Status

Accepted.

## Context

AD-039 through AD-042 established the canonical Knowledge Domain, relational database runtime, relational Knowledge persistence and specialized `KnowledgeCaptureApplicationService`.

AD-043 through AD-046 established the canonical Enterprise Document Domain, repository, relational persistence and specialized Document Registration application boundary.

AD-047 through AD-049 established canonical directed Document-to-Knowledge lineage, its persistence-neutral repository and its relational persistence adapter.

The accepted relational Knowledge and lineage repositories currently own independent SQLAlchemy session and transaction lifecycles.

Each standalone relational repository may independently acquire a session and own commit, rollback and close behavior.

AD-049 explicitly deferred:

- application transaction orchestration;
- shared Unit of Work;
- cross-repository transaction semantics;
- compensation;
- retry policy;
- Document-to-Knowledge ingestion.

A future accepted Document-derived Knowledge application capability may need one canonical `KnowledgeRecord` and its canonical `DocumentKnowledgeLineage` to participate in one relational transaction.

Without an accepted coordination boundary, introducing that capability would force transaction ownership, partial-failure semantics and rollback behavior implicitly into application code.

The minimum dependency-completing architecture is therefore a narrow Knowledge-and-lineage transaction coordination foundation.

## Decision

PlantMind SHALL establish a persistence-neutral coordination contract:

`KnowledgeLineageTransactionCoordinator`

under:

`app.knowledge_lineage_transaction`

The coordinator SHALL expose one synchronous coordinated execution responsibility equivalent to:

`execute(operation) -> T`

The supplied operation SHALL receive transaction-scoped implementations of exactly:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`.

RFC-064 / AD-050 SHALL NOT itself implement Document-to-Knowledge ingestion.

## Application-Level Responsibility

`KnowledgeLineageTransactionCoordinator` is an application-level persistence-coordination contract.

The term `application-level` describes responsibility and use-case position only.

AD-050 SHALL NOT introduce a seventh architectural layer.

The six-layer architecture defined by ARCH-001 remains unchanged.

The coordinator SHALL NOT become:

- an architectural layer;
- a Domain service;
- a Core Service;
- an Intelligence Engine;
- an AI Agent;
- an application workload entry point;
- a replacement or competitor for `ApplicationFacade`;
- an HTTP or other transport boundary.

It is a specialized supporting application-level persistence contract for future accepted Knowledge application capabilities.

## Dependency Decision

The persistence-neutral coordinator contract MAY depend only on:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`;
- Python standard-library typing and callable abstractions required to express the contract.

The persistence-neutral coordinator contract SHALL NOT depend on:

- SQLAlchemy;
- Psycopg;
- `DatabaseRuntime`;
- Infrastructure implementations;
- Composition;
- Runtime;
- Bootstrap;
- transport;
- agents;
- intelligence engines.

The SQLAlchemy implementation MAY depend on the persistence-neutral coordinator contract and its coordination-specific errors as required to implement this decision.

AD-050 explicitly authorizes that narrow implementation dependency.

This authorization SHALL NOT establish a general Infrastructure-to-Application dependency rule.

Infrastructure SHALL NOT thereby gain permission to depend on:

- application services;
- `ApplicationFacade`;
- orchestration services;
- business workflows;
- AI Agents;
- Intelligence Engines.

Canonical Domain and repository packages SHALL NOT depend outward on transaction infrastructure.

## Canonical Atomicity Boundary

For one coordinated operation, atomicity applies to Knowledge and lineage writes actually submitted through the transaction-scoped repositories during that operation.

If an application operation performs both:

1. one canonical Knowledge write; and
2. its corresponding canonical lineage write;

those participating writes SHALL commit together or neither SHALL be successfully committed by that transaction.

All successful participating writes within one coordinated operation SHALL commit together.

A failure before successful commit SHALL enter the accepted rollback path for the shared transaction.

The coordinator SHALL NOT itself:

- require both repositories to be written;
- infer whether lineage is required;
- infer correspondence between arbitrary Knowledge and lineage objects;
- enforce Knowledge-to-lineage business completeness;
- enforce business cardinality.

A future application capability that requires both writes SHALL own the obligation to invoke both required persistence operations before returning successful use-case completion.

AD-050 therefore guarantees transaction atomicity for participating relational writes.

It does not guarantee application-use-case completeness.

## Shared Session Invariant

One coordinated `execute(...)` invocation SHALL:

1. acquire exactly one synchronous SQLAlchemy session;
2. establish exactly one transaction scope;
3. provide transaction-scoped Knowledge and lineage repository participants using that exact session;
4. invoke the supplied operation exactly once;
5. own final commit authority;
6. own rollback authority;
7. own session-close authority.

The shared session SHALL NOT be retained for later independent executions.

Each independent execution SHALL own independent session and transaction state.

No shared active session SHALL be stored as reusable coordinator instance state.

## Transaction-Scoped Repository Participation

The SQLAlchemy implementation SHALL provide transaction-scoped implementations of the existing:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`.

Those participants SHALL preserve the accepted persistence-neutral repository contracts.

They SHALL NOT:

- create an engine;
- create an independent session;
- commit;
- rollback;
- close the shared session;
- generate Domain identity;
- construct Knowledge;
- construct lineage;
- change Domain semantics;
- change repository public operations.

They SHALL use the existing accepted relational mappings.

No alternate relational models for the same canonical entities are authorized.

## Transaction-Scoped Write Semantics

For transaction-scoped `add(...)`, the participant SHALL:

1. map the canonical value using the accepted mapper;
2. add the relational row to the shared session;
3. flush the shared session;
4. perform no commit;
5. perform no rollback;
6. perform no close.

Participant-owned flush exists to materialize repository-owned relational constraint failures at the repository boundary before final coordinated commit.

## Transaction-Scoped Read Semantics

For transaction-scoped `get(...)`, the participant SHALL:

- use the exact shared coordinator-owned session;
- acquire no independent session;
- perform no commit;
- perform no rollback;
- perform no close;
- preserve the accepted canonical row-to-Domain mapping;
- return `None` for an absent identity exactly as defined by the existing repository contract.

A transaction-scoped read SHALL NOT acquire transaction-lifecycle ownership.

## Standalone Repository Preservation

AD-050 SHALL NOT replace or redefine:

- `SQLAlchemyKnowledgeRecordRepository`;
- `SQLAlchemyDocumentKnowledgeLineageRepository`.

Existing standalone behavior remains authoritative outside coordinated execution.

Standalone repositories may continue to:

- acquire their own sessions;
- own standalone commit;
- own standalone rollback;
- own standalone close;
- preserve their existing duplicate translation behavior.

AD-050 adds a distinct coordinated persistence path rather than introducing ambiguous dual transaction ownership into the standalone repository classes.

## Duplicate Classification

Knowledge duplicate classification SHALL remain based on exactly:

- PostgreSQL SQLSTATE `23505`;
- constraint `pk_knowledge_records`.

Lineage duplicate classification SHALL remain based on exactly:

- PostgreSQL SQLSTATE `23505`;
- constraint `pk_document_knowledge_lineages`.

Knowledge identity conflict SHALL continue to translate to:

`KnowledgeRecordAlreadyExistsError`

Lineage identity conflict SHALL continue to translate to:

`DocumentKnowledgeLineageAlreadyExistsError`

Unrelated integrity failures SHALL remain unrelated integrity failures.

Message-text-only duplicate classification remains prohibited.

The coordinator SHALL NOT heuristically infer repository ownership of arbitrary database integrity errors.

Standalone and transaction-scoped paths SHALL use one canonical infrastructure-owned classification rule for each canonical identity constraint.

Implementation-private duplicate-classification helpers MAY be refactored to prevent semantic drift.

Such refactoring SHALL NOT change public repository APIs, exception types, constraint identity, SQLSTATE requirements or standalone transaction ownership.

## Commit-Time Failure Boundary

Repository-owned constraints SHALL be materialized through transaction-scoped participant flush whenever technically possible.

A failure appearing only at final commit SHALL NOT be heuristically reclassified by the coordinator as a Knowledge or lineage duplicate.

Commit-time failures SHALL enter the coordinated failure path and propagate unless a future accepted contract establishes safe additional classification.

## Session Acquisition and Transaction Start

The injected synchronous session factory SHALL be invoked exactly once per coordinated execution.

The supplied application operation SHALL NOT run before successful transaction establishment.

If session acquisition fails:

- the failure SHALL propagate;
- the operation SHALL NOT execute;
- no rollback SHALL be attempted for a nonexistent session;
- no close SHALL be attempted for a session that was never acquired.

If transaction establishment fails after session acquisition:

- the operation SHALL NOT execute;
- no commit SHALL occur;
- the acquired session SHALL be closed exactly once;
- rollback SHALL be attempted only when a transaction was actually established.

Nested transaction and savepoint behavior are not established by AD-050.

## Commit Semantics

After successful completion of the supplied operation:

1. participant persistence work SHALL already be submitted to the shared transaction;
2. required participant constraint validation SHALL already have been materialized through flush where technically possible;
3. the coordinator SHALL perform one final commit;
4. the operation result SHALL be returned only after successful final commit.

Transaction-scoped repositories SHALL NOT commit independently.

## Final Commit Failure and Outcome Certainty

If final commit raises:

- successful completion SHALL NOT be reported;
- the operation result SHALL NOT be returned as success;
- the accepted rollback path SHALL be attempted;
- no automatic retry SHALL occur.

AD-050 distinguishes database transaction atomicity from caller-visible outcome certainty.

A client-side or connection failure during final commit MAY prevent the caller from proving whether PostgreSQL accepted the commit before the failure became observable.

Therefore a commit exception SHALL NOT automatically be interpreted as proof that nothing was committed.

Rollback after a commit exception SHALL NOT be represented as proof that a previously completed server-side commit was reversed.

Automatic retry of a commit-failed coordinated operation is prohibited by AD-050.

Retry and reconciliation policy remain separately governed.

## Rollback Semantics

If a failure occurs before successful commit, including:

- Knowledge persistence failure;
- lineage persistence failure;
- translated duplicate conflict;
- unrelated integrity failure;
- application operation failure;
- flush failure;
- final commit failure;

the coordinator SHALL attempt one rollback of the shared transaction.

If rollback succeeds, the original failure SHALL propagate except where a repository duplicate has already been translated through its accepted contract.

If rollback itself fails, the rollback failure SHALL NOT be suppressed.

Rollback failure SHALL preserve causal linkage to the failure that triggered rollback.

Transaction-scoped repository participants SHALL NOT independently rollback.

## Session Cleanup Semantics

The coordinator SHALL attempt to close the acquired shared session exactly once after the transaction success or failure path.

During cleanup, PlantMind SHALL NOT explicitly invoke a second commit or second rollback.

Session close SHALL NOT be used as a second PlantMind transaction-decision mechanism.

SQLAlchemy, the database driver or the connection pool MAY perform internal implementation-level cleanup required by their own lifecycle semantics.

AD-050 SHALL NOT represent such internal cleanup as a new PlantMind transaction decision.

## Post-Commit Cleanup Failure

AD-050 SHALL establish the persistence-neutral coordination error:

`KnowledgeLineageTransactionPostCommitCleanupError`

This error applies only when:

1. final database commit completed successfully; and
2. subsequent coordinator-owned session cleanup fails.

Its meaning is explicit:

the coordinated database transaction committed successfully, but cleanup failed afterward.

A caller SHALL NOT interpret this error as evidence that the transaction rolled back.

Automatic retry solely because of this error is prohibited.

If an existing transaction or rollback failure is already primary and cleanup also fails, cleanup failure SHALL NOT replace or misrepresent the primary transaction outcome.

Diagnostic causal information about cleanup failure SHALL be preserved where technically possible.

## DatabaseRuntime Boundary

Canonical `DatabaseRuntime` SHALL remain responsible for:

- SQLAlchemy engine creation;
- canonical session-factory creation;
- engine disposal;
- database configuration lifecycle.

The SQLAlchemy coordinator SHALL receive an injected synchronous session factory.

It SHALL NOT:

- create another engine;
- construct another `DatabaseRuntime`;
- read `DATABASE_URL` directly;
- dispose the canonical engine;
- redefine database configuration;
- redefine database lifecycle ownership.

## Knowledge Capture Compatibility

AD-050 SHALL NOT modify the responsibilities or public behavior of:

`KnowledgeCaptureApplicationService`

That application service SHALL remain dependent on:

`KnowledgeRecordRepository`

A future accepted application capability MAY use `KnowledgeCaptureApplicationService` inside an AD-050 coordinated operation by supplying the transaction-scoped `KnowledgeRecordRepository`.

The coordinator SHALL NOT:

- generate Knowledge identity;
- generate capture timestamps;
- construct Knowledge provenance;
- construct Knowledge subject;
- automatically invoke Knowledge Capture;
- become a Knowledge factory.

Knowledge construction and capture semantics remain owned by the accepted Knowledge Capture application boundary.

## Enterprise Document Registration Preservation

AD-050 SHALL NOT modify:

`EnterpriseDocumentRegistrationApplicationService`

AD-050 SHALL NOT establish a transaction spanning:

- Enterprise Document registration;
- Knowledge capture;
- lineage persistence.

Any future transaction spanning those separate application use cases requires separate architecture evidence and acceptance.

## Persistence Ordering

AD-050 SHALL NOT impose a business-level ordering rule between Knowledge and lineage persistence.

A future application operation determines the order in which it invokes the transaction-scoped repositories.

Infrastructure transaction atomicity SHALL remain valid regardless of participant invocation order.

Any future use-case requirement that Knowledge must be constructed before lineage is an application concern rather than a database transaction rule.

## Synchronous and Concurrency Boundary

AD-050 establishes synchronous transaction coordination consistent with the accepted synchronous SQLAlchemy runtime.

It SHALL NOT establish:

- `AsyncSession`;
- asynchronous transaction coordination;
- concurrent use of one shared session by multiple threads or tasks;
- cross-thread transaction-scoped repository use.

Separate invocations MAY execute concurrently only when each invocation owns completely independent session and transaction state.

## External Side-Effect Boundary

AD-050 atomicity applies only to relational work participating in the same canonical PostgreSQL transaction.

It SHALL NOT claim atomicity for:

- file-system writes;
- binary document storage;
- network calls;
- PI / DCS / OPC UA operations;
- other databases;
- events or message publication;
- HTTP calls;
- parser execution;
- OCR;
- vector persistence;
- graph persistence;
- LLM invocation;
- any other non-participating external system.

Pure in-memory construction may occur inside the supplied operation.

Non-transactional external work SHALL NOT be treated as rollback-protected merely because it occurs inside the callback.

AD-050 does not introduce distributed transactions, outbox semantics or external compensation.

## Compensation Boundary

Because current Knowledge and lineage relational persistence can participate in the same canonical PostgreSQL transaction, AD-050 SHALL prefer database rollback over application compensation.

Application compensation SHALL NOT substitute for relational transaction atomicity.

Cross-system compensation remains outside scope.

## Retry and Idempotency Boundary

AD-050 SHALL NOT automatically retry:

- duplicate failures;
- integrity failures;
- operational database failures;
- deadlocks;
- commit failures;
- rollback failures;
- cleanup failures.

Application retry, reconciliation and idempotency remain separately governed.

No hidden retry loop is authorized.

## Relational Schema and Alembic Boundary

AD-050 SHALL NOT introduce:

- a new relational table;
- new canonical columns;
- new canonical constraints;
- relational foreign keys;
- a second SQLAlchemy metadata root.

Canonical tables remain unchanged:

- `knowledge_records`;
- `document_knowledge_lineages`;
- `enterprise_documents`.

No new Alembic revision is required by this decision.

Canonical Alembic head remains:

`0004`

Any newly discovered schema requirement SHALL stop technical implementation and require explicit architecture review before migration authorization.

## SQLAlchemy Infrastructure Boundary

The expected SQLAlchemy implementation namespace is:

`app.infrastructure.knowledge_lineage_transaction`

Expected minimum surface:

- `backend/app/infrastructure/knowledge_lineage_transaction/__init__.py`;
- `backend/app/infrastructure/knowledge_lineage_transaction/coordinator.py`;
- narrowly scoped transaction-scoped repository participant implementation.

The infrastructure package initializer SHALL remain empty unless a separately reviewed public API is required.

Accepted Knowledge and lineage mappings and canonical SQLAlchemy metadata SHALL be reused.

## Composition Boundary

AD-050 SHALL NOT automatically modify default:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`.

The existence of a transaction coordinator does not itself make PostgreSQL or coordinated persistence a mandatory default platform capability.

Production composition requires a separately accepted application capability that explicitly needs coordinated persistence.

## Runtime and Bootstrap Boundary

AD-050 SHALL NOT modify:

- Runtime lifecycle authority;
- Bootstrap authority;
- Operational Transition authority;
- readiness semantics;
- request-admission semantics;
- mandatory-capability policy;
- database availability policy.

No database startup dependency is introduced merely by this foundation.

## Security Boundary

AD-050 does not establish or claim:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- Data Permission Layer;
- actor audit;
- Cybersecurity approval;
- production security readiness.

Transaction atomicity is not an authorization mechanism.

## Explicitly Deferred

AD-050 SHALL NOT establish:

- Document-to-Knowledge ingestion;
- Document Library;
- binary document storage;
- file upload;
- parsing;
- OCR;
- chunking;
- Document revision lifecycle;
- source verification;
- Document approval or trust state;
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
- production-readiness claims.

## Alternatives Considered

### Implement Document-to-Knowledge ingestion now

Rejected.

The unresolved transaction boundary must be established before an ingestion use case can safely require Knowledge and lineage persistence together.

### Convert the existing standalone repositories into optional transaction owners

Rejected.

Allowing the same repository instance to sometimes own and sometimes not own commit, rollback and close would create ambiguous transaction ownership and weaken existing accepted standalone semantics.

### Introduce a generic platform-wide Unit of Work

Rejected.

Current evidence requires coordination only between Knowledge persistence and Document-to-Knowledge lineage persistence.

A generic transaction framework would exceed the demonstrated architectural need.

### Use application compensation instead of one PostgreSQL transaction

Rejected.

Both relational writes can participate in one canonical PostgreSQL transaction.

Compensation would introduce unnecessary partial-state and recovery complexity.

### Add relational foreign keys as part of transaction coordination

Rejected.

Cross-domain relational referential-integrity policy remains separately governed and is not required for transaction atomicity.

### Wire the coordinator into default Composition immediately

Rejected.

An infrastructure capability does not itself establish a default application dependency or mandatory database Runtime capability.

## Acceptance Requirements

Before AD-050 may become Accepted, architecture review SHALL confirm:

1. no new ARCH-001 architectural layer is introduced;
2. application-level responsibility does not compete with `ApplicationFacade`;
3. the coordinator contract remains persistence-neutral;
4. Domain and repository contracts remain unchanged;
5. the narrow Infrastructure dependency on the coordinator contract is explicitly contained by AD-050;
6. no general Infrastructure-to-Application dependency rule is created;
7. one coordinated execution owns exactly one session and one transaction scope;
8. transaction-scoped repositories share the exact same session;
9. final commit authority exists only in the coordinator;
10. rollback authority exists only in the coordinator;
11. session-close authority exists only in the coordinator;
12. transaction-scoped repositories flush but do not commit, rollback or close;
13. transaction-scoped reads preserve accepted repository semantics;
14. standalone repository transaction ownership remains unchanged;
15. Knowledge duplicate classification remains exact and constraint-aware;
16. lineage duplicate classification remains exact and constraint-aware;
17. standalone and coordinated duplicate-classification rules cannot drift independently;
18. commit-time failures are not heuristically misclassified;
19. commit uncertainty is not falsely represented as proof of rollback;
20. post-commit cleanup failure has explicit committed-outcome semantics;
21. transaction atomicity is distinguished from application-use-case completeness;
22. `KnowledgeCaptureApplicationService` remains unchanged and reusable;
23. `EnterpriseDocumentRegistrationApplicationService` remains unchanged;
24. canonical `DatabaseRuntime` lifecycle ownership remains unchanged;
25. no schema or Alembic revision is required;
26. canonical Alembic head remains `0004`;
27. default Composition remains unchanged;
28. Runtime and Bootstrap authority remain unchanged;
29. synchronous shared-session behavior is explicit;
30. PostgreSQL transaction atomicity is not falsely extended to external side effects;
31. all ingestion, Library, search, AI, security and deployment capabilities listed as deferred remain outside scope.

## Contract Acceptance Review

Outcome:

**PASS — AD-050 accepted.**

The final formal review confirmed that the recorded AD-050 decision is materially consistent with the reviewed RFC-064 architecture contract and current authoritative architecture.

The review was performed against:

- ARCH-001;
- CORE-002;
- CORE-003;
- AD-027 application-boundary semantics;
- AD-039 through AD-049;
- canonical Knowledge and lineage repository contracts;
- current standalone SQLAlchemy transaction ownership;
- canonical `DatabaseRuntime` authority;
- canonical metadata and Alembic authority;
- `KnowledgeCaptureApplicationService`;
- `EnterpriseDocumentRegistrationApplicationService`;
- default Composition;
- Runtime and Bootstrap authority.

All 31 AD-050 Acceptance Requirements are satisfied.

No unresolved architecture divergence requires further contract refinement before the implementation-entry Git gate.

The accepted decision preserves the narrow transaction-coordination responsibility and all explicitly deferred higher-level capabilities.

## Implementation Authorization

Status:

**Satisfied — Technical implementation completed and verified.**

The accepted RFC-064 / AD-050 contract was committed at:

`7f63e0262a1dc9c3f22466ae64d4c2235b74855c`

The implementation-entry Git gate was satisfied after:

1. the accepted contract was committed;
2. the contract commit was pushed to `origin/feature/engineering-platform`;
3. exact local / remote contract identity was verified;
4. the working tree was verified clean.

RFC-064 technical implementation was subsequently completed and committed at:

`f62179a621f1289b47833b6057661a631e5357be`

Exact local / remote technical implementation identity was verified after push.

## Post-Implementation Verification

Outcome:

**PASS — implementation conforms to AD-050.**

Verified evidence:

- RFC-064 targeted verification: 37 passed;
- full PlantMind regression: 754 passed;
- Python compileall: passed;
- `git diff --check`: passed;
- canonical Alembic head remains `0004`;
- no new schema or migration was introduced;
- one shared SQLAlchemy session is used per coordinated execution;
- transaction establishment occurs before the supplied operation;
- transaction-scoped Knowledge and lineage repositories share the exact session;
- scoped participants flush without independent commit / rollback / close ownership;
- coordinator owns final commit, rollback and session close;
- exact constraint-aware duplicate semantics remain preserved;
- standalone and coordinated duplicate paths share canonical classification rules;
- commit-time integrity failures are not heuristically reclassified;
- post-commit cleanup failure has explicit committed-outcome semantics;
- transaction failure is not masked by later cleanup failure;
- second-participant failure after first-participant flush enters one coordinated rollback path without partial-success reporting;
- canonical `DatabaseRuntime` ownership remains unchanged;
- default `CompositionRoot` remains unchanged;
- Runtime and Bootstrap authority remain unchanged;
- no new ARCH-001 architectural layer was introduced;
- Domain and Core do not depend on transaction infrastructure;
- transaction atomicity remains distinct from application-use-case completeness;
- no external-system atomicity, ingestion, Library, search, AI, security or production-readiness capability was introduced.

AD-050 therefore remains:

**Accepted**

and its authorized RFC-064 technical implementation is verified as conforming to the decision.

## Engineering Closure State

RFC-064 engineering-memory and architecture closure is complete.

Closure commit:

`43563a416a24fea7cad4a370a2a4599936c87380`

Exact local / remote closure identity was verified.

Working tree after closure push was clean.

AD-050 remains Accepted and RFC-064 is fully closed.

## Next Exact Action

Perform evidence-based selection of the next architecture workstream.

No RFC-065 content is assumed or preselected by AD-050 or RFC-064 closure.

Any next workstream SHALL be selected from current repository, project-charter and architecture evidence and SHALL require its own reviewed and accepted contract before technical implementation is authorized.

---

# AD-051 — Canonical Document-to-Knowledge Ingestion Application Boundary## Status

Accepted.

RFC-065 / AD-051 Contract Acceptance Review: passed.

Implementation-entry Git gate: satisfied.

Technical implementation completed and verified at:

`c1ab20b693ac90782592961d91dafda8e0782fa1`

Engineering-memory and architecture closure was committed and pushed at:

`cc99e2d0358f1ea7263789aac66747322a62d1f2`

Exact local / remote closure identity was verified.

Working tree after closure push was clean.

RFC-065 is fully closed.

Post-closure Source-of-Truth reconciliation is in progress.

## Context

AD-039 through AD-042 established canonical enterprise Knowledge,
relational Knowledge persistence and the specialized
`KnowledgeCaptureApplicationService`.

AD-043 through AD-046 established canonical immutable
`EnterpriseDocument`, its persistence-neutral repository, relational
persistence and the specialized
`EnterpriseDocumentRegistrationApplicationService`.

AD-047 through AD-049 established canonical directed
Document-to-Knowledge lineage, its repository contract and relational
persistence.

AD-050 / RFC-064 established the narrow persistence-neutral
`KnowledgeLineageTransactionCoordinator` required for canonical
Knowledge persistence and lineage persistence to participate in one
coordinated relational transaction.

Earlier Document Knowledge ingestion was intentionally deferred because
the platform previously lacked:

1. canonical Document identity;
2. canonical lineage identity;
3. lineage persistence;
4. coordinated Knowledge / lineage transaction semantics.

Those prerequisite foundations now exist.

PlantMind therefore has sufficient canonical lower-level architecture to
review one specialized application use case for creating Knowledge
derived from an already registered canonical Enterprise Document.

## Decision

PlantMind SHALL establish one specialized internal application boundary:

`DocumentKnowledgeIngestionApplicationService`

under:

`app.services.document_knowledge_ingestion_application_service`

with immutable application contracts:

- `DocumentKnowledgeIngestionRequest`;
- `DocumentKnowledgeIngestionResult`.

The canonical operation SHALL be:

`ingest(request: DocumentKnowledgeIngestionRequest) -> DocumentKnowledgeIngestionResult`

RFC-065 ingestion represents creation of one canonical Knowledge record
derived from one existing canonical Enterprise Document and creation of
the corresponding canonical `DocumentKnowledgeLineage`.

RFC-065 is not raw-file ingestion, parsing, Library behavior or AI
reasoning.

## Application-Level Responsibility

The term `application` describes use-case responsibility only.

AD-051 SHALL NOT introduce a seventh architectural layer.

The six-layer architecture defined by ARCH-001 remains unchanged.

The ingestion boundary is an internal specialized application use case.

It SHALL NOT become:

- the canonical external workload entry point;
- a Presentation component;
- an AI Agent;
- an Intelligence Engine;
- a Core Service;
- a generic orchestration layer;
- a generic Unit of Work.

AD-051 narrowly governs only the dependencies required by this accepted
use case and SHALL NOT establish a general dependency exception for
unrelated PlantMind components.

## ApplicationFacade Boundary

AD-027 remains authoritative.

`ApplicationFacade` remains the canonical application-level production
operational workload entry boundary.

`DocumentKnowledgeIngestionApplicationService` SHALL NOT compete with
`ApplicationFacade`.

AD-051 SHALL NOT modify:

- `ApplicationFacade`;
- `IntegrationGateway`;
- `OrchestrationService`;
- `WorkflowExecutor`.

AD-051 introduces no external transport or production workload-entry
path.

Any future production external exposure of ingestion requires separately
accepted transport, composition and security architecture consistent
with AD-027.

## Construction and Dependency Contract

`DocumentKnowledgeIngestionApplicationService` SHALL receive exactly
these application-level constructor dependencies:

- `document_repository: EnterpriseDocumentRepository`;
- `transaction_coordinator: KnowledgeLineageTransactionCoordinator`;
- optional `knowledge_capture_factory`.

The optional factory contract SHALL be equivalent to:

`Callable[[KnowledgeRecordRepository], KnowledgeCaptureApplicationService]`

When no factory is supplied, the ingestion service SHALL use a local
default factory that constructs:

`KnowledgeCaptureApplicationService(repository=scoped_knowledge_repository)`

without overriding the identity-source or capture-time defaults accepted
by AD-042.

For each ingestion invocation that resolves an existing canonical
Document, exactly one Knowledge Capture service SHALL be constructed
inside the RFC-064 coordinated operation after the transaction-scoped
repositories have been supplied.

The factory SHALL receive the exact transaction-scoped
`KnowledgeRecordRepository` supplied by RFC-064.

The ingestion-service constructor SHALL NOT accept a preconstructed
`KnowledgeCaptureApplicationService`.

A preconstructed Capture service would bind its repository before the
RFC-064 transaction scope exists and could therefore violate the
required atomic Knowledge / lineage persistence boundary.

The optional factory exists solely as a narrow deterministic
verification seam.

It SHALL NOT:

- perform persistence;
- own transaction lifecycle;
- perform external I/O;
- resolve dependencies globally;
- register services;
- become a provider registry;
- become a Core Service;
- become a dependency-injection framework.

## Canonical Application Input

`DocumentKnowledgeIngestionRequest` SHALL be immutable, keyword-only and
contain:

- `document_id: EntityId`;
- `kind: str`;
- `title: str`;
- `content: str`;
- `subject: KnowledgeCaptureSubject | None = None`.

Caller input SHALL NOT provide:

- Knowledge identity;
- Knowledge capture timestamp;
- Document source type;
- Document source reference;
- preconstructed `KnowledgeRecord`;
- preconstructed `DocumentKnowledgeLineage`.

## Canonical Result

`DocumentKnowledgeIngestionResult` SHALL be immutable, keyword-only and
contain exactly:

- `knowledge_record: KnowledgeRecord`;
- `lineage: DocumentKnowledgeLineage`.

The result SHALL be returned only after the RFC-064 coordinator reports
successful completion.

The result does not imply trust, approval, authorization, indexing,
searchability, RAG availability or production readiness.

## Existing Document Requirement

RFC-065 SHALL operate only on an already registered canonical
`EnterpriseDocument`.

The ingestion boundary SHALL NOT register, create, update or delete a
Document.

`EnterpriseDocumentRepository` SHALL be injected explicitly.

For one ingestion invocation, the application boundary SHALL call:

`EnterpriseDocumentRepository.get(request.document_id)`

exactly once before entering coordinated Knowledge / lineage
persistence.

No source-reference lookup or alternate Document identity is authorized.

## Document Not-Found Semantics

RFC-065 SHALL introduce the specialized application error:

`DocumentKnowledgeIngestionDocumentNotFoundError`

If Document lookup returns `None`, this error SHALL be raised before
transaction coordination begins.

For Document not-found:

- `KnowledgeLineageTransactionCoordinator.execute(...)` SHALL NOT run;
- Knowledge Capture SHALL NOT run;
- no Knowledge identity SHALL be generated;
- no capture timestamp SHALL be generated;
- no Knowledge write SHALL occur;
- no lineage write SHALL occur.

Unexpected Document repository failures SHALL propagate without
conversion to not-found, retry or synthetic success.

## Document Lookup Transaction Boundary

Document lookup SHALL occur before the RFC-064 Knowledge / lineage
transaction.

The accepted Enterprise Document is immutable and current architecture
provides no update, delete or mutable revision lifecycle.

AD-051 SHALL NOT extend `KnowledgeLineageTransactionCoordinator` to
include `EnterpriseDocumentRepository`.

AD-051 SHALL NOT establish one transaction spanning:

- Document registration;
- Knowledge capture;
- lineage persistence.

Future accepted Document mutation, deletion, replacement or revision
semantics SHALL require explicit review of this assumption before
changing ingestion behavior.

## Canonical Document Identity

Canonical derivation identity SHALL be:

`EnterpriseDocument.id`

Canonical lineage SHALL use this identity directly.

`DocumentSource.source_reference` remains external source traceability
only.

It SHALL NOT become:

- canonical Document identity;
- lineage identity;
- repository alternate identity;
- uniqueness identity;
- deduplication identity.

Canonical Document identity SHALL NOT be encoded into
`KnowledgeProvenance.source_reference`.

## Provenance Derivation

Knowledge provenance input SHALL be derived from the loaded canonical
Document source.

The ingestion boundary SHALL supply Knowledge Capture with:

- `source_type = document.source.source_type.value`;
- `source_reference = document.source.source_reference`.

Caller-provided provenance source metadata is not authorized by
RFC-065.

`KnowledgeCaptureApplicationService` remains responsible for canonical
Knowledge provenance construction and capture-time generation.

Canonical Document lineage and external-source provenance remain
separate concepts.

## Knowledge Subject Boundary

Document derivation SHALL NOT automatically replace the canonical
Knowledge subject.

The ingestion request MAY carry the already accepted
`KnowledgeCaptureSubject`.

RFC-065 SHALL pass that subject through accepted Knowledge Capture
semantics.

RFC-065 SHALL NOT establish:

- subject existence validation;
- subject accessibility validation;
- automatic Document-as-subject behavior;
- Asset Library resolution;
- new subject-type semantics.

## Knowledge Capture Preservation

AD-042 remains authoritative.

RFC-065 SHALL consume:

`KnowledgeCaptureApplicationService`

It SHALL NOT bypass Knowledge Capture by directly constructing a
canonical `KnowledgeRecord` as application logic or directly persisting
Knowledge through `KnowledgeRecordRepository.add(...)`.

Knowledge Capture retains ownership of:

- canonical Knowledge identity creation;
- canonical capture-time generation;
- canonical Knowledge domain construction;
- canonical provenance construction;
- canonical subject construction.

The public behavior and accepted responsibilities of
`KnowledgeCaptureApplicationService` SHALL remain unchanged.

## Transaction-Scoped Knowledge Capture Binding

RFC-064 provides a transaction-scoped `KnowledgeRecordRepository`.

RFC-065 SHALL use `KnowledgeCaptureApplicationService` bound to that
exact scoped repository inside the coordinated operation.

AD-051 SHALL use the Construction and Dependency Contract defined
above.

The capture-service factory SHALL be invoked exactly once inside the
coordinated operation and SHALL receive the exact transaction-scoped
Knowledge repository supplied by RFC-064.

RFC-065 SHALL NOT accept or reuse a preconstructed
`KnowledgeCaptureApplicationService`.

Default behavior SHALL preserve the accepted Knowledge Capture identity
and UTC capture-time semantics.

## Coordinated Transaction Boundary

For an existing Document, RFC-065 SHALL invoke:

`KnowledgeLineageTransactionCoordinator.execute(...)`

exactly once.

The supplied operation SHALL receive and use exactly the
transaction-scoped:

- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`

provided by RFC-064.

RFC-065 SHALL NOT directly own:

- SQLAlchemy Session;
- transaction primitives;
- commit;
- rollback;
- session close;
- engine;
- session factory.

RFC-064 / AD-050 remains authoritative for transaction lifecycle and
failure semantics.

## Persistence Ordering

Inside the coordinated operation, RFC-065 SHALL:

1. prepare one `KnowledgeCaptureRequest`;
2. invoke `KnowledgeCaptureApplicationService.capture(...)` exactly once;
3. obtain the resulting canonical `KnowledgeRecord`;
4. construct one canonical `DocumentKnowledgeLineage`;
5. call transaction-scoped lineage repository `add(...)` exactly once;
6. return one `DocumentKnowledgeIngestionResult` to the coordinator.

Knowledge Capture SHALL precede lineage construction because canonical
Knowledge identity is generated by Knowledge Capture.

This ordering does not transfer commit, rollback or session ownership
from RFC-064.

## Lineage Construction

The canonical lineage SHALL contain exactly:

- `document_id = enterprise_document.id`;
- `knowledge_record_id = knowledge_record.id`.

RFC-065 SHALL NOT introduce:

- lineage surrogate identity;
- lineage timestamp;
- lineage type;
- foreign-key lifecycle coupling;
- new lineage cardinality rules;
- primary-source semantics;
- corroboration;
- merge semantics;
- multi-source derivation.

## Success Semantics

RFC-065 SHALL report success only when
`KnowledgeLineageTransactionCoordinator.execute(...)` successfully
returns after coordinated commit.

Knowledge construction or flush alone is not successful ingestion.

Lineage construction or flush alone is not successful ingestion.

No partial-success result is authorized.

## Knowledge Failure Semantics

If Knowledge Capture fails:

- the failure SHALL propagate;
- lineage persistence SHALL not report success;
- RFC-065 SHALL not retry;
- RFC-065 SHALL not fabricate a result;
- coordinator-owned rollback semantics remain authoritative when a
  transaction is active.

Canonical Knowledge duplicate errors SHALL propagate unchanged.

## Lineage Failure Semantics

If lineage persistence fails after Knowledge has been added or flushed:

- the failure SHALL propagate;
- RFC-065 SHALL not return partial success;
- RFC-065 SHALL not manually compensate;
- RFC-065 SHALL not commit or rollback;
- RFC-064 coordinator behavior remains authoritative.

Canonical lineage duplicate errors SHALL propagate unchanged.

## Unexpected Failure Semantics

RFC-065 SHALL preserve unexpected Domain, repository, transaction and
persistence failures unless another accepted contract defines narrower
semantics.

It SHALL NOT:

- heuristically classify unrelated integrity failures as duplicates;
- regenerate Knowledge identity automatically;
- retry automatically;
- overwrite canonical records;
- convert failures into synthetic success.

## Post-Commit Cleanup Failure

`KnowledgeLineageTransactionPostCommitCleanupError` retains its accepted
AD-050 meaning.

RFC-065 SHALL not translate this outcome into an exception that falsely
claims rollback.

When this exception occurs, participating relational persistence may
already be committed.

RFC-065 SHALL not automatically retry after this outcome.

## Duplicate and Idempotency Boundary

RFC-065 introduces no new ingestion-level duplicate definition.

Existing canonical duplicate behavior remains authoritative.

Repeated ingestion from the same Document is not automatically a
duplicate because no accepted one-Knowledge-record-per-Document
cardinality exists.

Equal external source references do not establish duplicate ingestion.

RFC-065 introduces no idempotency key, content hash, deduplication
algorithm or retry policy.

Those require future explicit architecture if needed.

## Repository Preservation

AD-051 SHALL NOT change the public contracts of:

- `EnterpriseDocumentRepository`;
- `KnowledgeRecordRepository`;
- `DocumentKnowledgeLineageRepository`.

No ingestion-specific repository methods are authorized.

Standalone relational repository behavior remains unchanged.

RFC-064 transaction-scoped repository behavior remains unchanged.

## DatabaseRuntime Boundary

Canonical `DatabaseRuntime` remains sole owner of:

- SQLAlchemy engine;
- session factory;
- database configuration;
- database lifecycle.

RFC-065 SHALL NOT create another engine, session factory,
`DatabaseRuntime`, metadata root or database configuration source.

## Relational Schema and Alembic Boundary

RFC-065 SHALL introduce no relational schema change under the current
contract.

No new:

- table;
- column;
- constraint;
- index;
- relational foreign key;
- metadata root;
- Alembic revision

is required.

Canonical Alembic head remains:

`0004`

Discovery of a genuine schema requirement during technical review SHALL
stop implementation and require explicit architecture review before
migration authorization.

## Composition Boundary

AD-051 SHALL NOT automatically modify default:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`.

Existence of RFC-065 does not make PostgreSQL or Document / Knowledge
persistence a mandatory default platform capability.

Production composition remains separately governed.

## Runtime and Bootstrap Boundary

RFC-065 SHALL NOT modify:

- Runtime lifecycle authority;
- Bootstrap authority;
- readiness;
- Health;
- request admission;
- operational-transition authority;
- mandatory-capability policy.

Successful ingestion SHALL NOT itself change Runtime lifecycle state.

## Parsing and Document Library Boundary

RFC-065 ingests prepared Knowledge associated with an already registered
canonical Document.

It does not ingest or process raw files.

Caller-supplied Knowledge content is already prepared for Knowledge
Capture.

RFC-065 SHALL NOT implement:

- Document Library;
- binary storage;
- upload;
- download;
- file synchronization;
- PDF parsing;
- OCR;
- text extraction;
- chunking;
- metadata extraction;
- revision tracking.

Future parsing and extraction capabilities MAY consume RFC-065 only
after their own contracts are accepted.

## Search and AI Boundary

RFC-065 SHALL NOT establish:

- search;
- semantic retrieval;
- embeddings;
- vector persistence;
- graph persistence;
- Neo4j;
- Knowledge Graph redesign;
- RAG;
- LLM invocation;
- AI Agent behavior;
- engineering reasoning.

Canonical ingestion success does not imply searchability or AI
availability.

## Core Boundary

RFC-065 is not a Core Service.

Core Services SHALL NOT acquire ingestion workflow responsibility.

CORE-002 remains authoritative.

## Dependency Boundary

RFC-065 implementation SHALL depend on accepted contracts and public
application boundaries.

It SHALL NOT depend directly on SQLAlchemy or external systems.

Dependencies SHALL remain explicit and acyclic.

ARCH-001, CORE-002 and CORE-003 remain authoritative except only for the
narrow responsibility explicitly governed by this ADR.

AD-051 SHALL NOT establish a general reverse-dependency or layer-bypass
rule.

## Security and Trust Boundary

RFC-065 SHALL NOT establish or claim:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- LDAP;
- MFA;
- actor identity;
- actor audit;
- source authenticity;
- source correctness;
- Document trust;
- Knowledge trust;
- approval;
- safety approval;
- compliance approval;
- Cybersecurity approval;
- production-security readiness.

Provenance records traceable origin.

Lineage records derivation identity.

Neither establishes trust or authorization.

## Explicitly Deferred

AD-051 SHALL NOT establish:

- Document creation or registration during ingestion;
- Document mutation;
- Document deletion;
- Document revision or supersession lifecycle;
- Document Library;
- binary storage;
- upload or download;
- source synchronization;
- parsing;
- OCR;
- extraction;
- chunking;
- search;
- embeddings;
- vector persistence;
- graph persistence;
- Neo4j;
- RAG;
- LLM invocation;
- AI Agent behavior;
- HTTP transport;
- API endpoint creation;
- PI System integration;
- DCS integration;
- external-system transaction atomicity;
- source verification;
- approval lifecycle;
- lineage traversal APIs;
- lineage cardinality policy;
- corroboration;
- primary-source semantics;
- multi-source derivation;
- ingestion-level deduplication;
- ingestion-level idempotency;
- automatic retry;
- savepoints;
- nested transactions;
- distributed transactions;
- two-phase commit;
- transactional event publication;
- outbox semantics;
- asynchronous coordination;
- default production composition;
- authentication or authorization expansion;
- production-readiness claims.

## Alternatives Considered

### Bypass Knowledge Capture and construct Knowledge directly

Rejected.

AD-042 explicitly established Knowledge Capture as the specialized
application boundary that future ingestion capabilities shall consume.

Bypassing it would duplicate identity, timestamp, provenance, subject
and Domain-construction responsibilities.

### Use Document source_reference as Document identity

Rejected.

AD-043 through AD-047 explicitly separate source traceability from
canonical Document identity.

Canonical lineage shall use `EnterpriseDocument.id`.

### Allow caller-supplied provenance source metadata

Rejected.

The ingestion use case already identifies one canonical Document.

Deriving provenance source metadata from that canonical Document avoids
caller disagreement between Document identity and external source
traceability.

### Put Document lookup inside the RFC-064 transaction

Rejected under current architecture.

RFC-064 intentionally coordinates only Knowledge and lineage
persistence.

Enterprise Documents are currently immutable and have no delete or
mutable revision lifecycle.

Extending the coordinator would exceed demonstrated need.

### Include Document Registration in the transaction

Rejected.

AD-050 explicitly excludes a transaction spanning Document Registration,
Knowledge Capture and lineage persistence.

RFC-065 consumes an already existing canonical Document.

### Add a generic application Unit of Work

Rejected.

RFC-064 already provides the narrow coordination required by this use
case.

A generic Unit of Work would exceed evidence.

### Add parsing, OCR or chunking to RFC-065

Rejected.

RFC-065 consumes prepared Knowledge fields.

Raw-file transformation is a separate responsibility and future
workstream.

### Add idempotency or content deduplication now

Rejected.

No accepted business identity exists for duplicate Document-derived
Knowledge beyond canonical record and lineage identities.

Such semantics require separate evidence and contract.

## Acceptance Requirements

Before AD-051 may become Accepted, architecture review SHALL confirm:

1. no new ARCH-001 layer is introduced;
2. `ApplicationFacade` remains production workload-entry authority;
3. ingestion remains an internal specialized application use case;
4. ingestion begins from existing canonical `EnterpriseDocument.id`;
5. Document lookup uses `EnterpriseDocumentRepository.get(...)`;
6. Document lookup occurs exactly once before coordination;
7. Document not-found prevents all coordinated persistence;
8. source-reference identity or lookup is not introduced;
9. provenance source data derives from canonical Document source;
10. Document identity is not hidden inside provenance;
11. Knowledge subject remains independent from Document lineage;
12. Knowledge Capture is consumed rather than bypassed;
13. Knowledge Capture public behavior remains unchanged;
14. Knowledge identity remains owned by Knowledge Capture;
15. capture timestamp remains owned by Knowledge Capture;
16. exactly one Knowledge Capture service is constructed inside the
    coordinated operation through the narrow factory using the exact
    transaction-scoped Knowledge repository, and no preconstructed
    Knowledge Capture service is accepted;
17. coordinator execution occurs exactly once for an existing Document;
18. Knowledge Capture occurs exactly once inside the operation;
19. one lineage value is constructed from exact canonical identities;
20. lineage `add(...)` occurs exactly once;
21. no Knowledge or lineage duplicate pre-read is introduced;
22. success occurs only after coordinated commit;
23. no partial-success result is possible;
24. Knowledge failure prevents lineage success;
25. lineage failure uses RFC-064 rollback authority;
26. duplicate semantics remain exact and unchanged;
27. unrelated failures are not heuristically reclassified;
28. post-commit cleanup semantics remain unchanged;
29. no automatic retry is introduced;
30. no ingestion-level idempotency or deduplication is introduced;
31. repository public contracts remain unchanged;
32. standalone repository lifecycle behavior remains unchanged;
33. RFC-064 scoped repository behavior remains unchanged;
34. `DatabaseRuntime` ownership remains unchanged;
35. no schema or migration change is required;
36. canonical Alembic head remains `0004`;
37. default Composition remains unchanged;
38. Runtime and Bootstrap remain unchanged;
39. no Document Registration transaction is introduced;
40. parsing, OCR, Library, search, vector, graph, RAG and LLM remain
    outside scope;
41. security, trust and production-readiness claims remain outside scope;
42. dependency direction remains explicit, acyclic and compatible with
    ARCH-001 / CORE-002 / CORE-003 and approved ADR authority.

## Contract Acceptance Review

Status:

**Passed — 42 / 42 Acceptance Requirements**

RFC-065 / AD-051 Contract Acceptance Review is complete.

Review evidence:

- Gate 1 — Dependency & Application-Boundary Compatibility: PASS;
- Gate 2 — Canonical Document Identity & Existence Semantics: PASS;
- Gate 3 — Provenance & Knowledge Subject Preservation: PASS;
- Gate 4 — Transaction, Atomicity & Failure Semantics: PASS;
- Gate 5 — Schema, Composition, Runtime, Bootstrap & Security Preservation: PASS;
- Final Static Contract Review: PASS.

Final requirement disposition:

- PASS: 42;
- REFINE: 0;
- BLOCKED: 0.

The review covered:

- ARCH-001;
- CORE-002;
- CORE-003;
- AD-027;
- AD-039 through AD-050;
- canonical Domain contracts;
- repository ports;
- application services;
- RFC-064 transaction coordination;
- default Composition;
- Runtime and Bootstrap authority;
- canonical relational metadata and Alembic authority;
- current security implementation boundaries.

AD-051 is Accepted.

Acceptance does not by itself authorize implementation.

The implementation-entry Git gate requires the accepted contract to be
committed, pushed, exact local / remote commit identity verified and the
working tree confirmed clean.

## Implementation Authorization

Status:

**Satisfied — Technical implementation completed and verified.**

Accepted architecture contract commit:

`3db01142802d98f82a565808b3137a3db64158ac`

Verified technical implementation commit:

`c1ab20b693ac90782592961d91dafda8e0782fa1`

The implementation-entry Git gate was satisfied before production-code
implementation began.

Technical verification evidence:

- RFC-065 targeted verification: **25 passed**;
- preservation verification: **66 passed**;
- full PlantMind regression: **779 passed**;
- Python compileall: passed;
- canonical Alembic head remains `0004`;
- local / remote technical commit identity: verified;
- working tree after technical push: clean.

RFC-065 technical implementation is accepted as implemented within the
AD-051 boundary.

Engineering-memory and architecture closure is complete.

Closure commit:

`cc99e2d0358f1ea7263789aac66747322a62d1f2`

Exact local / remote closure identity was verified.

RFC-065 is fully closed.

## Next Exact Action

Complete and verify RFC-065 post-closure Source-of-Truth reconciliation.

After reconciliation is committed, pushed and verified, perform
evidence-based selection of the next architecture workstream.

No RFC-066 content is assumed or preselected by AD-051.

No new RFC implementation is authorized until its architecture contract
is reviewed, accepted, committed, pushed and its implementation-entry
Git gate is satisfied.
