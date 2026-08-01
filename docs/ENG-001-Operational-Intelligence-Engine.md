# ENG-001 — Operational Intelligence Engine

| Property | Value |
|----------|-------|
| Status | Approved |
| Version | 2.0 |
| Owner | Enterprise Architecture |
| Applies To | Operational Intelligence Engine |
| Classification | Engineering Engine Standard |

---

# Authority

This document is normative.

The Operational Intelligence Engine SHALL comply with all requirements defined in this document unless explicitly superseded by an approved Architecture Decision Record (ADR).

---

# Purpose

The Operational Intelligence Engine transforms validated operational evidence, engineering context, and governed knowledge into explainable Operational Intelligence.

Its purpose is to help authorized personnel understand:

- What is currently happening?
- What operational conditions are abnormal?
- What deviations are present?
- What evidence supports the assessment?
- What limitations or uncertainties remain?

The Engine supports engineering judgment.

It does not replace human operational authority.

---

# Architectural Responsibility

The Operational Intelligence Engine owns one engineering responsibility:

> Determine the current operational condition of an approved industrial scope from validated evidence and engineering context.

The Engine SHALL answer one primary engineering question:

> What is happening operationally?

The Engine SHALL NOT own:

- Root Cause Analysis
- Final Engineering Decisions
- Workflow Orchestration
- Maintenance Authorization
- Direct Risk Ownership
- Plant Control
- Knowledge Management
- Infrastructure Integration

---

# Scope

The Engine MAY assess:

- Equipment condition
- Process condition
- Operating mode
- Active deviations
- Alarm relationships
- Trend behavior
- Operational constraints
- Evidence quality
- Context completeness
- Immediate operational indicators

The Engine SHALL operate only within explicitly approved equipment, unit, system, or assessment boundaries.

---

# Architectural Position

The Operational Intelligence Engine belongs to the Enterprise Intelligence Engine Layer defined by ARCH-001.

It SHALL:

- consume approved Contracts;
- access knowledge through approved Knowledge Layer abstractions;
- remain independent from APIs and infrastructure;
- remain isolated from other Intelligence Engines;
- produce an approved Result Contract;
- expose no direct plant-control capability.

Cross-engine collaboration SHALL be managed by an approved orchestration component.

---

# Governing Standards

The Engine SHALL comply with:

- ARCH-001 — Enterprise Architecture Standard
- ARCH-002 — Intelligence Engine Design Standard
- ARCH-003 — Contract Design Standard
- CORE-001 — Foundation Certification Standard
- CORE-002 — Core Services Standard
- CORE-003 — Dependency Management Standard
- INTEL-001 — Engineering Intelligence Principles
- INTEL-002 — Engineering Reasoning Model
- STD-001 — PlantMind Development Standards
- STD-002 — Definition of Done
- STD-003 — Enterprise Terminology Standard

Terminology used by this document SHALL be interpreted according to STD-003.

---

# Input Contracts

The Engine SHALL consume immutable, strongly typed, versioned Contracts.

Approved inputs MAY include:

- OperationalSnapshot
- EquipmentSnapshot
- AlarmSnapshot
- HistorianSnapshot
- MaintenanceSnapshot
- ProcedureContext
- OperatingModeContext
- EngineeringRuleSet
- EvidenceCollection
- AuthorizationContext

Inputs SHALL contain only information required for the approved operational assessment.

The Engine SHALL NOT receive:

- Database connections
- PI connectors
- OPC UA clients
- API controllers
- Service registries
- Workflow objects
- User-interface objects
- Mutable platform state

---

# Input Validation

Before reasoning begins, the Engine SHALL validate:

- Contract schema
- Contract version
- Required identifiers
- Assessment scope
- Observation timestamps
- Evidence traceability
- Data quality
- Context completeness
- Authorization context
- Supported operating mode

Unsupported or invalid inputs SHALL be rejected explicitly.

No Engineering Conclusion SHALL be produced when mandatory validation fails.

---

# Operational Reasoning Lifecycle

The Engine SHALL follow the Engineering Reasoning Model defined by INTEL-002.

## Stage 1 — Observation Acquisition

Collect approved operational Observations from input Contracts.

Observations SHALL remain distinguishable from Evidence.

## Stage 2 — Context Establishment

Establish the relevant operating context, including:

