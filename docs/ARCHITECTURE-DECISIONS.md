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

# AD-051 — Canonical Document-to-Knowledge Ingestion Application Boundary

## Status

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

Post-closure Source-of-Truth reconciliation is complete and verified.

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

RFC-065 post-closure Source-of-Truth reconciliation is complete and
verified at:

`fe0d8bb82b4e3d22d1ad4e6191205fa05919d30b`

RFC-065 is fully closed and Source-of-Truth reconciled.

Evidence-based selection of the next architecture workstream is now
authorized.

No RFC-066 content is assumed or preselected by AD-051.

No new RFC implementation is authorized until its architecture contract
is reviewed, accepted, committed, pushed and its implementation-entry
Git gate is satisfied.
---

# AD-052 — Canonical Enterprise Document Content Foundation Boundary

## Status

Accepted.

RFC-066 formal architecture-contract review:

**Passed — 52 / 52 Acceptance Requirements**

Combined RFC-066 / AD-052 semantic-consistency review:

**Passed — 52 PASS / 0 REFINE / 0 BLOCKED**

AD-052 is Accepted.

The matching RFC-066 contract is Accepted.

Implementation authorization:

**SATISFIED — Technical implementation completed and verified**

Accepted architecture contract commit:

`fb277fe00a9e606192c795338ab5419f4b9db788`

Verified technical implementation commit:

`49080b6c1f6f0607e6ba04ba2476f222dea97155`

The implementation-entry Git gate was satisfied before RFC-066 TDD RED
implementation began.

Remote technical push and exact local / remote technical identity were
verified.

Full PlantMind regression after implementation: **840 passed**.

Engineering-memory and architecture closure remains pending.

## Context

RFC-057 / AD-043 established the immutable canonical
`EnterpriseDocument` with:

- canonical `EntityId`;
- `DocumentType`;
- title;
- `DocumentSource`.

RFC-058 through RFC-060 established persistence-neutral Document
repository semantics, relational Document persistence and the
Enterprise Document Registration application boundary.

RFC-061 through RFC-065 subsequently established canonical
Document-to-Knowledge lineage, lineage persistence, coordinated
Knowledge / lineage persistence and canonical Document-derived
Knowledge ingestion.

The current accepted Enterprise Document architecture intentionally
contains no:

- raw binary payload;
- textual payload;
- content-storage location;
- canonical content digest;
- content media type;
- content byte length;
- parser output;
- revision state.

`DocumentSource.source_reference` remains external traceability only.

It is not:

- canonical Document identity;
- canonical content identity;
- storage identity;
- storage location;
- repository alternate identity;
- uniqueness identity;
- deduplication identity.

PlantMind therefore requires a canonical persistence-neutral foundation
describing Document content before storage, acquisition, parsing,
extraction, indexing or AI capabilities may define their own content
semantics.

## Decision

PlantMind SHALL establish one new persistence-neutral Domain module:

`app.domain.document_content`

implemented at:

`backend/app/domain/document_content.py`

The canonical public surface SHALL contain exactly:

- `DocumentContentMediaType`;
- `DocumentContentDigest`;
- `DocumentContentDescriptor`.

AD-052 SHALL NOT modify the accepted RFC-057
`app.domain.document` contract.

AD-052 SHALL NOT introduce a new architectural layer.

AD-052 SHALL NOT introduce persistence, storage, parsing, Document
Library, search, AI or production-security behavior.

## Canonical Domain Representation

Document-content semantics SHALL be represented by immutable Domain
value contracts independent from the accepted `EnterpriseDocument`
class.

`EnterpriseDocument` SHALL NOT gain content fields.

The existing file:

`backend/app/domain/document.py`

SHALL remain unchanged by RFC-066 implementation.

The RFC-057 canonical Document class surface SHALL remain exactly:

- `DocumentType`;
- `DocumentSourceType`;
- `DocumentSource`;
- `EnterpriseDocument`.

## Canonical Content Identity

AD-052 SHALL NOT introduce an independent Document Content entity
identity.

There SHALL be no:

`DocumentContentId`

Document content SHALL NOT receive an independent `EntityId`.

The canonical association SHALL use the existing canonical:

`EnterpriseDocument.id`

`DocumentContentDescriptor` SHALL reference that identity through:

`document_id: EntityId`

The descriptor SHALL NOT inherit from `DomainEntity`.

It SHALL NOT generate or replace canonical identity.

The following SHALL NOT become Document Content identity:

- SHA-256 digest;
- media type;
- byte length;
- `DocumentSource.source_reference`.

## Canonical Cardinality

Under the current immutable and revision-neutral Enterprise Document
architecture, the canonical Domain relationship SHALL be:

`EnterpriseDocument.id -> zero-or-one DocumentContentDescriptor`

An Enterprise Document MAY exist without canonical content.

Absence of content SHALL NOT invalidate an already registered canonical
Enterprise Document.

AD-052 SHALL NOT establish:

- multiple independent content artifacts for one Document;
- attachment semantics;
- alternate rendition semantics;
- revision-specific content multiplicity.

This cardinality is a Domain architecture rule.

AD-052 introduces no persistence mechanism that enforces the rule.

A future repository/store architecture SHALL explicitly preserve or
review this cardinality.

## Canonical DocumentContentMediaType

`DocumentContentMediaType` SHALL be an immutable keyword-only value
object containing exactly:

`value: str`

Construction SHALL:

1. require a string;
2. trim surrounding whitespace;
3. lowercase the value;
4. reject an empty value;
5. reject media-type parameters containing `;`;
6. require exactly one `/`;
7. require a non-empty type component;
8. require a non-empty subtype component;
9. reject ASCII whitespace inside the normalized media type.

Examples include:

- `application/pdf`;
- `text/plain`;
- `image/png`;
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.

AD-052 SHALL NOT perform full IANA registry validation.

Unknown but structurally valid media types MAY remain representable.

Media-type parameters and character-set parameters are outside AD-052.

## Character-Encoding Boundary

Character encoding SHALL NOT be part of the canonical RFC-066 content
descriptor.

Encoding detection, declaration, conversion and normalization remain
future parsing/extraction responsibilities.

## Canonical DocumentContentDigest

`DocumentContentDigest` SHALL be an immutable keyword-only value object
containing exactly:

`value: str`

The algorithm fixed by AD-052 SHALL be:

`SHA-256`

Construction SHALL:

1. require a string;
2. trim surrounding whitespace;
3. lowercase the value;
4. require exactly 64 hexadecimal characters;
5. reject non-hexadecimal values.

The digest SHALL describe SHA-256 calculated over the exact canonical
raw byte sequence associated with the Document.

The digest input SHALL NOT be altered through:

- text normalization;
- parsing;
- OCR;
- decompression;
- semantic transformation.

Construction of `DocumentContentDigest` SHALL validate digest format
only.

Successful Domain construction SHALL NOT prove:

- payload existence;
- successful payload persistence;
- correct digest computation;
- verification against persisted bytes.

Verification against payload bytes belongs to a future accepted
content persistence/access contract.

## Digest Integrity Boundary

SHA-256 SHALL be an integrity descriptor only.

It SHALL NOT establish:

- Document identity;
- content identity;
- repository identity;
- uniqueness identity;
- idempotency identity;
- deduplication identity.

Digest-based deduplication requires a separate future architecture
decision.

## Canonical DocumentContentDescriptor

`DocumentContentDescriptor` SHALL be an immutable keyword-only Domain
value object containing exactly:

- `document_id: EntityId`;
- `media_type: DocumentContentMediaType`;
- `byte_length: int`;
- `digest: DocumentContentDigest`.

Construction SHALL require canonical instances of:

- `EntityId`;
- `DocumentContentMediaType`;
- `DocumentContentDigest`.

`byte_length` SHALL represent the exact number of bytes in the
canonical raw payload.

`byte_length` SHALL:

- require an integer;
- explicitly reject `bool`;
- allow zero;
- reject negative values.

The descriptor SHALL NOT contain:

- independent content identity;
- raw `bytes`;
- `bytearray`;
- memory buffer;
- stream;
- file handle;
- filesystem path;
- URI;
- object-storage key;
- source reference;
- title;
- Document type;
- character encoding;
- extracted text;
- parser result;
- revision;
- timestamp;
- actor;
- approval state;
- trust state.

## EnterpriseDocument Preservation

AD-052 SHALL NOT modify:

- `EnterpriseDocument`;
- `EnterpriseDocument.id`;
- `EnterpriseDocument.document_type`;
- `EnterpriseDocument.title`;
- `EnterpriseDocument.source`;
- Document validation;
- Document persistence mapping;
- Document relational schema;
- Document Registration behavior.

Document registration SHALL remain independent from future content
registration/persistence.

## Source Reference Boundary

`DocumentSource.source_reference` SHALL remain an opaque external
traceability value.

AD-052 SHALL NOT define it as:

- local filesystem path;
- mounted path;
- network path;
- file URI;
- HTTP URI;
- storage locator;
- storage key;
- object-store key;
- content key;
- canonical content locator;
- content identity;
- digest;
- deduplication key.

Future source-specific acquisition adapters MAY interpret an external
reference.

Such interpretation SHALL NOT redefine the canonical meaning of
`DocumentSource.source_reference`.

## Raw Payload Boundary

RFC-066 Domain contracts SHALL contain no raw payload bytes.

AD-052 SHALL NOT become:

- binary transport API;
- binary storage adapter;
- memory-loading policy;
- streaming framework;
- parser input implementation.

A future content-access contract SHALL separately define:

- byte writes;
- byte reads;
- streaming semantics;
- size limits;
- resource lifecycle;
- integrity verification;
- missing-content semantics;
- storage failures.

## Document Existence Boundary

`app.domain.document_content` SHALL NOT import or depend on:

`EnterpriseDocumentRepository`

Domain construction SHALL perform no I/O.

Domain construction SHALL perform no cross-aggregate existence lookup.

A future application boundary that establishes persisted canonical
Document content SHALL verify that the referenced canonical
`EnterpriseDocument.id` exists.

AD-052 SHALL NOT authorize orphan-content persistence semantics.

## Repository and Store Boundary

AD-052 SHALL introduce no:

- `DocumentContentRepository`;
- `DocumentContentStore`;
- content persistence port;
- persistence adapter;
- filesystem adapter;
- object-storage adapter;
- database BLOB adapter;
- session lifecycle;
- transaction coordinator.

A persistence-neutral content access/store contract SHALL be selected
and reviewed separately after RFC-066 is closed.

## Binary Storage Boundary

Future binary persistence SHALL remain Infrastructure responsibility
behind an accepted persistence-neutral contract.

AD-052 SHALL NOT select:

- local filesystem;
- network filesystem;
- database BLOB;
- object storage;
- file server;
- another storage technology.

## Content Retrieval Boundary

AD-052 SHALL NOT establish:

- byte retrieval operation;
- content retrieval operation;
- streaming operation;
- download operation;
- resource-lifecycle API.

Those responsibilities belong to a future content access/store
contract.

## Transaction and Atomicity Boundary

AD-052 introduces no new transaction.

AD-052 SHALL NOT change RFC-060 Document Registration transaction
semantics.

AD-052 SHALL NOT change RFC-064 Knowledge / lineage transaction
semantics.

AD-052 SHALL NOT change RFC-065 Document-to-Knowledge ingestion
transaction assumptions.

Atomicity between:

- Enterprise Document registration;
- content descriptor persistence;
- binary payload persistence

is not decided by AD-052.

A future content persistence/application architecture SHALL explicitly
decide those transaction and partial-failure semantics.

## Revision and Mutation Boundary

AD-052 SHALL remain revision-neutral.

It SHALL introduce no:

- update;
- replace;
- delete;
- revision number;
- revision identity;
- supersession relationship;
- current/latest pointer;
- mutable content state.

Canonical content descriptors SHALL be immutable.

If future architecture introduces Document revision, replacement,
supersession or multiple content states for one canonical Document
identity, AD-052 SHALL be explicitly reviewed before that behavior is
accepted.

## Parsing and Extraction Boundary

AD-052 SHALL NOT implement:

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

Future parsing SHALL consume bytes only through an accepted
content-access boundary.

A parser SHALL NOT perform:

`open(document.source.source_reference)`

or equivalent logic that silently converts source traceability into
canonical storage/access semantics.

## Document Library Boundary

AD-052 is not the Document Library.

It SHALL NOT establish:

- upload;
- download;
- browse;
- folder hierarchy;
- source synchronization;
- user file management;
- content registration workflow;
- Document permissions;
- approval workflow;
- retention policy;
- revision history.

## Search, Vector, Graph and AI Boundary

AD-052 SHALL NOT establish:

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

Existence of a canonical content descriptor does not mean the Document
content is parsed, indexed, searchable or available to AI.

## Security and Trust Boundary

AD-052 SHALL NOT establish or claim:

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

SHA-256 is an integrity descriptor.

It does not establish trust, approval, authorization or authenticity.

## DatabaseRuntime Boundary

AD-052 SHALL NOT create or own:

- database engine;
- SQLAlchemy session;
- session factory;
- `DATABASE_URL`;
- metadata root;
- database lifecycle;
- migration lifecycle.

Canonical `DatabaseRuntime` ownership remains unchanged.

## Relational Schema and Alembic Boundary

AD-052 requires:

- no new table;
- no new column;
- no new index;
- no new constraint;
- no foreign key;
- no new Alembic revision.

Canonical Alembic head remains:

`0004`

If a future implementation review discovers a genuine persistence
requirement, implementation SHALL stop and architecture review SHALL
occur before schema authorization.

## Composition Boundary

AD-052 SHALL NOT modify default:

- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`.

Existence of canonical Document-content Domain contracts SHALL NOT make
content persistence a mandatory default platform capability.

## Runtime and Bootstrap Boundary

AD-052 SHALL NOT modify:

- Runtime lifecycle;
- Bootstrap;
- readiness semantics;
- Health semantics;
- request-admission semantics;
- mandatory-capability policy.

## Architectural Layer Boundary

AD-052 introduces no new ARCH-001 layer.

`app.domain.document_content` is a Domain contract within the accepted
architecture.

The six-layer ARCH-001 architecture remains unchanged.

## Dependency Boundary

`app.domain.document_content` SHALL depend only on:

- Python standard library;
- accepted shared Domain primitives from `app.domain.base`.

It SHALL NOT depend on:

- `app.domain.document`;
- `app.document.repository`;
- `app.services`;
- `app.infrastructure`;
- SQLAlchemy;
- FastAPI;
- Pydantic;
- filesystem APIs;
- network clients.

`DocumentContentDescriptor` SHALL reference `EntityId`, not an
`EnterpriseDocument` instance.

This preserves explicit, acyclic Domain dependency direction and avoids
cross-aggregate circular dependency.

## Core Boundary

AD-052 does not create a Core Service.

Core Services SHALL NOT gain Document-content responsibility through
RFC-066.

CORE-002 remains authoritative.

CORE-003 dependency-management rules remain authoritative.

## Existing Responsibilities Preserved

AD-052 SHALL preserve accepted responsibility and public contracts for:

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
- canonical Knowledge relational persistence;
- canonical lineage persistence;
- standalone repository lifecycle semantics;
- RFC-064 transaction coordination;
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

AD-052 SHALL NOT establish a general dependency exception for unrelated
PlantMind components.

## Explicitly Deferred

AD-052 SHALL NOT establish:

- independent Document Content identity;
- content repository;
- content store;
- content persistence;
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
- multiple-content-artifact semantics;
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

## Alternatives Considered

### Add content fields directly to EnterpriseDocument

Rejected.

RFC-057 intentionally established a minimal immutable canonical Document
contract and architecture tests protect its exact class surface.

Adding content fields would silently redesign an accepted prior
contract.

### Introduce DocumentContentId

Rejected.

Current architecture requires no second entity identity for the
Document-content association.

Canonical association remains anchored to `EnterpriseDocument.id`.

### Store raw bytes inside the Domain descriptor

Rejected.

That would mix Domain description with payload transport, storage,
memory-loading and streaming concerns.

### Use DocumentSource.source_reference as the content locator

Rejected.

`source_reference` is accepted external traceability only.

Using it as canonical storage access would collapse source traceability
and internal content-storage semantics.

### Use SHA-256 as content identity or deduplication identity

Rejected.

SHA-256 is accepted only as integrity description.

Identity, deduplication and idempotency require separate contracts.

### Introduce DocumentContentRepository or DocumentContentStore now

Rejected.

RFC-066 establishes the Domain foundation only.

Persistence and byte-access semantics require a separately reviewed
architecture contract.

### Add parser or OCR behavior now

Rejected.

Parsing requires canonical byte-access semantics that RFC-066
deliberately does not own.

### Add Document revision semantics now

Rejected.

The accepted Enterprise Document architecture remains immutable and
revision-neutral.

Revision semantics require independent evidence and architecture review.

## Acceptance Requirements

Before AD-052 may become Accepted, combined RFC-066 / AD-052 review
SHALL confirm:

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

## Contract Acceptance Review

Status:

**PASSED — 52 / 52 Acceptance Requirements**

RFC-066 formal architecture-contract review:

**PASS**

Combined RFC-066 / AD-052 semantic-consistency review:

**PASS**

Disposition:

- PASS: 52;
- REFINE: 0;
- BLOCKED: 0.

The RFC-066 and AD-052 Acceptance Requirements are byte-for-byte
equivalent.

The combined review confirmed that AD-052 is materially and
semantically equivalent to the reviewed RFC-066 architecture contract.

AD-052 is Accepted.

RFC-066 is Accepted.

No accepted prior architecture decision was modified.

At architecture-contract acceptance, technical implementation remained
unauthorized pending the accepted-contract Git gate.

That Git gate was subsequently satisfied before RFC-066 TDD RED
implementation began.

## Implementation Authorization

Status:

**Satisfied — Technical implementation completed and verified.**

Accepted architecture contract commit:

`fb277fe00a9e606192c795338ab5419f4b9db788`

Verified technical implementation commit:

`49080b6c1f6f0607e6ba04ba2476f222dea97155`

The accepted-contract Git gate was satisfied before technical
implementation began.

Verified implementation evidence:

- canonical module:
  `backend/app/domain/document_content.py`;
- canonical public Domain surface remains exactly:
  `DocumentContentMediaType`,
  `DocumentContentDigest`,
  `DocumentContentDescriptor`;
- focused RFC-066 Domain and architecture verification: **65 passed**;
- full PlantMind regression: **840 passed**;
- `git diff --check`: passed;
- RFC-057 `backend/app/domain/document.py` remained unchanged;
- no schema or Alembic revision was introduced;
- canonical Alembic head remains `0004`;
- no repository, content store, persistence adapter or file-I/O
  responsibility was introduced;
- no default Composition, Runtime or Bootstrap expansion was introduced;
- remote technical push: verified;
- exact local / remote technical identity: verified;
- working tree after technical push: clean.

RFC-066 technical implementation conforms to accepted AD-052.

AD-052 remains Accepted.

## Post-Implementation System and Architecture Integrity Review

Outcome:

**PASS — RFC-066 technical implementation conforms to accepted AD-052
and the existing PlantMind architecture remains sound.**

Final verification evidence:

- focused RFC-066 Domain and architecture verification: **65 passed**;
- full PlantMind regression: **840 passed**;
- Python compile verification: passed;
- `git diff --check`: passed;
- canonical Alembic head remains `0004`;
- RFC-057 `backend/app/domain/document.py` remained unchanged;
- default `CompositionRoot` remained unchanged;
- no migration or schema change was introduced;
- the RFC-066 technical commit remained limited to:
  `backend/app/domain/document_content.py`,
  `tests/domain/test_document_content.py` and
  `tests/domain/test_document_content_architecture.py`;
- no repository, content store, persistence adapter or file-I/O
  responsibility was introduced;
- no new ARCH-001 architectural layer was introduced;
- RFC-060, RFC-064 and RFC-065 application / transaction semantics
  remain unchanged;
- all capabilities explicitly deferred by AD-052 remain deferred.

No architecture defect, accepted-contract violation or required
production-code redesign was identified by the post-implementation
review.

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

AD-052 remains Accepted. Its accepted architecture semantics and all 52
Acceptance Requirements remain unchanged.

## Next Exact Action

Perform the broad post-RFC-066 architecture and system evidence review
before selecting another architecture workstream.

The review SHALL examine:

1. maintained Source-of-Truth consistency;
2. accepted architecture contracts and dependency boundaries;
3. current implementation responsibilities and composition authority;
4. test and regression evidence;
5. persistence and transaction boundaries;
6. explicitly deferred capabilities;
7. remaining architecture debt, contradictions, stale state or required
   remediation.

No next RFC has been selected or authorized.

No next RFC selection or implementation may begin until the broad
architecture/system review passes and evidence-based workstream
selection is subsequently completed.

---

# Current Architecture Workstream Selection State — Non-Decision Record

## Classification

This is a current architecture-governance state record.

It is not AD-053, does not amend AD-052, does not constitute an accepted
RFC architecture contract and does not authorize implementation.

AD-001 through AD-052 remain unchanged.

## Broad Post-RFC-066 Architecture/System Review

The broad post-RFC-066 architecture/system review is complete.

Final judgment:

**PASS WITH REGISTERED NON-BLOCKING DEBT**

Selection baseline:

`1d7f09d5106b7714421a1035877ff82a0538d39e`

Verified evidence includes:

- full regression: 840 passed;
- Python compile audit: 342 files, 0 failures;
- canonical Alembic lineage:
  `0001 → 0002 → 0003 → 0004`;
- canonical Alembic head: `0004`;
- `CompositionRoot.build()` smoke verification: passed;
- exact local / remote baseline identity: verified;
- working tree clean at completion of the broad review.

No architecture blocker, accepted-contract violation or required platform
redesign was identified.

## Registered Non-Blocking Debt

### Operational Workload Evidence Contract Placement

Exactly two canonical Core modules currently import
`OperationalWorkloadEvidence` from:

`app.services.orchestration.workload_evidence`

The Core consumers are:

- `app.core.operational_transition_coordinator`;
- `app.core.operational_transition_evidence`.

The accepted semantics established through AD-032, AD-033, AD-036 and
AD-037 remain authoritative.

No functional, Runtime-authority, persistence, transaction or accepted
operational-transition semantic defect was identified.

The issue is physical package-placement and dependency-direction debt.

### Separate Neo4j Configuration Hygiene Debt

Unused legacy Neo4j URI / username / password defaults remain in
`app.config`.

They are not consumed by canonical Neo4j Runtime or default Composition
wiring and do not establish production Neo4j connectivity.

This debt is separate from the selected remediation workstream.

## Selected Successor Architecture Workstream

The evidence-based successor workstream is:

**Operational Workload Evidence Contract Placement Remediation**

Selection state:

**DRAFT — Architecture Contract Not Yet Authored or Accepted**

No RFC number has been assigned.

No new Architecture Decision number has been assigned.

The exact target package, namespace, relocation mechanism and compatibility
strategy remain undecided until architecture-contract review.

## Required Preservation

The future contract shall preserve accepted responsibilities and semantics
for:

- `OperationalWorkloadEvidence`;
- `ApplicationFacade`;
- `IntegrationGateway`;
- `OrchestrationService`;
- `WorkflowExecutor`;
- `OperationalTransitionEvidence`;
- `OperationalTransitionCoordinator`;
- `OperationalTransitionApplicationService`;
- mandatory-capability availability, policy and coverage;
- Runtime lifecycle and transition authority;
- Bootstrap;
- request admission;
- default `CompositionRoot`;
- ARCH-001;
- CORE-002;
- CORE-003;
- AD-032;
- AD-033;
- AD-036;
- AD-037;
- AD-052.

Any required change to an accepted prior contract must be identified and
reviewed explicitly before implementation.

## Explicit Non-Authorization

This selection does not authorize:

- technical implementation;
- workload or transition behavior changes;
- Runtime-authority changes;
- new application/orchestration authorities;
- a new Core Service;
- a seventh ARCH-001 layer;
- persistence, transaction, schema or Alembic changes;
- Document Content access/storage;
- Document Library;
- parser, OCR or chunking;
- search, vector, graph, RAG or LLM implementation;
- Neo4j production integration;
- PI production connectivity;
- authentication, authorization, RBAC or Active Directory implementation;
- Cybersecurity approval;
- production-readiness claims.

## Source-of-Truth State

The successor selection is now represented across:

- `ROADMAP-004-Active-Work-Register.md`;
- `PROJECT-CONTEXT.md`;
- `SESSION-HANDOFF.md`;
- append-only `ENGINEERING-JOURNAL.md`;
- this non-decision architecture-governance record.

Accepted AD-001 through AD-052 history remains unchanged.

## Five-Document Selection Consistency Review

The complete five-document successor-selection consistency review passed.

Review result:

**PASS**

The review verified:

- exact successor-workstream consistency;
- exact selection-baseline consistency;
- registered-debt consistency;
- preservation of accepted responsibilities;
- explicit non-authorization boundaries;
- committed AD-001 through AD-052 history preservation;
- committed Engineering Journal history preservation;
- absence of production-code and test-file changes;
- clean `git diff --check`;
- separation of successor selection from future architecture-contract
  acceptance and technical implementation.

The single automated clean-working-tree finding was independently verified
as a checker false negative.

The architecture-governance record already requires:

`verify a clean working tree`

before architecture-contract drafting.

No Source-of-Truth correction was required for that checker finding.

The reviewed successor-selection documentation is ready for the separate
selection commit gate.

## Next Exact Action

Open the successor-selection documentation commit gate.

Stage and review exactly the five maintained Source-of-Truth documents.

Do not create the selection commit unless the staged diff:

1. contains exactly those five documents;
2. preserves committed AD-001 through AD-052 history;
3. preserves committed Engineering Journal history;
4. contains no production-code or test-file change;
5. remains clean under `git diff --check`;
6. preserves the reviewed successor-selection architecture state.

After the reviewed selection commit is created:

1. push the selection commit;
2. verify exact local / remote selection identity;
3. verify a clean working tree;
4. only then begin architecture-contract drafting.

Technical implementation remains prohibited until a future architecture
contract is reviewed, accepted, committed, pushed and its implementation
Git gate is satisfied.

---

# AD-053 — Operational Workload Evidence Contract Placement Remediation

## Status

**Accepted**

RFC-067 formal RFC-side architecture review:

**PASSED — 52 / 52**

RFC-067 remains Draft and is not yet Accepted.

AD-053 is not yet Accepted.

Technical implementation:

**NOT AUTHORIZED**

## Decision Classification

AD-053 is the accepted matching Architecture Decision for:

`RFC-067 — Operational Workload Evidence Contract Placement Remediation`

This draft does not amend historical AD-032, AD-033, AD-036 or AD-037.

It does not alter AD-001 through AD-052 history.

It does not authorize technical implementation.

## Relationship to RFC-067

The normative architecture contract below is reproduced directly from the
formally reviewed RFC-067 draft without semantic modification.

References to `RFC-067` inside the reproduced normative contract are
intentional. They identify the paired RFC workstream whose architecture
AD-053 authorizes.

AD-053 SHALL NOT introduce an architecture requirement that is broader,
narrower or materially different from the reviewed RFC-067 contract.

The RFC-067 Acceptance Requirements reproduced below SHALL remain
byte-for-byte equivalent to the reviewed RFC-side requirements before
AD-053 may become Accepted.

## Normative Matching Architecture Contract

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

## AD-053 Formal Architecture Review

RFC-067 formal architecture review:

**52 PASS / 0 REFINE / 0 BLOCKED**

AD-053 formal architecture review:

**52 PASS / 0 REFINE / 0 BLOCKED**

Combined RFC-067 / AD-053 semantic-consistency review:

**PASS**

The normative architecture contracts are byte-for-byte equivalent.

The 52 Acceptance Requirements are byte-for-byte equivalent.

No semantic contradiction, architecture expansion, prior-contract
amendment or unauthorized responsibility transfer was identified.

AD-053 is Accepted together with RFC-067.

Acceptance does not authorize technical implementation until the
accepted-contract Git gate passes.

## Prior Architecture Preservation

AD-001 through AD-052 remain unchanged.

In particular, the accepted semantics of:

- AD-032;
- AD-033;
- AD-036;
- AD-037;

remain authoritative.

AD-053 authorizes only the package-placement, ownership, compatibility and
preservation decisions defined by RFC-067.

## Contract Acceptance Review

Status:

**PASSED — RFC-067 / AD-053 ACCEPTED**

Formal AD-053 architecture review:

**52 PASS / 0 REFINE / 0 BLOCKED**

Combined RFC-067 / AD-053 semantic-consistency review:

**PASS**

The review verified:

1. exact normative-contract equivalence;
2. exact 52-requirement equivalence;
3. canonical Domain ownership and namespace;
4. preservation of workload identity and evidence identity;
5. preservation of producer and propagation responsibilities;
6. removal of the identified Core-to-Services contract-placement debt;
7. exact legacy re-export compatibility policy;
8. preservation of ARCH-001, ARCH-003, CORE-002 and CORE-003;
9. preservation of AD-032, AD-033, AD-036 and AD-037;
10. preservation of Runtime, Composition, Bootstrap, API, persistence and
    transaction boundaries.

RFC-067 is Accepted.

AD-053 is Accepted.

Technical implementation remains unauthorized pending the accepted-contract
Git gate.

## Implementation Authorization

Status:

**NOT AUTHORIZED**

No:

- TDD RED test;
- production-code modification;
- package relocation;
- import migration;
- compatibility-module implementation;

is authorized by creation of this draft.

Technical implementation may begin only after the accepted RFC-067 /
AD-053 architecture-contract documentation is:

1. committed;
2. pushed;
3. verified at exact local / remote commit identity;
4. followed by a clean working tree.

## Next Exact Action

Perform the accepted-contract Git gate for RFC-067 / AD-053.

Commit the architecture-contract documentation separately from technical
implementation.

Then push and verify exact local / remote commit identity and a clean
working tree.

Only after that gate passes may technical implementation begin with TDD
RED.

Do not modify production code before the accepted-contract Git gate passes.

---

## Current Architecture Governance State — RFC-067 Technical Completion and Engineering-Memory Closure

**Record Classification: Non-Decision Current Architecture-Governance State**

This section is not a new Architecture Decision.

It does not create:

- AD-054;
- an amendment to AD-053;
- an amendment to AD-001 through AD-052;
- a new architecture contract;
- a new technical authorization.

AD-001 through AD-053 preceding this record remain historical accepted
Architecture Decisions and are preserved byte-for-byte.

### Historical AD-053 Procedural-State Clarification

AD-053 contains procedural-state language written during its architecture
contract acceptance and implementation-entry sequence.

That historical language includes pre-implementation statements concerning:

- Draft / acceptance transition state;
- implementation authorization;
- the accepted-contract Git gate;
- the requirement to begin implementation with TDD RED only after that
  gate passed.

Those statements remain preserved as historical decision-process evidence.

They SHALL NOT be read as the current RFC-067 execution state.

The authoritative current RFC-067 state is recorded below without rewriting
AD-053 history.

### Current RFC-067 Architecture State

RFC-067:

`Operational Workload Evidence Contract Placement Remediation`

Matching Architecture Decision:

`AD-053 — Operational Workload Evidence Contract Placement Remediation`

Architecture contract state:

**ACCEPTED**

Successor-selection baseline:

`1d7f09d5106b7714421a1035877ff82a0538d39e`

Successor-selection documentation commit:

`4ed69096aff2f201f6c5aa8d96c4ec96d43e4122`

Accepted RFC-067 / AD-053 architecture-contract commit:

`d5f743fc0d6d416a5e52d21a6aba0b0108cd7b08`

Verified technical implementation commit:

`48f245b1064a5f0f203ae0705556bb86628f7403`

The accepted-contract implementation-entry Git gate passed before
intentional TDD RED and production implementation began.

### Verified Implementation State

RFC-067 technical implementation is:

**COMPLETE — VERIFIED AND COMMITTED**

Canonical contract ownership is:

`app.domain.operational_workload_evidence`

Canonical physical module:

`backend/app/domain/operational_workload_evidence.py`

The legacy import path:

`app.services.orchestration.workload_evidence`

remains only as the accepted temporary exact-class-identity compatibility
re-export boundary.

The legacy module owns no independent workload-evidence contract class
definitions.

All maintained non-test backend consumers use the canonical Domain import.

The two Core consumers identified by the post-RFC-066 review no longer
depend on the Services-owned workload-evidence contract package.

### Verified Technical Evidence

RFC-067 technical verification established:

- intentional RED: 2 expected failures;
- RED failures matched the accepted package-placement debt;
- focused GREEN: 101 passed;
- full PlantMind regression: 850 passed;
- Python compilation: passed;
- static dependency / import integrity: passed;
- exact canonical / legacy Python class identity: verified;
- duplicate backend workload-evidence contract definitions: none;
- `app.domain.evidence`: byte-for-byte unchanged;
- `CompositionRoot.build()`: passed;
- Runtime authority: unchanged;
- Bootstrap and Health boundaries: unchanged;
- API and request-admission boundaries: unchanged;
- Infrastructure and relational migration surfaces: unchanged;
- canonical Alembic head remains `0004`;
- `git diff --check`: passed.

Technical Git verification:

- push: verified;
- exact local / remote technical identity:
  `48f245b1064a5f0f203ae0705556bb86628f7403`;
- working tree after technical push: clean.

### Architecture Preservation State

RFC-067 implementation conforms to accepted AD-053.

The accepted semantics and responsibilities of:

- AD-032;
- AD-033;
- AD-036;
- AD-037;

remain unchanged.

RFC-067 changes physical contract ownership and import placement only.

Runtime remains the sole lifecycle-transition authority.

Default CompositionRoot authority remains unchanged.

RFC-067 introduced no:

- seventh ARCH-001 layer;
- new Core Service;
- workload-execution redesign;
- operational-transition semantic redesign;
- persistence or transaction change;
- database schema or Alembic change;
- authentication or authorization;
- RBAC or Active Directory integration;
- new information-security classification;
- production-security readiness;
- Cybersecurity approval;
- Document or Knowledge redesign;
- parser or OCR;
- vector, graph, RAG or LLM behavior;
- PI or DCS production connectivity.

The separate legacy Neo4j configuration-hygiene debt remains outside
RFC-067.

The physical placement of:

`OperationalTransitionEvidence`

under:

`app.core.operational_transition_evidence`

also remains outside RFC-067 and is not declared remediated or fully
ARCH-003 compliant by this workstream.

### Engineering-Memory Closure State

Reviewed RFC-067 closure drafts now exist in all five maintained
Source-of-Truth documents:

1. `docs/ROADMAP-004-Active-Work-Register.md`;
2. `docs/PROJECT-CONTEXT.md`;
3. `docs/SESSION-HANDOFF.md`;
4. append-only `docs/ENGINEERING-JOURNAL.md`;
5. this non-decision current governance record in
   `docs/ARCHITECTURE-DECISIONS.md`.

Engineering-memory closure is:

**IN PROGRESS — FIVE-DOCUMENT CONSISTENCY REVIEW PENDING**

Closure commit:

**PENDING**

Post-closure Source-of-Truth reconciliation:

**NOT YET PERFORMED**

No new RFC or architecture workstream is selected by this closure record.

### Next Exact Action

Perform the complete RFC-067 five-document engineering-memory closure
consistency review.

That review SHALL verify:

- exact RFC-067 identity and workstream-name consistency;
- exact selection baseline and selection commit consistency;
- exact accepted-contract commit consistency;
- exact technical implementation commit consistency;
- consistent 850-test technical baseline;
- consistent canonical Domain ownership;
- consistent legacy compatibility-boundary semantics;
- preservation of AD-032, AD-033, AD-036 and AD-037;
- historical Engineering Journal byte preservation;
- historical AD-001 through AD-053 byte preservation;
- absence of AD-054 creation;
- documentation-only closure scope;
- clean `git diff --check`;
- no staged or technical-code changes.

Only after that review passes may the separate RFC-067 engineering-memory
closure commit gate open.

Do not select or begin another RFC or architecture workstream until the
closure commit is pushed, exact local / remote closure identity is verified,
the working tree is clean and post-closure Source-of-Truth reconciliation
is complete.


---

## Current Architecture Governance State — RFC-067 Post-Closure Source-of-Truth Reconciliation

**Record Classification: Non-Decision Current Architecture-Governance State**

This section is not a new Architecture Decision.

It does not create:

- AD-054;
- a successor RFC;
- a successor architecture workstream;
- an amendment to AD-053;
- an amendment to AD-001 through AD-052.

All architecture-decision content preceding this governance record is
preserved exactly as committed by the verified RFC-067 engineering-memory
closure.

### Verified RFC-067 Engineering Closure

RFC-067 — Operational Workload Evidence Contract Placement Remediation
completed engineering-memory closure at:

`76e59a3fe37628f8c60ba0243995ddd5a44bf0a6`

Closure Git verification:

- closure commit creation: **PASS**;
- closure push: **PASS**;
- exact local / remote closure identity: **PASS**;
- working tree after closure push: **clean**.

Engineering-memory closure is:

**COMPLETE — COMMITTED, PUSHED AND VERIFIED**

AD-053 remains the final accepted Architecture Decision.

No AD-054 Architecture Decision exists.

### Architecture Preservation

The reconciliation preserves:

- AD-032;
- AD-033;
- AD-036;
- AD-037;
- AD-053;
- ARCH-001;
- ARCH-003;
- CORE-002;
- CORE-003;
- Runtime lifecycle authority;
- Bootstrap and Health boundaries;
- API and request-admission boundaries;
- persistence and transaction boundaries;
- canonical Alembic head `0004`.

Canonical RFC-067 contract ownership remains:

`app.domain.operational_workload_evidence`

Legacy compatibility remains only at:

`app.services.orchestration.workload_evidence`

as a temporary exact-class-identity re-export boundary.

The physical placement of:

`OperationalTransitionEvidence`

under:

`app.core.operational_transition_evidence`

remains outside RFC-067 and is not declared remediated or fully ARCH-003
compliant by this reconciliation.

### Post-Closure Source-of-Truth Reconciliation

Status:

**IN PROGRESS**

Reconciliation commit:

**PENDING**

The five maintained Source-of-Truth reconciliation surfaces are:

1. `docs/ROADMAP-004-Active-Work-Register.md`;
2. `docs/PROJECT-CONTEXT.md`;
3. `docs/SESSION-HANDOFF.md`;
4. append-only `docs/ENGINEERING-JOURNAL.md`;
5. this non-decision reconciliation governance record in
   `docs/ARCHITECTURE-DECISIONS.md`.

### Governance Gate

Post-closure Source-of-Truth reconciliation SHALL NOT be declared complete
until:

1. the complete five-document reconciliation diff is reviewed;
2. historical Engineering Journal bytes are verified unchanged;
3. historical AD-001 through AD-053 bytes are verified unchanged;
4. no `# AD-054` Architecture Decision exists;
5. RFC-067 identity, commits and 850-test baseline are consistent;
6. the accepted RFC-067 / AD-053 architecture contract is preserved;
7. `git diff --check` passes;
8. the reconciliation diff is documentation-only;
9. the reconciliation documentation commit is created separately;
10. the reconciliation commit is pushed;
11. exact local / remote reconciliation identity is verified;
12. the working tree is clean.

No successor RFC or architecture workstream is selected or authorized by
this governance record.


---

## Current Architecture Governance State — RFC-067 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record does not create a new Architecture Decision.

RFC-067 — Operational Workload Evidence Contract Placement Remediation
is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Engineering closure commit:

`76e59a3fe37628f8c60ba0243995ddd5a44bf0a6`

Post-closure Source-of-Truth reconciliation commit:

`33a10d287111539d63c1042948233597b6ab4ed7`

Verified final Git state:

- reconciliation commit parent: `76e59a3fe37628f8c60ba0243995ddd5a44bf0a6`;
- reconciliation push: **PASS**;
- exact local / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**.

AD-053 remains Accepted and remains the final accepted Architecture
Decision.

No AD-054 Architecture Decision exists.

The final verification preserves:

- ARCH-001;
- ARCH-003;
- CORE-002;
- CORE-003;
- AD-032;
- AD-033;
- AD-036;
- AD-037;
- AD-053;
- Runtime lifecycle authority;
- Bootstrap and Health boundaries;
- API and request-admission boundaries;
- persistence and transaction boundaries;
- canonical Alembic head `0004`;
- canonical ownership at
  `app.domain.operational_workload_evidence`;
- temporary legacy compatibility at
  `app.services.orchestration.workload_evidence`;
- `OperationalTransitionEvidence` placement as outside RFC-067;
- all RFC-067 security and production-readiness non-claims.

No successor RFC or architecture workstream is selected, assumed or
preselected by this record.

Evidence-based successor-workstream selection may proceed only as a separate
governed activity.


---

## Current Architecture Governance State — Post-RFC-067 Successor Workstream Selection Draft

**Record Classification: Non-Decision Successor-Selection Governance Record**

This record does not create a new Architecture Decision.

AD-053 remains the final accepted Architecture Decision.

RFC-067 remains fully closed and Source-of-Truth reconciled.

Selection baseline:

`ed7106c1c232d18c04319559cc2c899e2ebfb61a`

Draft selected successor workstream:

**Canonical Document Content Repository Foundation Boundary**

Proposed successor numbering:

**RFC-068 — NUMBERING CANDIDATE ONLY; NOT ACTIVE**

### Architecture Basis

The selection recognizes that RFC-066 established canonical Document Content
Domain semantics while deliberately deferring repository/store, persistence,
binary access and retrieval responsibilities.

The next architecture review shall therefore determine the minimum
persistence-neutral repository boundary required before storage adapters,
Document Library behavior, parser/OCR, retrieval, vector, graph, RAG or LLM
capabilities are promoted.

### Preserved Authority

This draft selection does not modify or reinterpret accepted Architecture
Decisions.

In particular it preserves:

- AD-043 Enterprise Document foundation;
- AD-044 Enterprise Document repository foundation;
- AD-045 Document relational persistence;
- AD-046 Document Registration application boundary;
- AD-050 Knowledge/lineage transaction coordination;
- AD-051 Document-to-Knowledge ingestion application boundary;
- AD-052 Canonical Enterprise Document Content Foundation Boundary;
- AD-053 Operational Workload Evidence Contract Placement Remediation;
- Runtime, Bootstrap, Composition and API authority boundaries;
- current security and production-readiness non-claims.

### Governance Restrictions

No AD-054 Architecture Decision is created by this record.

No `RFC-068` architecture contract is accepted.

No production implementation is authorized.

No storage technology is selected.

No schema or Alembic change is authorized.

No Document Library, upload/download, parser/OCR, search, vector, graph,
RAG or LLM implementation is authorized.

The complete five-document successor-selection Source-of-Truth diff must be
reviewed before any staging or commit.

Only after the selection record is committed, pushed, exact local / remote
selection identity is verified and the working tree is clean may
architecture-contract drafting begin.


---

# AD-054 — Canonical Document Content Repository Foundation Boundary

## Status

Accepted.

AD-054 is the latest Accepted Architecture Decision.

AD-053 remains Accepted and historically preserved.

RFC-068 selection commit:

`287f3328f49627ce1e19a20d55d56f8bfbb76c58`

No production implementation is authorized.

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

### Contract Acceptance State

Status:

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

Technical implementation remains prohibited until the accepted architecture
documentation is committed separately, pushed, exact local / remote accepted
contract identity is verified and the working tree is clean.

No implementation-entry Git gate is open yet.


## Decision State

AD-054 is **Accepted**.

RFC-068 is **Active — Contract Accepted; Implementation Gate Pending**.

Formal architecture-contract acceptance review passed:

**52 PASS / 0 REFINE / 0 BLOCKED**

No accepted-contract commit exists yet.

No implementation-entry Git gate is open.

Technical implementation remains prohibited.

## Next Exact Action

Review the complete five-document accepted-contract Source-of-Truth diff.

If and only if that review passes, commit the accepted RFC-068 / AD-054
architecture documentation separately from technical implementation.

Then push the accepted-contract commit and verify:

- exact local / remote commit identity;
- clean working tree.

Only after those Git gates pass may RFC-068 TDD RED begin.

Production implementation remains prohibited until the implementation-entry
gate is satisfied.


## Current Architecture Governance State — RFC-068 Technical Completion and Engineering-Memory Closure Pending

**Record Classification: Non-Decision Current Architecture-Governance State**

This section is not a new Architecture Decision.

It does not amend or supersede AD-054.

AD-054 remains the latest Accepted Architecture Decision.

RFC-068 accepted-contract commit:

`6ac09336e223cfb18e049528d62d10b4753e8ee3`

RFC-068 technical implementation commit:

`a88f046567b2b56795f590a4852dbd144b7c2fde`

Technical verification established:

- focused RFC-068 repository contract tests: **16 passed**;
- impacted Document / Document Content regression: **91 passed**;
- full PlantMind regression: **866 passed**;
- Python compilation: **PASS**;
- canonical Alembic head: **0004**;
- `git diff --check`: **PASS**;
- technical push: **PASS**;
- exact local / tracking / remote technical commit identity: **PASS**;
- working tree after technical verification: **clean**.

The accepted descriptor-only persistence-neutral repository boundary is now
technically implemented.

No Infrastructure persistence adapter, binary store, parser, OCR, Document
Library, search, vector, graph, RAG, LLM, Composition expansion, Runtime
expansion or Bootstrap expansion was introduced by RFC-068.

RFC-068 engineering-memory closure remains:

**PENDING**

The separate five-document RFC-068 engineering-memory closure must first
be reviewed, committed, pushed, exact local / remote closure identity
verified and the working tree verified clean.

After that gate passes, a separate post-closure Source-of-Truth
reconciliation remains required.

RFC-068 SHALL NOT be declared fully closed and Source-of-Truth reconciled,
and no successor RFC or architecture workstream may be selected, until the
reconciliation commit is pushed, exact local / remote reconciliation
identity is verified and the working tree is clean.

This record makes no production-readiness, production-security or
Cybersecurity-approval claim.

### Next Exact Action

Review the complete five-document RFC-068 engineering-memory closure diff.

Do not stage or commit until that review passes.


## Current Architecture Governance State — RFC-068 Post-Closure Source-of-Truth Reconciliation

**Record Classification: Non-Decision Reconciliation Governance Record**

This section creates no new Architecture Decision.

It does not amend or supersede AD-054.

AD-054 remains the latest Accepted Architecture Decision.

RFC-068 engineering-memory closure commit:

`bcf2fc8b20c866584db8596341c8abdb965358ea`

Closure push:

**PASS**

Exact local / tracking / remote closure identity:

**PASS**

Working tree after closure push:

**clean**

The reconciliation preserves:

- RFC-068 accepted-contract commit `6ac09336e223cfb18e049528d62d10b4753e8ee3`;
- RFC-068 technical implementation commit `a88f046567b2b56795f590a4852dbd144b7c2fde`;
- technical verification baseline of **866 passed** full regression;
- canonical Alembic head `0004`;
- canonical `app.document_content.repository` ownership;
- descriptor-only persistence-neutral repository responsibility;
- absence of binary payload storage/access;
- absence of Infrastructure persistence implementation;
- absence of schema or migration expansion;
- absence of application, Composition, Runtime or Bootstrap expansion;
- all accepted AD-054 deferred-capability boundaries;
- production-readiness and Cybersecurity non-claims.

Post-closure Source-of-Truth reconciliation is currently:

**PENDING — DRAFT / REVIEW GATE**

No successor RFC or architecture workstream is selected or authorized by
this reconciliation draft.

RFC-068 SHALL NOT be described as fully closed and Source-of-Truth
reconciled until the reconciliation documentation is reviewed, committed,
pushed, exact local / remote reconciliation identity is verified and the
working tree is clean.

### Next Exact Action

Review the complete five-document RFC-068 post-closure reconciliation diff.

Do not stage or commit until that review passes.

---

## Current Architecture Governance State — RFC-068 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record does not create a new Architecture Decision.

It does not amend or supersede AD-054.

AD-054 remains the latest Accepted Architecture Decision.

RFC-068 — Canonical Document Content Repository Foundation Boundary is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Engineering-memory closure commit:

`bcf2fc8b20c866584db8596341c8abdb965358ea`

Post-closure Source-of-Truth reconciliation commit:

`074e534e0d97a927b6434341ad5d1c8671bfa381`

Verified final reconciliation Git state:

- reconciliation commit parent: `bcf2fc8b20c866584db8596341c8abdb965358ea`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- reconciliation commit changed exactly the five maintained Source-of-Truth
  documents;
- reconciliation introduced no production-code or test-file change.

The final verification preserves:

- AD-054 accepted architecture semantics;
- accepted architecture-contract commit `6ac09336e223cfb18e049528d62d10b4753e8ee3`;
- technical implementation commit `a88f046567b2b56795f590a4852dbd144b7c2fde`;
- engineering-memory closure commit `bcf2fc8b20c866584db8596341c8abdb965358ea`;
- reconciliation commit `074e534e0d97a927b6434341ad5d1c8671bfa381`;
- canonical `app.document_content.repository` ownership;
- descriptor-only persistence-neutral repository responsibility;
- full PlantMind regression baseline **866 passed**;
- canonical Alembic head `0004`;
- absence of binary payload storage/access;
- absence of Infrastructure persistence implementation;
- absence of schema or migration expansion;
- absence of application, Composition, Runtime or Bootstrap expansion;
- all AD-054 deferred-capability boundaries;
- all production-readiness, production-security and Cybersecurity non-claims.

No AD-055 is created by this record.

No successor RFC or architecture workstream is selected, assumed or
preselected by this record.

Evidence-based successor-workstream selection may proceed only after this
five-document final-verification record is itself reviewed, committed,
pushed, exact local / remote identity is verified and the working tree is
clean.

Verification of this final record's own future commit, push and exact
local / tracking / remote identity is an external Git gate.

The final record intentionally contains no self-referential future commit
hash, and that external Git gate requires no additional RFC-068
Source-of-Truth update.

After that gate passes, evidence-based successor-workstream selection may
proceed only as a separate governed activity.


---

## Current Architecture Governance State — Post-RFC-068 Successor Workstream Selection Draft

**Record Classification: Non-Decision Successor-Selection Governance Record**

This record creates no new Architecture Decision.

AD-054 remains the latest Accepted Architecture Decision.

RFC-068 remains fully closed and Source-of-Truth reconciled.

Selection baseline:

`bd52f9f74a2cff3138fbf08b13c21e8c1201547a`

Draft selected successor workstream:

**Canonical Document Content Relational Persistence Adapter Boundary**

Proposed successor numbering:

**RFC-069 — NUMBERING CANDIDATE ONLY; NOT ACTIVE**

### Architecture Basis

The accepted RFC-068 / AD-054 repository foundation now provides the
canonical descriptor-only persistence-neutral `DocumentContentRepository`.

Current repository evidence contains canonical relational adapters for:

- Enterprise Document;
- Knowledge;
- Document-to-Knowledge Lineage.

No canonical Document Content Infrastructure persistence adapter currently
exists.

The selected draft therefore addresses the missing descriptor-persistence
adapter before higher Document Intelligence capability is promoted.

Binary content store/access remains a distinct future responsibility.

Parser/OCR remains dependent on a separately accepted binary content
access/store boundary.

### Governance Restrictions

No AD-055 is created.

No RFC-069 architecture contract is accepted.

No production implementation is authorized.

No binary payload persistence technology is selected by this record.

No BLOB, filesystem, object-store or network-file-store behavior is
authorized.

No Document Library, parser, OCR, chunking, Search, Vector, Graph, RAG or
LLM implementation is authorized.

The complete five-document successor-selection diff must be reviewed before
staging or commit.

---

## AD-055 — Canonical Document Content Relational Persistence Adapter Boundary

