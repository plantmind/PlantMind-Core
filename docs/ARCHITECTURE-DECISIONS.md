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