- Equipment state
- Process state
- Operating mode
- Active constraints
- Recent maintenance
- Alarm state
- Historical behavior

## Stage 3 — Evidence Qualification

Determine which Observations qualify as Evidence.

Evidence SHALL be evaluated for:

- Relevance
- Accuracy
- Completeness
- Consistency
- Timeliness
- Reliability
- Traceability

## Stage 4 — Correlation Analysis

Correlate Evidence across:

- Time
- Equipment relationships
- Process relationships
- Alarm sequences
- Trend behavior
- Maintenance activity
- Operating conditions

## Stage 5 — Operational Condition Evaluation

Evaluate the current operational state against approved expectations, rules, limits, and contextual knowledge.

## Stage 6 — Deviation Detection

Identify supported deviations from expected operational behavior.

Each deviation SHALL include:

- Description
- Supporting Evidence
- Engineering relevance
- Severity indicator
- Confidence
- Known limitations

## Stage 7 — Confidence and Uncertainty Assessment

Assess Confidence using:

- Evidence quality
- Evidence completeness
- Evidence consistency
- Context completeness
- Rule coverage
- Knowledge availability

Uncertainty SHALL be reported explicitly.

## Stage 8 — Engineering Conclusion

Produce a bounded Engineering Conclusion describing the supported operational condition.

## Stage 9 — Engineering Recommendation

Produce advisory recommendations only when supported by validated conclusions.

Recommendations SHALL remain subject to authorized human review.

---

# Operational Condition Classification

The Engine MAY classify the operational condition as:

- Normal
- Stable with Observation
- Degraded
- Abnormal
- Critical
- Indeterminate

Classification SHALL NOT be produced without supporting Evidence.

`Indeterminate` SHALL be returned when the available Evidence is insufficient, conflicting, stale, or outside the approved assessment scope.

---

# Deviation Requirements

Every detected deviation SHALL be:

- evidence-based;
- context-aware;
- explainable;
- traceable;
- confidence-qualified;
- limited to the approved assessment boundary.

The Engine SHALL NOT convert correlation into causation without sufficient engineering support.

Root cause determination belongs to the approved Root Cause Intelligence capability.

---

# Output Contract

The Engine SHALL return an immutable:

`OperationalIntelligenceResult`

The Result Contract SHALL include:

- Result Identifier
- Engine Identity
- Engine Version
- Contract Version
- Assessment Scope
- Assessment Timestamp
- Operating Context
- Operational Condition
- Detected Deviations
- Supporting Evidence
- Engineering Conclusion
- Engineering Recommendations
- Confidence Assessment
- Uncertainty
- Assumptions
- Limitations
- Risk Indicators
- Traceability References
- Validation Status
- Human Review Requirement

Primitive outputs SHALL NOT be returned as final Operational Intelligence.

---

# Explainability

Every result SHALL explain:

- what condition was identified;
- which Evidence supported it;
- how operational context affected interpretation;
- which deviations were detected;
- why Confidence was assigned;
- which uncertainties remain;
- why any recommendation was produced.

Opaque conclusions are prohibited.

Internal private model reasoning SHALL NOT be exposed.

The Engine SHALL provide a reviewable engineering explanation rather than unrestricted hidden reasoning content.

---

# Traceability

Every result SHALL preserve traceability to:

- Input Contract identifiers
- Observation sources
- Evidence identifiers
- Knowledge references
- Engineering rules
- Engine version
- Contract versions
- Configuration version
- Model version when applicable
- Processing timestamp

Untraceable Operational Intelligence SHALL NOT be accepted.

---

# Safety and Human Authority

Safety SHALL take priority over production, optimization, and efficiency.

The Engine SHALL NEVER:

- issue plant-control commands;
- write to DCS, PLC, SCADA, or PI System;
- acknowledge alarms;
- change operating setpoints;
- authorize maintenance;
- approve operational actions;
- bypass engineering review.

Final operational responsibility SHALL remain with authorized personnel.

---

# Failure Behaviour

Failure SHALL be explicit and structured.

Failure conditions MAY include:

- Invalid Contract
- Unsupported Contract Version
- Missing Mandatory Evidence
- Conflicting Evidence
- Stale Evidence
- Unsupported Operating Mode
- Insufficient Context
- Knowledge Unavailable
- Rule Evaluation Failure
- Confidence Below Approved Threshold
- Internal Processing Failure