### Status

**ACCEPTED**

### Related RFC

**RFC-069 — Canonical Document Content Relational Persistence Adapter Boundary**

### Acceptance Baseline

`5d7794352029576e0b62c2ac8cbfa248fe11961d`

### Context

AD-054 established the canonical descriptor-only persistence-neutral
`DocumentContentRepository`.

The accepted repository exposes canonical `add()` and `get()` behavior, but
no canonical Document Content Infrastructure adapter or relational schema
exists. Existing Enterprise Document, Knowledge and
Document-to-Knowledge Lineage relational adapters provide the nearest accepted
architecture precedent. Binary payload storage/access remains outside the
descriptor repository boundary.

### Decision

PlantMind SHALL introduce a canonical SQLAlchemy relational adapter under
`app.infrastructure.document_content` for descriptor metadata only.

The Infrastructure model SHALL be `DocumentContentDescriptorRow` mapped to
`document_content_descriptors` with exactly:

- `document_id`: PostgreSQL UUID, non-null;
- `media_type`: String, non-null;
- `byte_length`: BigInteger, non-null;
- `digest`: String, non-null.

`document_id` SHALL be the sole primary key under
`pk_document_content_descriptors`.

No surrogate content identity SHALL be introduced. Digest remains an integrity
descriptor and SHALL NOT become relational identity or a unique key. No
foreign key to Enterprise Document SHALL be introduced by AD-055.

No additional relational identity or uniqueness rule is authorized.

This keeps the persistence adapter independent of cross-boundary existence,
lifecycle and transaction-coordination policy. Those semantics remain
separately governed.

### Repository Runtime

The concrete adapter SHALL be `SQLAlchemyDocumentContentRepository`,
implementing `DocumentContentRepository` through an injected session factory.

Standalone `add()` SHALL use one explicit session, add one row and commit once
on success. It SHALL perform no pre-read duplicate check and no Enterprise
Document repository lookup.

On persistence failure it SHALL attempt rollback and SHALL close the session
on all paths.

Failure precedence SHALL preserve the accepted relational-adapter semantics:

- successful rollback preserves the original persistence failure unless close
  itself fails;
- rollback failure is raised from the original persistence failure;
- close failure propagates with any earlier active operation failure retained
  in exception context.

`get()` SHALL be read-only, use exact `document_id`, perform no commit, return
`None` when missing, reconstruct the canonical Domain descriptor when present
and close the session on all paths.

Only SQLSTATE `23505` combined with `pk_document_content_descriptors` SHALL
translate to `DocumentContentAlreadyExistsError`.

No pre-read duplicate detection, message-text classification or Enterprise
Document repository lookup is permitted. Other integrity/database failures
remain unclassified and propagate.

### Database and Migration

The existing `DatabaseBase.metadata` remains the sole relational metadata
authority. `DatabaseRuntime` remains unchanged.

After separate implementation authorization, Alembic SHALL append
`0005_document_content_descriptors.py` with revision `0005` and down revision
`0004`.

The migration SHALL create only the accepted descriptor table and SHALL
introduce no foreign key, BLOB/binary payload field or unrelated schema change.

Alembic `env.py` SHALL import/register `DocumentContentDescriptorRow` before
`target_metadata = DatabaseBase.metadata` is bound. This is metadata
registration only and does not expand `DatabaseRuntime` ownership or runtime
lifecycle responsibility.

The current canonical Alembic head remains `0004` until technical
implementation is separately authorized and completed.

### Deferred Responsibilities

AD-055 does not authorize raw binary payload persistence/access,
filesystem/object/network storage, byte streaming/download APIs,
`DocumentContentStore`, application-level content establishment,
cross-boundary transaction coordination, Document Library, parser/OCR/chunking,
Search/Vector/Graph/RAG/LLM, Composition/Runtime/Bootstrap expansion or
production-readiness/security/Cybersecurity claims.

### Consequence

PlantMind gains an accepted canonical boundary for future durable relational
persistence of Document Content descriptor metadata while preserving binary
content storage/access and cross-boundary atomicity as separate future
architecture responsibilities.

### Final Contract Review

The refined five-document RFC-069 / AD-055 architecture-contract review is:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

The three prior refinement findings are resolved:

1. RFC-069 current Active Work control is maintained at the top of ROADMAP-004;
2. Alembic metadata registration is mandatory before `target_metadata` binding;
3. repository rollback/close failure precedence is explicit and aligned with
   accepted relational-adapter precedent.

### Implementation Authorization

**NONE — ACCEPTED-CONTRACT GIT GATE PENDING**

Technical implementation remains prohibited until this accepted
five-document contract is reviewed as an acceptance-propagation diff,
committed, pushed, exact local / tracking / remote commit identity is verified,
the working tree is clean, and a separate implementation-entry Git gate passes.

---

## Current Architecture Governance State — RFC-069 Technical Completion and Engineering-Memory Closure Pending

**Record Classification: Non-Decision Current Architecture-Governance State**

This section is not a new Architecture Decision.

It does not amend, replace or supersede AD-055.

AD-055 remains:

**ACCEPTED**

RFC-069 selection commit:

`5d7794352029576e0b62c2ac8cbfa248fe11961d`

RFC-069 accepted-contract commit:

`467440b6c5d16e599fbc0d0f5c820d31725fd29b`

RFC-069 technical implementation commit:

`4572b40cedecc263577453b95ca63ecab6e61428`

Technical verification established:

- focused RFC-069 verification: **46 passed**;
- impacted regression: **151 passed**;
- full PlantMind regression: **912 passed**;
- canonical Alembic chain: `0003 -> 0004 -> 0005`;
- canonical Alembic single head: **0005**;
- `git diff --check`: **PASS**;
- technical push: **PASS**;
- exact local / tracking / remote technical commit identity: **PASS**;
- working tree after technical verification: **clean**.

The accepted AD-055 descriptor-metadata relational persistence adapter is now
technically implemented.

The implementation establishes:

- canonical `app.infrastructure.document_content`;
- `DocumentContentDescriptorRow`;
- `document_content_descriptors`;
- sole primary-key identity `document_id`;
- `pk_document_content_descriptors`;
- explicit Domain/row mapping;
- `SQLAlchemyDocumentContentRepository`;
- exact structured duplicate classification;
- explicit session rollback/close failure semantics;
- read-only exact `get()` behavior;
- Alembic revision `0005` after `0004`;
- Alembic metadata registration before `target_metadata` binding.

No surrogate content identity, digest uniqueness, Enterprise Document foreign
key, CheckConstraint, binary payload field or storage-location field was
introduced.

No raw binary store/access, cross-repository transaction coordination,
application-service expansion, Composition/Runtime/Bootstrap expansion,
Document Library, parser, OCR, chunking, Search, Vector, Graph, RAG or LLM
capability is authorized or implied by technical completion.

Historical RFC-063 / RFC-064 / RFC-065 current-head assertions were reconciled
to durable revision-history invariants after repository-wide audit. This did
not change their original architecture responsibilities.

RFC-069 engineering-memory closure remains:

**PENDING — DRAFT / REVIEW GATE**

The separate five-document engineering-memory closure must be reviewed,
committed, pushed, exact local / tracking / remote closure identity verified
and the working tree verified clean.

A separate post-closure Source-of-Truth reconciliation remains required.

RFC-069 SHALL NOT be declared fully closed and Source-of-Truth reconciled, and
no successor RFC or architecture workstream may be selected, until those gates
complete.

This record introduces no production-readiness, production-security or
Cybersecurity-approval claim.

### Next Exact Action

Review the complete five-document RFC-069 engineering-memory closure diff.

Do not stage or commit until that review passes.

---

## Current Architecture Governance State — RFC-069 Post-Closure Source-of-Truth Reconciliation

**Record Classification: Non-Decision Reconciliation Governance Record**

This section creates no new Architecture Decision.

It does not amend, replace or supersede AD-055.

AD-055 remains:

**ACCEPTED**

Verified RFC-069 engineering-memory closure commit:

`63790de5312c69c709e2249b56e91995a00426b6`

Closure commit parent:

`4572b40cedecc263577453b95ca63ecab6e61428`

Closure push:

**PASS**

Exact local / tracking / remote closure identity:

**PASS**

Working tree after closure push:

**clean**

Engineering-memory closure is:

**COMPLETE — COMMITTED, PUSHED AND VERIFIED**

The reconciliation preserves:

- selection commit `5d7794352029576e0b62c2ac8cbfa248fe11961d`;
- accepted-contract commit `467440b6c5d16e599fbc0d0f5c820d31725fd29b`;
- technical implementation commit `4572b40cedecc263577453b95ca63ecab6e61428`;
- closure commit `63790de5312c69c709e2249b56e91995a00426b6`;
- full PlantMind regression baseline **912 passed**;
- canonical Alembic head `0005`;
- accepted AD-055 relational descriptor semantics;
- canonical `app.infrastructure.document_content` ownership;
- `DocumentContentDescriptorRow`;
- `document_content_descriptors`;
- `SQLAlchemyDocumentContentRepository`;
- exact PK duplicate classification;
- no surrogate content identity;
- no digest uniqueness;
- no Enterprise Document foreign key;
- no CheckConstraint;
- no binary payload or storage-location field;
- unchanged `DatabaseRuntime`;
- `DatabaseBase.metadata` authority;
- all accepted deferred application, binary-storage, coordination,
  Document Intelligence and production-security boundaries.

Post-closure Source-of-Truth reconciliation is currently:

**PENDING — DRAFT / REVIEW GATE**

Reconciliation commit:

**PENDING — NOT YET CREATED**

No successor RFC or architecture workstream is selected or authorized by this
reconciliation draft.

RFC-069 SHALL NOT be described as fully closed and Source-of-Truth reconciled
until the reconciliation documentation is reviewed, committed, pushed, exact
local / tracking / remote reconciliation identity is verified, the working
tree is clean and the separate final-verification record gate is completed.

This reconciliation introduces no production-readiness, production-security
or Cybersecurity-approval claim.

### Next Exact Action

Review the complete five-document RFC-069 post-closure reconciliation diff.

Do not stage or commit until that review passes.

---

## Current Architecture Governance State — RFC-069 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record does not create a new Architecture Decision.

It does not amend, replace or supersede AD-055.

AD-055 remains the latest Accepted Architecture Decision.

RFC-069 — Canonical Document Content Relational Persistence Adapter Boundary
is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Engineering-memory closure commit:

`63790de5312c69c709e2249b56e91995a00426b6`

Post-closure Source-of-Truth reconciliation commit:

`231e0cc66862c797e299fdb71ff20da8a39e8ae2`

Verified final reconciliation Git state:

- reconciliation commit parent: `63790de5312c69c709e2249b56e91995a00426b6`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- reconciliation surface: exactly five maintained Source-of-Truth documents;
- reconciliation production-code changes: none;
- reconciliation test-file changes: none.

The final architecture state preserves:

- selection commit `5d7794352029576e0b62c2ac8cbfa248fe11961d`;
- accepted-contract commit `467440b6c5d16e599fbc0d0f5c820d31725fd29b`;
- technical implementation commit `4572b40cedecc263577453b95ca63ecab6e61428`;
- closure commit `63790de5312c69c709e2249b56e91995a00426b6`;
- reconciliation commit `231e0cc66862c797e299fdb71ff20da8a39e8ae2`;
- full PlantMind regression baseline **912 passed**;
- canonical Alembic head `0005`;
- accepted AD-055 relational descriptor semantics;
- canonical `app.infrastructure.document_content`;
- `DocumentContentDescriptorRow`;
- `document_content_descriptors`;
- `SQLAlchemyDocumentContentRepository`;
- `document_id` as sole descriptor identity;
- no surrogate content identity;
- no digest uniqueness;
- no Enterprise Document foreign key;
- no CheckConstraint;
- no raw binary payload or storage-location persistence;
- unchanged `DatabaseRuntime`;
- `DatabaseBase.metadata` authority;
- all accepted deferred application, binary-storage, coordination,
  Document Intelligence and production-security boundaries.

No AD-056 is created or implied by this record.

No successor RFC or architecture workstream is selected, assumed or
preselected.

Successor-workstream selection remains a separate evidence-based governance
activity.

This final governance record is intentionally non-self-referential: it
records the verified reconciliation commit and does not reference the future
Git commit that persists this record. External Git verification of this
record's persistence does not create another RFC-069 governance record.

---

## Current Architecture Governance State — Post-RFC-069 Successor Workstream Selection Draft

**Record Classification: Non-Decision Successor-Selection Governance Record**

This record creates no new Architecture Decision.

AD-055 remains the latest Accepted Architecture Decision.

RFC-069 remains fully closed and Source-of-Truth reconciled.

Selection baseline:

`ffd0ec9c6df3d117792a72b394ee9532eb64de8d`

Draft selected successor workstream:

**Canonical Binary Document Content Store / Access Foundation**

Proposed successor numbering:

**RFC-070 — NUMBERING CANDIDATE ONLY; NOT ACTIVE**

### Architecture Basis

RFC-066 / AD-052 established canonical immutable Document Content descriptor
semantics.

RFC-068 / AD-054 established the descriptor-only persistence-neutral
`DocumentContentRepository`.

RFC-069 / AD-055 established the relational Infrastructure adapter for
descriptor metadata.

The canonical chain therefore now ends at durable descriptor metadata.

Binary content payload storage/access remains a distinct missing architecture
responsibility.

Current canonical code contains no accepted `DocumentContentStore`,
byte-access contract, stream/open contract or binary resource-lifecycle
contract.

The future binary workstream must consume existing Document Content semantics
without merging descriptor persistence with raw payload responsibility.

`DocumentSource.source_reference` shall remain external traceability and shall
not be reinterpreted as canonical content access.

The evidence also confirms:

- future Document Content establishment/application coordination remains
  separately governed;
- that future application boundary must explicitly decide descriptor/binary
  failure and atomicity behavior;
- parser/OCR/chunking remain dependent on a separately accepted binary
  content access/store boundary;
- Document Library remains downstream;
- Search/Vector/Graph/RAG/LLM remain higher-level dependent capabilities.

### Governance Restrictions

No AD-056 is created.

No RFC-070 architecture contract is accepted.

RFC-070 is not active.

No production implementation is authorized.

No storage technology is selected.

No PostgreSQL BLOB, filesystem, network filesystem, object store or file
server is authorized.

No byte-access method signature, streaming protocol or resource lifecycle is
accepted by this selection.

No content-establishment transaction or cross-boundary atomicity policy is
accepted.

No Document Library, parser, OCR, chunking, Search, Vector, Graph, RAG, LLM
or AI Agent implementation is authorized.

No production-readiness, production-security or Cybersecurity-approval claim
is introduced.

The complete five-document successor-selection diff must be reviewed before
staging or commit.

---

## AD-056 — Canonical Binary Document Content Store / Access Foundation Boundary

### Status

**ACCEPTED**

### Related RFC

**RFC-070 — Canonical Binary Document Content Store / Access Foundation**

### Selection Baseline

`13cfccc08d8c0a3b891990d38edaf9fc48874a5e`

### Context

RFC-066 / AD-052 established canonical immutable Document Content descriptor
semantics.

RFC-068 / AD-054 established the descriptor-only persistence-neutral
`DocumentContentRepository`.

RFC-069 / AD-055 established durable relational persistence for descriptor
metadata under `app.infrastructure.document_content`.

No canonical binary payload store/access contract currently exists.

Document Library and parser/OCR capability require a stable canonical content
access boundary without direct dependency on filesystem paths, database BLOBs
or provider-specific object handles.

### Decision

PlantMind SHALL introduce a persistence-neutral binary Document Content
store/access foundation under:

`app.document_content.store`

The canonical public contract SHALL expose:

- `DocumentContentStore`;
- `DocumentContentPayloadAlreadyExistsError`.

The store SHALL remain outside the Domain descriptor module.

`app.domain.document_content` SHALL remain unchanged.

`app.document_content.repository` SHALL remain descriptor-only and unchanged.

### Canonical Identity

Binary payload association SHALL use only:

`EnterpriseDocument.id`

represented by the existing canonical:

`EntityId`

No `DocumentContentId`, payload ID, blob ID, object key, path, URI or storage
locator SHALL become canonical identity.

The same byte sequence MAY be stored for multiple distinct document
identities.

At the canonical/public contract level, SHA-256 digest SHALL remain
integrity description only and SHALL NOT become:

- canonical storage identity;
- canonical uniqueness identity;
- canonical lookup identity;
- contract-level deduplication identity;
- contract-level idempotency identity.

RFC-070 does not decide internal physical addressing or transparent physical
deduplication techniques for a future concrete storage adapter.

Any such mechanism requires its own adapter architecture authorization and
MUST NOT alter the externally observable `document_id` identity semantics of
this contract.

### Canonical Store Operations

The minimum canonical contract SHALL be:

`add(document_id: EntityId, source: BinaryIO) -> None`

and:

`open(document_id: EntityId) -> AbstractContextManager[BinaryIO] | None`

No list, search, filter, query, delete, replace, update or upsert operation
SHALL be introduced by RFC-070.

### Write-Source Contract

`add()` SHALL consume bytes beginning at the source's current position and
continue through EOF.

The contract SHALL NOT require successful:

- `seek()`;
- `tell()`;
- `fileno()`.

The source MAY be non-seekable and need not be filesystem-backed.

The caller SHALL retain ownership of the supplied source.

`DocumentContentStore.add()` SHALL NOT close the caller-owned source.

The store SHALL NOT promise to rewind or restore the caller-owned source after
failure.

If `add()` fails after consuming any bytes, the caller-owned source MAY be
partially consumed and its resulting position is unspecified.

Callers SHALL NOT depend on the source position remaining unchanged after a
failed `add()`.

### Duplicate and Immutability Contract

At most one canonical binary payload may be established for one
`document_id`.

If a payload already exists for the same `document_id`, `add()` SHALL raise:

`DocumentContentPayloadAlreadyExistsError`

This applies whether the newly supplied bytes are identical or different.

No silent overwrite SHALL occur.

No idempotent-success or upsert semantics SHALL be introduced.

A zero-byte binary payload is valid.

A successful `add()` whose source is already at EOF SHALL establish a present,
zero-byte payload for that `document_id`.

That present zero-byte payload SHALL remain distinguishable from absence.

Concurrent `add()` operations targeting the same `document_id` SHALL NOT
produce more than one successful canonical payload establishment.

No concurrent operation may interleave, merge, append to or overwrite another
operation's bytes.

If one operation establishes the canonical payload and another operation loses
the same-identity race, the losing operation SHALL fail with
`DocumentContentPayloadAlreadyExistsError`.

A later failed `add()` SHALL NOT damage, replace or partially modify an already
established payload.

### Store-Local Visibility Contract

After successful `add()`, subsequent access SHALL expose the complete byte
sequence consumed by that operation.

If `add()` fails before completion, the store SHALL NOT expose a successfully
addressable partial payload for that `document_id`.

This is a store-local atomic visibility invariant only.

It SHALL NOT be interpreted as atomicity across Enterprise Document,
descriptor, Knowledge, Lineage or application operations.

### Binary Access and Resource Lifecycle

`open()` SHALL resolve only by exact `document_id`.

Confirmed missing payload SHALL return:

`None`

`None` is reserved exclusively for confirmed absence.

An operational storage/access failure, context-entry failure or provider
failure SHALL NOT be translated into `None`.

Such failures SHALL remain failures and propagate according to the future
concrete adapter's accepted failure contract.

A present zero-byte payload SHALL NOT return `None`.

It SHALL return a valid context-managed readable binary resource whose reads
reach EOF without yielding payload bytes.

A present payload SHALL return a context manager yielding a readable binary
resource.

The readable resource SHALL begin at the start of the stored payload and
preserve byte order and value exactly.

Consumers SHALL use the context manager for deterministic resource release.

Each successful `open()` SHALL establish an independent logical read context
beginning at the start of the stored payload.

Closing or exiting one read context SHALL NOT invalidate another independently
opened read context for the same `document_id`.

The storage implementation SHALL release the underlying read resource on both
normal and exceptional context exit.

Consumers SHALL NOT depend on the returned resource being:

- successfully seekable;
- a local file;
- path-backed;
- descriptor-backed;
- backed by a database cursor;
- backed by a specific object-storage SDK.

No byte-range or random-access contract is established.

### Descriptor Boundary

`DocumentContentStore` SHALL NOT accept, persist, mutate or reconstruct:

- `DocumentContentDescriptor`;
- `DocumentContentMediaType`;
- `DocumentContentDigest`;
- descriptor `byte_length`;
- `DocumentSource`.

The existing descriptor repository remains the sole canonical repository
boundary for descriptor metadata.

The binary store SHALL NOT perform a descriptor-repository lookup.

### Enterprise Document Boundary

The binary store SHALL NOT perform an
`EnterpriseDocumentRepository` existence lookup.

RFC-070 SHALL NOT decide orphan prevention or document/content establishment
workflow semantics.

Those responsibilities remain with a future application boundary.

### Integrity Boundary

The binary store SHALL preserve the stored byte sequence but SHALL NOT
independently establish cross-boundary consistency between payload bytes and
a separately persisted descriptor.

The store SHALL NOT require digest or byte-length metadata in its public
contract.

Future Document Content establishment/application architecture SHALL decide
where descriptor/payload SHA-256 and byte-length validation occurs and how
failure is coordinated.

### Source Reference Boundary

`DocumentSource.source_reference` SHALL remain provenance / external
traceability only.

It SHALL NOT be interpreted by `DocumentContentStore` as:

- a filesystem path;
- a URI to open;
- an object-storage key;
- a network-file locator;
- canonical binary content access.

### Persistence Technology Boundary

AD-056 SHALL remain persistence-neutral.

It SHALL NOT select or introduce:

- PostgreSQL BLOB;
- relational binary table;
- database large-object facility;
- filesystem adapter;
- network filesystem;
- object-storage adapter;
- file server;
- cloud provider;
- cloud SDK;
- bucket;
- storage path convention;
- storage key convention.

No SQLAlchemy model, database table, index, foreign key, constraint or
migration SHALL be introduced by RFC-070.

Canonical Alembic head remains:

`0005`

### Runtime and Composition Boundary

RFC-070 SHALL NOT modify or expand:

- `DatabaseRuntime`;
- Runtime authority;
- Bootstrap authority;
- readiness;
- request admission;
- `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`.

No default concrete storage adapter SHALL be wired by RFC-070.

### Application and Transaction Boundary

RFC-070 SHALL introduce no Document Content establishment/registration
application service.

It SHALL NOT modify:

