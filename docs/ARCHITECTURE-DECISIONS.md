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