The Engine SHALL NOT silently degrade into unsupported conclusions.

---

# State and Side Effects

The Engine SHALL remain stateless whenever practical.

The Engine SHALL NOT:

- modify source data;
- persist operational data directly;
- publish external messages directly;
- send notifications directly;
- update workflow state;
- modify engineering knowledge;
- invoke external systems;
- invoke another Intelligence Engine.

Its architectural output SHALL be the approved Result Contract.

---

# Security and Data Governance

The Engine SHALL:

- enforce the supplied Authorization Context;
- process only authorized assessment scopes;
- preserve data classification;
- prevent unauthorized knowledge access;
- reject untrusted or malformed inputs;
- avoid exposing sensitive operational information;
- support auditability;
- comply with least-privilege principles.

Prompt injection or malicious content affecting model-assisted processing SHALL be treated as a security condition.

---

# Determinism and Reproducibility

Deterministic reasoning SHALL be used whenever practical.

When probabilistic models contribute to processing, the execution context SHALL preserve:

- Model version
- Prompt version
- Knowledge version
- Rule version
- Configuration version
- Relevant generation settings
- Processing timestamp

Equivalent validated execution contexts SHOULD produce equivalent Engineering Conclusions.

---

# Observability

The Engine SHALL expose approved telemetry including:

- Execution Identifier
- Engine Version
- Result Status
- Processing Duration
- Input Contract Versions
- Operational Condition
- Confidence Band
- Warning Codes
- Failure Category
- Processing Timestamp

Telemetry SHALL NOT expose restricted engineering information without authorization.

---

# Verification Requirements

Verification SHALL include:

- Input Contract validation tests
- Operating-context tests
- Evidence qualification tests
- Correlation tests
- Deviation-detection tests
- Normal-condition tests
- Abnormal-condition tests
- Missing-evidence tests
- Conflicting-evidence tests
- Stale-evidence tests
- Unsupported-mode tests
- Confidence tests
- Uncertainty tests
- Explainability tests
- Traceability tests
- Safety-boundary tests
- Authorization tests
- Reproducibility tests
- Regression tests
- Performance tests
- Security tests

Verification Evidence SHALL be documented according to STD-002.

---

# Prohibited Behaviours

The Operational Intelligence Engine SHALL NOT:

- perform Root Cause Analysis;
- make final Engineering Decisions;
- orchestrate workflows;
- call other Intelligence Engines;
- access infrastructure directly;
- return generic dictionaries as final results;
- hide missing Evidence;
- hide uncertainty;
- fabricate certainty;
- infer causation from unsupported correlation;
- modify plant or platform state;
- learn or self-modify during production execution.

---

# Architecture Compliance Checklist

The Engine is compliant only when it:

- answers “What is happening operationally?”;
- owns one engineering responsibility;
- consumes approved Contracts;
- produces `OperationalIntelligenceResult`;
- follows INTEL-002;
- uses terminology from STD-003;
- remains isolated from infrastructure;
- remains isolated from other Engines;
- qualifies Evidence before reasoning;
- evaluates operational context;
- reports Confidence and Uncertainty;
- produces explainable and traceable conclusions;
- preserves human authority;
- passes mandatory verification;
- documents Verification Evidence.

---

# Definition of Done

ENG-001 is complete when:

- architecture review has passed;
- Contract designs are approved;
- implementation follows the defined boundaries;
- mandatory tests pass;
- runtime behavior is verified;
- Verification Evidence is documented;
- no critical issue remains;
- security requirements are satisfied;
- Git status is clean;
- engineering approval is recorded.

---

# Future Evolution

Future capabilities MAY include:

- Real-time event correlation
- Multi-equipment assessment
- Operating-mode inference
- Trend and anomaly intelligence
- Cross-unit operational assessment
- Predictive operational indicators
- Digital Twin context
- Validated outcome feedback

Future evolution SHALL preserve the responsibility boundary defined by this document.

---

# Engineering Philosophy

Observations describe industrial reality.

Context gives Observations meaning.

Qualified Observations become Evidence.

Governed reasoning transforms Evidence into Operational Intelligence.

Operational Intelligence supports safer human decisions.

Human authority remains final.

---

# Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Approved | Initial Operational Intelligence Engine definition |
| 2.0 | Approved | Full alignment with PlantMind architecture, reasoning, terminology, governance, and verification standards |