- `EnterpriseDocumentRegistrationApplicationService`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeCaptureApplicationService`;
- `KnowledgeLineageTransactionCoordinator`.

No cross-boundary transaction, compensation, outbox, distributed transaction
or retry policy SHALL be introduced.

### Parser / Document Intelligence Boundary

RFC-070 SHALL NOT implement:

- Document Library;
- upload UI/API;
- download UI/API;
- browse/catalogue behavior;
- parser integration;
- PDF extraction;
- OCR;
- DOCX extraction;
- spreadsheet extraction;
- text extraction;
- encoding detection;
- metadata extraction;
- chunking;
- semantic search;
- embeddings;
- vector persistence;
- graph persistence;
- Neo4j promotion;
- RAG;
- LLM;
- AI Agent behavior.

Those capabilities remain separately governed.

### Security Boundary

RFC-070 SHALL NOT claim or implement production:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- malware scanning;
- document approval;
- retention policy;
- compliance enforcement;
- Cybersecurity approval.

### Technical Surface After Separate Implementation Entry Gate

Only after this AD-056 acceptance is committed, pushed, exact
local / tracking / remote identity is verified, and a separate
implementation-entry Git gate passes may RFC-070 introduce:

- `backend/app/document_content/store.py`;
- focused `tests/document_content/` contract and architecture tests.

No Infrastructure storage adapter or migration is part of the accepted
RFC-070 foundation.

### Verification Model

RFC-070 distinguishes foundation verification from future concrete-adapter
behavioral conformance.

#### RFC-070 Foundation Verification

After this AD-056 acceptance is committed, pushed, exact identity is
verified and the separate implementation-entry gate passes, RFC-070
foundation implementation SHALL verify at minimum:

1. canonical public symbols;
2. `DocumentContentStore` is an abstract persistence-neutral contract;
3. exact `EntityId` association;
4. exact `add()` signature;
5. exact `open()` signature;
6. duplicate error public contract;
7. no descriptor or Enterprise Document repository dependency;
8. no canonical digest-as-identity behavior;
9. no source-reference access behavior;
10. no storage-technology dependency;
11. no SQLAlchemy/database/Alembic expansion;
12. no Runtime/Bootstrap/Composition expansion;
13. no application-service or transaction-coordination expansion;
14. no Document Library/parser/OCR/search/vector/graph/RAG/LLM promotion;
15. full existing PlantMind regression remains passing.

The RFC-070 foundation MAY provide reusable contract-test definitions or test
fixtures for future adapters, but the foundation SHALL NOT claim concrete
storage behavior has passed when no concrete adapter exists.

#### Future Concrete-Adapter Conformance

Only a separately authorized concrete storage adapter can verify behavioral
conformance including:

1. caller-owned write source is not closed;
2. failed write-source position is not falsely guaranteed or rewound;
3. non-seekable source compatibility;
4. valid zero-byte payload persistence and access;
5. duplicate same-document add rejection;
6. concurrent same-document add race safety;
7. no overwrite, merge, append or upsert behavior;
8. successful-add complete visibility;
9. failed-add partial-visibility prohibition;
10. preservation of any already-established payload after a failed add;
11. confirmed absence returns `None`;
12. operational access failures are not translated into `None`;
13. independent repeated `open()` contexts;
14. normal and exceptional context-exit resource release;
15. byte fidelity and order;
16. exact-document identity behavior.

Until a concrete adapter exists and passes its own accepted conformance gate,
these adapter-behavior checks SHALL be recorded as:

**NOT YET APPLICABLE / BLOCKED BY ABSENCE OF CONCRETE ADAPTER**

They SHALL NOT be reported as passed by RFC-070 foundation implementation.

### Acceptance Basis

Formal Architecture Contract review result:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

AD-056 accepts the complete refined RFC-070 contract, including:

- confirmed absence versus operational failure separation;
- valid zero-byte payload semantics;
- failed-write caller-source ownership and position semantics;
- same-document concurrent-add race safety;
- independent read contexts and normal/exceptional cleanup;
- separation of RFC-070 foundation verification from future concrete-adapter
  behavioral conformance;
- canonical/public digest identity restrictions;
- deferral of internal physical addressing and transparent physical
  deduplication to separately authorized adapter architecture;
- `document_id` as the stable externally observable canonical identity.

Concrete storage behavior remains unverified because RFC-070 contains no
concrete storage adapter.

Future concrete-adapter behavioral conformance remains:

**NOT YET APPLICABLE / BLOCKED BY ABSENCE OF CONCRETE ADAPTER**

This intentional blocked state does not block acceptance of the
persistence-neutral foundation contract.

### Consequence

PlantMind gains a canonical binary payload access seam while preserving the
existing descriptor model and avoiding premature commitment to a physical
storage technology.

Future concrete adapters may implement this contract only after their own
evidence-based architecture authorization.

### Current Review State

**ACCEPTED**

Architecture acceptance is complete.

Technical implementation remains unauthorized until this accepted contract is
committed, pushed, exact local / tracking / remote identity is verified, and
the separate RFC-070 implementation-entry Git gate passes.

## RFC-070 / AD-056 Engineering Closure Record

### Closure Baseline

RFC-070 workstream:

**Canonical Binary Document Content Store / Access Foundation**

Verified workstream-selection commit:

`13cfccc08d8c0a3b891990d38edaf9fc48874a5e`

Verified accepted-contract commit:

`cfd45d35144574d27a40e0f350b571a6298afd59`

Verified technical implementation commit:

`389ce20b9e01b99cf9b7c1a066a0e9a55bc71223`

The technical implementation commit is committed, pushed and exact
local / tracking / remote identity has been verified.

### Verified Foundation Outcome

RFC-070 establishes the canonical persistence-neutral binary Document Content
store/access seam under:

`app.document_content.store`

The completed technical foundation exposes:

- `DocumentContentStore`;
- `DocumentContentPayloadAlreadyExistsError`;
- `add(document_id: EntityId, source: BinaryIO) -> None`;
- `open(document_id: EntityId) -> AbstractContextManager[BinaryIO] | None`.

The production implementation surface is restricted to:

`backend/app/document_content/store.py`

The descriptor repository remains descriptor-only.

Canonical Alembic head remains:

`0005`

No Infrastructure storage adapter, storage technology, schema migration,
application service or Runtime / Bootstrap / Composition expansion was
introduced.

### Verification Evidence

TDD RED was observed for the expected missing RFC-070 store boundary.

Minimum GREEN passed.

Focused RFC-070 contract and architecture tests passed.

Full PlantMind regression at the pushed technical baseline:

**928 passed**

Repository integrity remained clean.

### Concrete Adapter Boundary

RFC-070 contains no concrete binary storage adapter.

Therefore concrete-adapter behavioral conformance remains:

**NOT YET APPLICABLE / BLOCKED BY ABSENCE OF CONCRETE ADAPTER**

No concrete-adapter behavior is claimed PASS by this foundation closure.

### Closure Governance State

Engineering closure documentation review:

**PASS**

Engineering closure staging review:

**PASS — EXACT FIVE SOURCE-OF-TRUTH DOCUMENTS**

The engineering closure documentation commit has **not** yet been created.

Closure push / exact-identity verification has **not** yet been performed.

Post-closure Source-of-Truth reconciliation has **not** yet been performed.

RFC-070 is therefore **not yet terminally closed**.

No successor workstream is authorized before closure and reconciliation
complete.

---

## Current Architecture Governance State — RFC-070 Post-Closure Source-of-Truth Reconciliation

**Record Classification: Non-Decision Reconciliation Governance Record**

This section creates no new Architecture Decision.

It does not amend, replace or supersede AD-056.

AD-056 remains:

**ACCEPTED**

RFC-070 workstream:

**Canonical Binary Document Content Store / Access Foundation**

Verified workstream-selection commit:

`13cfccc08d8c0a3b891990d38edaf9fc48874a5e`

Verified accepted-contract commit:

`cfd45d35144574d27a40e0f350b571a6298afd59`

Verified technical implementation commit:

`389ce20b9e01b99cf9b7c1a066a0e9a55bc71223`

Verified engineering closure commit:

`ab4438b02a8f34f83b462e3d8a86b4b5ab5d1092`

Closure commit parent:

`389ce20b9e01b99cf9b7c1a066a0e9a55bc71223`

Closure push:

**PASS**

Exact local / tracking / remote closure identity:

**PASS**

Working tree after closure push:

**clean**

Engineering closure surface:

**exactly the five maintained Source-of-Truth documents**

Engineering closure is:

**COMPLETE — COMMITTED, PUSHED AND VERIFIED**

Full PlantMind regression evidence remains:

**928 passed**

Canonical Alembic head remains:

`0005`

Canonical RFC-070 foundation remains:

- `app.document_content.store`;
- `DocumentContentStore`;
- `DocumentContentPayloadAlreadyExistsError`;
- immutable `add(document_id, source)` semantics;
- exact context-managed `open(document_id)` access;
- `document_id` as canonical public association identity;
- descriptor/binary responsibility separation;
- no concrete storage technology selection.

Concrete-adapter behavioral conformance remains:

**NOT YET APPLICABLE / BLOCKED BY ABSENCE OF CONCRETE ADAPTER**

No Infrastructure storage adapter, schema migration, application service,
Document Library, parser/OCR/chunking, Search/Vector/Graph/RAG/LLM,
Runtime/Bootstrap/Composition expansion or production-security claim is
introduced by this reconciliation.

Post-closure Source-of-Truth reconciliation is currently:

**PENDING — DRAFT / REVIEW GATE**

Reconciliation commit:

**PENDING — NOT YET CREATED**

RFC-070 is not yet fully closed and Source-of-Truth reconciled.

A separate final reconciliation verification record remains required after
the reconciliation commit is reviewed, committed, pushed and exact local /
tracking / remote reconciliation identity is verified.

No successor RFC or architecture workstream is selected, assumed or
pre-authorized by this reconciliation draft.

### Next Exact Action

Review the complete five-document RFC-070 post-closure reconciliation diff.

Do not stage or commit until that review passes.

---

## Current Architecture Governance State — RFC-070 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record creates no new Architecture Decision and does not amend,
replace or supersede AD-056.

AD-056 remains the latest Accepted Architecture Decision.

RFC-070 — Canonical Binary Document Content Store / Access Foundation is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

Verified chain:

- selection commit `13cfccc08d8c0a3b891990d38edaf9fc48874a5e`;
- accepted-contract commit `cfd45d35144574d27a40e0f350b571a6298afd59`;
- technical implementation commit `389ce20b9e01b99cf9b7c1a066a0e9a55bc71223`;
- engineering closure commit `ab4438b02a8f34f83b462e3d8a86b4b5ab5d1092`;
- post-closure reconciliation commit `4fc3e86bf495bbf93158d8e575645e4d556eda39`.

Verified reconciliation Git state:

- reconciliation parent: `ab4438b02a8f34f83b462e3d8a86b4b5ab5d1092`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- reconciliation surface: exactly five maintained Source-of-Truth documents;
- production-code changes: none;
- test-file changes: none.

Preserved technical baseline:

- full PlantMind regression: **928 passed**;
- canonical Alembic head: `0005`;
- canonical `app.document_content.store`;
- `DocumentContentStore`;
- `DocumentContentPayloadAlreadyExistsError`;
- `document_id` remains canonical public association identity;
- descriptor/binary responsibility separation;
- no concrete Infrastructure binary-storage adapter;
- no storage technology selection;
- no cross-boundary transaction coordination;
- no Document Library, parser, OCR, chunking, Search, Vector, Graph, RAG or
  LLM promotion;
- no production-readiness, production-security or Cybersecurity-approval
  claim.

Concrete-adapter behavioral conformance remains:

**NOT YET APPLICABLE / BLOCKED BY ABSENCE OF CONCRETE ADAPTER**

No successor RFC or architecture workstream is selected or preselected by
this record.

Successor selection is a separate evidence-based governance activity.

This final verification record is intentionally non-self-referential.

It records reconciliation commit `4fc3e86bf495bbf93158d8e575645e4d556eda39` and does not contain or predict
the future Git commit that persists this record.

Verification of this record's own commit, push, exact branch identity and
clean working tree is an external Git durability gate and does not require
another RFC-070 Source-of-Truth record.

---

## Current Architecture Governance State — RFC-071 Successor Workstream Selection

**Record Classification: Non-Decision Successor-Selection Governance Record**

Selection baseline:

`3a57f02167e9b69aafee7261b5901b64fe894446`

Last fully closed workstream:

**RFC-070 — Canonical Binary Document Content Store / Access Foundation**

RFC-070 remains:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

No Architecture Decision is created by this selection record.

AD-056 remains the latest Accepted Architecture Decision.

### Chief Architect Selection

The selected successor architecture workstream is:

**RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary**

Selection status:

**SELECTED — REVIEW PASS / STAGING GATE PENDING**

Architecture-contract status:

**NOT YET AUTHORED**

Architecture Decision:

**NOT YET CREATED**

Implementation authorization:

**NO**

### Evidence

Repository and architecture evidence establish:

1. RFC-070 now provides the canonical persistence-neutral
   `DocumentContentStore` port.
2. The canonical port exposes immutable `add(document_id, source)` and exact
   context-managed `open(document_id)` behavior.
3. `app.infrastructure.document_content` currently implements
   descriptor persistence only.
4. No concrete binary `DocumentContentStore` Infrastructure adapter exists.
5. Concrete-adapter behavioral conformance remains blocked specifically by
   absence of a concrete adapter.
6. AD-056 explicitly requires a separately authorized adapter architecture
   before concrete storage behavior may be claimed.
7. Descriptor/payload cross-boundary consistency remains a separate future
   application/coordination responsibility.
8. Document Content establishment/orphan-prevention policy remains a future
   application boundary.
9. Document Library, parser, OCR, chunking, Search, Vector, Graph, RAG and LLM
   remain downstream capabilities.
10. Selecting a higher layer now would leave the canonical binary port without
    a real persistence implementation underneath it.

### Selection Decision

The minimum dependency-completing successor is therefore the Infrastructure
adapter boundary that implements the accepted RFC-070
`DocumentContentStore` contract.

The selection does **not** yet decide:

- filesystem versus network filesystem;
- PostgreSQL binary/large-object storage;
- object storage;
- file server;
- internal physical locator/key structure;
- transparent physical deduplication;
- temporary-file/atomic-publication mechanism;
- durability/fsync policy;
- provider-specific failure translation;
- schema or migration requirements;
- default Runtime/Composition wiring.

Those are architecture-contract questions for RFC-071.

### Required RFC-071 Architecture Questions

The future architecture contract shall explicitly determine:

1. the concrete on-premise binary storage technology;
2. the canonical Infrastructure namespace and adapter class;
3. how the adapter implements `DocumentContentStore`;
4. how external canonical identity remains strictly `document_id`;
5. internal physical addressing rules, if any;
6. duplicate same-document write enforcement;
7. concurrent same-document add race behavior;
8. failed-write partial-publication prevention;
9. zero-byte payload persistence;
10. byte fidelity and ordering;
11. independent `open()` read contexts;
12. normal and exceptional resource cleanup;
13. operational/provider failure propagation;
14. caller-owned source lifecycle preservation;
15. whether an Infrastructure-specific failure hierarchy is justified;
16. crash/durability semantics required for successful `add()`;
17. configuration injection required by the adapter;
18. whether any schema or Alembic change is necessary;
19. whether `DatabaseRuntime` remains completely untouched;
20. whether default `CompositionRoot` remains unwired;
21. exact architecture and behavioral conformance tests;
22. full-regression evidence required for implementation acceptance.

### Explicitly Deferred Candidates

The following candidates are not selected now:

**Document Content / Descriptor Atomic Coordination Boundary**

Deferred because concrete binary persistence is not yet implemented and the
accepted architecture keeps descriptor/payload coordination separate.

**Document Content Establishment / Retrieval Application Boundary**

Deferred because application orchestration shall not absorb or simulate a
missing Infrastructure binary-storage implementation.

**Document Library / Parser / OCR / Chunking Entry Boundary**

Deferred because these are higher-level consumers of canonical binary content
access and shall not become the mechanism that selects or owns storage.

### Non-Goals

RFC-071 selection does not authorize:

- implementation;
- modification of `DocumentContentStore`;
- modification of `DocumentContentRepository`;
- descriptor model changes;
- descriptor/payload transaction coordination;
- Document Content establishment application services;
- Enterprise Document workflow changes;
- Document Library;
- upload/download API or UI;
- parser/PDF/OCR/DOCX/spreadsheet extraction;
- chunking;
- Search/Vector/Graph/RAG/LLM;
- Runtime/Bootstrap/Composition expansion;
- authentication/authorization/RBAC/Active Directory;
- Cybersecurity approval;
- production-readiness claims.

### Selection Git Gate

This selection is not durable until:

1. the complete five-document selection diff is reviewed;
2. exactly the five maintained Source-of-Truth documents are staged;
3. the selection commit is created separately;
4. the selection commit is pushed;
5. exact local / tracking / remote identity is verified;
6. the working tree is clean.

Architecture-contract drafting for RFC-071 shall not begin before that Git
gate is complete.

### Next Exact Action

Stage exactly the five maintained Source-of-Truth documents for a staging-only review.

Do not commit, push or author AD-057 until the staging review passes.

---

## AD-057 — Canonical Filesystem-Backed Binary Document Content Infrastructure Adapter Boundary

### Status

**ACCEPTED — ACCEPTED-CONTRACT GIT GATE PENDING; IMPLEMENTATION NOT AUTHORIZED**

### Related RFC

**RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary**

### Verified Workstream Selection

RFC-071 selection commit:

`92fc4196f24c84d49846ee9825aba9eeb1b03d8b`

Selection parent:

`3a57f02167e9b69aafee7261b5901b64fe894446`

Selection Git durability:

**PASS — LOCAL / TRACKING / REMOTE IDENTITY VERIFIED**

### Context

RFC-070 / AD-056 established the persistence-neutral binary
`DocumentContentStore` contract under:

`app.document_content.store`

The canonical operations remain:

`add(document_id: EntityId, source: BinaryIO) -> None`

and:

`open(document_id: EntityId) -> AbstractContextManager[BinaryIO] | None`

AD-056 deliberately selected no physical storage technology.

RFC-071 now governs the first concrete Infrastructure adapter.

Repository evidence establishes:

- no concrete binary Infrastructure adapter currently exists;
- descriptor persistence remains separately owned by
  `app.infrastructure.document_content`;
- no MinIO/S3/object-storage dependency is established;
- no NFS/SMB-specific dependency or mounted-volume contract is established;
- no evidence requires raw payloads to be persisted inside PostgreSQL;
- PlantMind remains enterprise on-premise;
- production HA, DR, permissions, mounts and Cybersecurity remain separate
  deployment/integration concerns.

### Accepted Decision

PlantMind SHALL introduce one concrete filesystem-backed implementation of:

`DocumentContentStore`

Canonical Infrastructure namespace:

`app.infrastructure.document_content`

Concrete module:

`app.infrastructure.document_content.filesystem_store`

Concrete class:

`FilesystemDocumentContentStore`

The accepted RFC-070 persistence-neutral port SHALL remain unchanged.

### Storage Technology

RFC-071 selects:

**filesystem-backed binary payload persistence using an explicitly injected
storage root**

The filesystem root may represent:

- local isolated storage for development/testing; or
- a separately approved enterprise-mounted filesystem in deployment.

RFC-071 SHALL NOT specifically select or require:

- NFS;
- SMB;
- a particular File Server product;
- Kubernetes PersistentVolume;
- Kubernetes StorageClass;
- PostgreSQL BLOB;
- PostgreSQL large-object storage;
- relational binary tables;
- S3;
- MinIO;
- object storage;
- cloud storage;
- provider-specific storage SDKs.

A mounted enterprise filesystem may host the root only after a separate
deployment/integration gate proves the required filesystem semantics.

### Storage Root Dependency

The adapter constructor SHALL receive:

`root: pathlib.Path`

through explicit dependency injection.

The supplied root SHALL be:

- absolute;
- already existing;
- a directory.

The adapter SHALL NOT:

- read the global `settings` object;
- read environment variables directly;
- perform hidden storage discovery;
- derive storage from `DocumentSource.source_reference`;
- create or provision the deployment storage root;
- own Bootstrap or Runtime lifecycle;
- change `ConfigurationProvider`;
- change default `CompositionRoot`.

Provisioning, permissions, capacity, quota, backup, restore, replication and
mount lifecycle remain deployment responsibilities.

### Adapter-Owned Shard Namespace

The injected storage root itself is deployment-owned and SHALL NOT be created,
recreated or provisioned by the adapter.

The two deterministic UUID shard-directory levels beneath that root are
adapter-owned Infrastructure structure.

Before an `add()` creates or uses shard directories, the adapter SHALL verify
that the configured root still exists and is a directory.

The adapter MAY create only:

`<root>/<h0h1>`

and:

`<root>/<h0h1>/<h2h3>`

when those shard directories are absent.

Shard creation SHALL proceed beneath the already-existing root and SHALL NOT use
recursive parent creation capable of recreating a missing configured root.

Concurrent creation of the same shard directory SHALL be benign when the
existing object is a directory.

If an expected shard component exists but is not a directory, or shard creation
fails for permission, I/O or other operational reasons, that failure SHALL
propagate as an operational filesystem failure.

Shard directories are Infrastructure-private and SHALL NOT become canonical
identity or application-visible storage semantics.

RFC-071 assumes the configured storage namespace is deployment-controlled.
It does not claim protection against hostile external mutation, symlink
substitution or unauthorized filesystem manipulation inside the configured
root.

Production deployment permissions SHALL prevent untrusted mutation of the
adapter-owned storage namespace.

### Canonical Identity

Externally observable payload identity SHALL remain only:

`document_id: EntityId`

No path, filename, inode, hard link, temporary name, digest or provider key
shall become canonical/public identity.

Digest remains integrity metadata only.

### Infrastructure-Private Physical Layout

The final payload path SHALL be derived only from:

`document_id.value.hex`

Accepted layout:

`<root>/<h0h1>/<h2h3>/<uuidhex>.bin`

where:

- `<h0h1>` = first two lowercase UUID hexadecimal characters;
- `<h2h3>` = next two lowercase UUID hexadecimal characters;
- `<uuidhex>` = full 32-character lowercase UUID hexadecimal value.

No caller-controlled path fragment participates in this layout.

The layout is Infrastructure-private and SHALL NOT become a public API.

### Write Source Semantics

`add()` SHALL:

- consume from the supplied source's current position through EOF;
- support non-seekable sources;
- not require `seek()`;
- not require `tell()`;
- not require caller `fileno()`;
- never close the caller-owned source;
- provide no rewind/restore guarantee after failure.

### Streaming Boundary

The adapter SHALL copy source bytes incrementally.

It SHALL NOT require complete payload materialization in memory.

Byte order and byte value SHALL be preserved exactly.

A source already at EOF SHALL establish a valid zero-byte payload.

### Temporary Write Boundary

Every new payload SHALL first be written to a uniquely created temporary file.

The temporary file SHALL:

- reside in the same final shard directory;
- be created exclusively;
- never be returned by `open()`;
- never represent canonical payload presence.

### Pre-Publication Flush

Before publication the adapter SHALL:

1. flush the temporary writable stream;
2. call `os.fsync()` on the temporary file descriptor;
3. close the temporary writable resource.

### Atomic Create-If-Absent Publication

RFC-071 SHALL NOT use an overwrite-capable final publication primitive.

The complete temporary payload SHALL be published using a same-filesystem
hard-link create operation equivalent to:

`os.link(temp_path, final_path)`

The final path SHALL be absent for successful publication.

The hard-link creation operation is the authoritative create-if-absent race
boundary.

### Duplicate Semantics

Only a destination-exists conflict raised by the authoritative final
publication operation:

`os.link(temp_path, final_path)`

SHALL translate to:

`DocumentContentPayloadAlreadyExistsError`

The translation therefore applies only when the final canonical payload path
already exists at the publication boundary.

A `FileExistsError` or equivalent conflict occurring during:

- unique temporary-file creation;
- shard-directory creation;
- unrelated cleanup;
- any operation other than final hard-link publication;

SHALL NOT be translated into canonical duplicate-document identity.

Temporary-name collision MAY be retried with a new unique temporary name.

If it is not retried successfully, it remains an operational filesystem
failure.

Any non-destination-exists `OSError` from `os.link(...)` SHALL remain an
operational filesystem failure and SHALL propagate.

The same canonical duplicate error applies whether the losing payload bytes are
identical or different.

No idempotent success, overwrite, update, replace, append or upsert semantics
shall be introduced.

### Concurrent Same-Document Add

Concurrent `add()` calls for the same `document_id` SHALL produce:

- at most one successful canonical publication;
- no overwrite;
- no interleaving;
- no merge;
- no append;
- canonical duplicate failure for each losing writer.

A process-local lock SHALL NOT be required for correctness.

The filesystem create-if-absent publication primitive SHALL remain the
concurrency authority.

### Pre-Publication Failure

If source reading, temporary writing, flushing, fsync or temporary close fails
before final publication:

- no final canonical payload SHALL become addressable because of that operation;
- temporary cleanup SHALL be attempted;
- the primary operation failure SHALL remain authoritative.

Temporary cleanup failure SHALL NOT transform temporary data into canonical
payload presence.

### Post-Publication Failure

After successful hard-link publication, the final payload is complete.

If temporary unlink/cleanup then fails:

- the complete final payload MAY remain established;
- `add()` MAY propagate the cleanup failure;
- the canonical final payload SHALL NOT be deleted as automatic rollback;
- no partial final payload may result.

A subsequent add for the same `document_id` SHALL encounter the established
final payload and resolve through canonical duplicate semantics.

This boundary is explicitly separate from future descriptor/payload
application-level coordination.

### Cleanup Failure Precedence

Where a primary operation failure already exists, cleanup failure SHOULD remain
diagnostic context rather than silently replace that primary failure.

If cleanup is the only failure after publication, that operational failure MAY
propagate while the complete canonical payload remains established.

Cleanup failure SHALL NOT be translated into duplicate identity.

### Successful Add Guarantee

Normal return from `add()` SHALL establish:

- complete source bytes from current position to EOF;
- pre-publication flush and file fsync;
- complete final canonical publication;
- no partial final payload;
- no overwrite of an existing payload.

### Durability Boundary

RFC-071 establishes code-level durability only through:

- temporary-file flush;
- temporary-file fsync;
- complete atomic filesystem namespace publication.

RFC-071 SHALL NOT claim:

- hardware power-loss durability;
- storage-controller durability;
- directory-entry persistence under every filesystem;
- replication durability;
- HA;
- DR;
- cluster durability.

Those remain deployment/integration properties requiring verification against
the actual approved storage environment.

### Required Filesystem Semantics

A conformant deployment filesystem SHALL support:

- regular binary files;
- exclusive temporary creation;
- same-filesystem hard-link creation;
- atomic destination-exists failure for hard-link publication;
- independent readable file handles;
- file fsync;
- deterministic close and unlink semantics.

If an actual deployment storage technology does not provide these guarantees,
the adapter SHALL NOT be claimed conformant in that deployment.

No overwrite-based fallback publication algorithm is introduced.

### Open Semantics

`open(document_id)` SHALL derive only the deterministic final path.

Before translating a missing final path into confirmed payload absence, the
adapter SHALL verify that the configured storage root still exists and is a
directory.

If the configured root itself is missing or is no longer a directory, that
condition SHALL be treated as storage unavailability and SHALL propagate as an
operational filesystem failure.

When the configured root is healthy:

- an absent first-level shard directory means the payload is confirmed absent;
- an absent second-level shard directory means the payload is confirmed absent;
- an absent final payload path means the payload is confirmed absent.

Those confirmed-absence conditions SHALL return:

`None`

Permission failures, I/O failures and other observable operational filesystem
errors SHALL propagate.

They SHALL NOT become `None`.

A mounted filesystem can fail in ways that leave its mount-point path
syntactically present while exposing a different or empty namespace.

The adapter cannot infer such an externally invisible mount substitution from
path existence alone.

RFC-071 therefore SHALL NOT claim complete mount-loss detection at code level.

Production deployment conformance SHALL ensure that mount loss or namespace
substitution is surfaced through deployment health/readiness or otherwise
prevents requests from being admitted while the configured storage namespace
is unavailable.

### Read Resource Lifecycle

A present payload SHALL yield an adapter-owned binary readable file through the
existing context-manager contract.

Each open SHALL:

- begin at byte zero;
- preserve byte order/value;
- establish an independent read handle.

Closing one handle SHALL NOT invalidate another.

Normal and exceptional context exit SHALL close the adapter-owned read
resource.

Consumers SHALL NOT rely on seekability even though the concrete file may be
seekable.

### Failure Contract

RFC-071 SHALL NOT introduce a generic
`DocumentContentStorageError` hierarchy.

The only adapter-specific canonical translation is:

destination already exists

→

`DocumentContentPayloadAlreadyExistsError`

Other OS/filesystem failures propagate without conversion into duplicate
identity or confirmed absence.

### Descriptor and Repository Separation

The adapter SHALL NOT import, accept, persist, mutate or reconstruct:

- `DocumentContentDescriptor`;
- `DocumentContentMediaType`;
- `DocumentContentDigest`;
- descriptor byte length;
- `DocumentSource`.

It SHALL NOT query:

- `DocumentContentRepository`;
- `EnterpriseDocumentRepository`;
- Knowledge repositories;
- Lineage repositories.

### Database / Migration Boundary

RFC-071 introduces:

- no SQLAlchemy model;
- no binary relational table;
- no BLOB;
- no PostgreSQL large object;
- no foreign key;
- no database constraint;
- no Alembic migration.

Canonical Alembic head remains:

`0005`

`DatabaseRuntime` remains unchanged.

### Dependency Boundary

The adapter SHALL use Python standard-library filesystem primitives.

No new external storage dependency or provider SDK is introduced.

### Runtime / Composition Boundary

RFC-071 SHALL NOT modify or expand:

- `DatabaseRuntime`;
- Runtime;
- Bootstrap;
- readiness;
- request admission;
- `ConfigurationProvider`;
- default `CompositionRoot`;
- `ServiceContainer`;
- `PlatformComposition`;
- `ApplicationFacade`.

RFC-071 SHALL NOT wire a default production
`FilesystemDocumentContentStore`.

The adapter remains explicitly constructible using an injected root.

### Application / Transaction Boundary

RFC-071 introduces no:

- descriptor/payload transaction coordinator;
- content-establishment application service;
- compensation policy;
- retry policy;
- outbox;
- distributed transaction;
- orphan-prevention workflow.

Existing application and coordination services remain unchanged.

### Document Intelligence Boundary

RFC-071 SHALL NOT introduce:

- Document Library;
- upload/download API or UI;
- parser integration;
- PDF extraction;
- OCR;
- DOCX extraction;
- spreadsheet extraction;
- text extraction;
- metadata extraction;
- chunking;
- semantic search;
- embeddings;
- vector persistence;
- graph persistence;
- RAG;
- LLM;
- AI Agent behavior.

### Security Boundary

RFC-071 SHALL NOT claim production:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- malware scanning;
- retention enforcement;
- compliance approval;
- Cybersecurity approval.

Filesystem permissions and access control remain separately governed deployment
concerns.

### Production Implementation Surface

Only after AD-057 architecture acceptance is separately reviewed, committed,
pushed and exact local/tracking/remote identity is verified, followed by a
separate implementation-entry gate, RFC-071 MAY introduce:

`backend/app/infrastructure/document_content/filesystem_store.py`

Focused tests MAY be added under:

`tests/infrastructure/document_content/`

No implementation is authorized by this architecture acceptance.

### Focused Conformance Requirements

Future implementation SHALL verify at minimum:

1. `FilesystemDocumentContentStore` implements `DocumentContentStore`;
2. absolute injected root contract;
3. no hidden global configuration;
4. deterministic document-id physical addressing;
5. Infrastructure-private physical locator;
6. source current-position-to-EOF behavior;
7. non-seekable source support;
8. caller source not closed;
9. zero-byte payload support;
10. byte fidelity/order;
11. same-document duplicate rejection;
12. duplicate identical bytes rejection;
13. duplicate different bytes rejection;
14. same-document concurrent add allows at most one success;
15. losing writer receives canonical duplicate error;
16. no overwrite/append/merge/interleave;
17. source-read failure publishes no partial final payload;
18. temporary-write failure publishes no partial final payload;
19. flush/fsync failure publishes no partial final payload;
20. existing final payload survives later failed add;
21. temporary artifacts do not represent canonical payload presence;
22. missing payload returns `None`;
23. operational access failure does not become `None`;
24. repeated open contexts are independent;
25. normal context exit closes read resource;
26. exceptional context exit closes read resource;
27. reads begin at byte zero;
28. temporary cleanup follows ordinary success;
29. temporary cleanup follows ordinary pre-publication failure;
30. create-if-absent publication is concurrency safe;
31. no descriptor/repository lookup;
32. no SQLAlchemy/Alembic dependency;
33. no Runtime/Bootstrap/Composition wiring;
34. no provider SDK;
35. Alembic head remains `0005`;
36. RFC-070 regressions remain passing;
37. full PlantMind regression remains passing;
38. Python compilation succeeds;
39. `git diff --check` succeeds;
40. the adapter never creates or recreates the configured storage root;
41. missing shard directories may be created safely beneath a healthy root;
42. concurrent shard-directory creation is benign;
43. root disappearance is an operational failure rather than payload absence;
44. missing shard or final path beneath a healthy root returns `None`;
45. temporary-file `FileExistsError` is not translated to document duplicate;
46. only destination-exists conflict from final `os.link(...)` publication maps
    to `DocumentContentPayloadAlreadyExistsError`;
47. other `os.link(...)` failures remain operational failures.

### Deployment Conformance Boundary

Code-level RFC-071 acceptance SHALL NOT mean production deployment readiness.

A later approved integration/deployment verification SHALL prove against the
real configured storage root:

- provisioning;
- permissions;
- capacity/quota;
- same-filesystem temp/final placement;
- hard-link create-if-absent semantics;
- concurrent race behavior;
- file fsync behavior;
- operational failure propagation;
- mount-loss behavior where applicable;
- prevention or reliable detection of namespace substitution beneath a mounted
  storage root;
- request-admission/readiness behavior when mounted storage is unavailable;
- backup/restore;
- HA where required;
- DR where required;
- Cybersecurity-approved access controls.

### Alternatives Considered

#### PostgreSQL BLOB / Large Object

Not selected.

Descriptor metadata already uses PostgreSQL, but raw payload persistence remains
architecturally separate.

Database binary persistence would expand schema, migration and DatabaseRuntime
coupling without current evidence requiring it.

#### On-Prem Object Storage

Not selected.

No accepted MinIO/S3 dependency or object-storage deployment contract currently
exists.

A future adapter may be separately authorized behind the unchanged canonical
store port.

#### Direct File Server Adapter

Not selected.

File Server exists as an external enterprise integration concept, but there is
no accepted direct File Server protocol/storage contract for canonical binary
payload persistence.

An approved enterprise-mounted filesystem may later host this adapter's root if
its required semantics pass deployment verification.

#### Network-Filesystem-Specific Adapter

Not selected.

No NFS/SMB-specific architecture currently exists.

The adapter depends on filesystem semantics, not a named network product.

### Consequences

PlantMind gains its first concrete binary payload persistence adapter while:

- preserving RFC-070 identity and lifecycle semantics;
- preserving descriptor/binary separation;
- avoiding premature PostgreSQL BLOB coupling;
- avoiding premature object-storage dependencies;
- supporting isolated local development;
- allowing future enterprise-mounted storage after verification;
- allowing future alternative adapters behind the same port;
- preserving future descriptor/payload coordination as a separate application
  responsibility.

### Architecture Review State

**ACCEPTED — ACCEPTED-CONTRACT GIT GATE PENDING**

Final refined architecture review:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

AD-057 is accepted as the RFC-071 architecture contract.

Implementation remains:

**NOT AUTHORIZED**

### Acceptance Boundary

Architecture acceptance establishes the reviewed AD-057 contract as the
current intended Source-of-Truth state.

Acceptance does not itself authorize implementation.

The accepted contract is not externally durable until:

1. the complete five-document acceptance state passes review;
2. exactly the five Source-of-Truth documents are staged;
3. the accepted-contract commit is created;
4. that commit is pushed;
5. local / tracking / remote identity is exact;
6. the working tree is clean.

Only after that Git durability gate may the separate RFC-071 implementation
entry gate be evaluated.

### Next Exact Action

Review the complete five-document RFC-071 / AD-057 architecture acceptance
state.

Do not stage until that acceptance-state review passes.

Do not implement before the accepted-contract Git durability gate and the
separate implementation-entry gate both pass.

---

## RFC-071 / AD-057 Engineering Closure Record

### Closure Baseline

RFC-071 workstream:

**Canonical Binary Document Content Infrastructure Adapter Boundary**

Accepted architecture decision:

**AD-057 — Canonical Filesystem-Backed Binary Document Content Infrastructure Adapter Boundary**

Verified workstream-selection commit:

`92fc4196f24c84d49846ee9825aba9eeb1b03d8b`

Verified accepted-contract commit:

`14b2b56e9395b680da7aaca1a98515eea3a71b01`

Verified technical implementation commit:

`9b556850adc011afca41cd6740a0265be03a2aa8`

Technical Git durability:

**PASS — LOCAL / TRACKING / REMOTE IDENTITY VERIFIED**

### Verified Technical Outcome

RFC-071 establishes the first concrete Infrastructure implementation of the
canonical persistence-neutral binary Document Content store contract.

Concrete adapter:

`FilesystemDocumentContentStore`

Canonical module:

`app.infrastructure.document_content.filesystem_store`

The adapter implements the existing RFC-070 `DocumentContentStore` port without
modifying that port.

The verified implementation preserves these AD-057 boundaries:

- explicitly injected absolute filesystem root;
- deployment-owned root must already exist;
- deterministic adapter-owned UUID shard directories beneath that root;
- Infrastructure-private physical addressing;
- caller-owned source consumed from current position through EOF;
- non-seekable sources supported;
- caller source never closed;
- zero-byte payload valid;
- incremental streaming;
- same-shard temporary file;
- flush and file `fsync` before publication;
- `os.link(temp_path, final_path)` as atomic create-if-absent publication;
- only final-link destination conflict maps to
  `DocumentContentPayloadAlreadyExistsError`;
- unrelated filesystem failures remain operational failures;
- no overwrite, update, append, merge, upsert or idempotent success;
- concurrent same-document add permits at most one successful publication;
- failed pre-publication operation exposes no canonical partial payload;
- post-publication cleanup failure may leave a complete payload but never a
  partial canonical payload;
- confirmed absence returns `None` only beneath a healthy root;
- root unavailability remains operational failure;
- independent read handles begin at byte zero and close deterministically.

### RFC-069 Historical-Test Reconciliation

The initial RFC-071 full regression exposed two RFC-069 historical architecture
expectations that predated any binary Infrastructure adapter.

Failure classification occurred before test mutation.

Production rewrite was neither authorized nor required.

The historical test was reconciled narrowly so that:

- RFC-069 relational Infrastructure files remain prohibited from owning the
  binary `DocumentContentStore` contract;
- `filesystem_store.py` is the only RFC-071-authorized binary-store owner;
- RFC-069 relational invariants remain protected;
- the historical architecture guard is not broadly weakened.

### Verification Evidence

Pre-implementation regression:

**928 passed**

Initial RFC-071 focused verification:

**43 passed**

Initial full regression:

**953 passed / 2 failed**

Failure classification:

**PASS — HISTORICAL RFC-069 TEST RECONCILIATION REQUIRED**

After narrow reconciliation:

- RFC-069 architecture verification: **9 passed**;
- RFC-071 focused plus historical verification: **52 passed**;
- full PlantMind regression: **956 passed**.

Technical staging review:

**PASS**

Technical commit review:

**PASS**

Technical push and exact Git durability:

**PASS**

### Persistence / Runtime Boundaries

RFC-071 introduced no:

- Domain model change;
- canonical store-port change;
- descriptor-repository change;
- SQLAlchemy binary model;
- PostgreSQL BLOB or large-object persistence;
- database schema change;
- Alembic migration;
- `DatabaseRuntime` expansion;
- default `CompositionRoot` wiring;
- provider SDK;
- object-storage dependency;
- application coordination service;
- Document Library / Parser / OCR / Chunking;
- Search / Vector / Graph / RAG / LLM capability.

Canonical Alembic head remains:

`0005`

### Deployment Conformance Boundary

Code-level RFC-071 verification does not establish production storage readiness.

Actual deployment storage still requires separately governed verification for:

- provisioning;
- permissions;
- capacity / quota;
- same-filesystem temporary/final placement;
- hard-link create-if-absent semantics;
- concurrency behavior;
- file-fsync behavior;
- mount-loss / namespace-substitution handling where applicable;
- backup / restore;
- HA / DR where required;
- Cybersecurity-approved controls.

No production HA, DR, mounted-storage or Cybersecurity completion claim is made.

### Engineering Closure State

Technical implementation:

**COMPLETE / COMMITTED / PUSHED / EXACT GIT IDENTITY VERIFIED**

Closure documentation:

**AUTHORED — REVIEW PENDING**

RFC-071 terminal closure:

**NOT YET CLAIMED**

Source-of-Truth reconciliation:

**PENDING — SEPARATE POST-CLOSURE GATE**

Successor workstream:

**NONE SELECTED**

### Next Exact Action

Review the complete five-document RFC-071 engineering closure documentation.

Do not stage closure documentation until that review passes.

Do not claim terminal closure until the closure commit/push gate and the
subsequent Source-of-Truth reconciliation are completed separately.

---

## Current Architecture Governance State — RFC-071 Post-Closure Source-of-Truth Reconciliation

**Record Classification: Non-Decision Reconciliation Governance Record**

This record creates no new Architecture Decision.

It does not amend, replace or supersede AD-057.

AD-057 remains:

**ACCEPTED**

RFC-071 workstream:

**Canonical Binary Document Content Infrastructure Adapter Boundary**

### Verified Durable Chain

Selection commit:

`92fc4196f24c84d49846ee9825aba9eeb1b03d8b`

Accepted-contract commit:

`14b2b56e9395b680da7aaca1a98515eea3a71b01`

Technical implementation commit:

`9b556850adc011afca41cd6740a0265be03a2aa8`

Engineering closure commit:

`c725163808d88d5b89e034b608eb51829efd0f4b`

Closure commit parent:

`9b556850adc011afca41cd6740a0265be03a2aa8`

Closure push / exact local-tracking-remote identity:

**PASS**

Working tree at reconciliation entry:

**CLEAN**

### Reconciliation Scope

This Source-of-Truth reconciliation records the durable RFC-071 closure state
without rewriting the committed RFC-071 engineering closure record.

Current maintained Source-of-Truth surfaces are reconciled so that:

- RFC-071 closure is recorded as committed, pushed and exact-identity verified;
- the verified full regression remains **956 passed**;
- canonical Alembic head remains `0005`;
- AD-057 remains the latest Accepted Architecture Decision;
- the concrete `FilesystemDocumentContentStore` remains the delivered RFC-071
  Infrastructure adapter;
- the RFC-069 historical-test reconciliation remains part of the durable
  RFC-071 technical commit;
- no production code, test, schema, migration, Runtime, Composition or provider
  SDK change is introduced by reconciliation;
- production deployment conformance remains separately governed and unclaimed.

### Governance State

Reconciliation documentation:

**AUTHORED — REVIEW PENDING**

Post-closure reconciliation commit:

**NOT YET CREATED**

Post-closure reconciliation push / exact identity verification:

**NOT YET PERFORMED**

Final reconciliation verification record:

**NOT YET CREATED**

RFC-071 terminal closure:

**NOT YET CLAIMED**

Successor selection:

**NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document RFC-071 post-closure reconciliation diff.

Do not stage reconciliation until that review passes.

Do not declare RFC-071 fully closed until reconciliation commit/push exact
identity verification and the separate final reconciliation verification record
are complete.

---

## Current Architecture Governance State — RFC-071 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record creates no new Architecture Decision and does not amend,
replace or supersede AD-057.

AD-057 remains the latest Accepted Architecture Decision.

RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

### Verified Commit Chain

- selection commit `92fc4196f24c84d49846ee9825aba9eeb1b03d8b`;
- accepted-contract commit `14b2b56e9395b680da7aaca1a98515eea3a71b01`;
- technical implementation commit `9b556850adc011afca41cd6740a0265be03a2aa8`;
- engineering closure commit `c725163808d88d5b89e034b608eb51829efd0f4b`;
- post-closure reconciliation commit `a6ad9bac7745a8c7e4583b9373acb3cbe889df75`.

### Verified Reconciliation Git State

- reconciliation parent: `c725163808d88d5b89e034b608eb51829efd0f4b`;
- reconciliation push: **PASS**;
- exact local / tracking / remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **clean**;
- reconciliation surface: exactly five maintained Source-of-Truth documents;
- production-code changes: none;
- test-file changes: none.

### Preserved Technical Baseline

- full PlantMind regression: **956 passed**;
- canonical Alembic head: `0005`;
- canonical persistence-neutral binary store port remains unchanged;
- concrete Infrastructure adapter:
  `app.infrastructure.document_content.filesystem_store.FilesystemDocumentContentStore`;
- descriptor/binary responsibility separation remains preserved;
- RFC-069 relational persistence invariants remain protected;
- no database schema or Alembic expansion;
- no `DatabaseRuntime` expansion;
- no default `CompositionRoot` wiring;
- no provider SDK or object-storage dependency;
- no application coordination, Document Library, parser, OCR, chunking,
  Search, Vector, Graph, RAG or LLM capability is promoted by RFC-071.

Production deployment conformance remains separately governed.

No production HA, DR, mounted-storage, production-security or Cybersecurity
completion claim is made.

### Successor Governance

No successor RFC or architecture workstream is selected or preselected by
this record.

Successor selection is a separate evidence-based governance activity.

### Non-Self-Referential Final Record

This final verification record is intentionally non-self-referential.

It records reconciliation commit `a6ad9bac7745a8c7e4583b9373acb3cbe889df75` and does not contain,
predict or require the future Git commit hash that persists this record.

Verification of this record's own commit, push, exact local / tracking / remote
identity and clean working tree is an external Git durability gate.

That external Git gate does not require another RFC-071 Source-of-Truth record.

---

## Selected Successor Architecture Workstream — RFC-072 — Canonical Document Content Establishment Application Coordination Boundary

**Record Classification: Non-Decision Successor Workstream Selection**

This record creates no new Architecture Decision.

AD-057 remains the latest Accepted Architecture Decision.

No AD-058 is created or accepted by this selection record.

### Selection Baseline

Last fully closed workstream:

**RFC-071 — Canonical Binary Document Content Infrastructure Adapter Boundary**

RFC-071 final verification commit:

`0363365989786c51d6757fb09662622dc54d5b44`

Full regression baseline:

**956 passed**

Canonical Alembic head:

`0005`

### Selected Successor

The next architecture workstream is selected as:

**RFC-072 — Canonical Document Content Establishment Application Coordination Boundary**

This is the smallest coherent architecture gap whose prerequisite
Document Content foundations are now durable.

### Evidence

The repository establishes all of the following:

1. canonical immutable Document Content Domain semantics already exist;
2. canonical `DocumentContentRepository` descriptor persistence exists;
3. canonical `DocumentContentStore` binary storage/access port exists;
4. the concrete RFC-071 filesystem Infrastructure adapter exists;
5. there is currently no application-layer consumer of
   `DocumentContentStore`;
6. content-establishment/application coordination was explicitly deferred
   as a separately governed future application boundary;
7. existing Document-to-Knowledge ingestion and Knowledge/Lineage transaction
   coordination already own distinct responsibilities and shall not be
   duplicated or absorbed;
8. Document Library, parser, OCR and chunking remain downstream;
9. Search, Vector, Graph, RAG and LLM remain higher-level dependent work;
10. default Runtime/Composition wiring remains intentionally absent;
11. filesystem production deployment conformance remains separately governed.

### RFC-072 Architecture Questions

RFC-072 architecture authoring must explicitly resolve, before implementation:

- the exact application use case for canonical Document Content establishment;
- which accepted persistence-neutral ports the application boundary consumes;
- whether canonical Document existence must be confirmed;
- descriptor/payload operation ordering;
- descriptor/payload consistency semantics;
- duplicate classification across descriptor and binary boundaries;
- failure behavior before and after payload publication;
- whether any compensating behavior is architecturally legal;
- retry and idempotency semantics;
- observable state when one persistence boundary succeeds and another fails;
- how the accepted no-overwrite/no-delete binary-store semantics constrain
  coordination;
- whether a new narrow coordination abstraction is required or whether
  application orchestration alone is sufficient;
- preservation of storage-provider neutrality at the Application layer.

These are architecture questions, not implementation decisions.

### Explicit Non-Selection

RFC-072 does **not** select or authorize:

- Document Library behavior;
- parser, PDF extraction, OCR or chunking;
- Search, embeddings or Vector persistence;
- Graph persistence or Neo4j production integration;
- RAG or LLM capability;
- default `CompositionRoot`, Runtime or Bootstrap wiring;
- production filesystem deployment conformance;
- production PostgreSQL or filesystem readiness;
- production security or Cybersecurity approval.

### Selection State

Successor workstream decision:

**SELECTED — RFC-072**

Architecture contract:

**NOT YET AUTHORED**

Architecture Decision:

**NONE CREATED — AD-057 REMAINS LATEST ACCEPTED**

Implementation:

**NOT AUTHORIZED**

The selection record is intentionally non-self-referential.

Its own commit/push/exact Git durability shall be verified externally before
RFC-072 architecture authoring begins.

---

# AD-058 — Canonical Document Content Establishment Application Coordination Boundary

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

## RFC-072 / AD-058 Engineering Closure Record

**Record Classification: Non-Decision Engineering Closure Governance Record**

This section creates no new Architecture Decision.

It does not amend, replace, supersede or rewrite AD-058.

AD-058 remains:

**ACCEPTED**

### Closure Baseline

RFC-072 workstream:

**Canonical Document Content Establishment Application Coordination Boundary**

Verified workstream-selection commit:

`0c9a8cba53221f547d340fa499f1ac7d07d1e7d3`

Verified accepted-contract commit:

`aa444f1f339c6aa00d37a9b3f0f564f3b5b6c06e`

Verified technical implementation commit:

`81a137d117df65c5beebd1fb935ca5b48e014733`

Technical Git durability:

**PASS — LOCAL / TRACKING / REMOTE IDENTITY VERIFIED**

### Verified Technical Outcome

RFC-072 establishes:

`DocumentContentEstablishmentApplicationService`

under:

`app.services.document_content_establishment_application_service`

with exactly the accepted persistence-neutral dependencies:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`.

The technical implementation preserves AD-058 semantics for:

- Document-existence verification before content mutation;
- payload-first fresh establishment;
- Application-derived canonical byte length and SHA-256;
- current-position-to-EOF caller-source consumption;
- non-seekable sources;
- caller-source ownership;
- zero-byte content;
- descriptor-present / payload-absent integrity classification;
- payload-present / descriptor-absent verified recovery;
- exact complete-state convergence;
- persisted-state integrity verification;
- racing binary-store duplicate conflict classification;
- exact descriptor-duplicate reconciliation only;
- operational-failure propagation;
- no automatic payload rollback/deletion;
- no automatic retry loop;
- no distributed cross-store atomicity claim.

### Verification Evidence

RFC-072 focused service and architecture verification:

**39 passed**

Relevant prior-boundary regression:

**175 passed**

Full PlantMind regression:

**995 passed**

Python compilation:

**PASS**

Reviewed and durable technical diff SHA-256:

`66ea75b2fbdccd1e423f123590261900f59e05679d7c708874600880dc3e0100`

Canonical Alembic head remains:

`0005`

### Architecture Preservation

RFC-072 introduced no:

- new ARCH-001 layer;
- Domain redesign;
- repository/store-port redesign;
- concrete Infrastructure dependency in the Application service;
- SQLAlchemy dependency in the Application service;
- schema or migration change;
- `DatabaseRuntime` expansion;
- default Runtime / Composition / Bootstrap wiring;
- generic transaction coordinator;
- Document Library / parser / OCR / chunking promotion;
- Search / Vector / Graph / RAG / LLM promotion;
- authentication / authorization / RBAC / Active Directory implementation;
- production-security readiness claim;
- Cybersecurity approval claim.

Existing AD-050 Knowledge/Lineage transaction coordination remains unchanged.

Existing RFC-069, RFC-070 and RFC-071 Document Content boundaries remain
authoritative.

### Engineering Closure State

Technical implementation:

**COMPLETE / COMMITTED / PUSHED / EXACT GIT IDENTITY VERIFIED**

Closure documentation:

**AUTHORED — REVIEW PENDING**

RFC-072 terminal closure:

**NOT YET CLAIMED**

Post-closure Source-of-Truth reconciliation:

**PENDING — SEPARATE POST-CLOSURE GATE**

Successor workstream:

**NONE SELECTED**

### Next Exact Action

Review the complete five-document RFC-072 engineering closure documentation.

Do not stage closure documentation until that review passes.

Do not claim terminal closure until closure Git durability and the subsequent
Source-of-Truth reconciliation complete separately.

---

## Current Architecture Governance State — RFC-072 Post-Closure Source-of-Truth Reconciliation

**Record Classification: Non-Decision Reconciliation Governance Record**

This record creates no new Architecture Decision.

It does not amend, replace or supersede AD-058.

AD-058 remains:

**ACCEPTED**

RFC-072 workstream:

**Canonical Document Content Establishment Application Coordination Boundary**

### Verified Durable Chain

Selection commit:

`0c9a8cba53221f547d340fa499f1ac7d07d1e7d3`

Accepted-contract commit:

`aa444f1f339c6aa00d37a9b3f0f564f3b5b6c06e`

Technical implementation commit:

`81a137d117df65c5beebd1fb935ca5b48e014733`

Engineering closure commit:

`99066acafd76205ba41d7997eba7486d2f572fc7`

Closure commit parent:

`81a137d117df65c5beebd1fb935ca5b48e014733`

Closure push / exact Local / Tracking / Remote identity:

**PASS**

Working tree at reconciliation entry:

**CLEAN**

### Reconciliation Scope

This Source-of-Truth reconciliation records the durable RFC-072 closure state
without rewriting the committed RFC-072 engineering closure record.

The maintained Source-of-Truth surfaces are reconciled so that:

- RFC-072 closure is recorded as committed, pushed and exact-identity verified;
- the verified full regression remains **995 passed**;
- canonical Alembic head remains `0005`;
- AD-058 remains Accepted;
- `DocumentContentEstablishmentApplicationService` remains the delivered
  RFC-072 Application boundary;
- RFC-069/RFC-070/RFC-071 Document Content responsibilities remain preserved;
- no production code, test, schema, migration, Runtime, Composition or
  Bootstrap change is introduced;
- no Document Library, parser/OCR/chunking, Search/Vector/Graph/RAG/LLM or
  production-security capability is promoted;
- production deployment conformance remains separately governed and unclaimed.

### Governance State

Reconciliation documentation:

**AUTHORED — REVIEW PENDING**

Post-closure reconciliation commit:

**NOT YET CREATED**

Post-closure reconciliation push / exact identity verification:

**NOT YET PERFORMED**

Final reconciliation verification record:

**NOT YET CREATED**

RFC-072 terminal closure:

**NOT YET CLAIMED**

Successor selection:

**NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document RFC-072 post-closure reconciliation diff.

Do not stage reconciliation until that review passes.

Do not declare RFC-072 fully closed until reconciliation commit/push exact
identity verification and the separate final reconciliation verification
record are complete.

---

## Current Architecture Governance State — RFC-072 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record creates no new Architecture Decision and does not amend, replace
or supersede AD-058.

AD-058 remains the latest Accepted Architecture Decision.

RFC-072 — Canonical Document Content Establishment Application Coordination Boundary
is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

### Verified Commit Chain

- selection commit `0c9a8cba53221f547d340fa499f1ac7d07d1e7d3`;
- accepted-contract commit `aa444f1f339c6aa00d37a9b3f0f564f3b5b6c06e`;
- technical implementation commit `81a137d117df65c5beebd1fb935ca5b48e014733`;
- engineering closure commit `99066acafd76205ba41d7997eba7486d2f572fc7`;
- post-closure reconciliation commit `3fab31e046c47c90a0b3a10467570af646273011`.

### Verified Reconciliation Git State

- reconciliation parent:
  `99066acafd76205ba41d7997eba7486d2f572fc7`;
- reconciliation push: **PASS**;
- exact Local / Tracking / Remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **CLEAN**;
- reconciliation surface: exactly five maintained Source-of-Truth documents;
- production-code changes: none;
- test-file changes: none.

### Preserved Technical Baseline

- full PlantMind regression: **995 passed**;
- canonical Alembic head: `0005`;
- delivered RFC-072 Application boundary:
  `app.services.document_content_establishment_application_service.DocumentContentEstablishmentApplicationService`;
- canonical Enterprise Document repository responsibility remains unchanged;
- canonical Document Content descriptor repository responsibility remains unchanged;
- canonical binary Document Content store responsibility remains unchanged;
- RFC-069 relational descriptor adapter remains unchanged;
- RFC-071 filesystem-backed binary store remains unchanged;
- no schema or Alembic expansion;
- no `DatabaseRuntime` expansion;
- no default Runtime / Composition / Bootstrap wiring;
- no Document Library / parser / OCR / chunking promotion;
- no Search / Vector / Graph / RAG / LLM promotion;
- no production-security or Cybersecurity completion claim.

Production deployment conformance remains separately governed.

### Successor Governance

No successor RFC or Architecture workstream is selected or preselected by
this record.

Successor selection is a separate evidence-based governance activity.

### Non-Self-Referential Final Record

This final verification record is intentionally non-self-referential.

It records reconciliation commit:

`3fab31e046c47c90a0b3a10467570af646273011`

and does not contain, predict or require the future Git commit hash that
persists this record.

Verification of this record's own commit, push, exact Local / Tracking / Remote
identity and clean working tree is an external Git durability gate.

That external gate does not require another RFC-072 Source-of-Truth record.

---

## Current Architecture Governance State — Post-RFC-072 Successor Workstream Selection Draft

**Record Classification: Non-Decision Successor-Selection Governance Record**

This record creates no new Architecture Decision.

Latest Accepted Architecture Decision remains:

**AD-058 — Canonical Document Content Establishment Application Coordination Boundary**

RFC-072 remains:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

### Candidate Successor

**RFC-073 — Canonical Document Content Access Application Boundary**

Selection baseline:

`60ede75cb850101afbcf08f6cac18cce3a04ef43`

### Dependency Evidence

The accepted architecture now contains:

- canonical Enterprise Document identity;
- canonical Document Content descriptor semantics;
- descriptor repository and relational persistence;
- canonical binary Document Content Store / Access foundation;
- concrete filesystem-backed binary adapter;
- canonical Document Content establishment Application coordination.

The current Application surface has no dedicated general content-access
Application boundary for downstream consumers.

RFC-072 explicitly requires future parser behavior to consume canonical bytes
through an accepted Application/access path and prohibits reinterpretation of
`source_reference` as canonical binary storage.

RFC-073 is therefore selected in this local draft as the smallest
dependency-completing architecture candidate before Document Intelligence
capabilities are promoted.

### Boundaries Preserved

RFC-073 selection does not itself authorize:

- an API or UI;
- Document Library behavior;
- parser/OCR/chunking;
- extraction;
- Search/Vector/Graph/RAG/LLM;
- Runtime / Composition / Bootstrap wiring;
- schema or Alembic expansion;
- authentication / authorization / RBAC / Active Directory;
- production deployment or Cybersecurity claims.

The future RFC-073 architecture contract must first define the exact
Application access semantics and accepted dependencies.

### Selection Gate

Selection documentation:

**AUTHORED — REVIEW PENDING**

Selection commit:

**NOT YET CREATED**

Selection push:

**NOT PERFORMED**

Exact Local / Tracking / Remote selection identity:

**NOT YET APPLICABLE**

Active RFC:

**NONE**

Architecture Decision:

**NOT CREATED**

Architecture contract:

**NOT AUTHORED**

Implementation:

**NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document successor-selection diff.

Only after selection documentation is reviewed, staged, committed, pushed and
verified exact may RFC-073 become the active architecture workstream and
architecture drafting begin.

---

## AD-059 — Canonical Document Content Access Application Boundary

**Status: DRAFT — NOT ACCEPTED**

**RFC: RFC-073**

Selection commit:

`059fbcbf404da390079ca77685eb2135e663e80d`

Selection Git durability:

**PASS — LOCAL / TRACKING / REMOTE EXACT IDENTITY VERIFIED**

Latest Accepted Architecture Decision remains:

**AD-058 — Canonical Document Content Establishment Application Coordination Boundary**

### Context

PlantMind now has a complete canonical Document Content foundation through:

1. canonical `EnterpriseDocument` identity;
2. canonical immutable `DocumentContentDescriptor`;
3. persistence-neutral `DocumentContentRepository`;
4. relational descriptor persistence;
5. persistence-neutral `DocumentContentStore`;
6. concrete `FilesystemDocumentContentStore`;
7. RFC-072 canonical Document Content establishment Application coordination.

The accepted binary store already exposes:

`open(document_id) -> AbstractContextManager[BinaryIO] | None`

where `None` represents confirmed payload absence.

The Application layer does not yet expose a dedicated general read/access use
case for downstream consumers.

RFC-072 explicitly preserved the requirement that future parser behavior
consume canonical bytes through an accepted Application/access path rather
than reinterpreting:

`EnterpriseDocument.source.source_reference`

as binary storage.

### Decision

RFC-073 shall introduce one narrow read-only Application service:

`DocumentContentAccessApplicationService`

under:

`app.services.document_content_access_application_service`

implemented, if later authorized, at:

`backend/app/services/document_content_access_application_service.py`

RFC-073 introduces no new ARCH-001 layer.

### Canonical Public Surface

The RFC-073 module shall expose exactly these public RFC-073 classes:

- `DocumentContentAccessRequest`;
- `DocumentContentAccess`;
- `DocumentContentAccessDocumentNotFoundError`;
- `DocumentContentAccessContentNotFoundError`;
- `DocumentContentAccessIntegrityError`;
- `DocumentContentAccessApplicationService`.

No package-level re-export is required.

Existing package initializers shall remain unchanged unless separately
reviewed.

### Request Contract

`DocumentContentAccessRequest` shall be:

- a dataclass;
- frozen;
- slots-based;
- keyword-only.

It shall contain exactly:

`document_id: EntityId`

RFC-073 shall not accept:

- filesystem paths;
- storage roots;
- source references;
- URLs;
- media-type search criteria;
- digest lookup keys;
- arbitrary repository filters.

Canonical association identity remains:

`document_id`

### Access Value

`DocumentContentAccess` shall be:

- a dataclass;
- frozen;
- slots-based;
- keyword-only.

It shall contain exactly:

- `descriptor: DocumentContentDescriptor`;
- `payload: BinaryIO`.

The `payload` member is store-owned and context-bound.

The value does not transfer persistence ownership to the caller.

### Application Service Dependencies

`DocumentContentAccessApplicationService` shall depend exactly on:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`.

It shall not depend directly on:

- SQLAlchemy;
- `DatabaseRuntime`;
- filesystem APIs;
- `pathlib.Path`;
- `FilesystemDocumentContentStore`;
- parser modules;
- OCR modules;
- Search;
- Vector DB;
- Graph DB;
- RAG;
- LLM;
- Runtime;
- Composition;
- Bootstrap.

### Application Operation

The canonical RFC-073 use case shall be:

`open(request: DocumentContentAccessRequest) -> AbstractContextManager[DocumentContentAccess]`

The returned context manager owns the Application access lifecycle.

Repository and store evaluation may occur when entering that context.

A consumer shall use the access only within the returned context-manager
lifecycle.

### Canonical Document Gate

RFC-073 shall first resolve:

`EnterpriseDocumentRepository.get(document_id)`

If the canonical Enterprise Document is absent, RFC-073 shall raise:

`DocumentContentAccessDocumentNotFoundError`

The service shall not expose orphan descriptor or orphan payload content when
the canonical Enterprise Document is absent.

It shall not use `source_reference` as fallback access.

RFC-073 is not an orphan-content audit capability.

### Descriptor / Payload Observation

After canonical Document existence is confirmed, RFC-073 shall observe:

`DocumentContentRepository.get(document_id)`

and:

`DocumentContentStore.open(document_id)`

Sequential observation is intentional.

RFC-073 does not claim those observations form one distributed, transactional
or linearizable snapshot.

### Canonical State Matrix

For an existing canonical Enterprise Document:

#### Descriptor absent / payload absent

Classification:

**CONTENT NOT FOUND**

Raise:

`DocumentContentAccessContentNotFoundError`

#### Descriptor present / payload absent

Classification:

**INTEGRITY ERROR**

Raise:

`DocumentContentAccessIntegrityError`

No automatic descriptor deletion or repair is permitted.

#### Descriptor absent / payload present

Classification:

**INTEGRITY ERROR**

Raise:

`DocumentContentAccessIntegrityError`

The non-None payload context shall be safely closed.

RFC-073 shall not reconstruct a descriptor because media-type ownership and
content establishment belong to RFC-072.

#### Descriptor present / payload present

The payload shall be fully verified before delivery.

### Pre-Delivery Integrity Verification

A successful RFC-073 access shall not expose unverified canonical bytes.

RFC-073 therefore selects:

**VERIFY → CLOSE → REOPEN → DELIVER**

The verification pass shall:

1. enter the first non-None store-owned payload context;
2. consume the canonical payload from byte zero through EOF;
3. count exact bytes;
4. calculate SHA-256 over those exact bytes;
5. compare byte length with `descriptor.byte_length`;
6. compare digest with `descriptor.digest`;
7. close the verification payload context before delivery begins.

Verification shall perform no:

- normalization;
- decoding;
- decompression;
- parsing;
- OCR;
- character conversion;
- metadata extraction;
- chunking;
- semantic transformation.

### Streaming Requirements

The verification algorithm shall be incremental.

It shall not require:

- complete payload buffering in memory;
- `seek()`;
- `tell()`;
- `fileno()`;
- an Application-owned temporary file;
- an Application-owned filesystem cache.

Zero-byte canonical payloads remain valid and shall verify against their
canonical descriptor normally.

### Verification Failure

If observed payload byte length differs from:

`descriptor.byte_length`

or calculated SHA-256 differs from:

`descriptor.digest.value`

RFC-073 shall raise:

`DocumentContentAccessIntegrityError`

The unverified payload shall never be yielded to the consumer.

### Delivery Reopen

After successful verification, RFC-073 shall call:

`DocumentContentStore.open(document_id)`

again.

The verification context must already be closed before this second open is
used for delivery.

This second open is selected instead of rewind because the persistence-neutral
store contract does not require a seekable stream.

If the delivery reopen returns `None` after successful verification, RFC-073
shall raise:

`DocumentContentAccessIntegrityError`

because an accepted immutable canonical payload cannot legitimately disappear
between successful verification and delivery access through the same
conforming store contract.

### Delivery Context

When the delivery reopen succeeds, RFC-073 shall yield:

`DocumentContentAccess(descriptor=descriptor, payload=payload)`

inside the delivery store context.

The delivery `payload`:

- begins at canonical byte zero;
- is readable incrementally;
- need not be seekable;
- need not provide `fileno()`;
- is valid only during the Application context;
- is closed when the Application context exits.

RFC-073 shall guarantee context closure when:

- the consumer completes normally;
- the consumer raises;
- downstream parsing later raises;
- the caller exits early.

The consumer shall not retain the payload for use after context exit.

### Integrity Versus Delivery Pass

The first pass is the canonical pre-delivery integrity verification.

The second pass is the consumer delivery stream.

RFC-073 does not require a third pass.

The architecture relies on the accepted immutability of the canonical
`DocumentContentStore` contract between those two opens.

It does not claim protection against out-of-band filesystem tampering,
host compromise or storage-media corruption occurring outside accepted store
semantics.

Production tamper detection and infrastructure integrity monitoring remain
separate Cybersecurity/deployment concerns.

### No Automatic Recovery

RFC-073 is read-only.

It shall never call:

- `EnterpriseDocumentRepository.add()`;
- `DocumentContentRepository.add()`;
- `DocumentContentStore.add()`.

It shall introduce no:

- update;
- delete;
- overwrite;
- upsert;
- repair;
- descriptor reconstruction;
- payload reconstruction;
- compensating transaction;
- retry loop.

Incomplete canonical state is reported, not repaired.

RFC-072 remains the canonical establishment/recovery Application use case.

### Operational Failure Propagation

Operational failures from:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- verification payload reads;
- delivery payload open;

shall propagate unless this contract explicitly classifies the observable state
as an RFC-073 Application error.

RFC-073 shall not introduce a generic catch-all storage/repository error
hierarchy.

### `source_reference` Decision

`EnterpriseDocument.source.source_reference` remains external provenance and
traceability only.

RFC-073 shall not:

- call `open(source_reference)`;
- interpret it as a filesystem path;
- interpret it as a storage key;
- treat it as a canonical URI;
- use it for payload lookup;
- use it for deduplication;
- use it as canonical Document identity;
- derive binary storage topology from it.

The only canonical content association key is:

`document_id`

### Responsibility Preservation

RFC-073 shall not modify or absorb the responsibility of:

- `EnterpriseDocumentRegistrationApplicationService`;
- `DocumentContentEstablishmentApplicationService`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeCaptureApplicationService`;
- `KnowledgeLineageTransactionCoordinator`;
- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- `FilesystemDocumentContentStore`;
- `EnterpriseDocument`;
- `DocumentContentDescriptor`.

Registration remains registration.

Establishment and incomplete-state recovery remain RFC-072 responsibility.

RFC-073 owns verified read access only.

### Parser / Document Intelligence Boundary

RFC-073 does not implement a parser.

A future parser may consume:

`DocumentContentAccess.payload`

only after RFC-073 is accepted, technically implemented and wired through its
own separately governed Application capability.

RFC-073 does not determine:

- PDF parsing;
- DOCX parsing;
- spreadsheet parsing;
- text extraction;
- encoding detection;
- OCR;
- metadata extraction;
- chunking strategy;
- parser result persistence;
- Knowledge generation.

### Document Library Boundary

RFC-073 is not a Document Library.

It does not introduce:

- browse;
- catalogue;
- list;
- search;
- upload workflow;
- download HTTP endpoint;
- revision lifecycle;
- supersession;
- publication lifecycle;
- document permissions UI.

Those require separate architecture.

### Search / Vector / Graph / RAG / LLM Boundary

Successful RFC-073 access means only:

**canonical binary content was verified and exposed through the governed
Application context**

It does not imply the Document is:

- parsed;
- indexed;
- searchable;
- embedded;
- present in Vector storage;
- represented in Graph storage;
- available to RAG;
- available to an LLM;
- trusted for autonomous AI action.

### Persistence and Migration Boundary

RFC-073 requires no new:

- SQLAlchemy model;
- table;
- column;
- index;
- constraint;
- migration;
- Alembic revision.

Canonical Alembic head remains:

`0005`

### Runtime / Composition Boundary

RFC-073 architecture acceptance shall not itself add:

- default `CompositionRoot` construction;
- Runtime registration;
- Bootstrap registration;
- API wiring;
- filesystem root configuration;
- deployment configuration.

Production composition is separately governed.

### Security Boundary

RFC-073 makes no claim of:

- authentication completion;
- authorization completion;
- RBAC completion;
- Active Directory completion;
- BOLA protection completion;
- Cybersecurity approval;
- secure production deployment;
- regulatory certification.

Future API/content-delivery authorization must be governed separately and
fail closed.

### No New Transaction Coordinator

RFC-073 introduces no coordinator.

It does not extend:

`KnowledgeLineageTransactionCoordinator`

That coordinator retains only its accepted Knowledge/Lineage scope.

### Rejected Alternative — Return `DocumentContentStore.open()` Directly

Rejected.

Reason:

That would expose a lower-level persistence port directly to downstream
Application consumers and would not guarantee descriptor/payload integrity
before use.

### Rejected Alternative — Seek Back After Verification

Rejected.

Reason:

The accepted persistence-neutral store does not require seekable payloads.

### Rejected Alternative — Buffer Entire Payload

Rejected.

Reason:

It unnecessarily creates an Application memory-scaling responsibility.

### Rejected Alternative — Temporary Application File

Rejected.

Reason:

It would introduce filesystem/storage ownership into the Application layer.

### Rejected Alternative — Use `source_reference`

Rejected.

Reason:

It violates accepted provenance semantics and reintroduces an implicit storage
contract.

### Rejected Alternative — Repair Payload-Only State

Rejected.

Reason:

Canonical descriptor establishment and media-type ownership already belong to
RFC-072.

### Proposed Technical Implementation Surface

Architecture acceptance alone shall not authorize implementation.

Only after:

1. this draft is reviewed and refined;
2. AD-059 is explicitly accepted;
3. the acceptance record is committed;
4. the acceptance record is pushed;
5. exact Local / Tracking / Remote accepted-contract identity is verified;
6. a separate implementation-entry review passes

may implementation introduce:

`backend/app/services/document_content_access_application_service.py`

and focused tests:

- `tests/services/test_document_content_access_application_service.py`;
- `tests/services/test_document_content_access_architecture.py`.

No other production file is pre-authorized.

### Required Technical Verification After Later Implementation

A later technical gate shall require coverage of at least:

1. Document absent;
2. Document exists / descriptor absent / payload absent;
3. descriptor-only integrity failure;
4. payload-only integrity failure;
5. exact complete payload verification;
6. byte-length mismatch;
7. SHA-256 mismatch;
8. zero-byte payload;
9. non-seekable verification stream;
10. verification context closure;
11. delivery reopen occurs only after verification close;
12. delivery reopen confirmed absence;
13. delivery context closes after normal consumer exit;
14. delivery context closes after consumer exception;
15. operational repository failure propagation;
16. operational store-open failure propagation;
17. operational payload-read failure propagation;
18. no write operations;
19. no `source_reference` access;
20. no Infrastructure path leakage;
21. exact public-surface architecture contract;
22. no existing responsibility absorbed;
23. no schema/Alembic expansion;
24. full PlantMind regression;
25. Python compilation;
26. `git diff --check`.

These technical tests belong to the later implementation gate, not to
architecture acceptance.

### Acceptance Requirements

Before AD-059 may become Accepted, architecture review must confirm:

1. RFC-073 introduces no new ARCH-001 layer;
2. the service is read-only;
3. canonical identity is `document_id`;
4. Document existence is checked first;
5. both-absent content state is distinct from Document absence;
6. descriptor-only is integrity failure;
7. payload-only is integrity failure;
8. descriptor/payload mismatch is integrity failure;
9. unverified bytes are never yielded;
10. verification is streaming and persistence-neutral;
11. successful access uses verify-close-reopen-deliver;
12. delivery resource ownership is context-managed;
13. no seekability requirement exists;
14. no full buffering exists;
15. zero-byte content remains valid;
16. no repair/write path exists;
17. `source_reference` remains provenance only;
18. RFC-072 establishment ownership is preserved;
19. parser/Document Library responsibilities remain downstream;
20. Search/Vector/Graph/RAG/LLM remain downstream;
21. no database migration is introduced;
22. no Runtime/Composition/Bootstrap expansion is introduced;
23. no production-security claim is introduced;
24. acceptance is separate from implementation entry.

### Current Gate

AD-059:

**DRAFT — NOT ACCEPTED**

Architecture review:

**PENDING**

Implementation:

**NOT AUTHORIZED**

Staging:

**NOT AUTHORIZED**

Commit:

**NONE**

Push:

**NONE**

### Next Exact Action

Perform Chief Architect review of the complete five-document RFC-073 / AD-059
architecture draft.

No staging, acceptance or implementation is authorized until that review
passes.

### RFC-073 / AD-059 Architecture Review Refinement — Observable-State and Fresh-Open Semantics

#### Observable-State Classification

RFC-073 error classifications describe the state observed by one access
invocation.

They SHALL NOT be interpreted as a claim that the observed persistence state
is permanently corrupt.

RFC-072 uses:

**payload first → descriptor second**

for fresh establishment.

Therefore a concurrent RFC-073 access may legitimately observe:

**payload present / descriptor absent**

during an RFC-072 establishment or recovery window.

RFC-073 shall still classify that observation as:

`DocumentContentAccessIntegrityError`

because verified canonical content cannot safely be delivered from the state
observed by that invocation.

This Application error means:

**the observed canonical content state is not safe for delivery now**

It does not mean:

**the persistence state is proven permanently unrecoverable**

RFC-073 shall perform no:

- automatic repair;
- automatic retry;
- waiting;
- polling;
- descriptor reconstruction;
- payload reconstruction;
- write.

A later explicit caller invocation re-observes canonical state from the
beginning and may succeed if RFC-072 has completed establishment or recovery.

Likewise:

**descriptor absent / payload absent → Content Not Found**

is a classification of the current observation only.

RFC-073 makes no linearizability claim that the same state must remain visible
after the invocation returns.

#### Fresh-Open Semantics

RFC-073 does not amend or replace the accepted `DocumentContentStore` port.

Each call to:

`DocumentContentStore.open(document_id)`

is treated as a fresh canonical payload access attempt under the accepted
store contract.

RFC-073 itself shall not:

- seek;
- rewind;
- reposition;
- cache;
- duplicate;
- reconstruct

a returned payload stream.

The verification pass consumes its fresh opened payload incrementally through
EOF.

After that verification context is closed, delivery uses a separate fresh:

`DocumentContentStore.open(document_id)`

result.

RFC-073 relies on the accepted immutable canonical-payload semantics.

It introduces no new binary-store responsibility and does not modify RFC-070
or RFC-071 ownership.

If a future storage adapter cannot satisfy the accepted store contract and
RFC-073 consumer semantics, that adapter requires separate conformance review
rather than silent weakening of RFC-073 integrity guarantees.

#### Refined Acceptance Meaning

Before AD-059 may be accepted, architecture review must additionally confirm:

1. `IntegrityError` is an access-safety classification, not a permanent
   corruption assertion;
2. RFC-072 payload-first transient/recoverable state remains architecturally
   valid;
3. RFC-073 performs no same-invocation retry or repair;
4. an explicit later invocation may re-observe and succeed;
5. fresh-open delivery does not amend persistence-neutral store ownership;
6. no seekability or buffering requirement is introduced.

Architecture review:

**PENDING — RE-REVIEW REQUIRED**

AD-059:

**DRAFT — NOT ACCEPTED**

Implementation:

**NOT AUTHORIZED**

---

## RFC-073 / AD-059 Architecture Contract Acceptance

**Record Classification: Architecture Contract Acceptance**

Verified RFC-073 selection commit:

`059fbcbf404da390079ca77685eb2135e663e80d`

Selected workstream:

**RFC-073 — Canonical Document Content Access Application Boundary**

Architecture Decision:

**AD-059 — Canonical Document Content Access Application Boundary**

### Final Architecture Review

Refined architecture review:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

Observable-state refinement:

**PASS**

Fresh-open semantics refinement:

**PASS**

Architecture acceptance and implementation entry remain separate gates.

### Accepted Decision

AD-059 is:

**ACCEPTED**

Acceptance Git durability is:

**PENDING**

Implementation is:

**NOT AUTHORIZED**

### Accepted Application Boundary

Accepted service:

`DocumentContentAccessApplicationService`

Accepted module:

`app.services.document_content_access_application_service`

Accepted future implementation path:

`backend/app/services/document_content_access_application_service.py`

Canonical dependencies are exactly:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`.

No additional repository, storage adapter, coordinator or Infrastructure
dependency is accepted by RFC-073.

### Accepted Public Surface

The RFC-073 module owns exactly:

- `DocumentContentAccessRequest`;
- `DocumentContentAccess`;
- `DocumentContentAccessDocumentNotFoundError`;
- `DocumentContentAccessContentNotFoundError`;
- `DocumentContentAccessIntegrityError`;
- `DocumentContentAccessApplicationService`.

`DocumentContentAccessRequest` is frozen, slots-based and keyword-only with
exactly:

`document_id: EntityId`

`DocumentContentAccess` is frozen, slots-based and keyword-only with exactly:

- `descriptor: DocumentContentDescriptor`;
- `payload: BinaryIO`.

Accepted operation:

`open(request: DocumentContentAccessRequest) -> AbstractContextManager[DocumentContentAccess]`

### Accepted Access Model

Successful RFC-073 access uses:

**VERIFY → CLOSE → REOPEN → DELIVER**

The first fresh store access is consumed incrementally through EOF and verifies:

- exact byte length;
- exact SHA-256 digest.

The verification context is closed before delivery access begins.

A second fresh:

`DocumentContentStore.open(document_id)`

provides the consumer delivery stream.

RFC-073 requires no:

- `seek()`;
- `tell()`;
- `fileno()`;
- complete payload buffering;
- Application temporary file;
- Application filesystem cache.

Unverified bytes are never delivered.

Zero-byte canonical content remains valid.

### Fresh-Open Conformance Clarification

AD-059 does not modify the public RFC-070 `DocumentContentStore` method
signature or transfer store ownership to the Application layer.

For RFC-073 consumer semantics, each fresh conforming
`DocumentContentStore.open(document_id)` access must expose the canonical
payload from the start of that newly opened payload stream.

The earlier draft wording:

`canonical byte zero`

means the beginning of the canonical payload exposed by that fresh open.

RFC-073 itself does not seek, rewind or reposition the stream.

The current filesystem adapter naturally satisfies this behavior through a
fresh binary file open.

A future adapter that cannot satisfy RFC-073 access/conformance semantics
requires separate architecture/conformance review.

Its limitation shall not silently weaken AD-059 integrity guarantees.

### Accepted State Classification

Canonical Enterprise Document absence:

**DocumentContentAccessDocumentNotFoundError**

For an existing canonical Document:

- descriptor absent / payload absent:
  **DocumentContentAccessContentNotFoundError**;

- descriptor present / payload absent:
  **DocumentContentAccessIntegrityError**;

- descriptor absent / payload present:
  **DocumentContentAccessIntegrityError**;

- descriptor/payload byte-length mismatch:
  **DocumentContentAccessIntegrityError**;

- descriptor/payload digest mismatch:
  **DocumentContentAccessIntegrityError**;

- successful verification followed by confirmed delivery-reopen absence:
  **DocumentContentAccessIntegrityError**.

### Observable-State Acceptance Semantics

RFC-073 Application errors classify the state observed by the current access
invocation.

They do not prove permanent persistence corruption.

RFC-072 accepted establishment remains:

**payload first → descriptor second**

Therefore payload-only state may be observed transiently during legitimate
RFC-072 establishment or recovery.

RFC-073 nevertheless fails closed for that access invocation because verified
canonical content cannot safely be delivered from the observed incomplete
state.

RFC-073 performs no:

- automatic retry;
- waiting;
- polling;
- repair;
- descriptor reconstruction;
- payload reconstruction;
- write.

A later explicit invocation re-observes canonical state and may succeed.

### Read-Only Ownership

RFC-073 never calls:

- `EnterpriseDocumentRepository.add()`;
- `DocumentContentRepository.add()`;
- `DocumentContentStore.add()`.

RFC-073 introduces no:

- update;
- delete;
- overwrite;
- upsert;
- compensation;
- recovery coordinator.

RFC-072 retains establishment and recovery ownership.

### Resource Ownership

Every non-None store-owned context acquired by RFC-073 is closed
deterministically.

The consumer payload is usable only within the RFC-073 Application context.

Normal exit, consumer exception and early exit all close the delivery context.

Persistence ownership remains with `DocumentContentStore`.

### Canonical Identity and Provenance

Canonical content association identity is:

`document_id: EntityId`

`EnterpriseDocument.source.source_reference` remains:

**external provenance / traceability only**

RFC-073 never uses it as:

- storage path;
- storage key;
- canonical URI;
- payload locator;
- deduplication key;
- canonical Document identity.

### Sequential Observation

RFC-073 does not claim one atomic, transactional or linearizable snapshot
across:

- Enterprise Document repository;
- Document Content descriptor repository;
- binary Document Content store.

It introduces no distributed transaction and no new coordinator.

### Operational Failure Rule

Underlying operational failures propagate unless AD-059 explicitly classifies
the observed condition as one of its Application errors.

No generic catch-all persistence error hierarchy is introduced.

### Preserved Responsibilities

AD-059 does not modify or absorb:

- `EnterpriseDocumentRegistrationApplicationService`;
- `DocumentContentEstablishmentApplicationService`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeCaptureApplicationService`;
- `KnowledgeLineageTransactionCoordinator`;
- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- `FilesystemDocumentContentStore`;
- `EnterpriseDocument`;
- `DocumentContentDescriptor`.

### Accepted Non-Scope

AD-059 does not introduce:

- Document Library;
- parser implementation;
- PDF/DOCX/spreadsheet/text extraction;
- OCR;
- metadata extraction;
- chunking;
- Search;
- embeddings;
- Vector persistence;
- Graph / Neo4j production integration;
- RAG;
- LLM;
- AI Agents;
- HTTP content-download API;
- Runtime / Composition / Bootstrap wiring;
- SQLAlchemy expansion;
- database schema change;
- Alembic revision;
- authentication completion;
- authorization completion;
- RBAC completion;
- Active Directory completion;
- Cybersecurity approval;
- production-readiness claim.

Canonical Alembic head remains:

`0005`

### Acceptance Requirements Verification

Architecture review confirms:

1. no new ARCH-001 layer — PASS;
2. read-only service — PASS;
3. canonical identity is `document_id` — PASS;
4. Document existence first — PASS;
5. Content Not Found distinct from Document Not Found — PASS;
6. descriptor-only fail-closed — PASS;
7. payload-only fail-closed — PASS;
8. mismatch fail-closed — PASS;
9. unverified bytes never delivered — PASS;
10. incremental verification — PASS;
11. verify-close-reopen-deliver — PASS;
12. context-managed resource ownership — PASS;
13. no seek requirement — PASS;
14. no full buffering — PASS;
15. zero-byte content valid — PASS;
16. no repair/write — PASS;
17. `source_reference` provenance only — PASS;
18. RFC-072 ownership preserved — PASS;
19. parser/Document Library downstream — PASS;
20. Search/Vector/Graph/RAG/LLM downstream — PASS;
21. no migration — PASS;
22. no Runtime/Composition/Bootstrap expansion — PASS;
23. no production-security claim — PASS;
24. acceptance separated from implementation entry — PASS;
25. IntegrityError is access-safety classification, not permanent-corruption
    assertion — PASS;
26. RFC-072 payload-first semantics preserved — PASS;
27. no same-invocation retry/repair — PASS;
28. later explicit invocation re-observes state — PASS;
29. fresh-open delivery does not transfer store ownership — PASS;
30. no seekability/buffering requirement introduced — PASS.

### Acceptance Gate State

AD-059:

**ACCEPTED — GIT DURABILITY PENDING**

Architecture review:

**PASS**

Acceptance staging:

**NOT YET PERFORMED**

Acceptance commit:

**NONE**

Acceptance push:

**NONE**

Implementation:

**NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document RFC-073 / AD-059 architecture acceptance
candidate.

Do not stage until that acceptance review passes.

Do not begin implementation until accepted-contract Git durability is
complete and a separate implementation-entry review passes.

---

## RFC-073 / AD-059 Engineering Closure Record

**Record Classification: Non-Decision Engineering Closure Governance Record**

This section creates no new Architecture Decision.

It does not amend, replace, supersede or rewrite AD-059.

AD-059 remains:

**ACCEPTED**

### Closure Baseline

RFC-073 workstream:

**Canonical Document Content Access Application Boundary**

Verified workstream-selection commit:

`059fbcbf404da390079ca77685eb2135e663e80d`

Verified accepted-contract commit:

`c6749fc75a67faf926c7d398a43f7c8825f719fd`

Verified technical implementation commit:

`52b1cbf50b2b248914ee00539419f9262b9c7530`

Technical Git durability:

**PASS — LOCAL / TRACKING / REMOTE IDENTITY VERIFIED**

Working tree at closure-entry gate:

**CLEAN**

### Verified Technical Outcome

RFC-073 establishes:

`DocumentContentAccessApplicationService`

under:

`app.services.document_content_access_application_service`

The service depends only on:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`.

Canonical request identity remains:

`document_id: EntityId`

Successful verified access remains:

**VERIFY → CLOSE → REOPEN → DELIVER**

Pre-delivery verification consumes the first canonical payload stream
incrementally through EOF, verifies exact byte length and SHA-256, closes that
context, and only then obtains a fresh delivery context.

The implementation preserves:

- Document-first lookup;
- fail-closed descriptor/payload state classification;
- payload-only integrity classification for the current invocation without
  asserting permanent persistence corruption;
- RFC-072 payload-first establishment semantics;
- zero-byte canonical payload support;
- non-seekable verification and delivery;
- no seek/tell/fileno requirement;
- no full-payload buffering requirement;
- deterministic context ownership and closure;
- no automatic repair, retry, waiting, polling or persistence write;
- `source_reference` as provenance only.

### Verified Engineering Evidence

Focused RFC-073 verification:

**33 passed**

Full PlantMind regression:

**1028 passed**

Canonical Alembic head:

`0005`

Reviewed technical diff SHA-256:

`63a922d37b63badb8a127de543c21686629ad2dc2c1eaed41dadd0711f286bd2`

### Responsibility Preservation

This closure record does not modify or absorb responsibility from:

- `EnterpriseDocumentRegistrationApplicationService`;
- `DocumentContentEstablishmentApplicationService`;
- `DocumentKnowledgeIngestionApplicationService`;
- `KnowledgeCaptureApplicationService`;
- `KnowledgeLineageTransactionCoordinator`;
- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- `FilesystemDocumentContentStore`;
- `EnterpriseDocument`;
- `DocumentContentDescriptor`.

RFC-073 owns verified read access only.

### Explicitly Preserved Non-Scope

This closure record does not authorize or claim:

- Document Library behavior;
- parser execution;
- PDF/DOCX/spreadsheet/text extraction;
- OCR;
- metadata extraction;
- chunking;
- Search;
- embeddings or Vector persistence;
- Graph / Neo4j production integration;
- RAG;
- LLM invocation;
- AI Agents;
- Runtime / Composition / Bootstrap wiring;
- HTTP/API content-download endpoints;
- schema or Alembic migration changes;
- authentication / authorization / RBAC / Active Directory completion;
- Cybersecurity approval;
- production deployment conformance;
- production-readiness claims.

Production deployment conformance remains separately governed.

### Closure Governance State

Closure documentation:

**AUTHORED — REVIEW PENDING**

Engineering closure commit:

**NOT YET CREATED**

Engineering closure push:

**NOT PERFORMED**

RFC-073 terminal closure:

**NOT YET CLAIMED**

Post-closure Source-of-Truth reconciliation:

**PENDING — SEPARATE POST-CLOSURE GATE**

Successor workstream:

**NONE SELECTED**

### Next Exact Action

Review the complete five-document RFC-073 engineering closure documentation.

Do not stage closure documentation until that review passes.

Do not claim terminal closure until closure Git durability and the subsequent
Source-of-Truth reconciliation complete separately.


---

## RFC-073 / AD-059 Post-Closure Source-of-Truth Reconciliation Record

**Record Classification: Non-Decision Engineering Reconciliation Governance Record**

This record creates no new Architecture Decision.

It does not amend, replace, supersede or rewrite AD-059.

AD-059 remains:

**ACCEPTED**

### Durable RFC-073 Commit Chain

Selection commit:

`059fbcbf404da390079ca77685eb2135e663e80d`

Accepted-contract commit:

`c6749fc75a67faf926c7d398a43f7c8825f719fd`

Technical implementation commit:

`52b1cbf50b2b248914ee00539419f9262b9c7530`

Engineering closure commit:

`570adbee4a86354204e1c1290b673fda279c5c17`

Closure commit parent:

`52b1cbf50b2b248914ee00539419f9262b9c7530`

Closure Git durability:

**PASS — LOCAL / TRACKING / REMOTE EXACT**

Working tree at reconciliation entry:

**CLEAN**

### Preserved Technical Baseline

RFC-073 canonical service:

`app.services.document_content_access_application_service.DocumentContentAccessApplicationService`

Successful access model:

**VERIFY → CLOSE → REOPEN → DELIVER**

Focused RFC-073 verification:

**33 passed**

Full PlantMind regression:

**1028 passed**

Canonical Alembic head:

`0005`

Reviewed technical diff SHA-256:

`63a922d37b63badb8a127de543c21686629ad2dc2c1eaed41dadd0711f286bd2`

### Reconciliation Responsibility

This reconciliation updates maintained engineering-memory current state only.

It does not modify production code, tests, database schema, Alembic migrations,
Runtime, Composition, Bootstrap, Document Library, parser/OCR/chunking,
Search/Vector/Graph/RAG/LLM, AI Agents or production-security capability.

RFC-073 remains limited to verified read-only canonical Document Content access.

`source_reference` remains provenance only.

### Current Reconciliation State

Source-of-Truth reconciliation:

**AUTHORED — REVIEW PENDING**

Reconciliation staging:

**NOT PERFORMED**

Reconciliation commit:

**NOT YET CREATED**

Reconciliation push / exact identity verification:

**NOT YET PERFORMED**

Final reconciliation verification record:

**NOT YET CREATED**

RFC-073 terminal closure:

**NOT YET CLAIMED**

Last fully closed RFC remains:

**RFC-072**

Successor workstream:

**NONE SELECTED / NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document RFC-073 post-closure Source-of-Truth
reconciliation diff.

Do not stage reconciliation until that review passes.

Do not declare RFC-073 fully closed until reconciliation Git durability and the
separate final reconciliation verification record are complete.


---

## Current Architecture Governance State — RFC-073 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record creates no new Architecture Decision and does not amend, replace,
supersede or rewrite AD-059.

AD-059 remains the latest Accepted Architecture Decision.

RFC-073 — Canonical Document Content Access Application Boundary is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

### Verified Commit Chain

- selection commit `059fbcbf404da390079ca77685eb2135e663e80d`;
- accepted-contract commit `c6749fc75a67faf926c7d398a43f7c8825f719fd`;
- technical implementation commit `52b1cbf50b2b248914ee00539419f9262b9c7530`;
- engineering closure commit `570adbee4a86354204e1c1290b673fda279c5c17`;
- post-closure reconciliation commit `a98fad393431a922276b15639504c86454a93c05`.

### Verified Reconciliation Git State

- reconciliation parent:
  `570adbee4a86354204e1c1290b673fda279c5c17`;
- reconciliation push: **PASS**;
- exact Local / Tracking / Remote reconciliation identity: **PASS**;
- working tree after reconciliation push: **CLEAN**;
- reconciliation surface: exactly five maintained Source-of-Truth documents;
- production-code changes: none;
- test-file changes: none.

### Preserved Technical Baseline

- full PlantMind regression: **1028 passed**;
- canonical Alembic head: `0005`;
- delivered RFC-073 Application boundary:
  `app.services.document_content_access_application_service.DocumentContentAccessApplicationService`;
- successful access model remains:
  **VERIFY → CLOSE → REOPEN → DELIVER**;
- RFC-072 payload-first content establishment remains unchanged;
- canonical Enterprise Document repository responsibility remains unchanged;
- canonical Document Content descriptor repository responsibility remains unchanged;
- canonical binary Document Content store responsibility remains unchanged;
- `source_reference` remains provenance only;
- no schema or Alembic expansion;
- no `DatabaseRuntime` expansion;
- no default Runtime / Composition / Bootstrap wiring;
- no Document Library / parser / OCR / chunking promotion;
- no Search / Vector / Graph / RAG / LLM / AI Agent promotion;
- no production-security or Cybersecurity completion claim.

Production deployment conformance remains separately governed.

### Successor Governance

No successor RFC or Architecture workstream is selected or preselected by
this record.

Successor selection is a separate evidence-based governance activity.

### Non-Self-Referential Final Record

This final verification record is intentionally non-self-referential.

It records reconciliation commit:

`a98fad393431a922276b15639504c86454a93c05`

and does not contain, predict or require the future Git commit hash that
persists this record.

Verification of this record's own commit, push, exact Local / Tracking / Remote
identity and clean working tree is an external Git durability gate.

That external gate does not require another RFC-073 Source-of-Truth record.


---

## Selected Successor Architecture Workstream Draft — RFC-074 — Canonical Document Content Parsing Application Boundary

**Record Classification: Non-Decision Successor-Selection Governance Record**

This record does not create or accept a new Architecture Decision.

RFC-073 / AD-059 remains fully closed, Source-of-Truth reconciled and
authoritative.

### Candidate Successor

**RFC-074 — Canonical Document Content Parsing Application Boundary**

Selection state:

**CANDIDATE AUTHORED — REVIEW PENDING**

Architecture contract:

**NOT YET AUTHORED OR ACCEPTED**

Technical implementation:

**NOT AUTHORIZED**

### Evidence Basis

The post-RFC-073 repository review established:

1. `backend/app/knowledge/document_parser.py` exists only as an empty seam;
2. no competing Parser or Extractor implementation currently owns the
   responsibility;
3. RFC-073 provides verified read-only canonical Document Content access as
   `DocumentContentDescriptor` plus context-bound `BinaryIO`;
4. future parser behavior is already required to consume canonical bytes
   through an accepted Application/access path;
5. RFC-073 now provides that accepted path;
6. `source_reference` remains provenance and SHALL NOT become parser storage;
7. `DocumentKnowledgeIngestionApplicationService` already exists and accepts
   prepared Knowledge fields rather than raw binary Document Content;
8. parsing therefore remains a distinct missing responsibility between
   verified canonical Document Content access and any later Knowledge,
   indexing or intelligence workflow.

### Candidate Responsibility

RFC-074 is selected for review as the narrow Application-level boundary that
shall define how one parsing use case consumes verified canonical Document
Content without taking ownership of storage, persistence or downstream
Knowledge responsibilities.

The future architecture contract shall determine the exact:

- parsing request;
- parsing result;
- parsing/extraction port shape;
- dependency on `DocumentContentAccessApplicationService`;
- media-type interaction;
- parser failure semantics;
- context-managed payload lifetime;
- boundary between Application orchestration and format-specific parser
  implementation.

### Mandatory Preserved Boundaries

RFC-074 SHALL NOT, merely by successor selection, authorize:

- promotion of the existing empty `app.knowledge.document_parser` seam as the
  canonical implementation;
- filesystem paths or storage keys as parser inputs;
- reinterpretation of `source_reference` as binary storage;
- Document Content mutation or repair;
- descriptor mutation;
- binary storage ownership;
- Document Library upload/download/browse/catalogue behavior;
- OCR implementation;
- PDF/DOCX/spreadsheet parser technology selection;
- chunking;
- parser-result persistence;
- automatic Knowledge creation;
- automatic `DocumentKnowledgeIngestionApplicationService` invocation;
- Search;
- embeddings or Vector persistence;
- Graph / Neo4j production integration;
- RAG;
- LLM invocation;
- AI Agents;
- Runtime / Composition / Bootstrap wiring;
- database-schema or Alembic migration changes;
- authentication / authorization / RBAC / Active Directory completion;
- production-security or Cybersecurity completion;
- production-readiness claims.

### Why Not Document Library Next

A Document Library would combine catalogue, browse, upload/download,
authorization and user-facing lifecycle responsibilities before the canonical
raw-content transformation boundary exists.

It remains downstream.

### Why Not Search / Vector / Graph / RAG Next

Those capabilities depend on reliable parsed or otherwise prepared information.

Promoting them now would bypass the missing canonical transformation boundary.

They remain downstream.

### Why Not Document Knowledge Ingestion Next

`DocumentKnowledgeIngestionApplicationService` already exists.

It accepts prepared Knowledge fields and coordinates canonical Knowledge and
lineage persistence.

RFC-074 SHALL NOT duplicate that responsibility.

### Selection Gate

This draft authorizes no architecture implementation.

The next action is Chief Architect review of the complete five-document
successor-selection diff.

Only after the reviewed selection record becomes Git durable may RFC-074 be
treated as the formally selected active architecture workstream and its
architecture contract be drafted.


---

# AD-060 — Canonical Document Content Parsing Application Boundary

**Status: DRAFT — REVIEW PENDING**

**Workstream: RFC-074 — Canonical Document Content Parsing Application Boundary**

**Verified Selection Commit: `b5d1e7fe434378ac7ee90912ac40932d5c5451eb`**

## Context

RFC-073 / AD-059 established verified read-only access to canonical
Document Content.

Its accepted access boundary exposes:

- the canonical `DocumentContentDescriptor`;
- a context-bound verified `BinaryIO` payload.

RFC-073 deliberately does not parse that payload.

The repository also contains:

`backend/app/knowledge/document_parser.py`

but that file remains an empty legacy capability seam and has no accepted
canonical responsibility.

RFC-065 already owns prepared Document-to-Knowledge ingestion through:

`DocumentKnowledgeIngestionApplicationService`

and therefore SHALL NOT be expanded into raw binary parsing.

A distinct boundary is required between verified canonical binary content and
all later Knowledge, indexing and intelligence behavior.

## Decision

PlantMind SHALL introduce a narrow persistence-neutral Application boundary
for canonical Document Content parsing.

The proposed technical boundary is:

`app.services.document_content_parsing_application_service.DocumentContentParsingApplicationService`

supported by a parsing port under:

`app.document_parsing`

RFC-074 SHALL define parsing as:

**VERIFIED CANONICAL CONTENT → FORMAT-NEUTRAL PARSER PORT → TEXTUAL PARSE RESULT**

RFC-074 SHALL NOT select or implement a concrete PDF, DOCX, spreadsheet or OCR
technology.

## Principle

Parsing is transformation of already verified canonical Document Content.

It is not storage, Document registration, Knowledge persistence, indexing or
AI inference.

## Implication

The parser SHALL receive canonical verified bytes only through RFC-073.

It SHALL NOT locate files, derive paths, inspect deployment storage topology or
reinterpret provenance as storage.

## Canonical Application Request

The Application request SHALL be immutable and contain exactly:

`document_id: EntityId`

The request SHALL NOT contain:

- filesystem path;
- storage key;
- `source_reference`;
- raw caller-supplied payload;
- parser implementation name;
- database session;
- Knowledge fields.

Canonical content identity remains the Enterprise Document identity.

## Canonical Application Result

The Application result SHALL be immutable and contain:

- the verified `DocumentContentDescriptor`;
- textual parsed content as `str`.

The result SHALL NOT contain or retain:

- `BinaryIO`;
- filesystem handles;
- storage paths;
- temporary-file references;
- repository objects;
- database sessions.

The payload lifetime ends before the completed Application result escapes the
RFC-073 access context.

## Parser Port

RFC-074 SHALL introduce a persistence-neutral parser contract:

`DocumentContentParser`

Its conceptual operation is:

`parse(*, descriptor: DocumentContentDescriptor, payload: BinaryIO) -> str`

The parser receives only:

- the verified canonical descriptor;
- the verified context-bound binary payload.

The parser SHALL NOT require access to:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- Knowledge repositories;
- lineage repositories;
- database runtime;
- Runtime / Composition / Bootstrap infrastructure.

## Payload Borrowing And Ownership

`DocumentContentParser` is a borrower of the RFC-073 delivery payload.

Payload ownership remains with the RFC-073 access context.

The parser SHALL NOT:

- close the supplied payload;
- retain the supplied payload beyond the synchronous `parse()` invocation;
- cache or persist the supplied payload;
- return the supplied payload or any stream wrapper around it;
- transfer payload ownership to another component;
- expose the supplied payload through parser result state.

`DocumentContentParsingApplicationService` SHALL NOT close the payload directly.

RFC-073 remains responsible for deterministic delivery-context closure after
the parser invocation completes or fails.

The descriptor may be propagated as immutable result metadata.

The binary payload itself SHALL NOT escape the active RFC-073 access context.

## Parser Output Semantics

Successful parsing returns Python `str`.

This is a runtime contract, not only a type annotation.

If `DocumentContentParser.parse()` returns a value that is not an actual
`str`, `DocumentContentParsingApplicationService` SHALL raise `TypeError`
before constructing or returning an Application result.

The Application boundary SHALL NOT coerce an invalid parser result through
`str(...)` or any other normalization.

The Application boundary SHALL NOT:

- trim parser output;
- rewrite text;
- summarize text;
- classify Knowledge;
- split text into chunks;
- generate embeddings;
- create Knowledge records.

An empty string MAY be a valid parser result.

For example, a structurally valid document may contain no text extractable by
a non-OCR parser.

RFC-074 SHALL NOT silently interpret empty parsed text as parser failure.

## Media-Type Semantics

The parser receives the canonical media type from
`DocumentContentDescriptor`.

RFC-074 SHALL NOT:

- sniff storage filenames;
- infer format from `source_reference`;
- use filesystem extensions as canonical media type;
- silently substitute a different parser;
- perform parser fallback chains.

Unsupported canonical media type SHALL fail explicitly.

Concrete media-type support remains the responsibility of future parser
implementations governed separately.

## Application Coordination

`DocumentContentParsingApplicationService` SHALL depend on exactly:

1. `DocumentContentAccessApplicationService`;
2. `DocumentContentParser`.

It SHALL NOT directly depend on:

- `EnterpriseDocumentRepository`;
- `DocumentContentRepository`;
- `DocumentContentStore`;
- Infrastructure adapters;
- SQLAlchemy;
- PostgreSQL;
- filesystem storage;
- Knowledge persistence.

The Application sequence SHALL be:

**OPEN VERIFIED CONTENT → PARSE INSIDE ACCESS CONTEXT → CLOSE CONTENT → RETURN RESULT**

The parser invocation SHALL occur while RFC-073 delivery access is active.

No payload or stream SHALL escape that context.

## RFC-073 Dependency Rule

RFC-074 SHALL consume RFC-073 rather than reproduce it.

RFC-074 SHALL NOT independently:

- verify byte length;
- verify SHA-256;
- reopen content;
- classify descriptor/payload consistency;
- repair content state;
- access the binary store directly.

RFC-073 remains the single Application owner of verified canonical content
delivery.

## Stream Semantics

RFC-074 Application orchestration SHALL NOT require:

- `seek()`;
- `tell()`;
- `fileno()`;
- filesystem-backed payloads.

The Application service SHALL pass the RFC-073 delivery stream to the parser
without converting canonical access into a path contract.

Any future concrete parser implementation that requires buffering, spooling or
format-specific stream adaptation requires explicit evidence and SHALL NOT
transfer such responsibility into the RFC-074 Application service.

## Failure Semantics

RFC-073 access failures SHALL propagate unchanged.

The initial `app.document_parsing.parser` contract SHALL define exactly
these public parser-contract failures:

- `DocumentContentParserUnsupportedMediaTypeError`;
- `DocumentContentParserInvalidContentError`.

`DocumentContentParserUnsupportedMediaTypeError` represents an unsupported
canonical `DocumentContentMediaType`.

`DocumentContentParserInvalidContentError` represents content that the selected
parser contract recognizes as its supported media type but cannot structurally
parse as valid content.

These parser-contract failures SHALL fail closed and SHALL propagate unchanged
through `DocumentContentParsingApplicationService`.

No generic RFC-074 parser wrapper exception is authorized.

Operational exceptions raised by a parser implementation remain distinct from
these two public parser-contract failures.

The Application service SHALL NOT:

- retry automatically;
- wait or poll;
- repair content;
- select fallback parsers;
- invoke OCR automatically;
- persist partial parsing output;
- invoke Knowledge ingestion after failure.

Operational failures raised by a parser implementation SHALL propagate unless
a future accepted architecture explicitly classifies them.

RFC-074 SHALL NOT introduce a generic catch-all exception that hides accepted
RFC-073 or parser failure semantics.

## Context Ownership

RFC-073 retains ownership of payload context creation and closure.

RFC-074 SHALL NOT close store internals directly.

The Application boundary SHALL ensure parsing completes within the RFC-073
context.

Normal return, parser failure and consumer-visible failure SHALL preserve
deterministic RFC-073 context cleanup.

## Relationship To RFC-065

`DocumentKnowledgeIngestionApplicationService` remains unchanged.

RFC-074 SHALL NOT invoke it automatically.

RFC-074 SHALL NOT create:

- `KnowledgeRecord`;
- `KnowledgeProvenance`;
- `KnowledgeSubject`;
- `DocumentKnowledgeLineage`.

A future separately accepted orchestration capability MAY consume an RFC-074
text result and invoke RFC-065.

That future orchestration is outside RFC-074.

## Legacy Parser Seam

The existing:

`app.knowledge.document_parser`

SHALL NOT be promoted, imported or treated as canonical merely because it
exists.

RFC-074 shall establish its canonical responsibility under the new
`app.document_parsing` boundary.

Any removal, migration or retirement of the legacy empty seam requires
evidence and SHALL NOT be performed silently.

## Document Library Boundary

RFC-074 is not a Document Library.

It SHALL NOT provide:

- upload;
- download API;
- browsing;
- catalogue behavior;
- listing;
- search UI;
- revision management;
- document approval workflow.

## OCR Boundary

OCR remains separately deferred.

RFC-074 SHALL NOT silently invoke OCR when textual parsing returns empty
content or fails.

OCR selection, confidence semantics and provenance require separate
architecture.

## Chunking Boundary

RFC-074 SHALL NOT chunk parsed text.

Chunk identity, overlap, ordering, revision linkage and persistence remain
separately governed.

## Search / Vector / Graph / RAG / LLM Boundary

Successful RFC-074 parsing does not mean content is:

- indexed;
- searchable;
- embedded;
- stored in a Vector database;
- represented in a Graph database;
- available to RAG;
- available to an LLM;
- approved as enterprise Knowledge.

All such capabilities remain downstream.

## Persistence Boundary

RFC-074 introduces no new persistence responsibility.

No:

- database table;
- Alembic revision;
- parsed-result repository;
- parser cache;
- temporary replay store;
- binary-store mutation

is authorized.

Canonical Alembic head remains:

`0005`

## Runtime / Composition Boundary

RFC-074 architecture acceptance SHALL NOT automatically authorize:

- default `CompositionRoot` registration;
- `DatabaseRuntime` expansion;
- Bootstrap registration;
- mandatory parser startup;
- production API exposure.

Those remain separate deployment/composition decisions.

## Security Boundary

RFC-074 does not claim completion of:

- authentication;
- authorization;
- RBAC;
- Active Directory;
- document-level authorization;
- parser sandboxing;
- malicious-document isolation;
- active-content security screening;
- Cybersecurity approval;
- production deployment conformance.

Future concrete parser deployment SHALL require separately governed security
evidence before production exposure.

## Proposed Technical Surface

If AD-060 is later Accepted, the initial technical implementation SHALL be
limited to the minimum canonical boundary required by this decision.

Expected new production surface:

- `backend/app/document_parsing/__init__.py`;
- `backend/app/document_parsing/parser.py`;
- `backend/app/services/document_content_parsing_application_service.py`.

Expected tests shall cover:

- exact immutable request/result contracts;
- exact Application dependencies;
- RFC-073 access reuse;
- parser invocation only inside the active access context;
- descriptor propagation;
- textual result propagation without normalization;
- rejection of non-`str` parser output without coercion;
- empty-text success;
- exact public parser failure-class surface;
- unsupported-media failure propagation;
- invalid-content failure propagation;
- operational parser failure propagation;
- parser borrower-only payload ownership;
- deterministic access-context closure;
- no payload escape or retention;
- no repository/store direct dependency;
- no Knowledge ingestion;
- no legacy parser-seam promotion;
- no Runtime / Composition / Bootstrap wiring;
- no schema/migration change;
- no Document Library/OCR/chunking/Search/Vector/Graph/RAG/LLM promotion.

## Explicitly Deferred

The following remain outside RFC-074:

- concrete PDF parser implementation;
- concrete DOCX parser implementation;
- concrete spreadsheet parser implementation;
- image parsing;
- OCR;
- parser registry/resolver;
- automatic parser fallback;
- language detection;
- encoding policy beyond concrete parser responsibility;
- metadata extraction;
- table extraction semantics;
- page/section model;
- chunking;
- parsed-result persistence;
- Document Library;
- automatic Document-to-Knowledge ingestion;
- Search;
- embeddings;
- Vector persistence;
- Graph persistence;
- RAG;
- LLM invocation;
- AI Agents;
- production transport exposure;
- production parser sandboxing;
- production security readiness.

## Alternatives Rejected

### Extend RFC-073 With Parsing

Rejected.

RFC-073 owns verified canonical content access.

Adding parsing would merge content-integrity/access responsibility with
content transformation.

### Extend RFC-065 With Raw Binary Parsing

Rejected.

RFC-065 owns prepared Knowledge ingestion and lineage persistence coordination.

Raw-content transformation would violate that accepted responsibility.

### Promote `app.knowledge.document_parser`

Rejected.

The file is an empty legacy seam with no accepted contract and its Knowledge
location would incorrectly suggest Knowledge ownership of raw Document
parsing.

### Let Parsers Read Filesystem Paths

Rejected.

That would bypass RFC-073, leak storage topology and undermine canonical
content integrity semantics.

### Select A PDF/OCR Library Now

Rejected.

Parser technology selection is not necessary to establish the canonical
Application contract.

## Architecture Acceptance State

AD-060:

**DRAFT — REVIEW PENDING**

RFC-074 implementation:

**NOT AUTHORIZED**

No production or test implementation change accompanies this architecture
draft.

## Next Gate

Chief Architect review of the complete five-document RFC-074 / AD-060
architecture draft.

No acceptance, staging, commit or technical implementation is authorized until
that review passes.


---

## RFC-074 / AD-060 Architecture Contract Acceptance

**Record Classification: Architecture Acceptance Governance Record**

### Final Architecture Review

The refined RFC-074 / AD-060 architecture review completed with:

**PASS — NO REMAINING REFINE / NO BLOCKED ITEM**

The final review confirmed:

1. RFC-073 remains the sole Application owner of verified canonical Document
   Content access;
2. RFC-074 consumes RFC-073 rather than duplicating integrity verification,
   reopen semantics or binary-store access;
3. the canonical parser port is persistence-neutral;
4. the parser receives only verified descriptor plus context-bound `BinaryIO`;
5. payload ownership remains with RFC-073;
6. the RFC-074 parser is borrower-only;
7. parser payload close, retention, caching, persistence or ownership transfer
   is prohibited;
8. no payload or stream escapes the RFC-073 access context;
9. Application request identity remains exactly `document_id: EntityId`;
10. Application result contains immutable verified descriptor plus parsed
    textual `str`;
11. non-`str` parser results fail with `TypeError`;
12. non-`str` results are never coerced through `str(...)`;
13. empty string remains a valid parser result;
14. the canonical parser contract defines exactly:
    `DocumentContentParserUnsupportedMediaTypeError` and
    `DocumentContentParserInvalidContentError`;
15. those parser-contract failures propagate unchanged;
16. operational parser failures remain distinct and propagate unless separately
    governed in future;
17. no generic catch-all RFC-074 parser wrapper exception is authorized;
18. canonical media type comes from `DocumentContentDescriptor`;
19. `source_reference` remains provenance only;
20. filesystem path or storage-key parser contracts are prohibited;
21. RFC-065 prepared Document-to-Knowledge ingestion remains unchanged;
22. RFC-074 performs no automatic Knowledge ingestion;
23. the legacy `app.knowledge.document_parser` seam is not promoted;
24. concrete PDF/DOCX/spreadsheet parser technology remains deferred;
25. OCR remains deferred;
26. chunking remains deferred;
27. parsed-result persistence remains deferred;
28. Document Library remains deferred;
29. Search / Vector / Graph / RAG / LLM / AI Agent behavior remains deferred;
30. no schema or Alembic expansion is introduced;
31. no Runtime / Composition / Bootstrap promotion is introduced;
32. no production-security or Cybersecurity completion is claimed;
33. architecture acceptance remains separate from implementation authorization.

### Accepted Architecture

Architecture Decision:

**AD-060 — Canonical Document Content Parsing Application Boundary**

Status:

**ACCEPTED — GIT DURABILITY PENDING**

Accepted Application service:

`DocumentContentParsingApplicationService`

Accepted parser port:

`DocumentContentParser`

Accepted Application request identity:

`document_id: EntityId`

Accepted parser operation:

`parse(*, descriptor: DocumentContentDescriptor, payload: BinaryIO) -> str`

Accepted Application result semantics:

**VERIFIED DESCRIPTOR + TEXTUAL PARSED CONTENT**

Accepted coordination model:

**OPEN VERIFIED CONTENT → PARSE INSIDE ACCESS CONTEXT → CLOSE CONTENT → RETURN RESULT**

Accepted payload ownership:

**RFC-073 OWNED / RFC-074 PARSER BORROWED ONLY**

Accepted public parser-contract failures:

- `DocumentContentParserUnsupportedMediaTypeError`;
- `DocumentContentParserInvalidContentError`.

Accepted invalid-result behavior:

**NON-STR → TYPEERROR / NO COERCION**

Accepted empty-text behavior:

**VALID SUCCESS / NO AUTOMATIC OCR**

### Preserved Ownership

RFC-073 remains canonical verified binary-content access.

RFC-072 remains canonical Document Content establishment coordination.

RFC-065 remains canonical prepared Document-to-Knowledge ingestion.

RFC-074 introduces no persistence ownership.

### Accepted Initial Technical Surface

After acceptance Git durability and a separate implementation-entry gate, the
initial authorized implementation may be limited to:

- `backend/app/document_parsing/__init__.py`;
- `backend/app/document_parsing/parser.py`;
- `backend/app/services/document_content_parsing_application_service.py`;
- focused RFC-074 behavior and architecture tests.

This acceptance does not itself authorize those changes.

### Preserved Deferrals

Still outside RFC-074:

- concrete parser adapters;
- parser registry/resolver;
- automatic parser fallback;
- OCR;
- metadata/table/page extraction models;
- chunking;
- parsed-result persistence;
- Document Library;
- automatic Knowledge ingestion;
- Search;
- embeddings / Vector;
- Graph;
- RAG;
- LLM;
- AI Agents;
- Runtime / Composition / Bootstrap wiring;
- API exposure;
- schema/migration expansion;
- production parser sandboxing;
- production-security readiness.

### Acceptance Gate State

AD-060:

**ACCEPTED — GIT DURABILITY PENDING**

Architecture review:

**PASS**

Acceptance authoring:

**COMPLETE LOCALLY / REVIEW CANDIDATE AUTHORED**

Acceptance staging:

**NOT YET PERFORMED**

Acceptance commit:

**NONE**

Acceptance push:

**NONE**

Implementation entry:

**NOT STARTED**

Implementation:

**NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document RFC-074 / AD-060 architecture acceptance
candidate.

Do not stage until that acceptance review passes.

Do not begin implementation until accepted-contract Git durability is complete
and a separate implementation-entry review passes.


---

## RFC-074 / AD-060 Engineering Closure Record

**Record Classification: Non-Decision Engineering Closure Governance Record**

This section creates no new Architecture Decision.

It does not amend, replace, supersede or rewrite AD-060.

AD-060 remains:

**ACCEPTED**

### Closure Baseline

RFC-074 workstream:

**Canonical Document Content Parsing Application Boundary**

Verified workstream-selection commit:

`b5d1e7fe434378ac7ee90912ac40932d5c5451eb`

Verified accepted-contract commit:

`44b068915e95a3965ab00f7a0e2ea726a9670120`

Verified technical implementation commit:

`34841f28b357bfb70686d3fb1622e5bd746f7396`

Technical Git durability:

**PASS — LOCAL / TRACKING / REMOTE IDENTITY VERIFIED**

Working tree at closure-entry gate:

**CLEAN**

### Verified Technical Outcome

RFC-074 establishes the canonical persistence-neutral parser port:

`app.document_parsing.parser.DocumentContentParser`

and the canonical Application service:

`app.services.document_content_parsing_application_service.DocumentContentParsingApplicationService`

Canonical request identity remains:

`document_id: EntityId`

Canonical parser operation remains conceptually:

`parse(*, descriptor: DocumentContentDescriptor, payload: BinaryIO) -> str`

The accepted successful orchestration remains:

**OPEN VERIFIED CONTENT → PARSE INSIDE ACCESS CONTEXT → CLOSE CONTENT → RETURN RESULT**

RFC-073 remains the owner of verified payload access and payload lifetime.

The RFC-074 parser is borrower-only.

The Application result contains only:

- verified `DocumentContentDescriptor`;
- parsed textual `str`.

No binary payload, stream handle, path, temporary file, repository or session
escapes through the RFC-074 result.

The implementation preserves:

- canonical media type from `DocumentContentDescriptor`;
- no filename or `source_reference` media-type inference;
- no parser fallback or content sniffing;
- exact `str` runtime validation;
- non-`str` parser output raises `TypeError`;
- no `str(...)` coercion or normalization;
- empty parsed text remains a valid successful result;
- `DocumentContentParserUnsupportedMediaTypeError` propagates unchanged;
- `DocumentContentParserInvalidContentError` propagates unchanged;
- operational parser failures remain distinct and propagate unchanged;
- RFC-073 content-access failures propagate unchanged;
- RFC-074 performs no direct repository or content-store access.

### Verified Engineering Evidence

Focused RFC-074 behavior and architecture verification:

**26 passed**

Full PlantMind regression:

**1054 passed**

Canonical Alembic head:

`0005`

Reviewed technical diff SHA-256:

`df65028433c6f8bb5e2fe03106d764ce5f9d88ca7deb5e9c1f1a7608a7dc9671`

### Responsibility Preservation

This closure record does not modify or absorb responsibility from RFC-073.

RFC-073 continues to own verified canonical Document Content access and payload
context lifetime.

RFC-074 does not own:

- binary content establishment;
- persistence or schema;
- concrete PDF, DOCX, spreadsheet or text parser adapters;
- OCR;
- metadata extraction;
- chunking;
- Document Library behavior;
- automatic Knowledge creation or RFC-065 invocation;
- Search;
- embeddings or Vector persistence;
- Graph / Neo4j production integration;
- RAG;
- LLM invocation;
- AI Agents;
- Runtime / Composition / Bootstrap wiring;
- HTTP/API exposure;
- authentication / authorization / RBAC / Active Directory completion;
- Cybersecurity approval;
- production deployment conformance;
- production-readiness claims.

The legacy empty `app.knowledge.document_parser` seam remains unpromoted.

No schema or Alembic migration changed.

### Closure Governance State

Closure documentation:

**AUTHORED — REVIEW PENDING**

Engineering closure commit:

**NOT YET CREATED**

Engineering closure push:

**NOT PERFORMED**

RFC-074 terminal closure:

**NOT YET CLAIMED**

Post-closure Source-of-Truth reconciliation:

**PENDING — SEPARATE POST-CLOSURE GATE**

Last fully closed RFC remains:

**RFC-073**

Successor workstream:

**NONE SELECTED / NOT AUTHORIZED**

### Next Exact Action

Review the complete five-document RFC-074 engineering closure documentation.

Do not stage closure documentation until that review passes.

Do not claim terminal closure until closure Git durability and the subsequent
Source-of-Truth reconciliation complete separately.


---

## RFC-074 / AD-060 Post-Closure Source-of-Truth Reconciliation Record

**Record Classification: Non-Decision Engineering Reconciliation Governance Record**

This record creates no new Architecture Decision.

It does not amend, replace, supersede or rewrite AD-060.

AD-060 remains:

**ACCEPTED**

### Durable RFC-074 Commit Chain

Selection commit:

`b5d1e7fe434378ac7ee90912ac40932d5c5451eb`

Accepted-contract commit:

`44b068915e95a3965ab00f7a0e2ea726a9670120`

Technical implementation commit:

`34841f28b357bfb70686d3fb1622e5bd746f7396`

Engineering closure commit:

`1f2360dd81a54788dadf3007177de17c4e5d2110`

Closure commit parent:

`34841f28b357bfb70686d3fb1622e5bd746f7396`

Closure Git durability:

**PASS — LOCAL / TRACKING / REMOTE EXACT**

Working tree at reconciliation entry:

**CLEAN**

### Preserved Technical Baseline

Canonical parser port:

`app.document_parsing.parser.DocumentContentParser`

Canonical Application service:

`app.services.document_content_parsing_application_service.DocumentContentParsingApplicationService`

Accepted successful flow remains:

**OPEN VERIFIED CONTENT → PARSE INSIDE ACCESS CONTEXT → CLOSE CONTENT → RETURN RESULT**

Payload ownership remains:

**RFC-073 OWNED / RFC-074 BORROWED ONLY**

Focused RFC-074 verification:

**26 passed**

Full PlantMind regression:

**1054 passed**

Canonical Alembic head:

`0005`

Reviewed technical diff SHA-256:

`df65028433c6f8bb5e2fe03106d764ce5f9d88ca7deb5e9c1f1a7608a7dc9671`

Reviewed engineering-closure diff SHA-256:

`adf2364013a8a37445d403207362988082d2fb5cdbcba65104634903ec8c11bd`

### Reconciliation Responsibility

This reconciliation updates maintained engineering-memory current state only.

It does not modify production code, tests, database schema, Alembic migrations,
Runtime, Composition, Bootstrap, parser implementation technology, Document
Library, OCR, chunking, automatic Knowledge ingestion, Search/Vector/Graph/RAG/LLM,
AI Agents or production-security capability.

RFC-073 continues to own verified canonical Document Content access and payload
lifetime.

RFC-074 continues to own only the persistence-neutral parsing Application boundary.

The legacy empty `app.knowledge.document_parser` seam remains unpromoted.

### Current Reconciliation State

Engineering closure:

**COMPLETE / COMMITTED / PUSHED / EXACT IDENTITY VERIFIED**

Source-of-Truth reconciliation:

**AUTHORED — REVIEW PENDING**

Reconciliation staging:

**NOT PERFORMED**

Reconciliation commit:

**NOT YET CREATED**

Reconciliation push / exact identity verification:

**NOT YET PERFORMED**

Final reconciliation verification record:

**NOT YET CREATED**

RFC-074 terminal closure:

**NOT YET CLAIMED**

Last fully closed RFC remains:

**RFC-073**

Successor workstream:

**NONE SELECTED / NOT AUTHORIZED**

### Next Exact Action

Review the complete RFC-074 post-closure Source-of-Truth reconciliation.

Do not stage reconciliation until that review passes.

Do not declare RFC-074 fully closed until reconciliation Git durability and the
separate final reconciliation verification record complete.


---

## Current Architecture Governance State — RFC-074 Final Source-of-Truth Reconciliation Verification

**Record Classification: Non-Decision Final Governance Verification**

This record creates no new Architecture Decision and does not amend, replace,
supersede or rewrite AD-060.

AD-060 remains the latest Accepted Architecture Decision.

RFC-074 — Canonical Document Content Parsing Application Boundary is:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

### Verified Commit Chain

- selection commit `b5d1e7fe434378ac7ee90912ac40932d5c5451eb`;
- accepted-contract commit `44b068915e95a3965ab00f7a0e2ea726a9670120`;
- technical implementation commit `34841f28b357bfb70686d3fb1622e5bd746f7396`;
- engineering closure commit `1f2360dd81a54788dadf3007177de17c4e5d2110`;
- post-closure reconciliation commit `69d951c386224a52d466d076eb08869c97ffc81c`.

### Verified Reconciliation Git State

- reconciliation parent: `1f2360dd81a54788dadf3007177de17c4e5d2110`;
- reconciliation push: **PASS**;
- exact Local / Tracking / Remote reconciliation identity: **PASS**;
- ahead / behind: **0 / 0**;
- working tree after reconciliation push: **CLEAN**;
- reconciliation surface: exactly five maintained Source-of-Truth documents;
- production-code changes: none;
- test-file changes: none.

### Final Technical Verification

Focused RFC-074 verification:

**26 passed**

Full PlantMind regression:

**1054 passed**

Canonical Alembic head:

`0005`

Technical implementation diff SHA-256:

`df65028433c6f8bb5e2fe03106d764ce5f9d88ca7deb5e9c1f1a7608a7dc9671`

Engineering closure diff SHA-256:

`adf2364013a8a37445d403207362988082d2fb5cdbcba65104634903ec8c11bd`

Post-closure reconciliation diff SHA-256:

`6d9dd2100050baccd586710980884e1afab298dd622b7783c6010cc656a93aa8`

### Preserved Architecture

Canonical parser port:

`app.document_parsing.parser.DocumentContentParser`

Canonical Application service:

`app.services.document_content_parsing_application_service.DocumentContentParsingApplicationService`

Accepted successful orchestration remains:

**OPEN VERIFIED CONTENT → PARSE INSIDE ACCESS CONTEXT → CLOSE CONTENT → RETURN RESULT**

RFC-073 remains the owner of verified canonical Document Content access and
payload lifetime.

RFC-074 remains borrower-only with respect to the payload.

No concrete parser adapter, OCR, Document Library, chunking, automatic Knowledge
ingestion, Search/Vector/Graph/RAG/LLM, AI Agent, Runtime/Composition/Bootstrap,
database-schema, Alembic or production-security capability is promoted by this
final governance record.

Production deployment conformance remains separately governed.

### Successor Governance

Active RFC:

**NONE**

Selected successor:

**NONE**

Successor-workstream selection has not started.

Any successor must be selected separately through evidence-based governance.

### Non-Self-Referential Final Record

This final verification record is intentionally non-self-referential.

It records only already durable commits through reconciliation commit:

`69d951c386224a52d466d076eb08869c97ffc81c`

It does not contain, predict or require the future Git commit hash that persists
this final verification record.

Verification of this record's own commit, push, exact Local / Tracking / Remote
identity and clean working tree is an external Git durability gate.

That external Git gate does not require another RFC-074 Source-of-Truth record.


---

## RFC-075 Successor Workstream Selection Record

**Record Classification: Non-Decision Successor Workstream Selection Record**

This record creates no Architecture Decision.

AD-060 remains the latest Accepted Architecture Decision.

RFC-074 remains:

**FULLY CLOSED AND SOURCE-OF-TRUTH RECONCILED**

RFC-074 terminal commit:

`a86ce4534174e8b815313e2205fa18ecb8f5ef04`

### Selected Successor Workstream

**RFC-075 — Canonical Document Content Parser Resolution & Dispatch Foundation**

### Evidence-Based Rationale

RFC-074 established the canonical persistence-neutral parser port and
Application parsing boundary while deliberately deferring parser
registry/resolution and every concrete parser technology.

The next architecture gap is deterministic parser resolution and dispatch
without changing RFC-074 ownership.

The successor shall preserve the existing RFC-074 parser contract rather
than make the Application service depend directly on PDF, DOCX, spreadsheet,
text, OCR or vendor-specific parser technology.

### Intended Architectural Problem

Establish a canonical, deterministic and extensible mechanism for selecting
the appropriate Document Content parser from canonical descriptor media type.

The architecture review must determine the exact resolver/registry/dispatch
contract and whether dispatch can remain behind the existing
`DocumentContentParser` boundary.

No exact class name or implementation shape is accepted by this selection.

### Explicitly Outside RFC-075 Selection

- concrete PDF/DOCX/spreadsheet/text parser adapters;
- OCR;
- parser fallback or content sniffing;
- metadata/table/page extraction models;
- chunking;
- parsed-result persistence;
- Document Library;
- automatic Knowledge ingestion or RFC-065 invocation;
- Search;
- embeddings / Vector;
- Graph / Neo4j production integration;
- RAG;
- LLM;
- AI Agents;
- Runtime / Composition / Bootstrap wiring;
- HTTP/API exposure;
- schema or Alembic migration expansion;
- production parser sandboxing;
- production-security readiness.

The legacy `app.knowledge.document_parser` seam remains unpromoted.

Existing legacy RAG, semantic-search or vector-memory surfaces are not
promoted by this selection.

### Current Gate

RFC-075 selection:

**AUTHORED — REVIEW PENDING**

Architecture Decision:

**NONE YET — AD-061 NOT AUTHORED**

Implementation:

**NOT AUTHORIZED**

### Next Exact Action

Review this RFC-075 successor selection before staging.

Do not author AD-061 until selection Git durability is complete.
